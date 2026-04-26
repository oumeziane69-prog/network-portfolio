"""
netconf_get.py — Full running config via NETCONF
Platform: Cisco Cat8k IOS-XE 17.9 | ncclient 0.7.1 | Python 3.8
Credentials via env vars: DEVNET_HOST, DEVNET_USER, DEVNET_PASS
"""

import os
import sys
from xml.dom.minidom import parseString

from ncclient import manager

NETCONF_PORT = 830


def pretty(xml_str):
    try:
        return parseString(xml_str).toprettyxml(indent="  ")
    except Exception:
        return xml_str


def get_credentials():
    host = os.environ.get("DEVNET_HOST")
    user = os.environ.get("DEVNET_USER")
    password = os.environ.get("DEVNET_PASS")
    missing = [
        name
        for name, val in [
            ("DEVNET_HOST", host),
            ("DEVNET_USER", user),
            ("DEVNET_PASS", password),
        ]
        if not val
    ]
    if missing:
        print(
            f"Error: missing environment variable(s): {', '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(1)
    return host, user, password


def main():
    host, user, password = get_credentials()

    with manager.connect(
        host=host,
        port=NETCONF_PORT,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={"name": "iosxe"},
        look_for_keys=False,
        allow_agent=False,
    ) as conn:
        print("=== GET full running config (no filter) ===")
        response = conn.get_config(source="running")
        print(pretty(str(response)))


if __name__ == "__main__":
    main()
