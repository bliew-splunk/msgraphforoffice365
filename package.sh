#!/usr/bin/env bash
set -xe

ENVIRONMENT="${1:-prod}"
echo "Environment: $ENVIRONMENT"
if [ "$ENVIRONMENT" != "prod" ] && [ "$ENVIRONMENT" != "dev" ]; then
  echo "Invalid environment: $ENVIRONMENT"
  exit 1
fi

APP_NAME="msgraphforoffice365"
APP_JSON="office365.json"
APP_JSON_TEMP="$APP_JSON.tmp"
version=$(jq -r ".app_version" "$APP_JSON")
bumped_version=$(echo "$version" | awk -F. '/[0-9]+\./{$NF++;print}' OFS=.)
echo "Version bump: $version -> $bumped_version"
jq ".app_version = \"$bumped_version\"" "$APP_JSON" > "$APP_JSON_TEMP"
mv "$APP_JSON_TEMP" "$APP_JSON"

mkdir -p build
timestamp=$(date +%s)
name_of_this_dir=$(basename "$(pwd)")
output="$(pwd)/build/$APP_NAME-$bumped_version-${timestamp}-${ENVIRONMENT}.tgz"
#tar --exclude=".*" --exclude="build" -C ../ -czvf "$output" "$name_of_this_dir"

temp_dir=$(mktemp -d)
echo "Temp dir: $temp_dir"
# Copy the files in this dir to a temp dir
rsync -av --exclude=".*" --exclude="build" --exclude="__pycache__" . "$temp_dir/app"

if [ "$ENVIRONMENT" == "dev" ]; then
echo "Overriding the MS GRAPH API URL config for dev environment"
  if [[ -z "${NGROK_URL}" ]]; then
    echo "Must set NGROK_URL environment variable"
    exit 1
  fi
cat <<EOT > "$temp_dir/app/office365_api_config.py"
NGROK_URL = "${NGROK_URL}"
SERVER_TOKEN_URL = NGROK_URL + "/{0}/oauth2/v2.0/token"
MSGRAPH_API_URL = f"{NGROK_URL}/v1.0"
MSGRAPH_BETA_API_URL = f"{NGROK_URL}/beta"
EOT
fi

cd "$temp_dir"
tar --exclude=".*" -czvf "$output" app/
echo "Output: $output"
