---
description: Installazione e setup per display
---

# 📺 Display

## Introduzione

di fondo è la visualizzazione di una pagina web, qualsiasi metodo per arrivarci va bene, anche smart tv\
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

Autologin

Se portatile, continua anche con lid chiuso

```sh
sudo apt update
sudo apt upgrade
```

```bash
sudo apt install unclutter sed chromium-browser
```

### Impostazione codice di autenticazione

blabla

### Esecuzione allo startup

Creare il file `kiosk.sh`\
La posizione del file nel sistema è irrilevante, l'importante è ricordarsela per la creazione dello script successivo.

```bash
#!/bin/bash

code=""
url="https://gandhi-merano.fuss.bz.it/display?code=$code"

xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences

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
Environment=DISPLAY=:0.0
Type=simple
ExecStart=/bin/bash /home/utente/kiosk.sh
Restart=on-abort
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

Sarà possibile controllare i log per eventuali errori dello script con

```sh
journalctl -u kiosk.service
```





