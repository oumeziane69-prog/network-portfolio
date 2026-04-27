"""
Lab: Jinja2 BGP config templating + Netmiko push
Platform : IOS-XE (Cat8000v / CSR1000v) — tested on 17.12.2
"""

from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

TEMPLATE_DIR = "templates"
TEMPLATE_FILE = "bgp_neighbor.j2"

# --- Device inventory -----------------------------------------------------------
DEVICES = [
    {
        "host": "<IP-DEVICE-1>",
        "username": "<USERNAME>",
        "password": "<PASSWORD>",
        "device_type": "cisco_ios",
        "bgp": {
            "local_as": 65001,
            "router_id": "1.1.1.1",
            "neighbors": [
                {
                    "ip": "10.10.20.2",
                    "remote_as": 65002,
                    "description": "eBGP-to-R2",
                },
                {
                    "ip": "10.10.20.3",
                    "remote_as": 65001,
                    "description": "iBGP-to-R3",
                    "update_source": "Loopback0",
                    "next_hop_self": True,
                },
            ],
        },
    },
    {
        "host": "<IP-DEVICE-2>",
        "username": "<USERNAME>",
        "password": "<PASSWORD>",
        "device_type": "cisco_ios",
        "bgp": {
            "local_as": 65002,
            "router_id": "2.2.2.2",
            "neighbors": [
                {
                    "ip": "10.10.20.1",
                    "remote_as": 65001,
                    "description": "eBGP-to-R1",
                },
            ],
        },
    },
]

# --- Template rendering ----------------------------------------------------------

def render_bgp_config(bgp_data: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(TEMPLATE_FILE)
    return template.render(**bgp_data)


# --- Netmiko push ----------------------------------------------------------------

def push_config(device: dict, config_lines: str) -> None:
    connection_params = {
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
        "device_type": device["device_type"],
    }
    commands = [line for line in config_lines.splitlines() if line.strip() and not line.strip().startswith("!")]

    print(f"\n[*] Connecting to {device['host']} ...")
    with ConnectHandler(**connection_params) as net_connect:
        net_connect.enable()
        output = net_connect.send_config_set(commands)
        net_connect.save_config()
        print(output)
    print(f"[+] Config applied and saved on {device['host']}")


# --- Main ------------------------------------------------------------------------

def main() -> None:
    for device in DEVICES:
        rendered = render_bgp_config(device["bgp"])

        print(f"\n{'='*60}")
        print(f"Device : {device['host']}  (AS {device['bgp']['local_as']})")
        print(f"{'='*60}")
        print("--- Rendered config ---")
        print(rendered)

        push_config(device, rendered)

    print("\n[✓] All devices configured.")


if __name__ == "__main__":
    main()
