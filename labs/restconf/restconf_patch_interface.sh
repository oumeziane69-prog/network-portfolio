#!/usr/bin/env bash
# restconf_patch_interface.sh — PATCH Loopback20 description via RESTCONF
# Device: Cisco Cat8k IOS-XE 17.12.2 | Cisco DevNet Always-On Sandbox
# YANG model: Cisco-IOS-XE-native | RFC 8040 | Expected: HTTP 204

HOST="${DEVNET_HOST:-10.10.20.48}"
USER="${DEVNET_USER:-developer}"
PASS="${DEVNET_PASS:-C1sco12345}"
PORT="${DEVNET_PORT:-443}"

URL="https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=20"

PAYLOAD='{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 20,
    "description": "RESTCONF-Lab-Loopback20"
  }
}'

echo "=== RESTCONF PATCH — Loopback20 description ==="
echo "URL: ${URL}"
echo "Payload:"
printf '%s\n' "${PAYLOAD}"
echo

HTTP_CODE=$(curl -sk \
  --user "${USER}:${PASS}" \
  -X PATCH \
  -H "Content-Type: application/yang-data+json" \
  -H "Accept: application/yang-data+json" \
  -d "${PAYLOAD}" \
  -o /dev/null \
  -w "%{http_code}" \
  "${URL}")

echo "HTTP Status: ${HTTP_CODE}"

if [ "${HTTP_CODE}" = "204" ]; then
  echo "Description updated successfully."
else
  echo "Unexpected response code: ${HTTP_CODE}" >&2
  exit 1
fi
