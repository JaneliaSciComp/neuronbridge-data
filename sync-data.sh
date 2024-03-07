#!/bin/bash

# Run this using data version (use '_' instead of '.') and the data bucket suffix e.g.,
# sh sync-data.sh v3_0_0 dev
# To only see the sync commands use
# NO_RUN=1 sh sync-data.sh v3_0_0 dev

SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})

function display_help {
    echo "sync-data.sh <version> <data-bucket-suffix>"
    echo "where:"
    echo "   <version> is the version prefixed with 'v' and with '_' instead of '.'"
    echo "   <data-bucket-suffix> is dev|devpre|val|prodpre|prod"
    echo "e.g. sync-data.sh v3_1_1 dev"
    echo "You can simulate the commands using NO_RUN environment variable:"
    echo "NO_RUN=1 sync-data.sh v3_1_1 dev"
    exit 1
}

if [[ "$1" == "-h" || "$1" == "-help" ]] ; then
   display_help
fi

DATA_VERSION=$1
DATA_BUCKET_SUFFIX=$2

if [[ -z ${DATA_VERSION} || -z ${DATA_BUCKET_SUFFIX} ]] ; then
    echo "Missing data version or the data bucket suffix"
    display_help
fi

RUNNER=
DRYRUN_ARG=

if [[ -n ${NO_RUN} ]] ; then
    RUNNER=echo
    DRYRUN_ARG=--dryrun
fi

${RUNNER} aws s3 cp ${SCRIPT_DIR}/janelia-neuronbridge-data/config.json s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/${DATA_VERSION}/config.json ${DRYRUN_ARG}
${RUNNER} aws s3 sync ${SCRIPT_DIR}/janelia-neuronbridge-data/schemas s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/${DATA_VERSION}/schemas ${DRYRUN_ARG}
${RUNNER} aws s3 cp ${SCRIPT_DIR}/janelia-neuronbridge-data/DATA_NOTES.md s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/${DATA_VERSION}/DATA_NOTES.md ${DRYRUN_ARG}
${RUNNER} aws s3 cp ${SCRIPT_DIR}/janelia-neuronbridge-data/next.txt s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/next.txt ${DRYRUN_ARG}
