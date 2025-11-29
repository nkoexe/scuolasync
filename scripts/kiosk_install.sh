#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root. Please run with sudo or as root."
  exit 1
fi

SCUOLASYNC_HOME="/home/scuolasync"

### Prerequisiti
apt-get update
apt-get install \
  xorg \
  lightdm \
  openbox \
  autorandr \
  rxvt-unicode \
  sed \
  unclutter \
  chromium \
  -y

# crea utente e gruppo, ignora errori se esistono già
/sbin/groupadd scuolasync || true
/sbin/useradd -m scuolasync -g scuolasync -s /bin/bash || true

# fix per chromium che altrimenti ci sputa
mkdir -p ${SCUOLASYNC_HOME}/.config/chromium/

# Autologin
cat > /etc/lightdm/lightdm.conf << EOF
[SeatDefaults]
autologin-user=scuolasync
user-session=openbox
EOF

# Niente pisolini
mkdir -p /etc/systemd/sleep.conf.d
cat > /etc/systemd/sleep.conf.d/nosuspend.conf << EOF
[Sleep]
AllowSuspend=no
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
EOF

### Input dati ScuolaSync
echo "Inserire l'url di base del sito:"
read -p "> https://" url

echo "Inserire il codice di autorizzazione (oppure premere invio per non utilizzarlo):"
read -p "> " code


mkdir -p ${SCUOLASYNC_HOME}/.config/openbox

# keybinds
cat > ${SCUOLASYNC_HOME}/.config/openbox/rc.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<openbox_config xmlns="http://openbox.org/3.4/rc">
  <keyboard>
    <keybind key="W-Escape">
      <action name="Exit"/>
    </keybind>
    <keybind key="C-A-Escape">
      <action name="Exit"/>
    </keybind>
    <keybind key="W-Enter">
      <action name="Execute">
        <command>urxvt</command>
      </action>
    </keybind>
    <keybind key="C-A-t">
      <action name="Execute">
        <command>urxvt</command>
      </action>
    </keybind>
  </keyboard>
</openbox_config>
EOF

# script di avvio openbox
cat > ${SCUOLASYNC_HOME}/.config/openbox/autostart << EOF
#!/bin/bash

# ---- variabili -----

# codice di autorizzazione definito nelle impostazioni del sito
code="$code"
url="https://$url/display?code=\$code"

# --------------------

# mantieni lo schermo attivo
xset s noblank
xset s off
xset -dpms

# nascondi il cursore
unclutter -idle 0.1 -root &

while :
do
  # setup e aggiornamento display
  autorandr clone-largest

  # tempo per eventuale ridimensionamento display
  sleep 2

  # rimuovi flag di chromium per non far mostrare dialoghi
  if [ -f "${SCUOLASYNC_HOME}/.config/chromium/Default/Preferences" ]; then
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ${SCUOLASYNC_HOME}/.config/chromium/Default/Preferences
    sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' ${SCUOLASYNC_HOME}/.config/chromium/Default/Preferences
  fi

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
EOF

chown -R scuolasync:scuolasync "${SCUOLASYNC_HOME}"

echo
echo "Installazione completata! Riavviare il sistema per avviare il kiosk."