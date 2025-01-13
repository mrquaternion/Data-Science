#!/bin/bash
REGION="us-central1"
PROJECT_ID="hw5-20269985"

SERVICE_NAME="frontendv2"

IMAGE_URI="us-central1-docker.pkg.dev/hw5-20269985/hw5-images/frontend_v2:d263c1fe-47e3-4cf6-a02f-709f412abb7d"

SERVING_URL="https://backendv2-634488752371.us-central1.run.app"

SERVING_PORT="8000"

gcloud run deploy ${SERVICE_NAME} \
    --region=${REGION} \
    --image=${IMAGE_URI} \
    --min-instances=1 \
    --max-instances=1 \
    --memory="2Gi" \
    --cpu=2 \
    --port=${SERVING_PORT} \
    --allow-unauthenticated \
    --set-env-vars="SERVING_URL=${SERVING_URL}"
