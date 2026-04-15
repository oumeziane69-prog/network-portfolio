# Lab — RADIUS / 802.1X

## Objectif / Objective

**FR** — Déployer l'authentification 802.1X sur un réseau filaire avec FreeRADIUS comme serveur d'authentification, Active Directory comme backend LDAP, et des switches Cisco comme authenticators. Mise en oeuvre du fallback MAB (MAC Authentication Bypass) pour les équipements sans supplicant 802.1X.

**EN** — Deploy 802.1X authentication on a wired network with FreeRADIUS as authentication server, Active Directory as LDAP backend, and Cisco switches as authenticators. Implement MAB (MAC Authentication Bypass) fallback for devices without 802.1X supplicant.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

[Endpoint (supplicant)]
       | EAP (802.1X)
[Cisco Switch (authenticator)]
       | RADIUS (UDP 1812/1813)
[FreeRADIUS Server]
       | LDAP/Kerberos
[Active Directory (Windows Server)]

MAB fallback path (printers, IoT):
[Device without 802.1X] ──► [Switch] ──► RADIUS (MAC lookup) ──► Guest VLAN or restricted VLAN
```

**Équipements / Equipment:** Cisco Catalyst IOS (EVE-NG) + FreeRADIUS VM + Windows Server VM

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Cisco Catalyst IOS | Authenticator 802.1X |
| FreeRADIUS 3.x | Serveur RADIUS (AAA) |
| Active Directory (LDAP) | Backend d'authentification |
| EAP-TLS / PEAP-MSCHAPv2 | Méthodes EAP d'authentification |
| MAB (MAC Authentication Bypass) | Fallback pour équipements sans supplicant |
| VLAN dynamique | Attribution de VLAN post-authentification |
| EVE-NG | Environnement de simulation réseau |

---

## Concepts couverts / Concepts Covered

- Architecture AAA : Authentication, Authorization, Accounting
- EAP-TLS (authentification par certificat) vs PEAP-MSCHAPv2 (login/mdp)
- Configuration Cisco : `dot1x`, `authentication port-control auto`
- FreeRADIUS : modules LDAP, EAP, policy
- MAB : contournement pour imprimantes, caméras IP, IoT
- VLAN dynamique via attributs RADIUS (Tunnel-Type, Tunnel-Medium-Type)
- Journalisation et audit RADIUS (Accounting)
- Guest VLAN et Auth-Fail VLAN
