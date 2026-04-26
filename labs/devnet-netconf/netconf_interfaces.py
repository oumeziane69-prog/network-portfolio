"""
netconf_interfaces.py — Filtered NETCONF get via Cisco-IOS-XE-native YANG model
Platform: Cisco Cat8k IOS-XE 17.9 | ncclient 0.7.1 | Python 3.8
Returns: hostname, GigabitEthernet1, Vlan20/21, VirtualPortGroup31 as JSON
Credentials via env vars: DEVNET_HOST, DEVNET_USER, DEVNET_PASS
"""

import json
import os
import sys
from xml.etree import ElementTree as ET

from ncclient import manager
from ncclient.xml_ import to_ele

NETCONF_PORT = 830

# Subtree filter — hostname + targeted interfaces (Cisco-IOS-XE-native)
FILTER_XML = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <interface>
      <GigabitEthernet>
        <name>1</name>
      </GigabitEthernet>
      <Vlan>
        <name>20</name>
      </Vlan>
      <Vlan>
        <name>21</name>
      </Vlan>
      <VirtualPortGroup>
        <name>31</name>
      </VirtualPortGroup>
    </interface>
  </native>
</filter>
"""

NS = {
    "nc": "urn:ietf:params:xml:ns:netconf:base:1.0",
    "ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
}


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


def _text(element, xpath):
    node = element.find(xpath, NS)
    return node.text if node is not None else None


def parse_response(response_xml):
    root = ET.fromstring(response_xml)
    native = root.find(".//ios:native", NS)
    if native is None:
        return {"error": "native element not found in response"}

    result = {}

    hostname = _text(native, "ios:hostname")
    if hostname:
        result["hostname"] = hostname

    interfaces = {}
    iface_container = native.find("ios:interface", NS)
    if iface_container is not None:
        type_map = [
            ("ios:GigabitEthernet", "GigabitEthernet"),
            ("ios:Vlan", "Vlan"),
            ("ios:VirtualPortGroup", "VirtualPortGroup"),
        ]
        for xpath, label in type_map:
            for iface in iface_container.findall(xpath, NS):
                name_el = iface.find("ios:name", NS)
                if name_el is None:
                    continue
                key = f"{label}{name_el.text}"
                entry = {"name": name_el.text}

                ip_addr = _text(iface, ".//ios:address/ios:primary/ios:address")
                if ip_addr:
                    entry["ip_address"] = ip_addr

                desc = _text(iface, "ios:description")
                if desc:
                    entry["description"] = desc

                # shutdown leaf is present (no value) when interface is shut
                entry["shutdown"] = iface.find("ios:shutdown", NS) is not None

                interfaces[key] = entry

    result["interfaces"] = interfaces
    return result


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
        print("=== GET-CONFIG filtered (Cisco-IOS-XE-native) ===")
        response = conn.get_config(
            source="running",
            filter=("subtree", to_ele(FILTER_XML)),
        )
        result = parse_response(str(response))
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
