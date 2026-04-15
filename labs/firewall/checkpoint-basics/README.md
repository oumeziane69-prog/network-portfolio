# Lab — Check Point Firewall — Basics

## Objectif / Objective

**FR** — Prendre en main l'architecture Check Point (Security Gateway + Management Server), configurer des politiques de sécurité de base, NAT, et VPN site-à-site. Familiarisation avec SmartConsole et les logs.

**EN** — Get hands-on with Check Point architecture (Security Gateway + Management Server), configure basic security policies, NAT, and site-to-site VPN. Familiarize with SmartConsole and log analysis.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

  Internet
     |
[CP Gateway R81.x]──────[Management Server (SmartConsole)]
  /          \
LAN          DMZ
(192.168.1.0/24)  (10.10.1.0/24)

  Remote Site
     |
[CP Gateway 2] ──── Site-to-Site VPN ──── [CP Gateway 1]
```

**Équipements / Equipment:** Check Point R81.x (SmartConsole + Gateway VM) sur EVE-NG

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Check Point R81.x (GAIA OS) | Passerelle de sécurité |
| SmartConsole | Interface de gestion centralisée |
| SmartLog / SmartView | Analyse de logs |
| Check Point VPN (IKEv1/v2) | VPN site-à-site |
| NAT (Hide / Static) | Translation d'adresses |
| EVE-NG | Environnement de simulation réseau |

---

## Concepts couverts / Concepts Covered

- Architecture Check Point : SGW, SMS, SmartConsole
- Objets réseau, règles de sécurité, et blades
- NAT Hide (masquerading) et NAT statique
- VPN site-à-site avec IKEv2 et Phase 1/2
- Analyse de logs : SmartLog et audit trail
- Gestion des certificats et PKI interne
- Blade IPS : activation et tuning de signatures
