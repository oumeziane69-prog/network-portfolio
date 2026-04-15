# Lab — Segmentation selon le Modèle de Purdue

## Objectif / Objective

**FR** — Implémenter une architecture réseau industrielle basée sur le Modèle de Purdue (ISA-95 / IEC 62443), avec une segmentation stricte entre les niveaux 0 à 4. Le lab couvre la conception des zones IDMZ, les politiques de flux entre niveaux, et la protection des équipements OT (PLCs, HMI, Historian).

**EN** — Implement an industrial network architecture based on the Purdue Model (ISA-95 / IEC 62443), with strict segmentation between levels 0 to 4. The lab covers IDMZ zone design, inter-level flow policies, and protection of OT equipment (PLCs, HMI, Historian).

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

Level 4 — Enterprise IT (ERP, AD, Email)
     |
  [Firewall IT/IDMZ]
     |
Level 3.5 — IDMZ (Historian, Jump Server, Patch Server)
     |
  [Firewall IDMZ/OT]
     |
Level 3 — Site Operations (MES, Historian client)
     |
Level 2 — Supervisory (SCADA / HMI)
     |
Level 1 — Control (PLCs / DCS)
     |
Level 0 — Field (Sensors, Actuators, Robots)
```

**Équipements / Equipment:** FortiGate VM + switches L2/L3 + Ignition SCADA (optionnel)

---

## Statut / Status

🚧 En cours de construction

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Purdue Model (ISA-95) | Cadre de référence pour l'architecture OT |
| IEC 62443 | Standard de sécurité pour les systèmes industriels |
| FortiGate / Fortinet | Pare-feu de segmentation IT/OT |
| IDMZ (Industrial DMZ) | Zone tampon entre IT et OT |
| SCADA / HMI (simulé) | Supervision industrielle |
| Protocoles OT : Modbus, DNP3, OPC-UA | Protocoles de terrain industriels |
| EVE-NG | Environnement de simulation réseau |

---

## Concepts couverts / Concepts Covered

- Les niveaux du Modèle de Purdue : 0 à 4
- Conception de l'IDMZ : jump server, patch server, historian replication
- Matrice de flux IT/OT : quels flux sont autorisés entre niveaux
- Protocoles OT et leurs vulnérabilités (Modbus sans auth, DNP3)
- Règles firewall inter-zones : principe du moindre privilège
- Journalisation et supervision des flux OT
- Risques de la connectivité IT/OT non maîtrisée
