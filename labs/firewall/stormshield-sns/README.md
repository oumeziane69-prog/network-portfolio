# Lab — Stormshield SNS

## Objectif / Objective

**FR** — Configurer un pare-feu Stormshield Network Security (SNS) pour un cas d'usage entreprise : politiques de filtrage, IPS, VPN SSL et IPSec, proxy HTTP/HTTPS, et durcissement de l'administration. Préparation à la certification SNS-100.

**EN** — Configure a Stormshield Network Security (SNS) firewall for an enterprise use case: filtering policies, IPS, SSL and IPSec VPN, HTTP/HTTPS proxy, and administration hardening. Preparation for the SNS-100 certification.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

  Internet (WAN)
       |
  [SNS Firewall]
   /    |    \
  LAN  DMZ  VPN Users
  |         (SSL VPN)
[Active Directory]

  Remote Branch ──── IPSec VPN ──── SNS (HQ)
```

**Équipements / Equipment:** Stormshield SNS VM (EVA) sur EVE-NG ou VMware

---

## Statut / Status

📅 Planifié / Planned

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Stormshield SNS (SNS OS) | Pare-feu de nouvelle génération (NGFW) |
| SSL VPN (OpenVPN) | Accès distant sécurisé |
| IPSec IKEv2 | VPN site-à-site |
| IPS / ASQ | Inspection applicative et prévention d'intrusion |
| Proxy HTTP/HTTPS | Filtrage du web et inspection SSL |
| Active Directory | Authentification utilisateur (LDAP/Kerberos) |
| SMC (Stormshield Management Center) | Gestion centralisée (optionnel) |

---

## Concepts couverts / Concepts Covered

- Interface d'administration SNS : SAS (System Administration Server)
- Politiques de filtrage et règles NAT
- Profils IPS et protection contre les exploits
- VPN SSL : portail web et client VPN
- IPSec IKEv2 avec certificats ou PSK
- Proxy explicite et transparent avec inspection SSL
- Durcissement : bannière SSH, comptes admin, supervision SNMP
- Préparation SNS-100 : domaines de l'examen
