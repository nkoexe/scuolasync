# 🖥️ **Prerequisiti**

## **Requisiti del Sistema**

### Hardware
- **CPU:** Minimo 1 GHz
- **RAM:** Minimo 2 GB (consigliato 4 GB)
- **Spazio su Disco:** Minimo 1 GB libero

Questi sono requisiti minimi fittizi, il sistema di per se funzionerebbe anche su una patata.
  
### Software
- **Sistema Operativo:** 
  - **Linux:** Consigliato Debian 12 (lo script di installazione automatica funziona solo su distribuzioni basate su Debian, come Ubuntu).
  - **Pacchetti Necessari:**
    - `git`
    - `python3` (versione 3.11 o superiore)
    - `python3-pip`
    - `nginx`


## **Configurazione del servizio di Autenticazione**

### Scelta del Provider
Scegli il provider *Single-Sign-On* (SSO) in base agli account utilizzati dall'istituto:

- **Microsoft**: Office 365 Education.
- **Google**: Google Workspace for Education.

### Configurazione Single-Sign-On (SSO)

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
3. **Ottieni Client ID e Client Secret**:
   - Vai su "API & Services" > "Credentials".
   - Clicca su "Create Credentials" e scegli "OAuth 2.0 Client IDs".
   - Seleziona "Web application" come tipo di applicazione e aggiungi i tuoi redirect URI (tuodominio + `loginredirect`, ad es. `http://scuolasync.fuss.bz.it/loginredirect`).
   - Salva il **Client ID** e il **Client Secret**.

### Nota Finale
Assicurati di configurare correttamente i redirect URI nelle impostazioni del tuo progetto, in modo che il sistema SSO possa autenticarlo correttamente. Questi valori saranno utilizzati nella configurazione dell'applicazione ScuolaSync.


## **Requisiti per lo script di installazione automatica**
- **Accesso Root** per configurare avvio automatico e permessi del sistema
- **Connessione Internet** per scaricare i pacchetti e il codice sorgente 

