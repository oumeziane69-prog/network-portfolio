# Lab — IDS/IPS avec Suricata

## Objectif / Objective

**FR** — Déployer Suricata en mode IDS (détection) puis IPS (prévention inline) sur un segment réseau. Configurer des règles de détection pour des menaces réseau courantes, analyser les alertes, et intégrer avec ELK Stack pour la visualisation des événements de sécurité.

**EN** — Deploy Suricata in IDS (detection) mode then inline IPS (prevention) mode on a network segment. Configure detection rules for common network threats, analyze alerts, and integrate with ELK Stack for security event visualization.

---

## Topologie prévue / Planned Topology

```
[Topology placeholder — full diagram to be added]

Mode IDS (passive / SPAN port):
[Switch]──SPAN port──►[Suricata IDS]──►[ELK Stack (Kibana)]
    |
[LAN clients + servers]

Mode IPS (inline):
[Router/FW]──►[Suricata IPS (NFQUEUE/AF_PACKET)]──►[LAN]
                   |
              Block / Alert
                   |
            [ELK Stack (Kibana)]
```

**Équipements / Equipment:** Suricata VM (Linux) + ELK Stack VM + réseau de test

---

## Statut / Status

🚧 En cours de construction

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
