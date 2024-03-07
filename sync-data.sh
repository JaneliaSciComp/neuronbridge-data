# Run this using data version (use '_' instead of '.') and the data bucket suffix e.g.,
# sh sync-data.sh v3_0_0 prod
DATA_VERSION=$1
DATA_BUCKET_SUFFIX=$2

RUNNER=echo

RUNNER aws s3 cp janelia-neuronbridge-data/${DATA_VERSION}/config.json s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/${DATA_VERSION}/config.json
RUNNER aws s3 sync janelia-neuronbridge-data/${DATA_VERSION}/schemas s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/${DATA_VERSION}/schemas
RUNNER aws s3 cp janelia-neuronbridge-data/${DATA_VERSION}/DATA_NOTES.md s3://janelia-neuronbridge-data-${DATA_BUCKET_SUFFIX}/${DATA_VERSION}/DATA_NOTES.md
