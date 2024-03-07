# NeuronBridge Data

This repository contains data schema and release notes deployed to neuronbridge data bucket - [s3://janelia-neuronbridge-data-prod](https://open.quiltdata.com/b/janelia-neuronbridge-data-prod/tree/). The repository does not contain actual precomputed data for NeuronBridge.

## Bucket Structure

* Root
  * **current.txt** - pointer to the current production version
  * **next.txt** - pointer to the next version, currently in testing
  * `<version>`
    * **DATA_NOTES.md** - release notes for this version of the data
    * **config.json** - data configuration (follows `schemas/DataConfig.json`)
    * **publishedNames.txt** - complete list of published names (EM and LM) included in this data version
    * **schemas**
      * **DataConfig.json** - JSON schema for the `config.json` file
      * **ImageLookup.json** - JSON schema for the
      * **PrecomputedMatches.json** - JSON schema for precomputed matches in `cdsresults` and `pppresults`
      * **CustomMatches.json** - JSON schema for custom search results
    * metadata
      * **by_body** - image metadata for EM bodies
        * `<publishedName>.json`
      * **by_line** - image metadata for LM lines
        * `<publishedName>.json`
      * **cdsresults** - CDS match results
        * `<imageId>.json`
      * **pppresults** - PPPM match results
        * `<bodyId>.json`


## Sync data with NeuronBridge

To sync data after everything was updated run
```
sh sync-data <DATA_VERSION> <DATA_BUCKET_SUFFIX>
```
where:
* DATA_VERSION is the version prefixed with 'v' and '.' replaced with '_';
  so for '3.1.0' use `v3_1_0`
* DATA_BUCKET_SUFFIX is one of `dev`, `prod`, `val`, `devpre`, `prodpre`