#!/usr/bin/env bash
set -euo pipefail
if [[ -z "${PROJECT_ID:-}" ]]; then echo 'PROJECT_ID environment variable kerak'; exit 1; fi
gcloud auth login
gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud run deploy public-transport-analytics --source . --region "${REGION:-us-central1}" --allow-unauthenticated --port 8080 --memory 1Gi --cpu 1 --min 0 --max 2
