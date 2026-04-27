# Lab RESTCONF/YANG — Cisco Cat8k IOS-XE / RESTCONF/YANG Lab — Cisco Cat8k IOS-XE

**Status: Completed ✅**

---

## FR — Description

Ce lab démontre l'automatisation réseau via **RESTCONF/YANG** sur un routeur Cisco Catalyst 8000V
dans le sandbox DevNet Always-On. Deux scripts Bash (`curl`) couvrent :
la lecture de la configuration BGP complète (HTTP 200, JSON) et la modification de la description
de l'interface Loopback20 via un `PATCH` (HTTP 204).

| Paramètre | Valeur |
|---|---|
| Plateforme | Cisco Cat8k IOS-XE 17.12.2 |
| Device (sandbox) | 10.10.20.48 |
| Port RESTCONF | 443 (HTTPS) |
| Protocole | RESTCONF over HTTPS (RFC 8040) |
| Outil | curl |
| Format de données | JSON (`application/yang-data+json`) |
| Modèle YANG | `Cisco-IOS-XE-native` |

### Opérations démontrées

| Script | Méthode HTTP | Endpoint YANG | HTTP attendu |
|---|---|---|---|
| `restconf_get_bgp.sh` | `GET` | `.../router/bgp` | 200 + JSON |
| `restconf_patch_interface.sh` | `PATCH` | `.../interface/Loopback=20` | 204 |

### Prérequis

```bash
# curl et python3 doivent être disponibles
curl --version
python3 --version
```

Variables d'environnement (optionnelles — valeurs sandbox DevNet par défaut dans les scripts) :

```bash
export DEVNET_HOST=<IP-HERE>
export DEVNET_USER=<USERNAME-HERE>
export DEVNET_PASS=<PASSWORD-HERE>
export DEVNET_PORT=443
```

### Exécution

```bash
chmod +x restconf_get_bgp.sh restconf_patch_interface.sh

# Lecture de la config BGP
./restconf_get_bgp.sh

# Modification de la description Loopback20
./restconf_patch_interface.sh
```

---

## EN — Description

This lab demonstrates network automation via **RESTCONF/YANG** on a Cisco Catalyst 8000V router
in the DevNet Always-On sandbox. Two Bash scripts (`curl`) cover: reading the full BGP running
config (HTTP 200, JSON) and modifying the description of Loopback20 via a `PATCH` (HTTP 204).

| Parameter | Value |
|---|---|
| Platform | Cisco Cat8k IOS-XE 17.12.2 |
| Device (sandbox) | 10.10.20.48 |
| RESTCONF port | 443 (HTTPS) |
| Protocol | RESTCONF over HTTPS (RFC 8040) |
| Tooling | curl |
| Data format | JSON (`application/yang-data+json`) |
| YANG model | `Cisco-IOS-XE-native` |

### Demonstrated operations

| Script | HTTP method | YANG endpoint | Expected HTTP |
|---|---|---|---|
| `restconf_get_bgp.sh` | `GET` | `.../router/bgp` | 200 + JSON |
| `restconf_patch_interface.sh` | `PATCH` | `.../interface/Loopback=20` | 204 |

### Prerequisites

```bash
# curl and python3 must be available
curl --version
python3 --version
```

Environment variables (optional — DevNet sandbox defaults are set in the scripts):

```bash
export DEVNET_HOST=<IP-HERE>
export DEVNET_USER=<USERNAME-HERE>
export DEVNET_PASS=<PASSWORD-HERE>
export DEVNET_PORT=443
```

### Run

```bash
chmod +x restconf_get_bgp.sh restconf_patch_interface.sh

# Read BGP config
./restconf_get_bgp.sh

# Patch Loopback20 description
./restconf_patch_interface.sh
```

---

## Output example / Exemple de sortie

### restconf_get_bgp.sh

```
=== RESTCONF GET — BGP config ===
URL: https://10.10.20.48:443/restconf/data/Cisco-IOS-XE-native:native/router/bgp

{
  "Cisco-IOS-XE-bgp:bgp": [
    {
      "id": 65001,
      "bgp": {
        "log-neighbor-changes": [null]
      },
      "neighbor": [
        {
          "id": "192.168.1.2",
          "remote-as": 65002,
          "description": "eBGP-peer-AS65002"
        }
      ],
      "address-family": {
        "no-vrf": {
          "ipv4": [
            {
              "af-name": "unicast",
              "neighbor": [
                {
                  "id": "192.168.1.2",
                  "activate": [null],
                  "route-map": [
                    { "inout": "in",  "route-map-name": "RM-IN" },
                    { "inout": "out", "route-map-name": "RM-OUT" }
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  ]
}

HTTP Status: 200
```

### restconf_patch_interface.sh

```
=== RESTCONF PATCH — Loopback20 description ===
URL: https://10.10.20.48:443/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=20
Payload:
{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 20,
    "description": "RESTCONF-Lab-Loopback20"
  }
}

HTTP Status: 204
Description updated successfully.
```

---

## RESTCONF vs NETCONF

| Feature | RESTCONF | NETCONF |
|---|---|---|
| Standard | RFC 8040 | RFC 6241 |
| Transport | HTTPS (port 443) | SSH (port 830) |
| Data format | JSON or XML | XML only |
| Operations | GET / POST / PUT / PATCH / DELETE | `get-config` / `edit-config` / `commit` … |
| Tooling | curl, Postman, any HTTP client | ncclient, Python |
| Authentication | HTTP Basic / OAuth token | SSH credentials |
| Success on write | HTTP 204 No Content | `<ok/>` in XML reply |
| Use case | REST-friendly integrations, quick scripting | Full config management, transactions |
| YANG model used here | `Cisco-IOS-XE-native` | `Cisco-IOS-XE-native` |
