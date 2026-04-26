"""
netconf_edit.py — edit-config via NETCONF: set Loopback2 description
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

# edit-config payload — Cisco-IOS-XE-native namespace
# Sets the description on Loopback2 using merge operation
EDIT_PAYLOAD = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>2</name>
        <description>BGP-Filtering-Lab-NETCONF</description>
      </Loopback>
    </interface>
  </native>
</config>
"""


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
        print("=== EDIT-CONFIG: set Loopback2 description ===")
        response = conn.edit_config(target="running", config=EDIT_PAYLOAD)
        print(pretty(str(response)))

        if "<ok/>" in str(response) or "<ok>" in str(response):
            print("Description updated successfully.")
        else:
            print("Unexpected response — check device output above.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
