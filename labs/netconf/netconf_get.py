"""
netconf_get.py — Full running-config via NETCONF get-config (no filter)
Device: Cisco Cat8k IOS-XE 17.12.2 | Cisco DevNet Always-On Sandbox
ncclient 0.7.1 | Python 3.8
"""

import os
import sys
from xml.dom.minidom import parseString

from ncclient import manager

# Cisco DevNet Always-On Sandbox defaults
HOST = os.environ.get("DEVNET_HOST", "10.10.20.48")
USER = os.environ.get("DEVNET_USER", "developer")
PASS = os.environ.get("DEVNET_PASS", "C1sco12345")
PORT = 830


def pretty(xml_str):
    try:
        return parseString(xml_str).toprettyxml(indent="  ")
    except Exception:
        return xml_str


def main():
    print(f"Connecting to {HOST}:{PORT} ...")
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"},
        look_for_keys=False,
        allow_agent=False,
    ) as conn:
        print("=== GET full running config (source: running) ===")
        response = conn.get_config(source="running")
        print(pretty(str(response)))


if __name__ == "__main__":
    main()
