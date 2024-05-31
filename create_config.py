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
import jrc_common.jrc_common as JRC

# pylint: disable=broad-exception-caught,logging-fstring-interpolation

AREAS = {"Brain": {"label": "Brain",
                   "alignmentSpace": "JRC2018_Unisex_20x_HR"},
         "VNC": {"label": "Ventral Nerve Cord",
                 "alignmentSpace": "JRC2018_VNC_Unisex_40x_DS"}
        }
BASE = "https://s3.amazonaws.com/"
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
    dbs = ['neuronbridge']
    for source in dbs:
        dbo = attrgetter(f"{source}.prod.read")(dbconfig)
        LOGGER.info("Connecting to %s prod on %s as %s", dbo.name, dbo.host, dbo.user)
        try:
            DB["nb" if source == "neuronbridge" else source] = JRC.connect_database(dbo)
        except Exception as err:
            terminate_program(err)
    # AWS S3
    if ARG.MANIFOLD == 'prod':
        try:
            aws = JRC.get_config("aws")
        except Exception as err:
            terminate_program(err)
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
    LOGGER.info(f"Reading {bucket}/{key}")
    try:
        data = AWSS3["client"].get_object(Bucket=bucket, Key=key)
        contents = data['Body'].read().decode("utf-8")
    except Exception as err:
        LOGGER.error(f"Could not read {bucket}/{key}")
        terminate_program(err)
    return json.loads(contents)


def get_count(lib, template):
    ''' Get the searchable neuron count from AWS S3 or publishedURL
        Keyword arguments:
          lib: library name
          template: alignment space
        Returns:
          Count
    '''
    if ARG.SOURCE == "mongo":
        coll = DB['nb'].publishedURL
        count = coll.count_documents({"libraryName": lib, "alignmentSpace": template})
        if ARG.DEBUG:
            rows = coll.find({"libraryName": lib, "alignmentSpace": template})
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


def get_libraries(area):
    ''' Get libraries to create a customSearch block
        Keyword arguments:
          area: anatomical area
        Returns:
          JSON customSearch block
    '''
    libs = JRC.simplenamespace_to_dict(JRC.get_config("cdm_library"))
    coll = DB['nb'].publishedURL
    rows = coll.distinct('libraryName')
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
    for lib in libs:
        count = get_count(libraries[lib] if ARG.SOURCE == "mongo" else lib, \
                          AREAS[area]['alignmentSpace'])
        if 'FlyLight' in lib:
            csblock["lmLibraries"].append({"name": lib.replace(" ", "_"),
                                           "count": count
                                          })
        else:
            csblock["emLibraries"].append({"name": lib.replace(" ", "_"),
                                           "publishedNamePrefix": get_prefix(lib),
                                           "count": count
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
    for area in AREAS:
        csblock = get_libraries(area)
        key = f"fl:open_data:{area.lower()}"
        short = "" if ARG.MANIFOLD == "prod" else f"-{ARG.MANIFOLD}"
        manifest = {"label": f"FlyLight {area} Open Data Store",
                    "anatomicalArea": area,
                    "prefixes": {"CDM": f"{BASE}janelia-flylight-color-depth{short}/",
                                 "CDMThumbnail": f"{BASE}janelia-flylight-color-depth-thumbnails" \
                                                 + f"{short}/",
                                 "CDMInput": f"{BASE}janelia-flylight-color-depth{short}/",
                                 "CDMMatch": f"{BASE}janelia-flylight-color-depth{short}/",
                                 "CDMBest": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "CDMBestThumbnail": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "CDMSkel": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMip": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMipMasked": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMipMaskedSkel": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "SignalMipExpression": f"{BASE}janelia-ppp-match-{ARG.MANIFOLD}/",
                                 "AlignedBodySWC": f"{BASE}janelia-flylight-color-depth{short}/",
                                 "AlignedBodyOBJ": f"{BASE}janelia-flylight-color-depth{short}/",
                                 "CDSResults": f"{BASE}janelia-neuronbridge-data-" \
                                               + f"{ARG.MANIFOLD}/{ARG.VERSION}/metadata" \
                                               + "/cdsresults/",
                                 "PPPMResults": f"{BASE}janelia-neuronbridge-data-" \
                                                + f"{ARG.MANIFOLD}/{ARG.VERSION}/metadata/" \
                                                + "pppmresults/",
                                 "VisuallyLosslessStack": f"{BASE}janelia-flylight-imagery/",
                                 "Gal4Expression": f"{BASE}janelia-flylight-imagery/"
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
    initialize_program()
    create_config()
    terminate_program()
