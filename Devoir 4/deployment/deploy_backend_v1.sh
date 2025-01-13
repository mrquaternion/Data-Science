#!/bin/bash
REGION="us-central1"
PROJECT_ID="hw5-20269985"

SERVICE_NAME="backendv1"

IMAGE_URI="us-central1-docker.pkg.dev/hw5-20269985/hw5-images/backend_v1:3267be26-e8ea-4f79-84ff-ecd957db8303"

SERVING_PORT="8000"

gcloud run deploy ${SERVICE_NAME} \
    --region=${REGION} \
    --image=${IMAGE_URI} \
    --min-instances=1 \
    --max-instances=1 \
    --memory="2Gi" \
    --cpu=2 \
    --port=${SERVING_PORT} \
    --allow-unauthenticated
