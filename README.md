<div align="center">

# 👋 Hakim Oumeziane

### Administrateur Réseaux & Télécoms | NetDevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-oumeziane69--prog-181717?style=flat-square&logo=github)](https://github.com/oumeziane69-prog)
[![HNO Nightly Check](https://github.com/oumeziane69-prog/network-portfolio/actions/workflows/hno-nightly-check.yml/badge.svg?branch=main)](https://github.com/oumeziane69-prog/network-portfolio/actions/workflows/hno-nightly-check.yml)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profil-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/oumeziane69/)
[![▶ Formation YouTube](https://img.shields.io/badge/▶_Formation-YouTube-red?logo=youtube)](https://youtu.be/3CaPH8SWNH4)
[![CV](https://img.shields.io/badge/CV-PDF-blue?style=flat-square&logo=adobeacrobatreader)](https://raw.githubusercontent.com/oumeziane69-prog/network-portfolio/main/docs/cv-hakim-oumeziane.pdf)
[![Discussions](https://img.shields.io/badge/Discussions-purple?style=flat-square&logo=github)](https://github.com/oumeziane69-prog/network-portfolio/discussions)
[![▶ Formation HTML](https://img.shields.io/badge/▶_Formation-HTML-orange?style=flat-square)](docs/formation_netdevops.html)

</div>

---

## 🇫🇷 À propos / 🇬🇧 About

**FR** — Administrateur Réseaux & Télécoms avec une spécialisation progressive en **NetDevOps** : automatisation des déploiements de configurations réseau via des pipelines CI/CD, scripts Python et outils d'infrastructure as code. Je conçois et opère des pipelines bout-en-bout, de la génération de configuration jusqu'au déploiement sur équipements physiques.

**EN** — Network & Telecom Administrator with a growing focus on **NetDevOps**: automating network configuration deployments through CI/CD pipelines, Python scripting, and infrastructure-as-code tooling. I design and operate end-to-end pipelines, from configuration generation to physical device deployment.

---

## 🛠️ Stack technique / Tech Stack

### Équipements / Devices

| Catégorie | Marques / Brands |
|-----------|-----------------|
| Switches | Cisco, HP/Aruba, Juniper, Netgear, TP-Link |
| Routeurs / Routers | Cisco IOS/IOS-XE, MikroTik, Fortinet, Ubiquiti |
| Pare-feux / Firewalls | Fortinet FortiGate, Palo Alto, pfSense/OPNsense, Cisco ASA/FTD, Stormshield |
| Wi-Fi | Cisco Meraki, Aruba, Ubiquiti UniFi, Ruckus |
| VoIP | 3CX, Microsoft Teams Direct Routing, Cisco CUCM, Alcatel |

### Automatisation / Automation

| Outil / Tool | Rôle / Role |
|-------------|-------------|
| 🤖 Claude AI | Stratégie, génération de prompts / Strategy & prompt engineering |
| ⚡ Claude Code | Génération et exécution de code / Code generation & execution |
| 🔄 GitHub Actions | Validation CI/CD, auto-merge / CI/CD validation & auto-merge |
| 🐍 Netmiko (Python) | Déploiement sur équipements / Device deployment |
| 🐧 WSL | Environnement d'exécution / Runtime environment |
| 🐙 Git / GitHub | Versioning, branching strategy / Versioning & branching |
| 🤖 Renovate Bot | Mises à jour de dépendances automatisées / Automated dependency updates |

### Pipeline NetDevOps

\`\`\`
Claude AI  ──►  Claude Code  ──►  GitHub Actions  ──►  Netmiko  ──►  Équipements
(stratégie)    (génère+push)      (validation CI)      (Python)       (déploiement)
\`\`\`

---

## 📁 Projets / Projects

> Les dépôts sont privés pour des raisons de confidentialité.
> *Repositories are private for confidentiality reasons.*

### \`configs-reseau\` — Pipeline de déploiement réseau / Network Deployment Pipeline

**FR** Pipeline NetDevOps complet pour la gestion et le déploiement automatisé de configurations réseau multi-marques.

**EN** Full NetDevOps pipeline for automated multi-vendor network configuration management and deployment.

\`Python\` \`Netmiko\` \`GitHub Actions\` \`Cisco IOS\` \`Fortinet\`

---

### \`scc-coordinator\` — Coordination de livrables télécom / Telecom Deliverables Coordinator

**FR** Outil d'assistance à la production de livrables techniques télécom : CCTP, devis, PV de réception, rapports d'intervention.

**EN** Tool for assisting in the production of telecom technical deliverables: specifications, quotes, acceptance reports.

\`Claude AI\` \`Markdown\` \`Documentation\`

---

### \`telecom-ops-toolkit\` — Boîte à outils opérations télécom / Telecom Ops Toolkit

**FR** Bibliothèque de configurations et procédures pour des cas d'usage télécom avancés : SIP NAT, migration RNIS, fibre OTDR, RAN 5G NR NSA/SA.

**EN** Library of configurations and procedures for advanced telecom use cases: SIP NAT traversal, ISDN migration, fiber OTDR, 5G NR NSA/SA RAN.

\`SIP\` \`VoIP\` \`5G NR\` \`Fiber Optics\` \`RNIS/ISDN\`

---

## 🚀 Pipeline NetDevOps — `deploy_safe.py` & `vault.py`

**FR** — Ce pipeline bout-en-bout automatise le déploiement sécurisé de configurations sur équipements réseau physiques, avec des mécanismes de protection à chaque étape.

**EN** — This end-to-end pipeline automates the secure deployment of configurations to physical network devices, with protection mechanisms at every stage.

### Flux complet / Full Flow

```
Claude AI  ──►  Claude Code  ──►  GitHub Actions  ──►  Netmiko  ──►  Équipements
(stratégie)    (génère+push)      (validation CI)      (Python)       (déploiement)
```

### `deploy_safe.py` — Déploiement sécurisé / Safe Deployment

| Fonctionnalité 🇫🇷 | Feature 🇬🇧 |
|---|---|
| 📸 Snapshot pré-déploiement (`show run`) | 📸 Pre-deploy snapshot (`show run`) |
| 🔍 Mode dry-run (simulation sans appliquer) | 🔍 Dry-run mode (simulate without applying) |
| ↩️ Rollback automatique en cas d'échec | ↩️ Automatic rollback on failure |
| 📋 Journalisation horodatée de chaque opération | 📋 Timestamped logging of every operation |

**FR** — Avant tout déploiement, `deploy_safe.py` capture l'état courant de l'équipement (snapshot), exécute les commandes en mode dry-run pour validation, puis applique la configuration. En cas d'erreur détectée, le script restaure automatiquement le snapshot précédent via Netmiko.

**EN** — Before any deployment, `deploy_safe.py` captures the current device state (snapshot), runs commands in dry-run mode for validation, then applies the configuration. If an error is detected, the script automatically restores the previous snapshot via Netmiko.

### `vault.py` — Chiffrement des secrets / Secrets Encryption

| Fonctionnalité 🇫🇷 | Feature 🇬🇧 |
|---|---|
| 🔐 Chiffrement Fernet (AES-128-CBC + HMAC) | 🔐 Fernet encryption (AES-128-CBC + HMAC) |
| 🗄️ Stockage sécurisé des credentials SSH/Telnet | 🗄️ Secure storage of SSH/Telnet credentials |
| 🔑 Clé dérivée depuis variable d'environnement | 🔑 Key derived from environment variable |
| 🚫 Aucune donnée sensible en clair dans le dépôt | 🚫 No plaintext sensitive data in the repository |

**FR** — `vault.py` utilise la bibliothèque `cryptography` avec l'algorithme Fernet pour chiffrer les identifiants SSH/Telnet des équipements. La clé de chiffrement est injectée via une variable d'environnement (`VAULT_KEY`) ou un secret GitHub Actions — jamais stockée dans le code.

**EN** — `vault.py` uses the `cryptography` library with the Fernet algorithm to encrypt SSH/Telnet device credentials. The encryption key is injected via an environment variable (`VAULT_KEY`) or a GitHub Actions secret — never stored in code.

```python
# vault.py — usage example (no real credentials committed)
vault = Vault(key=os.environ["VAULT_KEY"])
creds = vault.decrypt("<ENCRYPTED-BLOB-HERE>")
# deploy_safe.py uses creds to connect via Netmiko
```

`Python` `Netmiko` `Fernet` `GitHub Actions` `Cisco IOS` `CI/CD`

---

## 📊 Compétences clés / Key Skills

| 🇫🇷 Compétence | 🇬🇧 Skill |
|---|---|
| ✅ Administration réseau multi-constructeurs | ✅ Multi-vendor network administration |
| ✅ Sécurité & segmentation (VLAN, ACL, VPN) | ✅ Security & segmentation (VLAN, ACL, VPN) |
| ✅ Automatisation Python / Netmiko | ✅ Python / Netmiko automation |
| ✅ Pipelines CI/CD GitHub Actions | ✅ GitHub Actions CI/CD pipelines |
| ✅ Infrastructure as Code (IaC) | ✅ Infrastructure as Code (IaC) |
| ✅ VoIP & Téléphonie IP | ✅ VoIP & IP Telephony |
| ✅ Fibre optique & mesures OTDR | ✅ Fiber optics & OTDR measurements |
| ✅ 5G NR NSA/SA | ✅ 5G NR NSA/SA |

---


## 🎯 Compétences techniques / Technical Skills Matrix

> ✅ Maîtrisé — 🚧 En cours — 📅 Planifié

### Routage & Protocoles / Routing & Protocols

| Compétence / Skill | Détail | Statut |
|--------------------|--------|--------|
| OSPF multi-area | OSPFv2/v3, ABR, ASBR, stub/NSSA, LSA types | ✅ Maîtrisé |
| BGP iBGP / eBGP | Route Reflector, attributs MED/LP/Communities, filtrage | ✅ Maîtrisé |
| MPLS / L3VPN | LDP, VRF, MP-BGP VPNv4, PE/P/CE | 🚧 En cours |
| Juniper JunOS | Interfaces, politiques de routage, sessions BGP | 🚧 En cours |
| VLAN / Spanning Tree | 802.1Q, RSTP, VTP, agrégation LACP | ✅ Maîtrisé |
| QoS réseau | Classification, marquage DSCP, policing/shaping | ✅ Maîtrisé |

### Sécurité firewall / Firewall Security

| Compétence / Skill | Détail | Statut |
|--------------------|--------|--------|
| Fortinet FortiGate | NGFW, IPS, SSL-VPN, IPSec, FortiOS 7.x, NSE4 | 🚧 En cours |
| Check Point | R81.x, SmartConsole, Security Gateway, VPN | 🚧 En cours |
| Stormshield SNS | SNS OS, politiques, IPS ASQ, VPN SSL/IPSec | 📅 Planifié |
| pfSense / OPNsense | Firewall open-source, règles NAT, HAProxy | ✅ Maîtrisé |
| Cisco ASA / FTD | ACL, NAT, AnyConnect VPN, FTD avec FMC | ✅ Maîtrisé |
| Palo Alto NGFW | Security policies, App-ID, URL filtering | 🚧 En cours |

### Architecture sécurité / Security Architecture

| Compétence / Skill | Détail | Statut |
|--------------------|--------|--------|
| DMZ multi-niveau | Architecture IT/OT, IDMZ, segmentation Purdue | ✅ Maîtrisé |
| VPN IPSec site-à-site | IKEv2, AES-256-GCM, PFS, certificats X.509 | ✅ Maîtrisé |
| IDS/IPS (Suricata) | Règles, EVE JSON, intégration ELK, tuning | 🚧 En cours |
| RADIUS / 802.1X | FreeRADIUS, EAP-TLS, PEAP, MAB fallback, VLAN dynamique | ✅ Maîtrisé |
| [Matrice de flux IT/OT](docs/flux-matrix-IT-OT.md) | Modèle Purdue, default deny, protocoles OT | ✅ Maîtrisé |
| Zero Trust | Principes, micro-segmentation, identity-based access | 🚧 En cours |

> 📄 [Cas d'usage sécurité / Security use cases](docs/security-usecases.md)

### Sécurité industrielle OT / OT Industrial Security

| Compétence / Skill | Détail | Statut |
|--------------------|--------|--------|
| [IEC 62443](docs/iec62443-overview.md) | Zones/conduits, SL 1-4, FR 1-7, gap analysis | 🚧 En cours |
| Modèle de Purdue | Niveaux 0-4, IDMZ, segmentation SCADA/HMI/PLC | ✅ Maîtrisé |
| Protocoles OT | Modbus TCP, DNP3, OPC-UA, S7Comm | 🚧 En cours |
| Sécurité SCADA | Hardening, whitelisting applicatif, IDS OT | 📅 Planifié |
| ANSSI Guide ICS | Recommandations sécurité systèmes industriels FR | 🚧 En cours |
| NIS2 / OIV | Obligations réglementaires opérateurs critiques | 🚧 En cours |

### Documentation technique / Technical Documentation

| Compétence / Skill | Détail | Statut |
|--------------------|--------|--------|
| [DAT (Dossier d'Architecture Technique)](docs/templates/DAT-template.md) — [exemple DMZ industrielle](docs/DAT-example-dmz-industrial.md) | Topologie, matrice de flux, règles firewall, risques | ✅ Maîtrisé |
| [DEX (Document d'Exploitation)](docs/templates/DEX-template.md) | Procédure, rollback, contrôles post-intervention | ✅ Maîtrisé |
| Schémas réseau (ASCII / draw.io) | Diagrammes logiques et physiques | ✅ Maîtrisé |
| Audit et rapports de sécurité | Synthèse de vulnérabilités, plan de remédiation | 🚧 En cours |

### Méthodes & Agilité / Methods & Agile

| Compétence / Skill | Détail | Statut |
|--------------------|--------|--------|
| SAFe (Scaled Agile Framework) | PI Planning, Agile Release Train, backlog | 🚧 En cours |
| Agile / Scrum | Sprints, user stories, rétrospectives | ✅ Maîtrisé |
| ITIL (bases) | Gestion des incidents, changements, problèmes | ✅ Maîtrisé |
| Gestion de projet | Planification, jalons, coordination équipes | ✅ Maîtrisé |

> Les labs pratiques associés à ces compétences sont disponibles dans le dossier [`labs/`](labs/).

---

## 🔬 Labs actifs / Active Labs

| Lab | Stack | Statut |
|-----|-------|--------|
| **DevNet** | | |
| `devnet-bgp` | C8000V · BGP · IOS-XE | ✅ Complété |
| `devnet-bgp-attributes` | IOS-XE · BGP · Local-Pref · MED | ✅ Complété |
| `devnet-bgp-ebgp` | IOS-XE · eBGP AS65001/65002 | ✅ Complété |
| `devnet-bgp-filtering` | IOS-XE · BGP · prefix-list | ✅ Complété |
| `devnet-mpls` | IOS-XE · MPLS · LDP | ✅ Complété |
| `devnet-mpls-l3vpn` | IOS-XE · LDP · MP-BGP · VRF | ✅ Complété |
| `devnet-netconf` | C8000V · ncclient · YANG | ✅ Complété |
| `devnet-ospf` | C8000V · OSPF Area 0 | ✅ Complété |
| `devnet-ospf-vpn` | Cat8kv · OSPF · OpenConnect VPN | ✅ Complété |
| `devnet-redistribution` | IOS-XE · OSPF → BGP redistribution | ✅ Complété |
| **Routing** | | |
| `routing/bgp-ibgp-ebgp` | IOS-XE · iBGP · eBGP · Route Reflector | ✅ Complété |
| `routing/juniper-junos-basics` | vSRX · JunOS · BGP eBGP | ✅ Complété |
| `routing/mpls-l3vpn` | IOS-XE · LDP · VRF · MP-BGP | ✅ Complété |
| `routing/mpls-traffic-engineering` | IOS-XE · RSVP-TE · FRR | 🚧 En cours |
| `routing/ospf-multi-area` | IOS-XE · OSPF · ABR/ASBR · stub/NSSA | ✅ Complété |
| `routing/gre-over-ipsec` | IOS-XE · GRE · IPSec · IKEv2 | ✅ Complété |
| `routing/qos` | IOS-XE · MQC · DSCP · policing | ✅ Complété |
| `routing/sdwan-lite` | IOS-XE · PBR · IP SLA · SD-WAN | ✅ Complété |
| `bgp-filtering` | C8000V · BGP · prefix-list · AS-path · communities | ✅ Complété |
| `gre-tunnel` | IOS-XE · GRE · Tunnel0 · static routing | ✅ Complété |
| `ipsla` | IOS-XE · IP SLA · icmp-echo · track · floating route | ✅ Complété |
| `ospf-multiarea` | IOS-XE · OSPFv2 · ABR · Area 0/Area 1 · LSA 3 | ✅ Complété |
| `qos` | IOS-XE · MQC · class-map · priority · bandwidth | ✅ Complété |
| **Firewall** | | |
| `firewall/checkpoint-basics` | R81.x · SmartConsole · VPN | 🚧 En cours |
| `firewall/fortinet-dmz-industrial` | FortiOS 7.x · IT/OT · IDMZ | 🚧 En cours |
| `firewall/stormshield-sns` | SNS OS · IPS ASQ · VPN SSL/IPSec | 📅 Planifié |
| **Security Services** | | |
| `security-services/ids-ips-suricata` | Suricata · ELK · custom rules | 🚧 En cours |
| `security-services/radius-dot1x` | FreeRADIUS · 802.1X · MAB · Cisco | ✅ Complété |
| `security-services/vpn-ipsec-site-to-site` | FortiGate · IKEv2 · AES-256-GCM · X.509 | ✅ Complété |
| **OT Industrial** | | |
| `ot-industrial/iec62443-overview` | IEC 62443 · SL 1-4 · zones/conduits | 🚧 En cours |
| `ot-industrial/purdue-model-segmentation` | Purdue · IDMZ · SCADA/HMI/PLC | ✅ Complété |
| **Transmission** | | |
| `transmission` | Faisceau hertzien · Fibre optique · OTDR | ✅ Complété |
| **Programmabilité / Programmability** | | |
| `netconf` | C8000V · NETCONF · YANG · ncclient | ✅ Complété |
| `restconf` | C8000V · RESTCONF · HTTP · JSON · YANG | ✅ Complété |
| `eem` | IOS-XE · EEM · syslog · timer 60s | ✅ Complété |
| `jinja2` | Python · Jinja2 · Netmiko · BGP template | ✅ Complété |

---

## 📚 Formation NetDevOps

Pipeline CI/CD complet pour automatiser le déploiement de configurations réseau multi-constructeurs, de la génération IA au déploiement physique via Netmiko.

📄 [Voir la formation](docs/formation_netdevops.html)

[![▶ Voir la vidéo](https://img.shields.io/badge/▶_Vidéo-YouTube-red)](https://youtu.be/vfQ1HxVoSHo)

---


## 📊 GitHub Stats

<div align="center">

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=oumeziane69-prog&show_icons=true&theme=dark&hide_border=true&count_private=true)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=oumeziane69-prog&layout=compact&theme=dark&hide_border=true)

![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=oumeziane69-prog&theme=dark&hide_border=true)

</div>

---

## 🗺️ Roadmap

**FR** — Suivi de progression des labs, certifications et projets NetDevOps. Tableau de bord complet disponible sur GitHub Project.

**EN** — Progress tracking for NetDevOps labs, certifications, and projects. Full board available on GitHub Project.

[![GitHub Project — Network Portfolio Roadmap](https://img.shields.io/badge/GitHub_Project-Network_Portfolio_Roadmap-0075ca?style=flat-square&logo=github)](https://github.com/users/oumeziane69-prog/projects/1)

| Item | Type | Tech | Priority | Status |
|------|------|------|----------|--------|
| MPLS VRF L3VPN Lab | Lab | Cisco | High | ✅ Completed |
| BGP eBGP AS65001/65002 | Lab | Cisco | High | ✅ Completed |
| Netmiko automation pipeline | Script | Python | High | ✅ Completed |
| NETCONF/YANG lab | Lab | Cisco | Medium | ✅ Completed |
| pyATS lab | Lab | Cisco | Medium | ✅ Completed |
| CI/CD NetDevOps pipeline | Documentation | Python | High | ✅ Completed |
| NSE4 Fortinet ([study guide](docs/certif-prep/nse4-study-guide.md) · [cheatsheet](docs/certif-prep/nse4-cheatsheet.md)) | Certification | Fortinet | High | 🔨 In Progress |
| DevNet Associate | Certification | Cisco | High | 🎯 Roadmap |

---

## 📬 Contact

Tu peux me retrouver sur **LinkedIn**, par **email** ou via mon profil **GitHub** ci-dessus.
📧 [oumeziane.69@gmail.com](mailto:oumeziane.69@gmail.com) · 📄 [CV PDF](docs/cv-hakim-oumeziane.pdf) · 📄 [CV Canva](https://www.canva.com/design/DAHFDa3H5No/view)

*Feel free to reach out via **LinkedIn**, **email**, or my **GitHub** profile above.*
*📧 [oumeziane.69@gmail.com](mailto:oumeziane.69@gmail.com) · 📄 [CV PDF](docs/cv-hakim-oumeziane.pdf) · 📄 [CV Canva](https://www.canva.com/design/DAHFDa3H5No/view)*

---

<div align="center">

*Le développement actif se fait en dépôts privés — ce portfolio présente l'architecture, les labs et la documentation.*

*Active development happens in private repos — this portfolio showcases architecture, labs & documentation.*

*Dernière mise à jour : Avril 2026 / Last updated: April 2026*

</div>

