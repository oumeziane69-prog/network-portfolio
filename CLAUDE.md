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
