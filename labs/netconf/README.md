# Lab NETCONF/YANG — Cisco Cat8k IOS-XE / NETCONF/YANG Lab — Cisco Cat8k IOS-XE

**Status: Completed ✅**

---

## FR — Description

Ce lab démontre l'automatisation réseau via **NETCONF/YANG** sur un routeur Cisco Catalyst 8000V
dans le sandbox DevNet Always-On. Deux scripts Python couvrent :
la lecture de la configuration BGP complète et la modification de la description d'une interface
Loopback via `edit-config`.

| Paramètre | Valeur |
|---|---|
| Plateforme | Cisco Cat8k IOS-XE 17.12.2 |
| Device (sandbox) | 10.10.20.48 |
| Port NETCONF | 830 |
| Protocole | NETCONF over SSH |
| Bibliothèque Python | ncclient 0.7.1 |
| Version Python | 3.8 |
| Modèle YANG | `Cisco-IOS-XE-native` |

### Opérations démontrées

| Script | Opération NETCONF | Description |
|---|---|---|
| `netconf_get.py` | `get-config` | Lecture de la config running complète (BGP, AS-path, route-maps) |
| `netconf_edit.py` | `edit-config` | Ajout de la description `BGP-Filtering-Lab-NETCONF` sur Loopback2 |

### Prérequis

```bash
pip install ncclient==0.7.1
```

Variables d'environnement (optionnelles — valeurs sandbox par défaut dans les scripts) :

```bash
export DEVNET_HOST=<IP-HERE>
export DEVNET_USER=<USERNAME-HERE>
export DEVNET_PASS=<PASSWORD-HERE>
```

### Exécution

```bash
python netconf_get.py
python netconf_edit.py
```

---

## EN — Description

This lab demonstrates network automation via **NETCONF/YANG** on a Cisco Catalyst 8000V router
in the DevNet Always-On sandbox. Two Python scripts cover: reading the full BGP running config
and modifying a Loopback interface description via `edit-config`.

| Parameter | Value |
|---|---|
| Platform | Cisco Cat8k IOS-XE 17.12.2 |
| Device (sandbox) | 10.10.20.48 |
| NETCONF port | 830 |
| Protocol | NETCONF over SSH |
| Python library | ncclient 0.7.1 |
| Python version | 3.8 |
| YANG model | `Cisco-IOS-XE-native` |

### Demonstrated operations

| Script | NETCONF operation | Description |
|---|---|---|
| `netconf_get.py` | `get-config` | Read full running config (BGP, AS-path ACLs, route-maps) |
| `netconf_edit.py` | `edit-config` | Set description `BGP-Filtering-Lab-NETCONF` on Loopback2 |

### Prerequisites

```bash
pip install ncclient==0.7.1
```

Environment variables (optional — sandbox defaults are set in the scripts):

```bash
export DEVNET_HOST=<IP-HERE>
export DEVNET_USER=<USERNAME-HERE>
export DEVNET_PASS=<PASSWORD-HERE>
```

### Run

```bash
python netconf_get.py
python netconf_edit.py
```

---

## Output example / Exemple de sortie

### netconf_get.py

```xml
=== GET full running config (source: running) ===
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:...">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <hostname>Cat8k-Lab</hostname>
      <router>
        <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
          <id>65001</id>
          ...
        </bgp>
      </router>
      <route-map>
        <name>RM-OUT</name>
        ...
      </route-map>
    </native>
  </data>
</rpc-reply>
```

### netconf_edit.py

```xml
=== EDIT-CONFIG: set Loopback2 description ===
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:...">
  <ok/>
</rpc-reply>
Description updated successfully.
```
