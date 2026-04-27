# Lab — IEC 62443 — Overview & Application

## Objectif / Objective

**FR** — Explorer le cadre normatif IEC 62443 (cybersécurité des systèmes d'automatisation et de contrôle industriels), comprendre sa structure en séries, appliquer le concept de Security Level (SL) et de zones/conduits sur un cas concret de réseau industriel. Préparation à une démarche de conformité IEC 62443.

**EN** — Explore the IEC 62443 normative framework (cybersecurity for industrial automation and control systems), understand its series structure, apply Security Level (SL) concepts and zones/conduits to a concrete industrial network case. Prepare for an IEC 62443 compliance approach.

---

## Topologie prévue / Planned Topology

```
  Zone 1 (SL1-2 — IT/ERP) ↔ Conduit C1 (FW+ACL) ↔ Zone 2 (SL2-3 — SCADA/HMI/Historian) ↔ Conduit C2 (FW strict+IDS) ↔ Zone 3 (SL3-4 — PLCs/DCS/RTUs)
  Référence complète : docs/iec62443-overview.md

  Zone 1 (SL2 — Enterprise IT)
  +─────────────────────+
  | ERP, AD, Email      |
  +─────────────────────+
           | Conduit (FW + ACL)
  Zone 2 (SL3 — SCADA / OT Supervision)
  +─────────────────────+
  | SCADA, HMI, Historian|
  +─────────────────────+
           | Conduit (FW strict)
  Zone 3 (SL4 — Control Layer)
  +─────────────────────+
  | PLCs, DCS, RTUs     |
  +─────────────────────+
```

**Note :** Lab documentaire et de conception — simulation partielle sur EVE-NG

---

## Statut / Status

✅ Complété / Completed

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| IEC 62443 (séries 1, 2, 3, 4) | Standard de référence cybersécurité OT |
| Security Level (SL 1-4) | Niveau de sécurité cible par zone |
| Zones et conduits (IEC 62443-3-3) | Segmentation du réseau industriel |
| IACS (Industrial Automation & Control Systems) | Systèmes cibles du standard |
| Risk Assessment (IEC 62443-3-2) | Évaluation des risques par zone |
| FortiGate / pare-feu OT | Mise en oeuvre des conduits |

---

## Concepts couverts / Concepts Covered

- Structure du standard IEC 62443 : séries 1 (général), 2 (process), 3 (système), 4 (composant)
- Security Level cible (SL-T) vs atteint (SL-A) vs capacité (SL-C)
- Zones et conduits : définition, délimitation, exigences
- Foundational Requirements (FR) : 7 exigences fondamentales
- Risk Assessment selon IEC 62443-3-2
- Démarche de conformité : gap analysis, plan de remédiation
- Relation avec NIST CSF, ISO 27001, NIS2 dans un contexte OT

---

## Référence / Reference

📄 [docs/iec62443-overview.md](../../docs/iec62443-overview.md)
