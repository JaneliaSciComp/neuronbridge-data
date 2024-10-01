''' create_config.py
    Create a janelia-neuronbridge-data config file
'''

import argparse
import json
from operator import attrgetter
import re
import sys
import boto3
import inquirer
from inquirer.themes import BlueComposure
from tqdm import tqdm
import jrc_common.jrc_common as JRC
import doi_common.doi_common as DL

# pylint: disable=broad-exception-caught,logging-fstring-interpolation

__version__ = '1.0.0'

BASE = {}
RELEASES = {}
# Database
DB = {}
# AWS S3
AWSS3 = {"client": None}


def terminate_program(msg=None):
    ''' Terminate the program gracefully
        Keyword arguments:
          msg: error message or object
        Returns:
          None
    '''
    if msg:
        if not isinstance(msg, str):
            msg = f"An exception of type {type(msg).__name__} occurred. Arguments:\n{msg.args}"
        LOGGER.critical(msg)
    sys.exit(-1 if msg else 0)


def initialize_program():
    ''' Initialize database connection and AWS S3 client
        Keyword arguments:
          None
        Returns:
          None
    '''
    # Database
    try:
        dbconfig = JRC.get_config("databases")
    except Exception as err:
        terminate_program(err)
    for source in ['sage', 'neuronbridge']:
        dbo = attrgetter(f"{source}.prod.read")(dbconfig)
        LOGGER.info("Connecting to %s prod on %s as %s", dbo.name, dbo.host, dbo.user)
        try:
            DB["nb" if source == "neuronbridge" else source] = JRC.connect_database(dbo)
        except Exception as err:
            terminate_program(err)
    try:
        aws = JRC.get_config("aws")
    except Exception as err:
        terminate_program(err)
    BASE['s3'] = aws.base_aws_url + "/"
    # AWS S3
    if ARG.MANIFOLD == 'prod':
        sts_client = boto3.client('sts')
        aro = sts_client.assume_role(RoleArn=aws.role_arn,
                                     RoleSessionName="AssumeRoleSession1")
        credentials = aro['Credentials']
        AWSS3["client"] = boto3.client('s3',
                                       aws_access_key_id=credentials['AccessKeyId'],
                                       aws_secret_access_key=credentials['SecretAccessKey'],
                                       aws_session_token=credentials['SessionToken'])
    else:
        AWSS3["client"] = boto3.client('s3')


def get_prefix(lib):
    ''' Get the prefix from a FlyEM library name
        Keyword arguments:
          lib: library name
        Returns:
          Prefix
    '''
    return lib.replace("FlyEM ", "").replace(" v", ":v").lower()


def read_object(bucket, key):
    ''' Read a file from AWS S3 and return the contents
        Keyword arguments:
          bucket: bucket name
          key: object key
        Returns:
          JSON
    '''
    LOGGER.debug(f"Reading {bucket}/{key}")
    try:
        data = AWSS3["client"].get_object(Bucket=bucket, Key=key)
        contents = data['Body'].read().decode("utf-8")
    except Exception as err:
        LOGGER.error(f"Could not read {bucket}/{key}")
        terminate_program(err)
    return json.loads(contents)


def get_count(lib, template, source, release=None):
    ''' Get the searchable neuron count from AWS S3 or publishedURL
        Keyword arguments:
          lib: library name
          template: alignment space
          release: ALPS release (default: None)
        Returns:
          Count
    '''
    if source == "mongo":
        coll = DB['nb'].publishedURL
        payload = {"libraryName": lib, "alignmentSpace": template}
        if release:
            payload["alpsRelease"] = release
        else:
            LOGGER.info(f"Getting count from MongoDB for {lib}/{template}")
        count = coll.count_documents(payload)
        if ARG.DEBUG:
            rows = coll.find(payload)
            with open(f"{lib}_{template}.txt", 'w', encoding='ascii') as outfile:
                for row in rows:
                    outfile.write(f"{row['uploaded']['searchable_neurons']}\n")
        return count
    bucket = "janelia-flylight-color-depth"
    if ARG.MANIFOLD != "prod":
        bucket = f"{bucket}-{ARG.MANIFOLD}"
    count = read_object(bucket, f"{template}/{lib.replace(' ', '_')}/" \
                                + "searchable_neurons/counts_denormalized.json")
    return count["objectCount"]


def get_em_releases_block(lib, count):
    ''' Get the releases block for a FlyEM library
        Keyword arguments:
          lib: library name
          count: image count
        Returns:
          Releases block
    '''
    if "FlyEM" in lib:
        key = lib.replace("FlyEM ", "").lower()
        key = re.sub(r" v.+", "", key)
    elif "FlyWire FAFB" in lib:
        key = "flywire_fafb"
    else:
        terminate_program(f"Can't parse EM library {lib}")
    if key not in EMDOI:
        terminate_program(f"Missing entry in em_dois configuration for {key} ({lib})")
    if not EMDOI[key]:
        terminate_program(f"Undefined DOI in em_dois configuration for {key} ({lib})")
    dois = []
    if isinstance(EMDOI[key], list):
        for doi in EMDOI[key]:
            dois.append({doi: DL.short_citation(doi)})
    else:
        dois = [{EMDOI[key]: DL.short_citation(EMDOI[key])}]
    payload = {lib.replace(" ", "_"): {"count": count,
                                       "dois": dois
                                      }}
    return [payload]


def get_flylight_dois(release):
    ''' Get the DOI for FlyLight
        Keyword arguments:
          None
        Returns:
          DOI
    '''
    if release in RELEASES:
        return RELEASES[release]
    stmt = "SELECT DISTINCT value FROM line_property_vw WHERE type='doi' AND name in " \
           + "(SELECT DISTINCT line FROM image_data_mv WHERE alps_release=%s) ORDER BY 1"
    try:
        DB['sage']['cursor'].execute(stmt, (release,))
        rows = DB['sage']['cursor'].fetchall()
    except Exception as err:
        terminate_program(err)
    dois = []
    for row in rows:
        if "in prep" in row['value'].lower():
            continue
        dois.append(row['value'])
    if LMDOI['global']:
        dois.extend(LMDOI['global'])
    if release in LMDOI['release']:
        dois.extend(LMDOI['release'][release])
    doirecs = []
    for doi in dois:
        doirecs.append({doi: DL.short_citation(doi)})
    RELEASES[release] = doirecs
    return doirecs


def get_lm_releases_block(libint, area):
    ''' Get the releases block for a FlyLight library
        Keyword arguments:
          libint: library internal name (e.g. flylight_split_gal4_published)
          area: anatomical area
        Returns:
          Releases block
    '''
    try:
        coll = DB['nb'].publishedURL
        rows = coll.distinct("alpsRelease", {"libraryName": libint})
    except Exception as err:
        terminate_program(err)
    payload = []
    LOGGER.debug(f"Getting releases for {libint} {area}")
    progress = False
    if len(rows) > 1:
        progress = True
        rows = (pbar := tqdm(rows, position=1, colour="#4169e1"))
    for rel in rows:
        if progress:
            pbar.set_description(rel)
        count = get_count(libint, AREAS[area]["alignmentSpace"], 'mongo', rel)
        if not count:
            continue
        dois = get_flylight_dois(rel)
        if not dois:
            continue
        payload.append({rel: {"count": count,
                              "dois": dois}})
    return payload


def get_libraries(area):
    ''' Get libraries to create a customSearch block
        Keyword arguments:
          area: anatomical area
        Returns:
          JSON customSearch block
    '''
    libs = JRC.simplenamespace_to_dict(JRC.get_config("cdm_library"))
    coll = DB['nb'].publishedURL
    rows = coll.distinct("libraryName",
                         {"alignmentSpace": AREAS[area]['alignmentSpace']})
    msg = f"Select libraries for {AREAS[area]['label']} ({AREAS[area]['alignmentSpace']})"
    libraries = {}
    for lib, val in libs.items():
        if lib in rows:
            libraries[val['name'].replace("_", " ")] = lib
    defaults = ['FlyLight Gen1 MCFO', 'FlyLight Split-GAL4 Drivers']
    quest = [inquirer.Checkbox('checklist',
             message=msg,
             choices=sorted(libraries), default=defaults)]
    libs = inquirer.prompt(quest, theme=BlueComposure())['checklist']
    csblock = {"searchFolder": "searchable_neurons",
               "lmLibraries": [],
               "emLibraries": []
    }
    for lib in (pbar := tqdm(libs, position=0, leave=True, colour="cyan")):
        pbar.set_description(lib)
        count = get_count(libraries[lib] if ARG.SOURCE == "mongo" else lib, \
                          AREAS[area]['alignmentSpace'], ARG.SOURCE)
        if 'FlyLight' in lib:
            payload = get_lm_releases_block(libraries[lib], area)
            csblock["lmLibraries"].append({"name": lib.replace(" ", "_"),
                                           "count": count,
                                           "releases": payload
                                          })
        else:
            payload = get_em_releases_block(lib, count)
            csblock["emLibraries"].append({"name": lib.replace(" ", "_"),
                                           "publishedNamePrefix": get_prefix(lib),
                                           "count": count,
                                           "releases": payload
                                          })
    return csblock


def create_config():
    ''' Create a new config file
        Keyword arguments:
          None
        Returns:
          None
    '''
    manifest = {}
    master = {"anatomicalAreas": AREAS,
              "stores": {}}
    base = BASE['s3']
    for area in AREAS:
        csblock = get_libraries(area)
        key = f"fl:open_data:{area.lower()}"
        short = "" if ARG.MANIFOLD == "prod" else f"-{ARG.MANIFOLD}"
        manifest = {"label": f"FlyLight {area} Open Data Store",
                    "anatomicalArea": area,
                    "prefixes": {"CDM": f"{base}janelia-flylight-color-depth{short}/",
                                 "CDMThumbnail": f"{base}janelia-flylight-color-depth-thumbnails" \
                                                 + f"{short}/",
                                 "CDMInput": f"{base}janelia-flylight-color-depth{short}/",
                                 "CDMMatch": f"{base}janelia-flylight-color-depth{short}/",
                                 "CDMBest": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "CDMBestThumbnail": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "CDMSkel": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMip": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMipMasked": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMipMaskedSkel": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMipExpression": f"{base}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "AlignedBodySWC": f"{base}janelia-flylight-color-depth{short}/",
                                 "AlignedBodyOBJ": f"{base}janelia-flylight-color-depth{short}/",
                                 "CDSResults": f"{base}janelia-neuronbridge-data-" \
                                               + f"{ARG.MANIFOLD}/{ARG.VERSION}/metadata" \
                                               + "/cdsresults/",
                                 "PPPMResults": f"{base}janelia-neuronbridge-data-" \
                                                + f"{ARG.MANIFOLD}/{ARG.VERSION}/metadata/" \
                                                + "pppmresults/",
                                 "VisuallyLosslessStack": f"{base}janelia-flylight-imagery/",
                                 "Gal4Expression": f"{base}janelia-flylight-imagery/"
                                },
                    "customSearch": csblock
                   }
        master['stores'][key] = manifest
    try:
        with open("new_config.json", "w", encoding="ascii") as outstream:
            outstream.write(json.dumps(master, indent=4) + "\n")
    except Exception as err:
        LOGGER.error("Could not write new_config.json")
        terminate_program(err)
    print("Wrote new_config.json")

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="Create a janelia-neuronbridge-data config file")
    PARSER.add_argument('--source', dest='SOURCE', action='store',
                        default='s3', choices=['s3', 'mongo'],
                        help='Source for searchable neuron count (s3, mongo)')
    PARSER.add_argument('--version', dest='VERSION', action='store',
                        default='v3_2_1', help='Version')
    PARSER.add_argument('--manifold', dest='MANIFOLD', action='store',
                        default='prod', choices=['dev', 'prod'],
                        help='Manifold (dev, prod)')
    PARSER.add_argument('--verbose', dest='VERBOSE', action='store_true',
                        default=False, help='Flag, Chatty')
    PARSER.add_argument('--debug', dest='DEBUG', action='store_true',
                        default=False, help='Flag, Very chatty')
    ARG = PARSER.parse_args()
    LOGGER = JRC.setup_logging(ARG)
    if not re.match(r"^v\d+_\d+_\d+$", ARG.VERSION):
        terminate_program("--version must be in the format v_x_y_z; e.g. v_3_2_1")
    try:
        EMDOI = JRC.simplenamespace_to_dict(JRC.get_config("em_dois"))
        LMDOI = JRC.simplenamespace_to_dict(JRC.get_config("lm_dois"))
        AREAS = JRC.simplenamespace_to_dict(JRC.get_config("neuprint"))["areas"]
    except Exception as gerr:
        terminate_program(gerr)
    initialize_program()
    create_config()
    terminate_program()
