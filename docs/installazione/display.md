# 📺 Display

Questa pagina mostra come creare una visualizzazione passiva (kiosk) delle informazioni del sistema.

**Prerequisiti** sono l'installazione e la configurazione del **server**, e l'impostazione di un **codice di autenticazione**.

Questa guida mostra come raggiungere lo scopo utilizzando un sistema operativo basato su *Debian* (Ubuntu, Linux Mint, Pop!_OS, ...), quindi i comandi mostrati includono `apt` per la gestione di pacchetti, `systemd` per gestione di sistema, ecc.

Essenzialmente un *kiosk* è la visualizzazione di una pagina web, quindi qualsiasi metodo per arrivarci andrà bene - vecchi laptop, Smart TV, single-board computer, ...

È possibile comunque seguire i passaggi in questa guida, usandoli come riferimento e adattandoli per ottenere lo stesso risultato su un sistema differente.


## Requisiti

* Computer dedicato (Raspberry PI, laptop, ...)
* Connessione internet
* Monitor (preferibilmente 16:9)

### Impostazione Codice di Autenticazione

**Istruzioni temporanee**: modificare il file `configurazione.json`, aggiungendo all'opzione `displayauthcode` un valore.
```json
{
  "displayauthcode": {
    ...
    "valore": [
      {"valore": "xxxxxxxxxxxxxx"},
      {"valore": "yyyyyyyyyyyyyy"}
    ]
  }
}
```

Istruzioni future (da implementare):
Nell'interfaccia di ScuolaSync, andare in **Impostazioni > Visualizzazione Fisica > Codici di autorizzazione** e aggiungere un codice alfanumerico a piacere.

### Prevenire la sospensione automatica

Se utilizzando un laptop, previeni la sospensione quando si abbassa lo schermo.
Modifica il file `/etc/systemd/logind.conf`:

```ini
[Login]
HandleLidSwitch=ignore
HandleLidSwitchDocked=ignore
```

## Installazione

La procedura di setup può essere eseguita in modo automatico con uno script, oppure manualmente seguendo i passaggi indicati.

### Installazione automatica

La procedura automatica può essere eseguita solamente se:
- Il sistema operativo è basato su Debian
- Si ha accesso `root`

[Questo script](https://github.com/nkoexe/scuolasync/blob/main/scripts/kiosk_install.sh) installa i software necessari, crea un utente 'scuolasync', configura il login automatico e l'apertura automatica della schermata.
Deve essere eseguito come root.


```sh
wget https://raw.githubusercontent.com/nkoexe/scuolasync/main/scripts/kiosk_install.sh
sudo bash kiosk_install.sh
```

Seguire le istruzioni a schermo, inserendo l'url del sito e il codice di autenticazione.

Se dovessere venire chiesto quale gestore di login usare, selezionare `lightdm`

### Installazione manuale

Aggiornare il sistema

```sh
sudo apt update
```

Installazione dei software necessari

```sh
sudo apt install xorg lightdm openbox autorandr rxvt-unicode sed unclutter chromium
```

Creazione file di configurazione di lightdm per il login automatico all'accensione `/etc/lightdm/lightdm.conf`

Impostare `UTENTE` allo username effettivo.

```ini
[SeatDefaults]
autologin-user=UTENTE
user-session=openbox
```

Prevenire la sospensione automatica del display

```sh
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

Creare il file di startup di Openbox in `~/.config/openbox/autostart`
Questo script verrà eseguito all'accensione, imposterà automaticamente la risoluzione del display e avvierà chromium.
Rimpiazzare URL con l'effettivo url del sito, e assicurarsi di inserire il codice di autenticazione definito prima.

```bash
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
  if [ -f "${HOME}/.config/chromium/Default/Preferences" ]; then
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ${HOME}/.config/chromium/Default/Preferences
    sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' ${HOME}/.config/chromium/Default/Preferences
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
```
