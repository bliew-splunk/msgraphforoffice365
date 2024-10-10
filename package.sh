#!/usr/bin/env bash
set -xe
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
output="build/$APP_NAME-$bumped_version-${timestamp}.tgz"
echo "Output: $output"
name_of_this_dir=$(basename "$(pwd)")
tar --exclude=".*" --exclude="build" -C ../ -czvf "$output" "$name_of_this_dir"
