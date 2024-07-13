# 📺 Display

Installazione e setup per display


## Introduzione

di fondo è la visualizzazione di una pagina web, qualsiasi metodo per arrivarci va bene, anche smart tv
questa è una guida per l'installazione con debian per semplicità, quindi i comandi utilizzeranno systemd, apt eccetera, ma qualunque modo per ottenere il risultato desiderato per ogni step andrà bene.
cosa importante è impostare i codici di sicurezza

## Requisiti

* pc (raspberry pi, vecchio laptop)
* internet
* un cervello
* display

## Impostazione Codice di Autenticazione

## Installazione Sistema Operativo

Debian

Chiavetta usb, installazione, internet

Installare versione minimale, solo sistema base

Nella selezione di software da installare, installare soltanto i software standard di sistema, mentre togliere la spunta da ambiente desktop debian e gnome

riavviare

eseguire il login

### Configurazione di sistema

#### Prevenire la sospensione automatica

Crea il file `/etc/systemd/sleep.conf.d/nosuspend.conf`

```
[Sleep]
AllowSuspend=no
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
```

Se utilizzando un laptop, previeni la sospensione quando si abbassa lo schermo.
Modifica il file `/etc/systemd/logind.conf`:

```
[Login]
HandleLidSwitch=ignore
HandleLidSwitchDocked=ignore
```

## Installazione Software

### Installazione automatica

Assicurarsi di eseguire lo script da una shell con accesso Root.

```
su root
```

Questo script installa i software necessari, crea un utente 'sostituzioni' e configura lo startup automatico.

```
wget https://raw.githubusercontent.com/nkoexe/sostituzioni/main/scripts/kiosk_install.sh; sh kiosk-install.sh
```

Se viene chiesto quale gestore di login usare, selezionare `lightdm`

Inserire l'url del sito senza https e il codice di autenticazione

### Installazione manuale

Aggiorna il sistema

<pre class="language-sh"><code class="lang-sh">sudo apt update
<strong>sudo apt upgrade
</strong></code></pre>

Installazione dei software necessari

```bash
sudo apt install xorg lightdm openbox sed unclutter chromium
```

Creazione file di configurazione di lightdm per il login automatico all'accensione
`/etc/lightdm/lightdm.conf`
Impostare `UTENTE` allo username effettivo.

```
[SeatDefaults]
autologin-user=UTENTE
user-session=openbox
```

Creare il file di startup di Openbox in `~/.config/openbox/autostart`
Questo script verrà eseguito all'accensione, avvia chromium
Rimpiazzare URL con l'effettivo url del sito, e assicurarsi di inserire il codice di autenticazione definito prima.

```bash
#!/bin/bash

# ---- variabili -----

# codice di autorizzazione definito nelle impostazioni del sito
code=""
url="https://URL/display?code=\$code"

# --------------------

# mantieni lo schermo attivo
xset s noblank
xset s off
xset -dpms

# Chiudi sessione con Ctrl-Alt-Backspace
setxkbmap -option terminate:ctrl_alt_bksp

# nascondi il cursore
unclutter -idle 0.1 -root &

while :
do
  # setup e aggiornamento display
  xrandr --auto

  # rimuovi flag di chromium per non far mostrare dialoghi
  sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/sostituzioni/.config/chromium/Default/Preferences
  sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/sostituzioni/.config/chromium/Default/Preferences

  # avvia chromium in modalità kiosk a schermo intero
  chromium \\
    --no-first-run \\
    --start-maximized \\
    --noerrdialogs \\
    --disable-translate \\
    --disable-infobars \\
    --disable-suggestions-service \\
    --disable-save-password-bubble \\
    --disable-session-crashed-bubble \\
    --kiosk \$url

  # delay per il riavvio in caso di errore o chiusura manuale
  sleep 5
done &
```

\

Creare il file `kiosk.sh`
La posizione del file nel sistema è irrilevante, l'importante è ricordarsela, servirà in futuro.

<pre class="language-bash"><code class="lang-bash"><strong>#!/bin/bash
</strong>
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
</code></pre>
