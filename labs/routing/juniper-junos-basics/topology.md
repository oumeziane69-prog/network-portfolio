# Topology — Juniper JunOS Basics Lab

## Schéma logique / Logical Diagram

```
                    AS 65001
          ┌─────────────────────────┐
          │  SRX1 (Juniper vSRX)    │
          │  Lo0 : 10.255.1.1/32   │
          │  ge-0/0/0 : 10.0.12.1  │
          │  ge-0/0/1 : 10.0.13.1  │
          └──────┬────────┬─────────┘
                 │ eBGP   │ eBGP
    10.0.12.0/30 │        │ 10.0.13.0/30
                 │        │
          ┌──────┘        └─────────────────┐
          │                                  │
  AS 65002│                                  │AS 65003
┌─────────┴──────────┐              ┌────────┴─────────────┐
│  SRX2 (Juniper vSRX│              │  R1-Cisco (IOS-XE)   │
│  Lo0 : 10.255.2.1  │              │  Lo0 : 10.255.3.1/32 │
│  ge-0/0/0 :        │  eBGP        │  Gi0/0 : 10.0.13.2   │
│    10.0.12.2       ├──────────────┤  Gi0/1 : 10.0.23.2   │
│  ge-0/0/1 :        │ 10.0.23.0/30 │                      │
│    10.0.23.1       │              └──────────────────────┘
└────────────────────┘
```

---

## Plan d'adressage / Addressing Plan

### Loopbacks

| Équipement | Interface | Adresse IP | AS BGP |
|------------|-----------|-----------|--------|
| SRX1 | lo0.0 | `10.255.1.1/32` | 65001 |
| SRX2 | lo0.0 | `10.255.2.1/32` | 65002 |
| R1-Cisco | Loopback0 | `10.255.3.1/32` | 65003 |

### Liens point-à-point / Point-to-Point Links

| Lien | Réseau | SRX1 / SRX2 / R1 | Interface SRX1/SRX2/R1 |
|------|--------|------------------|------------------------|
| SRX1 ↔ SRX2 | `10.0.12.0/30` | SRX1: `10.0.12.1` — SRX2: `10.0.12.2` | SRX1: ge-0/0/0 — SRX2: ge-0/0/0 |
| SRX1 ↔ R1 | `10.0.13.0/30` | SRX1: `10.0.13.1` — R1: `10.0.13.2` | SRX1: ge-0/0/1 — R1: Gi0/0 |
| SRX2 ↔ R1 | `10.0.23.0/30` | SRX2: `10.0.23.1` — R1: `10.0.23.2` | SRX2: ge-0/0/1 — R1: Gi0/1 |

---

## Sessions BGP / BGP Sessions

| Peer 1 | Peer 2 | Type | Source IP | Dest IP | Auth |
|--------|--------|------|-----------|---------|------|
| SRX1 (65001) | SRX2 (65002) | eBGP | 10.0.12.1 | 10.0.12.2 | MD5 `<BGP-PASSWORD-HERE>` |
| SRX1 (65001) | R1 (65003) | eBGP | 10.0.13.1 | 10.0.13.2 | MD5 `<BGP-PASSWORD-HERE>` |
| SRX2 (65002) | R1 (65003) | eBGP | 10.0.23.1 | 10.0.23.2 | MD5 `<BGP-PASSWORD-HERE>` |

---

## Équipements simulés / Simulated Equipment

| Équipement | Image EVE-NG / GNS3 | vCPU | vRAM | Notes |
|------------|---------------------|------|------|-------|
| SRX1 | Juniper vSRX 21.4R1 | 2 | 4 GB | vSRX in packet mode (routing only) |
| SRX2 | Juniper vSRX 21.4R1 | 2 | 4 GB | vSRX in packet mode |
| R1-Cisco | Cisco IOSv 15.9 ou IOS-XE | 1 | 512 MB | GNS3 : IOSvL2 ou CSR1000v |

---

## Préfixes annoncés par BGP / BGP Advertised Prefixes

Chaque routeur annonce uniquement son loopback via BGP :

| Routeur | Préfixe annoncé | Visible sur |
|---------|----------------|-------------|
| SRX1 | `10.255.1.1/32` | SRX2, R1 |
| SRX2 | `10.255.2.1/32` | SRX1, R1 |
| R1 | `10.255.3.1/32` | SRX1, SRX2 |

---

## Notes d'installation / Setup Notes

1. Démarrer les trois VMs dans l'ordre : SRX1 → SRX2 → R1
2. JunOS nécessite ~3 minutes de boot — attendre l'invite `login:`
3. Connexion console JunOS : login `root`, puis `cli` pour l'interface opérationnelle
4. Commencer par vérifier les interfaces avant de configurer BGP : `show interfaces terse`
