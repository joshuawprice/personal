#!/usr/bin/env bash

# Returns the ID of a cloudflare record. Useful for importing into opentofu.
# From: https://www.adyxax.org/blog/2024/07/16/importing-cloudflare-dns-records-in-terraform/opentofu/

set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "usage: $(basename $0) <zone-name> <record-type> <record-name>"
    exit 1
else
    ZONE_NAME="$1"
    RECORD_TYPE="$2"
    RECORD_NAME="$3"
fi

if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
    echo "Please export a CLOUDFLARE_API_TOKEN environment variable prior to running this script" >&2
    exit 1
fi

BASE_URL="https://api.cloudflare.com"

get () {
    REQUEST="$1"
    curl -s -X GET "${BASE_URL}${REQUEST}" \
         -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
         -H "Content-Type: application/json" | jq -r '.result[] | .id'
}

ZONE_ID=$(get "/client/v4/zones?name=${ZONE_NAME}")

get "/client/v4/zones/${ZONE_ID}/dns_records?name=${RECORD_NAME}&type=${RECORD_TYPE}"
