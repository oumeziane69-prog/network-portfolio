#!/usr/bin/env bash
# restconf_get_bgp.sh — GET BGP running config via RESTCONF
# Device: Cisco Cat8k IOS-XE 17.12.2 | Cisco DevNet Always-On Sandbox
# YANG model: Cisco-IOS-XE-native | RFC 8040 | Expected: HTTP 200 + JSON

HOST="${DEVNET_HOST:-10.10.20.48}"
USER="${DEVNET_USER:-developer}"
PASS="${DEVNET_PASS:-C1sco12345}"
PORT="${DEVNET_PORT:-443}"

URL="https://${HOST}:${PORT}/restconf/data/Cisco-IOS-XE-native:native/router/bgp"

echo "=== RESTCONF GET — BGP config ==="
echo "URL: ${URL}"
echo

RESPONSE=$(curl -sk \
  --user "${USER}:${PASS}" \
  -H "Accept: application/yang-data+json" \
  -w "\n__HTTP_STATUS__%{http_code}" \
  "${URL}")

HTTP_CODE=$(printf '%s' "${RESPONSE}" | grep -o '__HTTP_STATUS__[0-9]*' | cut -d_ -f5)
BODY=$(printf '%s' "${RESPONSE}" | sed 's/__HTTP_STATUS__[0-9]*$//')

printf '%s\n' "${BODY}" | python3 -m json.tool 2>/dev/null || printf '%s\n' "${BODY}"

echo
echo "HTTP Status: ${HTTP_CODE}"

if [ "${HTTP_CODE}" != "200" ]; then
  echo "Unexpected response code: ${HTTP_CODE}" >&2
  exit 1
fi
