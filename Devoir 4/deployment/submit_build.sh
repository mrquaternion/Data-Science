#!/bin/bash
REGION="us-central1" # FILL ME IN
PROJECT_ID="hw5-20269985" # FILL ME IN


# This makes sure that we are uploading our code from the proper path.
# Don't change this line.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

REPO_NAME="hw5-images" # FILL ME IN
REGISTRY="us-central1-docker.pkg.dev" # FILL ME IN
APP_IMAGE="frontend_v2" # FILL ME IN (frontend_v1, backend_v1, frontend_v2 or backend_v2)
TARGET_DOCKERFILE="Dockerfile.${APP_IMAGE}"
SERVING_PORT="8000"

# It's not expected to know bash scripting to the level below.
# The following is known as substitutions in cloud build.

# The full path to an image is a combination of the
# registry, project ID, repository name, and the image name.
REPO_URI="${REGISTRY}/${PROJECT_ID}/${REPO_NAME}"
BASE_IMAGE_URI="${REPO_URI}/base_image"
APP_URI="${REPO_URI}/${APP_IMAGE}"

echo "Script Directory: ${SCRIPT_DIR}"

REPO_URI="${REGISTRY}/${PROJECT_ID}/${REPO_NAME}"
gcloud builds submit \
    --region=${REGION} \
    --config="${SCRIPT_DIR}/cloudbuild.yaml" \
    --substitutions=_BASE_IMAGE_URI="${BASE_IMAGE_URI}",_APP_URI="${APP_URI}",_SERVING_PORT=${SERVING_PORT},_TARGET_DOCKERFILE="${TARGET_DOCKERFILE}" \
    "${SCRIPT_DIR}/.."
