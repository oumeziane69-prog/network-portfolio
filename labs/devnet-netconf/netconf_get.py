"""
NETCONF lab — Cisco C8000V IOS XE 17.15.04c
Demonstrates: get interfaces (ietf-interfaces) + get-config OSPF (Cisco-IOS-XE-native)
Credentials via env vars: DEVNET_HOST, DEVNET_USER, DEVNET_PASS
"""

import os
import sys
from xml.dom.minidom import parseString

from ncclient import manager

NETCONF_PORT = 830

FILTER_INTERFACES = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""

FILTER_OSPF = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <router>
      <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf"/>
    </router>
  </native>
</filter>
"""


def pretty(xml_str: str) -> str:
    try:
        return parseString(xml_str).toprettyxml(indent="  ")
    except Exception:
        return xml_str


def get_credentials() -> tuple[str, str, str]:
    host = os.environ.get("DEVNET_HOST")
    user = os.environ.get("DEVNET_USER")
    password = os.environ.get("DEVNET_PASS")
    missing = [name for name, val in [("DEVNET_HOST", host), ("DEVNET_USER", user), ("DEVNET_PASS", password)] if not val]
    if missing:
        print(f"Error: missing environment variable(s): {', '.join(missing)}", file=sys.stderr)
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
        print("=== GET interfaces (ietf-interfaces) ===")
        response = conn.get(FILTER_INTERFACES)
        print(pretty(str(response)))

        print("=== GET-CONFIG OSPF (Cisco-IOS-XE-native) ===")
        response = conn.get_config(source="running", filter=FILTER_OSPF)
        print(pretty(str(response)))


if __name__ == "__main__":
    main()
