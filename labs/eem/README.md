# Lab EEM — Cisco Cat8k IOS-XE / EEM Lab — Cisco Cat8k IOS-XE

**Status: Completed ✅**

---

## FR — Description

Ce lab démontre l'utilisation de l'**Embedded Event Manager (EEM)** sur un routeur Cisco Catalyst
8000V IOS-XE 17.12.2. Trois applets couvrent les cas d'usage les plus courants en production :
surveillance périodique BGP, réaction automatique à la perte d'un voisin, et notification de
sauvegarde de configuration.

| Paramètre | Valeur |
|---|---|
| Plateforme | Cisco Cat8k IOS-XE 17.12.2 |
| Fonctionnalité | Embedded Event Manager (EEM) |
| Config | `labs/eem/eem_config.txt` |
| Type d'événements | timer, syslog, cli |

### Applets démontrées

| Applet | Événement déclencheur | Actions |
|---|---|---|
| `HEARTBEAT` | `timer watchdog 60s` | Syslog + `show ip bgp summary` toutes les 60 s |
| `BGP-NEIGHBOR-DOWN` | `syslog pattern "BGP-5-ADJCHANGE.*Down"` | Syslog + collecte automatique de diagnostics BGP |
| `SAVE-NOTIFIER` | `cli pattern "wr"` | Syslog de notification à chaque `write memory` |

### Exécution

Coller le contenu de `eem_config.txt` en mode configuration globale :

```
Cat8k# configure terminal
Cat8k(config)# [coller le contenu de eem_config.txt]
Cat8k(config)# end
```

Tester manuellement l'applet HEARTBEAT :

```
Cat8k# event manager run HEARTBEAT
Cat8k# show logging | include HEARTBEAT
```

---

## EN — Description

This lab demonstrates the **Embedded Event Manager (EEM)** on a Cisco Catalyst 8000V router
running IOS-XE 17.12.2. Three applets cover the most common production use cases: periodic BGP
health monitoring, automatic reaction to neighbor loss, and configuration-save notification.

| Parameter | Value |
|---|---|
| Platform | Cisco Cat8k IOS-XE 17.12.2 |
| Feature | Embedded Event Manager (EEM) |
| Config | `labs/eem/eem_config.txt` |
| Event types | timer, syslog, cli |

### Demonstrated applets

| Applet | Trigger event | Actions |
|---|---|---|
| `HEARTBEAT` | `timer watchdog 60s` | Syslog + `show ip bgp summary` every 60 s |
| `BGP-NEIGHBOR-DOWN` | `syslog pattern "BGP-5-ADJCHANGE.*Down"` | Syslog + automatic BGP diagnostic collection |
| `SAVE-NOTIFIER` | `cli pattern "wr"` | Syslog notification on every `write memory` |

### Apply config

Paste the content of `eem_config.txt` in global configuration mode:

```
Cat8k# configure terminal
Cat8k(config)# [paste content of eem_config.txt]
Cat8k(config)# end
```

Manually trigger HEARTBEAT to verify:

```
Cat8k# event manager run HEARTBEAT
Cat8k# show logging | include HEARTBEAT
```

---

## Output example / Exemple de sortie

### event manager run HEARTBEAT

```
Cat8k# event manager run HEARTBEAT
Cat8k#
*Apr 27 06:12:00.001: %SYS-5-CONFIG_I: Configured from console by EEM
*Apr 27 06:12:00.010: %HA_EM-6-LOG: HEARTBEAT: BGP health check triggered
*Apr 27 06:12:00.250: %HA_EM-6-LOG: HEARTBEAT: BGP summary collected
```

### show logging | include HEARTBEAT

```
*Apr 27 06:12:00.010: %HA_EM-6-LOG: HEARTBEAT: BGP health check triggered
*Apr 27 06:12:00.250: %HA_EM-6-LOG: HEARTBEAT: BGP summary collected
*Apr 27 06:13:00.010: %HA_EM-6-LOG: HEARTBEAT: BGP health check triggered
*Apr 27 06:13:00.248: %HA_EM-6-LOG: HEARTBEAT: BGP summary collected
```

### BGP-NEIGHBOR-DOWN triggered

```
*Apr 27 06:15:33.120: %BGP-5-ADJCHANGE: neighbor 192.168.1.2 Down BGP Notification sent
*Apr 27 06:15:33.135: %HA_EM-6-LOG: BGP-NEIGHBOR-DOWN: neighbor state change detected
*Apr 27 06:15:33.140: %HA_EM-6-LOG: BGP-NEIGHBOR-DOWN: diagnostics collection complete
```

### SAVE-NOTIFIER triggered

```
Cat8k# wr
*Apr 27 06:18:05.002: %HA_EM-6-LOG: SAVE-NOTIFIER: write memory detected — configuration save in progress
Building configuration...
[OK]
```

### show event manager policy registered

```
Cat8k# show event manager policy registered
No.  Class     Type    Event Type          Trap  Time Registered        Name
1    applet    system  timer watchdog      Off   Mon Apr 27 06:00:00    HEARTBEAT
2    applet    system  syslog              Off   Mon Apr 27 06:00:00    BGP-NEIGHBOR-DOWN
3    applet    system  cli                 Off   Mon Apr 27 06:00:00    SAVE-NOTIFIER
```
