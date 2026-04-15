# Lab — VPN IPSec Site-to-Site

## Objectif / Objective

**FR** — Configurer et valider un tunnel VPN IPSec site-à-site entre deux pare-feux (Fortinet FortiGate), avec IKEv2, chiffrement AES-256-GCM, authentification par certificats X.509. Test du trafic, du fail-over, et du re-keying automatique.

**EN** — Configure and validate a site-to-site IPSec VPN tunnel between two firewalls (Fortinet FortiGate), using IKEv2, AES-256-GCM encryption, and X.509 certificate authentication. Test traffic, fail-over, and automatic re-keying.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

  Site A (HQ)                              Site B (Branch)
+──────────────+                         +──────────────+
| LAN A        |                         | LAN B        |
| 10.0.1.0/24  |                         | 10.0.2.0/24  |
|    [FGT-A]───|───── IPSec Tunnel ──────|───[FGT-B]    |
|    WAN: <IP> |   IKEv2 / AES-256-GCM  |   WAN: <IP>  |
+──────────────+                         +──────────────+

Phase 1 : IKEv2, AES-256-GCM, SHA-256, DH Group 14
Phase 2 : ESP, AES-256-GCM, PFS enabled
```

**Équipements / Equipment:** 2 × FortiGate VM (FortiOS 7.x) sur EVE-NG

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Fortinet FortiGate (FortiOS 7.x) | Pare-feu et endpoint VPN |
| IPSec (IKEv2) | Protocole de tunneling sécurisé |
| AES-256-GCM | Chiffrement symétrique du trafic |
| X.509 / PKI | Authentification par certificats |
| PFS (Perfect Forward Secrecy) | Protection des sessions passées |
| EVE-NG | Environnement de simulation réseau |

---

## Concepts couverts / Concepts Covered

- Phases IKE : Phase 1 (ISAKMP SA) et Phase 2 (IPSec SA)
- Modes de tunnel : tunnel mode vs transport mode
- Authentification PSK vs certificats X.509
- Sélecteurs de trafic et politiques de sécurité
- DPD (Dead Peer Detection) et re-keying
- Dépannage : `diagnose vpn ike`, `diagnose vpn tunnel`
- Scénario de fail-over : lien redondant avec SD-WAN
