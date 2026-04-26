# Lab 010 — NETCONF/YANG — Cisco Cat8k IOS-XE / NETCONF/YANG Lab — Cisco Cat8k IOS-XE

**Status: Completed ✅**

---

## FR — Description

Ce lab démontre l'automatisation réseau via **NETCONF/YANG** sur un routeur Cisco Catalyst 8000V.
Deux scripts Python couvrent : la récupération de la configuration complète et un get filtré
retournant hostname + interfaces spécifiques au format JSON.

| Paramètre | Valeur |
|---|---|
| Plateforme | Cisco Cat8k IOS-XE 17.9 |
| Protocole | NETCONF (SSH port 830) |
| Bibliothèque Python | ncclient 0.7.1 |
| Version Python | 3.8 |
| Modèle YANG | `Cisco-IOS-XE-native` |

### Activation de NETCONF sur IOS-XE

```
R1# conf t
R1(config)# netconf-yang
R1(config)# end
R1# show netconf-yang status
```

### Scripts

| Script | Opération | Sortie |
|---|---|---|
| `netconf_get.py` | `get-config` sans filtre | XML — configuration complète |
| `netconf_interfaces.py` | `get-config` filtré (subtree) | JSON — hostname + interfaces ciblées |

### Interfaces récupérées par le filtre

- `GigabitEthernet1`
- `Vlan20`, `Vlan21`
- `VirtualPortGroup31`

### Point clé — syntaxe ncclient

La syntaxe `filter=("subtree", to_ele(...))` est **obligatoire** pour passer un filtre XML
sous forme d'objet ElementTree à ncclient :

```python
from ncclient.xml_ import to_ele

response = conn.get_config(
    source="running",
    filter=("subtree", to_ele(FILTER_XML)),
)
```

### Prérequis

```bash
pip install ncclient==0.7.1
```

Variables d'environnement requises :

```bash
export DEVNET_HOST=<IP-HERE>
export DEVNET_USER=<USERNAME-HERE>
export DEVNET_PASS=<PASSWORD-HERE>
```

### Exécution

```bash
python netconf_get.py
python netconf_interfaces.py
```

---

## EN — Description

This lab demonstrates network automation via **NETCONF/YANG** on a Cisco Catalyst 8000V router.
Two Python scripts cover: full running-config retrieval and a filtered get returning hostname
and specific interfaces as JSON.

| Parameter | Value |
|---|---|
| Platform | Cisco Cat8k IOS-XE 17.9 |
| Protocol | NETCONF (SSH port 830) |
| Python library | ncclient 0.7.1 |
| Python version | 3.8 |
| YANG model | `Cisco-IOS-XE-native` |

### Enabling NETCONF on IOS-XE

```
R1# conf t
R1(config)# netconf-yang
R1(config)# end
R1# show netconf-yang status
```

### Scripts

| Script | Operation | Output |
|---|---|---|
| `netconf_get.py` | `get-config` with no filter | XML — full running config |
| `netconf_interfaces.py` | `get-config` filtered (subtree) | JSON — hostname + targeted interfaces |

### Interfaces returned by the filter

- `GigabitEthernet1`
- `Vlan20`, `Vlan21`
- `VirtualPortGroup31`

### Key point — ncclient syntax

The `filter=("subtree", to_ele(...))` syntax is **required** to pass an XML filter
as an ElementTree object to ncclient:

```python
from ncclient.xml_ import to_ele

response = conn.get_config(
    source="running",
    filter=("subtree", to_ele(FILTER_XML)),
)
```

### Prerequisites

```bash
pip install ncclient==0.7.1
```

Required environment variables:

```bash
export DEVNET_HOST=<IP-HERE>
export DEVNET_USER=<USERNAME-HERE>
export DEVNET_PASS=<PASSWORD-HERE>
```

### Run

```bash
python netconf_get.py
python netconf_interfaces.py
```

---

## Output example / Exemple de sortie

### netconf_get.py

```
=== GET full running config (no filter) ===
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:...">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <hostname>Cat8k-Lab</hostname>
      <version>17.9</version>
      <interface>
        ...
      </interface>
    </native>
  </data>
</rpc-reply>
```

### netconf_interfaces.py

```json
{
  "hostname": "Cat8k-Lab",
  "interfaces": {
    "GigabitEthernet1": {
      "name": "1",
      "ip_address": "<IP-HERE>",
      "description": "MGMT",
      "shutdown": false
    },
    "Vlan20": {
      "name": "20",
      "ip_address": "<IP-HERE>",
      "shutdown": false
    },
    "Vlan21": {
      "name": "21",
      "shutdown": false
    },
    "VirtualPortGroup31": {
      "name": "31",
      "ip_address": "<IP-HERE>",
      "shutdown": false
    }
  }
}
```
