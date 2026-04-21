# Lab — MPLS L3VPN (VRF CLIENT_A on Cat8k)

---

## FR — Description

Simulation d'un réseau MPLS L3VPN sur un seul équipement Cisco Catalyst 8000 (IOS-XE).  
L'objectif est de configurer une instance VRF complète (`CLIENT_A`), d'activer MPLS LDP sur le lien backbone, de monter une session MP-BGP avec address-family VPNv4, et de placer une interface CE dans la VRF.

### Objectif

| Composant        | Rôle                                                        |
|------------------|-------------------------------------------------------------|
| VRF `CLIENT_A`   | Isolation du plan d'adressage client                        |
| MPLS LDP         | Distribution des labels sur le lien backbone                |
| MP-BGP VPNv4     | Transport des routes VPN entre PE (ou simulation mono-PE)   |
| GigabitEthernet2 | Interface CE — adresse `192.168.1.1/24` dans la VRF         |

### Topologie (simulation mono-device)

```
  CE1 ─────────────────────────────────── CE2
        │                           │
       PE1 ──── P (backbone) ──── PE2
       Gi2      Gi1 (MPLS LDP)   (simulé)
  VRF CLIENT_A  AS65000 BGP VPNv4
```

> Dans ce lab, PE1 est le seul équipement physique. CE1, P, et PE2 sont simulés
> ou représentés par des loopbacks/neighbors statiques.

### Paramètres de configuration

| Paramètre              | Valeur             |
|------------------------|--------------------|
| VRF name               | `CLIENT_A`         |
| Route Distinguisher    | `65000:1`          |
| Route Target export    | `65000:1`          |
| Route Target import    | `65000:1`          |
| Interface backbone     | `GigabitEthernet1` |
| Interface CE (VRF)     | `GigabitEthernet2` |
| Adresse CE             | `192.168.1.1/24`   |
| BGP AS                 | `65000`            |
| BGP neighbor (PE2)     | `10.0.0.2`         |
| Update-source          | `Loopback0`        |

### Commandes de vérification

```bash
# Liste des VRFs et leurs RD
show ip vrf

# Session LDP avec le voisin backbone
show mpls ldp neighbor

# Table BGP VPNv4 (toutes les VRFs)
show bgp vpnv4 unicast all

# Table de forwarding MPLS (LFIB)
show mpls forwarding-table
```

### Comment exécuter le script

1. **Prérequis** : Python 3.10+, `netmiko` installé.

   ```bash
   pip install netmiko
   ```

2. **Renseigner les credentials** dans `mpls_l3vpn_lab.py` :

   ```python
   DEVICE = {
       "device_type": "cisco_ios",
       "host": "<HOST-HERE>",       # IP ou hostname du Cat8k
       "username": "<USER-HERE>",   # compte SSH
       "password": "<PASS-HERE>",   # mot de passe SSH
   }
   ```

3. **Lancer le script** depuis la racine du lab :

   ```bash
   cd labs/devnet-mpls-l3vpn
   python mpls_l3vpn_lab.py
   ```

4. **Consulter les résultats** dans `logs/mpls_l3vpn_output.txt`.

---

## EN — Description

Single-device MPLS L3VPN simulation on a Cisco Catalyst 8000 (IOS-XE).  
The lab configures a complete VRF instance (`CLIENT_A`), enables MPLS LDP on the backbone link, establishes an MP-BGP VPNv4 session, and places a CE-facing interface inside the VRF.

### Objective

| Component        | Role                                                        |
|------------------|-------------------------------------------------------------|
| VRF `CLIENT_A`   | Customer address-space isolation                            |
| MPLS LDP         | Label distribution on the backbone link                     |
| MP-BGP VPNv4     | VPN route transport between PEs (single-PE simulation)      |
| GigabitEthernet2 | CE interface — address `192.168.1.1/24` inside the VRF      |

### Topology (single-device simulation)

```
  CE1 ─────────────────────────────────── CE2
        │                           │
       PE1 ──── P (backbone) ──── PE2
       Gi2      Gi1 (MPLS LDP)   (simulated)
  VRF CLIENT_A  AS65000 BGP VPNv4
```

> In this lab, PE1 is the only physical device. CE1, P, and PE2 are simulated
> or represented by loopbacks / static neighbors.

### Configuration Parameters

| Parameter              | Value              |
|------------------------|--------------------|
| VRF name               | `CLIENT_A`         |
| Route Distinguisher    | `65000:1`          |
| Route Target export    | `65000:1`          |
| Route Target import    | `65000:1`          |
| Backbone interface     | `GigabitEthernet1` |
| CE interface (VRF)     | `GigabitEthernet2` |
| CE address             | `192.168.1.1/24`   |
| BGP AS                 | `65000`            |
| BGP neighbor (PE2)     | `10.0.0.2`         |
| Update-source          | `Loopback0`        |

### Verification Commands

```bash
# List VRFs and their RDs
show ip vrf

# LDP session with backbone neighbor
show mpls ldp neighbor

# BGP VPNv4 table (all VRFs)
show bgp vpnv4 unicast all

# MPLS forwarding table (LFIB)
show mpls forwarding-table
```

### How to Run the Script

1. **Prerequisites**: Python 3.10+, `netmiko` installed.

   ```bash
   pip install netmiko
   ```

2. **Set credentials** in `mpls_l3vpn_lab.py`:

   ```python
   DEVICE = {
       "device_type": "cisco_ios",
       "host": "<HOST-HERE>",       # Cat8k IP or hostname
       "username": "<USER-HERE>",   # SSH account
       "password": "<PASS-HERE>",   # SSH password
   }
   ```

3. **Run the script** from the lab directory:

   ```bash
   cd labs/devnet-mpls-l3vpn
   python mpls_l3vpn_lab.py
   ```

4. **Check results** in `logs/mpls_l3vpn_output.txt`.
