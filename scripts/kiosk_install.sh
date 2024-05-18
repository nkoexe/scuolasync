#!/bin/bash

# aggiorna e installa pacchetti necessari
apt-get update
apt-get install \
  xorg \
  lightdm \
  openbox \
	unclutter \
  chromium \
  -y

# crea gruppo
/sbin/groupadd sostituzioni

# crea utente
/sbin/useradd -m sostituzioni -g sostituzioni -s /bin/bash

# rimuovi console virtuale
cat > /etc/X11/xorg.conf << EOF
Section "ServerFlags"
    Option "DontVTSwitch" "true"
EndSection
EOF

# crea configurazione lightdm
cat > /etc/lightdm/lightdm.conf << EOF
[SeatDefaults]
autologin-user=sostituzioni
user-session=openbox
EOF

# input da utente del sito web
read -p "Inserire l'url di base del sito (senza https://): " url
# input da utente per il codice di autorizzazione
read -p "Inserire il codice di autorizzazione (oppure premere invio per non utilizzarlo): " code


# creazione script di avvio openbox
mkdir -p /home/sostituzioni/.config/openbox

cat > /home/sostituzioni/.config/openbox/autostart << EOF
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

# setup e aggiornamento display
xrandr --auto

# rimuovi flag di chromium per non far mostrare dialoghi
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/sostituzioni/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/sostituzioni/.config/chromium/Default/Preferences

# avvia chromium in modalità kiosk a schermo intero
# chromium \
#   --no-first-run \
#   --start-maximized \
#   --noerrdialogs \
#   --disable-translate \
#   --disable-infobars \
#   --disable-suggestions-service \
#   --disable-save-password-bubble \
#   --disable-session-crashed-bubble \
#   --kiosk \$url
# sleep 5
EOF