"""
MPLS L3VPN lab — single-device simulation on Cisco Cat8k (IOS-XE).
Configures VRF CLIENT_A, MPLS LDP, MP-BGP VPNv4, and a CE-facing interface,
then captures verification output to logs/mpls_l3vpn_output.txt.
"""

import os
from datetime import datetime
from netmiko import ConnectHandler

# ---------------------------------------------------------------------------
# Device credentials — replace placeholders before running
# ---------------------------------------------------------------------------
DEVICE = {
    "device_type": "cisco_ios",
    "host": "<HOST-HERE>",
    "username": "<USER-HERE>",
    "password": "<PASS-HERE>",
}

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "mpls_l3vpn_output.txt")

# ---------------------------------------------------------------------------
# Configuration payloads
# ---------------------------------------------------------------------------
VRF_CONFIG = [
    "ip vrf CLIENT_A",
    " rd 65000:1",
    " route-target export 65000:1",
    " route-target import 65000:1",
    " exit",
]

MPLS_LDP_CONFIG = [
    "mpls ip",
    "interface GigabitEthernet1",
    " mpls ip",
    " exit",
]

MPBGP_CONFIG = [
    "router bgp 65000",
    " no bgp default ipv4-unicast",
    " neighbor 10.0.0.2 remote-as 65000",
    " neighbor 10.0.0.2 update-source Loopback0",
    " address-family vpnv4",
    "  neighbor 10.0.0.2 activate",
    "  neighbor 10.0.0.2 send-community extended",
    " exit-address-family",
    " exit",
]

CE_INTERFACE_CONFIG = [
    "interface GigabitEthernet2",
    " ip vrf forwarding CLIENT_A",
    " ip address 192.168.1.1 255.255.255.0",
    " no shutdown",
    " exit",
]

VERIFICATION_COMMANDS = [
    "show ip vrf",
    "show mpls ldp neighbor",
    "show bgp vpnv4 unicast all",
    "show mpls forwarding-table",
]


def push_config(connection, commands: list[str], section: str) -> str:
    output = connection.send_config_set(commands)
    print(f"[OK] {section} configured.")
    return f"\n{'='*60}\n{section}\n{'='*60}\n{output}\n"


def run_verifications(connection) -> str:
    results = []
    for cmd in VERIFICATION_COMMANDS:
        output = connection.send_command(cmd)
        results.append(f"\n{'='*60}\n$ {cmd}\n{'='*60}\n{output}\n")
        print(f"[OK] {cmd}")
    return "".join(results)


def save_log(content: str) -> None:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as fh:
        fh.write(content)
    print(f"\n[LOG] Output saved to: {LOG_FILE}")


def main() -> None:
    print(f"\n[START] MPLS L3VPN lab — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Connecting to {DEVICE['host']} ...")

    log = f"MPLS L3VPN Lab Output\nGenerated: {datetime.now()}\nDevice: {DEVICE['host']}\n"

    with ConnectHandler(**DEVICE) as conn:
        conn.enable()
        print("[OK] Connected.\n")

        log += push_config(conn, VRF_CONFIG, "VRF CLIENT_A (RD 65000:1 / RT 65000:1)")
        log += push_config(conn, MPLS_LDP_CONFIG, "MPLS LDP — GigabitEthernet1")
        log += push_config(conn, MPBGP_CONFIG, "MP-BGP AS65000 — VPNv4 address-family")
        log += push_config(conn, CE_INTERFACE_CONFIG, "GigabitEthernet2 — VRF CLIENT_A 192.168.1.1/24")

        print("\n[INFO] Running verification commands ...")
        log += run_verifications(conn)

    save_log(log)
    print("[DONE] Lab complete.\n")


if __name__ == "__main__":
    main()
