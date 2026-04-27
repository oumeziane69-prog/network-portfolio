# Lab — Jinja2 BGP Config Templating + Netmiko Push

## FR | Contexte

Jinja2 est le moteur de templates Python de référence pour la génération de
configurations réseau. Combiné à **Netmiko**, il permet de rendre un template
une fois et de le pousser automatiquement sur plusieurs équipements — sans
copier-coller de CLI.

## EN | Overview

This lab renders a Jinja2 BGP neighbor template against a Python device
inventory, then pushes the resulting config blocks to live IOS-XE routers via
**Netmiko** `send_config_set`. Every device gets a tailored config from one
shared template.

---

## Files

```
labs/jinja2/
├── README.md                   ← this file
├── jinja2_bgp.py               ← main script (render + push)
└── templates/
    └── bgp_neighbor.j2         ← Jinja2 template
```

---

## Topology

```
  AS 65001                    AS 65002
  +---------+   eBGP (10.10.20.x)   +---------+
  |   R1    |<-------------------->|   R2    |
  | 1.1.1.1 |                      | 2.2.2.2 |
  +---------+                      +---------+
       |
       | iBGP (Loopback0, next-hop-self)
       v
  +---------+
  |   R3    |
  | 3.3.3.3 |
  +---------+
```

---

## Jinja2 Template — `templates/bgp_neighbor.j2`

```jinja2
router bgp {{ local_as }}
 bgp router-id {{ router_id }}
 bgp log-neighbor-changes
{% for neighbor in neighbors %}
 neighbor {{ neighbor.ip }} remote-as {{ neighbor.remote_as }}
 neighbor {{ neighbor.ip }} description {{ neighbor.description }}
{% if neighbor.update_source is defined %}
 neighbor {{ neighbor.ip }} update-source {{ neighbor.update_source }}
{% endif %}
{% if neighbor.next_hop_self is defined and neighbor.next_hop_self %}
 neighbor {{ neighbor.ip }} next-hop-self
{% endif %}
{% endfor %}
!
```

### Variables

| Variable                    | Type   | Description                         |
|-----------------------------|--------|-------------------------------------|
| `local_as`                  | int    | Local BGP AS number                 |
| `router_id`                 | str    | BGP router-id (IPv4 format)         |
| `neighbors`                 | list   | List of neighbor dicts (see below)  |
| `neighbors[].ip`            | str    | Neighbor IP address                 |
| `neighbors[].remote_as`     | int    | Remote AS number                    |
| `neighbors[].description`   | str    | Neighbor description label          |
| `neighbors[].update_source` | str    | (optional) Source interface         |
| `neighbors[].next_hop_self` | bool   | (optional) next-hop-self flag       |

---

## Rendered Output — R1 (AS 65001)

```
router bgp 65001
 bgp router-id 1.1.1.1
 bgp log-neighbor-changes
 neighbor 10.10.20.2 remote-as 65002
 neighbor 10.10.20.2 description eBGP-to-R2
 neighbor 10.10.20.3 remote-as 65001
 neighbor 10.10.20.3 description iBGP-to-R3
 neighbor 10.10.20.3 update-source Loopback0
 neighbor 10.10.20.3 next-hop-self
!
```

---

## Script Flow — `jinja2_bgp.py`

```
DEVICES dict
    │
    ▼
render_bgp_config()      ← Jinja2 Environment + FileSystemLoader
    │  bgp_neighbor.j2 + device["bgp"] dict
    ▼
config string (rendered)
    │
    ▼
push_config()            ← Netmiko ConnectHandler
    │  send_config_set(commands)
    │  save_config()
    ▼
Config applied live on IOS-XE
```

### Dependencies

```
pip install jinja2 netmiko
```

---

## Lab Result — Cat8000v IOS-XE 17.12.2

| Step                                        | Result |
|---------------------------------------------|--------|
| Template renders correctly for R1 (2 nbrs)  | ✅     |
| Template renders correctly for R2 (1 nbr)   | ✅     |
| Optional fields (update-source, next-hop)   | ✅     |
| Netmiko push via send_config_set            | ✅     |
| save_config() persists to NVRAM             | ✅     |
| BGP neighbors Up after push                 | ✅     |

### Verification

```
show bgp summary
show run | section router bgp
```

---

## Related Labs

- [NETCONF — get-config / edit-config](../netconf/)
- [RESTCONF — GET / PATCH](../restconf/)
- [EEM — event-based automation](../eem/)
