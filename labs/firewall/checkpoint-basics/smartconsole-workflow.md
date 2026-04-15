# SmartConsole Workflow — Check Point R81.x
# Complete SmartConsole R81.x Administration Workflow

---

## 1. Connexion à SmartConsole

```
SmartConsole (Windows app) → Login
  Server   : 10.0.50.10          (SMS IP)
  Username : admin
  Password : <ADMIN-PASSWORD-HERE>
  
  Fingerprint vérification : comparer avec hash affiché en console SMS
  → Trust & Connect
```

**En CLI (SSH sur SMS) — version headless :**

```bash
# Connexion SSH sur SMS
ssh admin@10.0.50.10

# Vérifier l'état du management
cpstat mg

# Passer en mode expert (bash)
expert
```

---

## 2. Création d'objets réseau / Network Objects

### 2.1 Hosts et réseaux

```
SmartConsole → Object Explorer (Ctrl+E) → New → Host
  Name    : Web-Server-DMZ
  IPv4    : 172.16.50.10
  Color   : Blue
  Comment : Nginx HTTPS server in DMZ
  → OK

SmartConsole → New → Network
  Name    : Net-Internal
  IPv4    : 10.0.50.0 / 255.255.255.0
  → OK
```

**CLI API équivalent (check_point_mgmt_cli) :**

```bash
mgmt_cli add host name "Web-Server-DMZ" ip-address "172.16.50.10" \
  color "blue" comments "Nginx HTTPS server in DMZ" --root true

mgmt_cli add network name "Net-Internal" subnet "10.0.50.0" \
  subnet-mask "255.255.255.0" --root true
```

### 2.2 Services personnalisés

```
SmartConsole → Object Explorer → New → Service → TCP
  Name     : Custom-OPC-UA
  Port     : 4840
  Protocol : TCP
  → OK
```

---

## 3. Création de la Rulebase

### 3.1 Créer une nouvelle règle

```
SmartConsole → Security Policies → Access Control → Policy
  → Add Rule Above (ou Ctrl+Insert)
  
  Remplir les colonnes :
    Name        : Allow-Internal-to-Internet
    Source      : Net-Internal  (drag-drop depuis Object Explorer)
    Destination : Internet
    VPN         : Any (ou spécifier)
    Services    : HTTP, HTTPS, DNS
    Action      : Accept ▼ → Add Profile : AppControl+URLFilter
    Track       : Log
    Install On  : FW-CLUSTER
    Comment     : Accès Internet LAN interne
```

### 3.2 Réorganiser les règles

```
Drag & Drop pour réordonner les règles
Ou : clic droit → Move Up / Move Down
Ou numérotation automatique — vérifier l'ordre de correspondance (first-match)
```

### 3.3 Désactiver une règle sans la supprimer

```
Clic droit sur la règle → Disable Rule
→ La règle apparaît en grisé — inactive mais conservée
```

---

## 4. NAT Rules

```
SmartConsole → Security Policies → NAT
  → Add Rule

  SNAT (Hide NAT — masquerading) :
    Original Source      : Net-Internal
    Original Destination : Any
    Original Services    : Any
    Translated Source    : <Hide behind gateway> (ou Cluster-VIP-External)
    Translated Dest      : Original
    Install On           : FW-CLUSTER

  DNAT (Static NAT — port forwarding) :
    Original Source      : Any
    Original Destination : Cluster-VIP-External
    Original Services    : HTTPS
    Translated Source    : Original
    Translated Dest      : Web-Server-DMZ
    Translated Services  : HTTPS
```

---

## 5. Publish & Install Policy

### 5.1 Publish (sauvegarder les changements dans la base SMS)

```
SmartConsole → haut de l'écran → Publish (ou Ctrl+S)
  → Session description : "Add Internet policy + SNAT — 2026-04-15"
  → Publish

Note : Sans Publish, les autres admins ne voient pas les changements.
       Les changements ne sont pas appliqués sur le gateway.
```

**CLI :**

```bash
mgmt_cli publish --root true
```

### 5.2 Install Policy (déployer sur les gateways)

```
SmartConsole → Security Policies → Access Control → Policy
  → Install Policy (bouton en haut) ou Ctrl+Shift+I
  
  Gateways : FW-CLUSTER (coché)
  Policy   : Standard (Access Control)
  Options  :
    [x] Install on each selected gateway independently
    [x] For Gateway Clusters, if installation fails on one member, abort
  → Install
  
  Progress window :
    Compiling policy...
    Pushing to GW-A... Done
    Pushing to GW-B... Done
    → Installation complete (0 errors)
```

**CLI :**

```bash
mgmt_cli install-policy policy-package "Standard" \
  targets.1 "FW-CLUSTER" --root true
```

### 5.3 En cas d'échec d'installation

```bash
# Voir les logs d'installation sur la gateway
ssh admin@<GW-A-IP>
expert
grep "install" /var/log/messages | tail -50

# Vérifier la politique courante active
fw stat -l
# Affiche : Policy name, install time, interface list
```

---

## 6. Révocation / Discard Changes

```
SmartConsole → haut → Discard (ou sessions non publiées)
  → Confirmation "Discard all unpublished changes ?"
  → Yes → Retour à l'état du dernier Publish
```

**Voir les sessions en cours (multi-admin) :**

```
SmartConsole → Manage & Settings → Sessions
  → Liste des sessions ouvertes (admins connectés)
  → Voir les objets en cours de modification par chaque admin
  → Possibilité de "Take Over" une session ou de la révoquer
```

---

## 7. Analyse des logs — SmartView

### 7.1 SmartConsole Logs & Monitor

```
SmartConsole → Logs & Monitor → New Tab → Audit Logs / Traffic Logs

Filtres utiles :
  Action:Drop    → Voir les flux bloqués
  Blade:Firewall → Voir les décisions de la policy
  Source:10.0.50.100 → Logs d'un hôte spécifique
  Destination:172.16.50.10 → Logs vers le web server

Export des logs :
  Clic droit → Export to CSV
  Ou : SmartView Monitor pour rapports planifiés
```

### 7.2 Commandes CLI pour les logs

```bash
# Sur la gateway — logs en temps réel
fw log -t -n

# Statistiques en temps réel
fw ctl pstat

# Logs filtrés
fw log -b 14/04/2026 -e 15/04/2026 | grep "DROP"

# Logs dans fichier
ls -la $FWDIR/log/
# fw.log = log courant, fw.log.YYYYMMDD = archives
```

---

## 8. Comparatif Check Point vs FortiGate

| Critère | Check Point R81.x | FortiGate 7.4 |
|---------|-------------------|---------------|
| **Architecture** | SMS séparé (management) + GW (enforcement) | All-in-one (config locale) ou FortiManager |
| **Interface principale** | SmartConsole (app Windows) | GUI web (HTTPS) ou CLI |
| **Config backup** | SMS centralise tout — GW = slave | Config locale sur chaque FGT (+ FortiManager optionnel) |
| **Règles** | Publish → Install (2 étapes) | Apply immédiat (ou FortiManager en 2 étapes) |
| **Multi-admin** | Sessions nommées, verrouillage objet par objet | Lock en mode FortiManager, pas de lock natif seul |
| **Clustering** | ClusterXL (A/A ou A/P) intégré | FGCP (A/P) intégré, FortiLink pour VDOM |
| **IPS/UTM** | Threat Prevention blades séparées | UTM intégré dans les policies (profiles) |
| **Identité utilisateur** | Identity Awareness blade (AD, Captive Portal) | FSSO / RSSO pour AD (FortiAuthenticator) |
| **VPN** | SmartConsole GUI, IPSec/SSL intégré | CLI ou GUI, IPSec/SSL intégré |
| **Logs** | SmartView (app dédiée) + SmartLog | FortiLog (GUI intégrée) + FortiAnalyzer |
| **Automation** | API REST + CLI SmartConsole | FortiManager + API REST + CLI |
| **Cas d'usage** | Grands SI, banques, OIV — management centralisé fort | Entreprises, MSSP, multi-sites — facilité de déploiement |
| **Courbe d'apprentissage** | Élevée (architecture multi-composants) | Modérée (all-in-one plus intuitif) |
| **Certification** | CCSE (Check Point) | NSE (Fortinet) |
