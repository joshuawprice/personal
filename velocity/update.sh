#!/usr/bin/env sh

# Created using the papermc downloads api
# https://docs.papermc.io/misc/downloads-api/

if ! command -v jq >/dev/null; then
    echo '`jq` command not found' >&2
    exit 1
fi

project="velocity"

latest_version=$(curl -s https://api.papermc.io/v2/projects/${project} | \
    jq -r '.versions[-1]')

latest_build=$(curl -s https://api.papermc.io/v2/projects/${project}/versions/${latest_version}/builds | \
  jq -r '.builds | map(select(.channel == "default") | .build) | .[-1]')

if [ "$latest_build" != "null" ]; then
  jar_name=${project}-${latest_version}-${latest_build}.jar
  papermc_url="https://api.papermc.io/v2/projects/${project}/versions/${latest_version}/builds/${latest_build}/downloads/${jar_name}"

  curl -o velocity.jar $papermc_url
else
  echo "No stable build for version $latest_version found :("
fi

# vim: sts=4 sw=4 et
