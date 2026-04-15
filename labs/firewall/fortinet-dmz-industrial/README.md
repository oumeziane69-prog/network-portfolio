# Lab — Fortinet FortiGate — DMZ Industrial

## Objectif / Objective

**FR** — Concevoir et configurer une DMZ industrielle (IT/OT) sur FortiGate, avec segmentation entre les réseaux bureautiques, la DMZ (serveurs exposés), et le réseau OT (SCADA/ICS). Mise en oeuvre de politiques de sécurité strictes, NAT, et inspection applicative.

**EN** — Design and configure an industrial DMZ (IT/OT) on FortiGate, with segmentation between corporate networks, the DMZ (exposed servers), and the OT network (SCADA/ICS). Implement strict security policies, NAT, and application inspection.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

  Internet
     |
 [FortiGate] (perimeter)
  /    |    \
LAN   DMZ   OT Network
(IT)  (Web, (SCADA,
      SFTP)  Historian)

  LAN  ──►  DMZ   : allowed (restricted)
  LAN  ──►  OT    : denied by default
  DMZ  ──►  OT    : denied
  OT   ──►  DMZ   : historian polling only (port 443)
  OT   ──►  Internet : denied
```

**Équipements / Equipment:** FortiGate VM (FortiOS 7.x) + FortiSwitch simulé

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Fortinet FortiGate (FortiOS 7.x) | Pare-feu de périmètre et segmentation |
| FortiSwitch | Commutation avec VLAN 802.1Q |
| VLAN (802.1Q) | Isolation des segments réseau |
| NAT / PAT | Translation d'adresses |
| Application Control | Inspection L7 du trafic OT |
| IPS (Intrusion Prevention) | Détection d'intrusion en ligne |
| EVE-NG / FortiOS VM | Environnement de simulation |

---

## Concepts couverts / Concepts Covered

- Architecture DMZ multi-niveau pour réseaux IT/OT
- Politiques de sécurité FortiGate : zones, interfaces, profils
- NAT statique et dynamique (PAT)
- Inspection SSL/TLS et profilage applicatif
- Intégration FortiSwitch (FortiLink)
- Matrice de flux : documentation et validation
- Journalisation FortiAnalyzer (introduction)
