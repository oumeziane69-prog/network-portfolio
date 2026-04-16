# Lab NETCONF — Cisco C8000V IOS XE / NETCONF Lab — Cisco C8000V IOS XE

---

## FR — Description

Ce lab démontre l'automatisation réseau via **NETCONF/YANG** sur un routeur virtuel Cisco C8000V.

| Paramètre | Valeur |
|---|---|
| Plateforme | Cisco C8000V IOS XE 17.15.04c |
| Protocole | NETCONF (SSH port 830) |
| Bibliothèque Python | ncclient 0.7.1 |
| Modèles YANG | `ietf-interfaces`, `Cisco-IOS-XE-native` |

### Opérations démontrées

- **get interfaces** — récupère l'état opérationnel de toutes les interfaces via `ietf-interfaces`
- **get-config OSPF** — extrait la configuration OSPF en XML via `Cisco-IOS-XE-native`

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
```

---

## EN — Description

This lab demonstrates network automation via **NETCONF/YANG** on a Cisco C8000V virtual router.

| Parameter | Value |
|---|---|
| Platform | Cisco C8000V IOS XE 17.15.04c |
| Protocol | NETCONF (SSH port 830) |
| Python library | ncclient 0.7.1 |
| YANG models | `ietf-interfaces`, `Cisco-IOS-XE-native` |

### Demonstrated operations

- **get interfaces** — retrieves the operational state of all interfaces via `ietf-interfaces`
- **get-config OSPF** — extracts OSPF configuration as XML via `Cisco-IOS-XE-native`

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
```

---

## Output example / Exemple de sortie

```xml
=== GET interfaces (ietf-interfaces) ===
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>GigabitEthernet1</name>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
          ianaift:ethernetCsmacd
        </type>
        <enabled>true</enabled>
      </interface>
    </interfaces>
  </data>
</rpc-reply>

=== GET-CONFIG OSPF (Cisco-IOS-XE-native) ===
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <router>
        <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
          <id>1</id>
          <network>
            <ip><NETWORK-HERE></ip>
            <mask><MASK-HERE></mask>
            <area><AREA-HERE></area>
          </network>
        </ospf>
      </router>
    </native>
  </data>
</rpc-reply>
```
