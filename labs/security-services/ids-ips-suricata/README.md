# Lab — IDS/IPS avec Suricata

## Objectif / Objective

**FR** — Déployer Suricata en mode IDS (détection) puis IPS (prévention inline) sur un segment réseau. Configurer des règles de détection pour des menaces réseau courantes, analyser les alertes, et intégrer avec ELK Stack pour la visualisation des événements de sécurité.

**EN** — Deploy Suricata in IDS (detection) mode then inline IPS (prevention) mode on a network segment. Configure detection rules for common network threats, analyze alerts, and integrate with ELK Stack for security event visualization.

---

## Topologie prévue / Planned Topology

```
  Mode IDS (passive AF_PACKET / SPAN):
  [Switch SPAN] → [Suricata 7.x Ubuntu 22.04] → EVE JSON → [Filebeat] → [ELK Stack / Kibana]
  Mode IPS (inline NFQUEUE):
  [FGT-INTERNAL] → [Suricata NFQUEUE bridge] → [LAN-OT] | Drop/Alert → [ELK Stack]
  HOME_NET: 10.0.10.0/24, 172.16.10-20-30.0/24 | OT protocols: Modbus/DNP3/S7Comm/OPC-UA/EIP
```

**Équipements / Equipment:** Suricata VM (Linux) + ELK Stack VM + réseau de test

---

## Statut / Status

✅ Complété / Completed

---

## Technologies utilisées / Technologies Used

| Technologie | Rôle |
|-------------|------|
| Suricata 7.x | Moteur IDS/IPS open-source |
| Emerging Threats (ET) Rules | Ruleset de détection de menaces |
| ELK Stack (Elasticsearch, Logstash, Kibana) | SIEM / visualisation d'alertes |
| NFQUEUE / AF_PACKET | Modes inline Suricata |
| Filebeat | Collecte et transfert de logs vers ELK |
| Linux (Debian/Ubuntu) | Système hôte Suricata |

---

## Concepts couverts / Concepts Covered

- Architecture IDS vs IPS : passive vs inline
- Écriture de règles Suricata : header, options, content matching
- Rulesets : Emerging Threats Open, ET Pro, Snort Community Rules
- Modes de capture : AF_PACKET, NFQUEUE (netfilter)
- Analyse d'alertes : EVE JSON, fast.log
- Intégration ELK : pipeline Filebeat → Logstash → Elasticsearch → Kibana
- Détection de menaces : scan de ports, brute-force SSH, exfiltration DNS
- Tuning et suppression des faux positifs
