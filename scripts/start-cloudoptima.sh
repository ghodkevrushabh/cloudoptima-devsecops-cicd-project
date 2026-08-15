#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== Syncing platform outputs ==="
./scripts/sync-platform-outputs.sh

echo
echo "=== Starting CloudOptima ==="
docker compose up -d --no-build --force-recreate flask

echo
echo "=== Verifying shared ALB values ==="
docker exec cloudoptima-flask sh -c '
echo "TARGET_GROUP_ARN=$TARGET_GROUP_ARN"
echo "ALB_SECURITY_GROUP_ID=$ALB_SECURITY_GROUP_ID"
'

echo
echo "CloudOptima started successfully."
