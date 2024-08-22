from os import environ

environ["SOSTITUZIONI_SETUP"] = "1"

from sostituzioni.control.configurazione import ROOT_PATH, CONFIG_FILE, configurazione


if not CONFIG_FILE.exists():
    configurazione.load(ROOT_PATH / "database" / "configurazione.json.template")
    print("Inizializzazione configurazione di sistema.")
    configurazione.esporta(CONFIG_FILE)
    print("Configurazione di sistema completata.")

else:
    print("Configurazione già esistente.")


databasepath = configurazione.get("databasepath").path

if not databasepath.exists():
    from sostituzioni.control.cli import crea_db

    crea_db()
    print("Database creato.")

else:
    print("Database già esistente.")


authdatabasepath = configurazione.get("authdatabasepath").path

if not authdatabasepath.exists():
    from sostituzioni.control.cli import crea_db_utenti, aggiungi_utente

    crea_db_utenti()
    print("Database utenti creato.")
    aggiungi_utente("niccolo.rag@gmail.com")

else:
    print("Database utenti già esistente.")


configurazione.set("oauthclientid", environ["SOSTITUZIONI_OAUTHCLIENTID"])
configurazione.set("oauthclientsecret", environ["SOSTITUZIONI_OAUTHCLIENTSECRET"])
configurazione.set("redirecturi", environ["SOSTITUZIONI_REDIRECTURI"])


print("Installazione completata.")
