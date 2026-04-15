<div align="center">

# 👋 Hakim Oumeziane

### Administrateur Réseaux & Télécoms | NetDevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-oumeziane69--prog-181717?style=flat-square&logo=github)](https://github.com/oumeziane69-prog)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profil-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/oumeziane69/)
[![▶ YouTube](https://img.shields.io/badge/▶_Formation-YouTube-red?logo=youtube)](https://youtu.be/vfQ1HxVoSHo)

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

## 🗺️ Roadmap & Certifications

**FR** — Plan de montée en compétences sur les technologies réseau et sécurité, orienté expertises opérateur et sécurité industrielle.

**EN** — Skills development roadmap focused on carrier-grade networking and industrial security expertise.

| Étape | Certification / Compétence | Domaine | Statut |
|-------|---------------------------|---------|--------|
| 1 | **NSE 4** — Fortinet Network Security Professional | Firewall / NGFW | 🔄 En cours |
| 2 | **NSE 7** — Fortinet Network Security Architect | Architecture sécurité | 🗓️ Planifié |
| 3 | **MPLS / L3VPN** — Approfondissement opérateur | Routage avancé | 🗓️ Planifié |
| 4 | **Stormshield SNS-100** — Administrateur SNS | Firewall industriel FR | 🗓️ Planifié |

```
NSE4 ──► NSE7 ──► MPLS/L3VPN ──► SNS-100
 (NGFW)  (Archi)  (Opérateur)   (OT/FR)
```

> Les labs pratiques associés à cette roadmap sont disponibles dans le dossier [`labs/`](labs/).

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

![GitHub Streak](https://streak-stats.demolab.com/?user=oumeziane69-prog&theme=dark&hide_border=true)

</div>

---

## 📬 Contact

Tu peux me retrouver sur **LinkedIn** ou via mon profil **GitHub** ci-dessus.

*Feel free to reach out via **LinkedIn** or my **GitHub** profile above.*

---

<div align="center">

*Ce profil GitHub est en consultation uniquement — les dépôts de travail sont privés.*

*This GitHub profile is read-only — working repositories are private.*

</div>

