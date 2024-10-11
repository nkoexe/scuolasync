# 🖥️ **Prerequisiti e Installazione per ScuolaSync**

## ⚙️ **Prerequisiti del Sistema**

### Hardware
- **CPU:** Minimo 1 GHz
- **RAM:** Minimo 2 GB (consigliato 4 GB)
- **Spazio su Disco:** Minimo 1 GB libero

Questi sono requisiti minimi fittizi, il sistema di per se funzionerebbe anche su una patata.
  
### Software
- **Sistema Operativo:** 
  - **Linux:** Ubuntu 20.04 o superiore / Debian 10 o superiore
  - **Pacchetti Necessari:**
    - `git`
    - `python3` (versione 3.11 o superiore)
    - `pip`
    - `nginx`

## 📦 **Installazione del Sistema Operativo**

Saltare questa sezione se il tuo sistema operativo è già installato, ma assicurarsi di possedere privilegi di amministratore.

1. **Scarica l'immagine ISO** di Ubuntu o Debian dal sito ufficiale.
2. **Crea un'unità USB avviabile** utilizzando software come Rufus (Windows) o `dd` (Linux).
3. **Avvia il server dall'unità USB** e segui le istruzioni per installare il sistema operativo.
4. **Aggiorna il sistema** dopo l'installazione:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## 🔐 **Configurazione dell'Autenticazione SSO**

### Scelta del Provider SSO
Scegli il provider SSO in base agli account utilizzati dalla tua scuola:

- **Microsoft SSO**: Utilizzato principalmente in istituti che utilizzano Office 365.
- **Google SSO**: Utilizzato principalmente da scuole che fanno uso di Google Workspace for Education.

### Passaggi per Configurare SSO

Istruzioni temporanee. Questa sezione verrà aggiornata in futuro.

#### **Microsoft SSO**

1. **Accedi al portale di Azure**: [Azure Portal](https://portal.azure.com).
2. **Crea un nuovo progetto**:
   - Vai su "Azure Active Directory" > "App registrations" > "New registration".
   - Compila i dettagli del progetto:
     - Nome: `ScuolaSync`
     - Tipo di account: `Account in questo directory organizzativa`.
   - Clicca su "Register".
3. **Ottieni Client ID e Client Secret**:
   - Dopo la registrazione, vai su "Certificates & secrets".
   - Clicca su "New client secret" per creare un nuovo segreto.
   - Salva il **Client ID** (disponibile nella pagina di registrazione) e il **Client Secret** (copialo immediatamente, poiché non sarà visibile in seguito).

#### **Google SSO**

1. **Accedi alla Google Cloud Console**: [Google Cloud Console](https://console.cloud.google.com/).
2. **Crea un nuovo progetto**:
   Questo passo non è necessario se un progetto Google Cloud scolastico è già stato creato.
   - Clicca su "Select a project" e poi su "New Project".
   - Dai un nome al progetto (es. `ScuolaSync`).
   - Clicca su "Create".
3. **Abilita l'API di Google**:
   - Vai su "API & Services" > "Library".
   - Cerca e abilita "Google People API".
4. **Ottieni Client ID e Client Secret**:
   - Vai su "API & Services" > "Credentials".
   - Clicca su "Create Credentials" e scegli "OAuth 2.0 Client IDs".
   - Seleziona "Web application" come tipo di applicazione e aggiungi i tuoi URI di reindirizzamento (es. `http://scuolasync.fuss.bz.it/loginredirect`).
   - Salva il **Client ID** e il **Client Secret**.

### Nota Finale
Assicurati di configurare correttamente i redirect URI nelle impostazioni del tuo progetto, in modo che il sistema SSO possa autenticarlo correttamente. Questi valori saranno utilizzati nella configurazione dell'applicazione ScuolaSync.
