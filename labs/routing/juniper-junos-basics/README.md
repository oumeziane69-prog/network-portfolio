# Lab — Juniper JunOS Basics

## Objectif / Objective

**FR** — Prendre en main la CLI Junos et l'architecture hiérarchique de configuration des équipements Juniper (vSRX). Configurer des sessions BGP eBGP entre deux routeurs Juniper vSRX et un routeur Cisco IOS, et comprendre les différences fondamentales de syntaxe et de philosophie entre IOS et JunOS.

**EN** — Get hands-on with the Junos CLI and its hierarchical configuration architecture on Juniper vSRX devices. Configure eBGP sessions between two Juniper vSRX routers and a Cisco IOS router, and understand the fundamental syntax and philosophy differences between IOS and JunOS.

---

## Comparaison IOS vs JunOS / IOS vs JunOS Comparison

| Aspect | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| **Mode de config** | Ligne par ligne, immédiat | Hiérarchique, transaction validée par `commit` |
| **Annulation** | `no <commande>` pour chaque ligne | `rollback N` (50 versions conservées) |
| **Validation** | Immédiate dès saisie | Candidat config → `commit confirm` → actif |
| **Nommage interfaces** | `GigabitEthernet0/0` | `ge-0/0/0` (FPC/PIC/Port) |
| **Sécurité** | IOS ZBF (optionnel) | Security zones + policies (natif sur SRX) |
| **Filtres** | ACL (`access-list`) | Firewall filters (stateless) + security policies (stateful) |
| **BGP policy** | `route-map` + `prefix-list` | `policy-statement` + `prefix-list` |
| **Debug** | `debug ip bgp` | `traceoptions` dans la hiérarchie `protocols bgp` |

---

## Topologie / Topology

Voir [topology.md](topology.md)

```
SRX1 (AS 65001)  ←──eBGP──→  SRX2 (AS 65002)
       ↕  eBGP                     ↕  eBGP
      R1-Cisco (AS 65003)  ←──────┘
```

---

## Statut / Status

✅ Complété / Completed

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Juniper vSRX (JunOS 21.x) | Routeur/firewall — noeud BGP AS 65001 et 65002 |
| Cisco IOS-XE | Routeur — noeud BGP AS 65003 (interopérabilité) |
| BGP-4 eBGP (RFC 4271) | Protocole de routage inter-AS |
| Firewall filters JunOS | Protection du routing engine (PROTECT-RE) |
| Security zones JunOS | Segmentation et contrôle des flux sur SRX |
| EVE-NG / GNS3 | Environnement de simulation réseau |
| Python / Netmiko | Automatisation (optionnel) |

---

## Fichiers du lab / Lab Files

| Fichier | Description |
|---------|-------------|
| [topology.md](topology.md) | Plan d'adressage, schéma, description des équipements |
| [configs/SRX1.junos](configs/SRX1.junos) | Configuration complète SRX1 (AS 65001) |
| [configs/SRX2.junos](configs/SRX2.junos) | Configuration complète SRX2 (AS 65002) |
| [configs/R1-cisco.ios](configs/R1-cisco.ios) | Configuration Cisco IOS R1 (AS 65003) |
| [junos-vs-ios-cheatsheet.md](junos-vs-ios-cheatsheet.md) | Tableau comparatif CLI IOS ↔ JunOS |
| [verification.md](verification.md) | Commandes `show` JunOS avec output attendu |

---

## Concepts couverts / Concepts Covered

- CLI Junos : modes opérationnel et configuration, navigation dans la hiérarchie
- `commit`, `commit confirm`, `rollback`, `show | compare`
- Firewall filters JunOS vs ACL IOS : différences et application
- Security zones et policies sur vSRX
- Configuration BGP eBGP avec authentification MD5
- Export/import policies : `policy-statement` + `prefix-list`
- Interopérabilité Juniper ↔ Cisco sur une session BGP eBGP
