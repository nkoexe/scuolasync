# 🖥️ Server

Installazione del server di sistema.


## Introduzione

server scuolasync

## Requisiti

* connessione internet
* un server linux
* python 3.11 o superiore
* boh di spazio

## Installazione

Clona il repository

```sh
git clone https://github.com/nkoexe/scuolasync.git
cd scuolasync
```

Creare un virtualenv

```sh
python -m venv env
source env/bin/activate
```

Installa le dipendenze

```sh
pip install -r requirements.txt
```

Oppure installando manualmente le dipendenze

```sh
pip install flask flask-login flask-socketio flask-wtf beartype apscheduler pandas openpyxl xlsxwriter odspy pylibmagic python-magic oauthlib google-auth google-api-python-client qrcode gunicorn gevent
```

Esegui lo script di setup

```sh
python -m sostituzioni.setup
```

Creazione servizio systemd `scuolasync.service`

```sh
nano /etc/systemd/system/scuolasync.service
```

Assicurarsi di sostituire gli attributi correttamente:
  - `<USER>` e `<GROUP>` con il nome utente e gruppo corretto
  - `<REPODIR>` con il percorso del repository
  - `<PYENV>` con il percorso dell'ambiente virtuale di python


```systemd
[Unit]
Description=ScuolaSync - Server
After=network.target

[Service]
Type=simple
User=<USER>
Group=<GROUP>
WorkingDirectory=<REPODIR>
Environment=PATH=<PYENV>/bin:/usr/bin
Environment=SCUOLASYNC_SERVICE=scuolasync.service
ExecStart=<PYENV>/bin/gunicorn --workers 1 -k gevent --bind 127.0.0.1:5123 sostituzioni.app:app
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
```

Esempio:

```systemd
[Unit]
Description=ScuolaSync - Server
After=network.target

[Service]
Type=simple
User=scuolasync
Group=www-data
WorkingDirectory=/scuolasync
Environment=PATH=/scuolasync/env/bin:/usr/bin
Environment=SCUOLASYNC_SERVICE=scuolasync.service
ExecStart=/scuolasync/env/bin/gunicorn --workers 1 -k gevent --bind 127.0.0.1:5123 sostituzioni.app:app
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target

[Service]
WorkingDirectory=/home/scuolasync
ExecStart=/usr/bin/python -m sostituzioni
```

Abilita il servizio allo startup

```sh
systemctl daemon-reload
systemctl enable scuolasync.service
```

Configurazione nginx

```sh
nano /etc/nginx/sites-available/scuolasync
```

Assicurarsi di sostituire gli attributi correttamente:
  - `<SERVERNAME>` con il nome del server web (esempio: `scuolasync.fuss.bz.it`)

```nginx
server {
    listen 80;
    server_name <SERVERNAME>;

    location / {
        proxy_pass http://127.0.0.1:5123;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```