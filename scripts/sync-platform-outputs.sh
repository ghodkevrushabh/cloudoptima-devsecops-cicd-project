#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLATFORM_DIR="$PROJECT_ROOT/terraform/platform"
ENV_FILE="$PROJECT_ROOT/.env"

export AWS_PROFILE="${AWS_PROFILE:-terraform}"
export AWS_REGION="${AWS_REGION:-eu-north-1}"

cd "$PLATFORM_DIR"

TARGET_GROUP_ARN="$(terraform output -raw target_group_arn)"
ALB_SECURITY_GROUP_ID="$(terraform output -raw alb_security_group_id)"

if [[ -z "$TARGET_GROUP_ARN" || -z "$ALB_SECURITY_GROUP_ID" ]]; then
  echo "ERROR: Required platform outputs are empty."
  exit 1
fi

touch "$ENV_FILE"

grep -v '^TARGET_GROUP_ARN=' "$ENV_FILE" > "${ENV_FILE}.tmp" || true
mv "${ENV_FILE}.tmp" "$ENV_FILE"

grep -v '^ALB_SECURITY_GROUP_ID=' "$ENV_FILE" > "${ENV_FILE}.tmp" || true
mv "${ENV_FILE}.tmp" "$ENV_FILE"

printf 'TARGET_GROUP_ARN=%s\n' "$TARGET_GROUP_ARN" >> "$ENV_FILE"
printf 'ALB_SECURITY_GROUP_ID=%s\n' "$ALB_SECURITY_GROUP_ID" >> "$ENV_FILE"

echo "Platform outputs synchronized."
echo "TARGET_GROUP_ARN=$TARGET_GROUP_ARN"
echo "ALB_SECURITY_GROUP_ID=$ALB_SECURITY_GROUP_ID"
