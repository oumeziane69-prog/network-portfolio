# JunOS vs IOS CLI Cheatsheet

> Référence rapide pour les ingénieurs réseau IOS souhaitant prendre en main JunOS.
> Quick reference for IOS network engineers getting started with JunOS.

---

## 1. Modes CLI / CLI Modes

| Action | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| Mode opérationnel (show, ping...) | Mode `>` par défaut | Mode `>` (`cli` depuis shell root) |
| Entrer en configuration | `configure terminal` / `conf t` | `configure` / `edit` |
| Quitter la config (sans sauver) | `end` ou `Ctrl+Z` | `exit discard` ou `rollback 0; exit` |
| Quitter un niveau de hiérarchie | `exit` | `exit` (remonte d'un niveau) ou `top` (retour racine) |
| Naviguer dans la hiérarchie | N/A (linéaire) | `edit protocols bgp` pour descendre dans `[edit protocols bgp]` |

---

## 2. Sauvegarde et validation / Save & Commit

| Action | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| Appliquer / sauvegarder la config | `copy running-config startup-config` / `wr mem` | `commit` |
| Valider avec confirmation | N/A | `commit confirmed 5` (rollback auto dans 5 min si pas de 2e commit) |
| Vérifier avant d'appliquer | `do show run` (partiel) | `show \| compare` (diff candidat vs actif) |
| Annuler les changements en cours | Annuler ligne par ligne (`no ...`) | `rollback 0` (restaure la config active) |
| Historique des commits | N/A | `show system commit` (50 versions conservées) |
| Restaurer une version précédente | `copy flash:backup run` (manuel) | `rollback 3` (restaure la 3e version précédente) |
| Config active | `show running-config` | `show configuration` |
| Config sauvegardée | `show startup-config` | `show configuration \| display set` |
| Diff entre deux versions | N/A | `show system rollback compare 0 1` |

---

## 3. Interfaces

| Action | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| Nommage | `GigabitEthernet0/0` (`Gi0/0`) | `ge-0/0/0` (FPC/PIC/Port) |
| Loopback | `interface Loopback0` | `interfaces lo0 unit 0` |
| Assigner une IP | `ip address 10.0.1.1 255.255.255.252` | `set interfaces ge-0/0/0 unit 0 family inet address 10.0.1.1/30` |
| Activer une interface | `no shutdown` | Activée par défaut — désactiver avec `set interfaces ge-0/0/0 disable` |
| Désactiver | `shutdown` | `set interfaces ge-0/0/0 disable` |
| Description | `description Lien vers SRX2` | `set interfaces ge-0/0/0 description "Lien vers SRX2"` |
| Afficher résumé | `show interfaces brief` / `show ip int brief` | `show interfaces terse` |
| Afficher détail | `show interfaces GigabitEthernet0/0` | `show interfaces ge-0/0/0 detail` |
| Afficher IP seulement | `show ip interface brief` | `show interfaces terse \| match inet` |

---

## 4. Table de routage / Routing Table

| Action | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| Table de routage complète | `show ip route` | `show route` |
| Route spécifique | `show ip route 10.255.1.1` | `show route 10.255.1.1` |
| Routes BGP uniquement | `show ip bgp` | `show route protocol bgp` |
| Routes statiques | `show ip route static` | `show route protocol static` |
| Table de routage résumée | `show ip route summary` | `show route summary` |
| Prochains sauts | `show ip route 10.0.0.0/8 longer-prefixes` | `show route 10.0.0.0/8 longer` |

---

## 5. BGP

| Action | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| Résumé des voisins | `show ip bgp summary` | `show bgp summary` |
| Détail d'un voisin | `show ip bgp neighbors 10.0.12.2` | `show bgp neighbor 10.0.12.2` |
| Routes reçues d'un voisin | `show ip bgp neighbors 10.0.12.2 received-routes` | `show route receive-protocol bgp 10.0.12.2` |
| Routes envoyées à un voisin | `show ip bgp neighbors 10.0.12.2 advertised-routes` | `show route advertising-protocol bgp 10.0.12.2` |
| Table BGP complète | `show ip bgp` | `show bgp` |
| Reset voisin (soft) | `clear ip bgp 10.0.12.2 soft` | `clear bgp neighbor 10.0.12.2 soft [in\|out]` |
| Reset voisin (hard) | `clear ip bgp 10.0.12.2` | `clear bgp neighbor 10.0.12.2` |
| Debug BGP | `debug ip bgp 10.0.12.2` | `set protocols bgp traceoptions file bgp-trace` puis `set protocols bgp traceoptions flag all` |

---

## 6. Filtrage / Policy

| Concept IOS | Concept JunOS | Description |
|-------------|---------------|-------------|
| `ip prefix-list` | `policy-options prefix-list` | Liste de préfixes IP |
| `route-map` | `policy-statement` | Politique de routage (match + action) |
| `match ip address prefix-list X` | `from { prefix-list X; }` | Condition d'entrée |
| `set local-preference 200` | `then { local-preference 200; }` | Action d'application |
| `permit` (route-map) | `then accept;` | Accepter le préfixe |
| `deny` (route-map) | `then reject;` | Rejeter le préfixe |
| `neighbor X route-map Y in` | `neighbor X { import POLICY; }` | Appliquer policy en entrée |
| `neighbor X route-map Y out` | `neighbor X { export POLICY; }` | Appliquer policy en sortie |

---

## 7. Filtres et sécurité / Filters & Security

| Concept IOS | Concept JunOS | Description |
|-------------|---------------|-------------|
| `ip access-list extended` | `firewall filter` (family inet) | Filtre stateless sur interface |
| `permit tcp any any eq 179` | `term X { from { protocol tcp; destination-port bgp; } then accept; }` | Autoriser BGP |
| `deny ip any any log` | `term DENY { then { discard; log; syslog; } }` | Règle de refus finale avec log |
| `ip access-group ACL in` | `filter { input FILTER-NAME; }` dans la config interface | Application du filtre en entrée |
| Zone-Based Firewall (ZBF) | Security zones + policies (natif SRX) | Firewall stateful inter-zones |

---

## 8. Diagnostics / Diagnostics

| Action | Cisco IOS | Juniper JunOS |
|--------|-----------|---------------|
| Ping | `ping 10.255.2.1` | `ping 10.255.2.1` |
| Traceroute | `traceroute 10.255.2.1` | `traceroute 10.255.2.1` |
| Ping source | `ping 10.255.2.1 source Loopback0` | `ping 10.255.2.1 routing-instance default source 10.255.1.1` |
| Log système | `show logging` | `show log messages` |
| Log en temps réel | `terminal monitor` | `monitor start messages` |
| Compteurs interfaces | `show interfaces GigabitEthernet0/0 counters` | `show interfaces ge-0/0/0 statistics` |
| ARP table | `show arp` | `show arp` |
| NTP | `show ntp status` | `show ntp status` |
| Version OS | `show version` | `show version` |

---

## 9. Particularités JunOS à retenir

| Point | Description |
|-------|-------------|
| **Candidate config** | Toutes les modifications sont en "candidate config" jusqu'au `commit`. L'équipement tourne toujours sur la config active. |
| **Commit confirm** | `commit confirmed 5` : si vous n'exécutez pas un 2e `commit` dans 5 min, la config se rollback automatiquement. Utile pour les changements à risque. |
| **Rollback 50 versions** | JunOS conserve les 50 dernières configurations commitées. `rollback 1` = version précédente. |
| **`\| display set`** | Affiche la config au format `set` (une ligne par commande) : `show configuration \| display set` |
| **`\| compare`** | Affiche le diff entre la candidate config et la config active : `show \| compare` |
| **Hiérarchie** | La config est un arbre. `edit protocols bgp group EBGP` descend dans ce contexte. `top` revient à la racine. |
| **Interfaces unités** | Chaque interface physique a des unités logiques (`unit 0`, `unit 100`...). Une interface sans `unit 0` n'a pas d'IP. |
