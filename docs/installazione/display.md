---
description: Installazione e setup per display
---

# 📺 Display

## Introduzione

di fondo è la visualizzazione di una pagina web, qualsiasi metodo per arrivarci va bene, anche smart tv\
questa è una guida per l'installazione con debian per semplicità, quindi i comandi utilizzeranno systemd, apt eccetera, ma qualunque modo per ottenere il risultato desiderato per ogni step andrà bene.\
cosa importante è impostare i codici di sicurezza

## Requisiti

* pc (raspberry pi, vecchio laptop)
* internet
* un cervello
* display

## Procedimento



### Installazione sistema operativo

Debian

Chiavetta usb, installazione, internet

Autologin (?)

Rimuovi sospensione automatica: crea il file `/etc/systemd/sleep.conf.d/nosuspend.conf`

```
[Sleep]
AllowSuspend=no
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
```



Se utilizzando un laptop, previeni la sospensione quando si abbassa lo schermo.\
Modifica il file `/etc/systemd/logind.conf`:

```
[Login]
HandleLidSwitch=ignore
HandleLidSwitchDocked=ignore
```



Aggiorna il sistema

<pre class="language-sh"><code class="lang-sh">sudo apt update
<strong>sudo apt upgrade
</strong></code></pre>



Installazione dei software necessari

```bash
sudo apt install unclutter sed chromium-browser
```



### Impostazione codice di autenticazione

blabla



### Esecuzione allo startup

Creare il file `kiosk.sh`\
La posizione del file nel sistema è irrilevante, l'importante è ricordarsela, servirà in futuro.

```bash
#!/bin/bash

# ---- variabili -----

# codice di autorizzazione definito nelle impostazioni del sito
code=""
# rimpiazzare URL con l'effettivo url del sito
url="https://URL/display?code=$code"

# --------------------

# mantieni lo schermo attivo
xset s noblank
xset s off
xset -dpms

# nascondi il cursore
unclutter -idle 0.5 -root &

# rimuovi flag di chromium per non far mostrare dialoghi
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences

# avvia chromium in modalità kiosk a schermo intero
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk $url &
```



Renderlo eseguibile

```bash
chmod +x kiosk.sh
```



Creare il file in `/etc/systemd/system/kiosk.service`\
Questo file di configurazione avvia lo script `kiosk.sh` all'avvio del sistema\
Importante: Inserire il percorso corretto del file `kiosk.sh`, e modificare gli attributi `User` e `Group` per riflettere lo username effettivo.

```systemd
[Unit]
Description=Kiosk ScuolaSync
Wants=graphical.target
After=graphical.target

[Service]
Type=simple
ExecStart=/bin/bash /home/utente/kiosk.sh
Restart=always
User=utente
Group=utente

[Install]
WantedBy=graphical.target
```



Abilitare il servizio allo startup

```sh
sudo systemctl daemon-reload
sudo systemctl enable kiosk.service
```



Sarà possibile controllare i log per eventuali errori dello script con:

```sh
journalctl -u kiosk.service
```





