# Topology — Stormshield SNS Lab

## Schéma logique / Logical Diagram

```
  Internet (WAN)
       │ <WAN-IP>/30
       │ interface out
┌──────┴──────────────────────────────────────────────────────┐
│  Stormshield SNS (SN-S-Series-220 ou SNS-EVA VM)            │
│  interface out  : WAN — DHCP ou statique <WAN-IP>/30        │
│  interface dmz  : 172.16.60.1/24                            │
│  interface in   : 10.0.60.1/24                              │
│                                                             │
│  SMC (Stormshield Management Center) : optionnel            │
│  Qualification ANSSI EAL3+ (CSPN)                          │
└──────┬──────────────────┬──────────────────────────────────-┘
       │ DMZ               │ LAN (in)
  ┌────┴───────────┐   ┌───┴────────────────────────────────┐
  │  DMZ servers   │   │  LAN Interne                       │
  │  Web  : .10    │   │  Active Directory  : 10.0.60.101   │
  │  SFTP : .20    │   │  Client Windows    : 10.0.60.200+  │
  │  Proxy: .30    │   │  Admin station     : 10.0.60.10    │
  └────────────────┘   │  SNMP NMS          : 10.0.60.50    │
                       └────────────────────────────────────┘

  VPN IPSec site-à-site (IKEv2) :
  SNS HQ ──── Internet ──── SNS Site-B (172.16.61.0/24 remote LAN)

  SSL VPN (portail web) :
  Utilisateurs distants ──── HTTPS/443 ──── SNS (Virtual IP pool: 192.168.10.0/24)
```

---

## Contexte CNPE EDF / CNPE EDF Context

| Critère | Stormshield SNS | Pertinence CNPE |
|---------|----------------|----------------|
| **Qualification ANSSI** | CSPN (Certification Sécurité Premier Niveau) + EAL3+ | Exigée pour systèmes OIV et sensibles CNPE |
| **Conformité RGS** | Référentiel Général de Sécurité — niveau élevé | Administration publique et OIV |
| **Produit souverain** | Conception et développement France (Airbus CyberSecurity) | Réduction du risque d'espionnage industriel |
| **Gestion centralisée** | SMC (Stormshield Management Center) | Gestion multi-sites CNPE |
| **Support contractuel** | Support disponible en français — contrats spécifiques défense/nucléaire | SLA adapté |

---

## Plan d'adressage / Addressing Plan

| Interface | Réseau | Adresse SNS | Usage |
|-----------|--------|------------|-------|
| `out` (WAN) | `<WAN-NET>/30` | `<WAN-IP>` | Lien opérateur |
| `dmz` | `172.16.60.0/24` | `172.16.60.1` | Serveurs DMZ |
| `in` (LAN) | `10.0.60.0/24` | `10.0.60.1` | Réseau interne |
| VPN tunnel | `192.168.10.0/24` | Pool SSL VPN | Utilisateurs distants |
| VPN site-B remote | `172.16.61.0/24` | — | LAN site distant |

### Hôtes fixes / Fixed Hosts

| Hôte | IP | Interface | Rôle |
|------|----|-----------|------|
| SNS firewall | `10.0.60.1` / `172.16.60.1` / `<WAN-IP>` | Toutes | Stormshield SNS |
| Active Directory | `10.0.60.101` | in | LDAP auth utilisateurs |
| Admin station | `10.0.60.10` | in | Gestion SNS (HTTPS) |
| NMS (supervision) | `10.0.60.50` | in | Polling SNMP v3 |
| Web server | `172.16.60.10` | dmz | Serveur web HTTPS |
| SFTP server | `172.16.60.20` | dmz | Transferts de fichiers sécurisés |

---

## Composants Stormshield / SNS Components

| Composant | Description |
|-----------|-------------|
| **SAS** (System Administration Server) | Interface web d'administration sur port 443 — CLI `stcli` disponible en SSH |
| **ASQ** (Active Security Qualification) | Moteur d'inspection applicative et IPS — spécifique Stormshield |
| **SMC** | Gestion centralisée multi-firewall (optionnel — recommandé multi-sites) |
| **SSL VPN** | Portail web + client SN-SSL-VPN (OpenVPN-based) |
| **Filtrage URL** | Bases embarquées + cloud Stormshield Network Security |
