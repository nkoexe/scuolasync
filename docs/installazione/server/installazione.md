# 🛠️ **Installazione di ScuolaSync**

### 1. **Clonare il Repository Git**

Clona il repository di **ScuolaSync** sul tuo server utilizzando `git`:

```bash
git clone https://github.com/nkoexe/scuolasync.git
cd scuolasync
```

### 2. **Creare un Ambiente Virtuale Python**

Per mantenere isolate le dipendenze dell'applicazione, crea un ambiente virtuale Python:

```bash
python -m venv env
source env/bin/activate
```

### 3. **Installare le Dipendenze**

Installa tutte le dipendenze richieste dall'applicazione utilizzando il file `requirements.txt`:

```bash
pip install -r requirements.txt
```

Altrimenti, se desideri installare manualmente i pacchetti, usa il comando seguente:

```bash
pip install flask flask-login flask-socketio flask-wtf beartype apscheduler pandas openpyxl xlsxwriter odspy pylibmagic python-magic oauthlib google-auth google-api-python-client qrcode gunicorn gevent
```

---


## 🔧 **Configurazione del Servizio Systemd**

Affinché ScuolaSync venga eseguito come servizio di sistema e si avvii automaticamente, devi configurare un'unità **systemd**. Segui i passaggi riportati di seguito.

### 1. **Creare il File del Servizio systemd**

Crea un file per il servizio **scuolasync**:

```bash
nano /etc/systemd/system/scuolasync.service
```

### 2. **Inserire la Configurazione del Servizio**

Inserisci il seguente contenuto nel file, ricordando di sostituire i segnaposto (`<USER>`, `<GROUP>`, `<REPODIR>`, `<PYENV>`) con i valori appropriati per il tuo server.

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

#### Parametri chiave da sostituire:
- **`<USER>`**: L'utente che eseguirà il servizio (ad esempio `scuolasync`).
- **`<GROUP>`**: Il gruppo dell'utente (spesso `www-data`).
- **`<REPODIR>`**: Il percorso completo della cartella del progetto clonato (es: `/home/scuolasync`).
- **`<PYENV>`**: Il percorso dell'ambiente virtuale creato (es: `/home/scuolasync/env`).

#### Esempio completato:

```systemd
[Unit]
Description=ScuolaSync - Server
After=network.target

[Service]
Type=simple
User=scuolasync
Group=www-data
WorkingDirectory=/home/scuolasync
Environment=PATH=/home/scuolasync/env/bin:/usr/bin
ExecStart=/home/scuolasync/env/bin/gunicorn --workers 1 -k gevent --bind 127.0.0.1:5123 sostituzioni.app:app
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
```

### 3. **Abilitare e Avviare il Servizio**

Dopo aver creato il file di servizio, abilita e avvia il servizio di **ScuolaSync**:

```bash
systemctl daemon-reload
systemctl enable scuolasync.service
```

Verifica lo stato del servizio per assicurarti che sia attivo e funzionante correttamente:

```bash
systemctl status scuolasync.service
```

---

## 🌐 **Configurazione di Nginx come Reverse Proxy**

Per esporre il server Flask all'esterno e gestire il traffico HTTP, configureremo **Nginx** come reverse proxy.

### 1. **Creare la Configurazione di Nginx**

Crea un file di configurazione per il sito **ScuolaSync** in **Nginx**:

```bash
nano /etc/nginx/sites-available/scuolasync
```

### 2. **Aggiungere la Configurazione**

Inserisci la seguente configurazione, sostituendo `<SERVERNAME>` con il nome di dominio del server (es: `scuolasync.fuss.bz.it` o l'IP pubblico se non hai un dominio).

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

### 3. **Abilitare la Configurazione del Sito**

Attiva la configurazione del sito creando un collegamento simbolico nella cartella `sites-enabled` di Nginx:

```bash
ln -s /etc/nginx/sites-available/scuolasync /etc/nginx/sites-enabled/
```

### 4. **Riavviare Nginx**

Applica le modifiche riavviando il servizio **Nginx**:

```bash
systemctl restart nginx
```

Verifica che Nginx stia funzionando correttamente con:

```bash
systemctl status nginx
```
