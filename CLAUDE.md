# CLAUDE.md — network-portfolio

## Context / Contexte

**EN** — Public portfolio repository for Hakim Oumeziane, Network & Telecom Administrator / NetDevOps Engineer.
Contains a bilingual (FR/EN) README and a NetDevOps training document (`docs/formation_netdevops.html`).
All working repositories (configs-reseau, scc-coordinator, telecom-ops-toolkit) are private.

**FR** — Dépôt de portfolio public pour Hakim Oumeziane, Administrateur Réseaux & Télécoms / Ingénieur NetDevOps.
Contient un README bilingue (FR/EN) et un document de formation NetDevOps (`docs/formation_netdevops.html`).
Tous les dépôts de travail (configs-reseau, scc-coordinator, telecom-ops-toolkit) sont privés.

---

## Branch Conventions / Conventions de branches

All Claude Code feature branches follow this pattern:

```
claude/<task-slug>-<short-id>
```

Examples:
- `claude/add-gitignore-claude-md-K9mX3`
- `claude/update-youtube-link-ZMCO7`
- `claude/fix-scroll-speed-QQuhq`

Rules:
- Branch names and file names must be in **English only**
- One branch per task, one PR per branch
- Never push directly to `main`

---

## PR Workflow

1. Create branch from `main`: `git checkout -b claude/<task>-<id>`
2. Make changes, commit with a clear message
3. Push: `git push -u origin <branch>`
4. Open PR targeting `main`
5. PR is reviewed and merged by the repository owner (Hakim Oumeziane)

---

## README Style Rules

- **Bilingual**: all sections have a FR label and an EN label
- **Badges**: use `img.shields.io` flat-square style for GitHub, LinkedIn; standard style for YouTube
- **Tables**: used for tech stack, skills, and structured comparisons
- **No emojis in file/folder names** — emojis allowed in README headings and badges only
- Keep the pipeline diagram in plain ASCII (```code block```)

---

## Security Rules / Règles de sécurité

**Never commit the following into any file tracked by git:**

- Real passwords or credentials
- Pre-shared keys (PSK), API keys, tokens
- Real IP addresses of production equipment
- Personal email addresses or phone numbers
- Private keys (`.key`, `.pem`, `.p12`)

Use placeholders in examples: `<IP-HERE>`, `<PASSWORD-HERE>`, `<TOKEN-HERE>`

Real values must come from `.env` files that are listed in `.gitignore` and never committed.

---
## Session Log

After every Claude Code session, append a summary here:

Format:
### YYYY-MM-DD — <branch-name>
- Files modified: <list>
- Actions: <summary>
- Status: ✅ Done / 🔄 In progress / ⚠️ Issue

### 2026-04-25
- HNO Nightly Check : 4/4 ✅ verts
- Fix faux positif structure docs/scripts : telecom-ops-toolkit PR #54
- Ajout compteur fichiers 24h HNO : 4 repos PR #103/70/55/83
- Fix Node.js 20→24 Actions : 4 repos PR #104/71/+2
- Test multi-agents : concluant, timeout sur configs-reseau (7 fichiers)

### 2026-04-26
- GitHub Discussions activé sur network-portfolio
- README : badges corrigés, 24 labs listés, NSE4 on hold, badge Formation HTML, badge YouTube
- Labs DevNet : OSPF multi-area, GRE over IPSec, QoS MQC, SD-WAN Lite (PBR+IP SLA)
- PRs mergées : #94 #95 #96 #97 #98 #99 #100
- HNO bloqué jusqu'au 1er mai (carte expirée)
- Lab BGP Filtering : prefix-list, AS-path ACL, route-map, communities (cat8000v AS65001, IOS-XE 17.12.2)
- Lab NETCONF : get-config BGP/YANG, edit-config interface Loopback2
- PR #103 merged — labs/bgp-filtering/ ajouté sur main

### 2026-04-27
- Lab RESTCONF : GET BGP (HTTP 200 JSON), PATCH Loopback20 (HTTP 204)
- PR #107 merged — labs/restconf/ ajouté sur main
- Stack programmabilité complète validée : CLI → NETCONF → RESTCONF → Netmiko → pyATS

### 2026-04-27 (suite)
- Lab EEM : HEARTBEAT (timer 60s), BGP-NEIGHBOR-DOWN (syslog), SAVE-NOTIFIER (cli pattern)
- Test live : event manager run HEARTBEAT → syslog confirmé
- PR #109 merged — labs/eem/ ajouté sur main

### 2026-04-27 (suite 2)
- Lab IP SLA : icmp-echo 10.10.20.50, RTT=1ms, track 1 Up, route flottante AD=10
- PR #111 merged — labs/ipsla/ ajouté sur main

### 2026-04-27 (suite 3)
- Lab Jinja2 : template BGP neighbor, render + push Netmiko live sur cat8000v
- PR #113 merged — labs/jinja2/ ajouté sur main

### 2026-04-27 (suite 4)
- Lab OSPF multi-area : router-id 2.2.2.2, ABR Area 0/Area 1, LSA Type 3 inter-area
- PR #115 merged — labs/ospf-multiarea/ ajouté sur main
