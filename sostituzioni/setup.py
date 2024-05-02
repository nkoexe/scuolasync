from os import environ


def yes_or_no(question: str, default: bool = True):
    while True:
        answer = input("> " + question + (" [Y/n] " if default else " [y/N] ")).lower()
        if answer == "":
            return default
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            # Elimina linea precedente e ripete la domanda
            print("\033[1A\033[K", end="")


def text_input(question: str, allow_empty: bool = False):
    while True:
        answer = input(question).lower()
        if answer == "":
            if allow_empty:
                return ""
            else:
                print("\033[1A\033[K", end="")
                continue
        return answer


# //////////////////////////////


def load_configurazione():
    print(
        """
╔═══════════════════════════════════╗
║ Configurazione del sistema        ║
╚═══════════════════════════════════╝
"""
    )

    if not CONFIG_FILE.exists():
        print("Nessun file di configurazione trovato.")
        init_configurazione()
        return

    print("Configurazione esistente trovata.")

    usa_esistente = yes_or_no(
        "Vuoi utilizzare la configurazione già esistente?", default=True
    )

    if usa_esistente:
        configurazione.load(CONFIG_FILE)
        print("Configurazione esistente caricata.")

    else:
        init_configurazione()


def init_configurazione():
    configurazione.load(ROOT_PATH / "database" / "configurazione.json.template")

    print("Inizializzazione configurazione di sistema.")

    configurazione.esporta(CONFIG_FILE)

    print("Configurazione di sistema completata.")


# //////////////////////////////


def load_database():

    print(
        """
╔═══════════════════════════════════╗
║ Configurazione del database       ║
╚═══════════════════════════════════╝
"""
    )

    databasepath = configurazione.get("databasepath").path

    if not databasepath.exists():
        init_database()
        return

    print("Database esistente trovato.")
    keep = yes_or_no("Vuoi utilizzare il database già esistente?", default=True)

    if not keep:
        from sostituzioni.control.cli import elimina_db

        elimina_db()
        init_database()


def init_database():
    from sostituzioni.control.cli import crea_db

    crea_db()
    print("Database creato.")


# //////////////////////////////


def load_database_utenti():

    print(
        """
╔════════════════════════════════════════╗
║ Configurazione del database di utenti  ║
╚════════════════════════════════════════╝
"""
    )

    authdatabasepath = configurazione.get("authdatabasepath").path

    if not authdatabasepath.exists():
        init_database_utenti()
        return

    print("Database utenti esistente trovato.")
    keep = yes_or_no("Vuoi utilizzare il database utenti già esistente?", default=True)

    if not keep:
        from sostituzioni.control.cli import elimina_db_utenti

        elimina_db_utenti()
        init_database_utenti()


def init_database_utenti():
    from sostituzioni.control.cli import crea_db_utenti, aggiungi_utente

    crea_db_utenti()
    print("Database utenti creato.")
    utente_admin = text_input("Inserisci l'email dell'utente admin: ")
    aggiungi_utente(utente_admin)


# //////////////////////////////


def main():
    global ROOT_PATH, CONFIG_FILE, configurazione
    environ["SOSTITUZIONI_SETUP"] = "1"

    from sostituzioni.control.configurazione import (
        ROOT_PATH,
        CONFIG_FILE,
        configurazione,
    )

    print(
        """                                                                                              
 ___             _    _    _             _            _ 
/ __> ___  ___ _| |_ <_> _| |_  _ _ .___<_> ___ ._ _ <_>
\__ \/ . \<_-<  | |  | |  | |  | | | / /| |/ . \| ' || |
<___/\___//__/  |_|  |_|  |_|  `___|/___|_|\___/|_|_||_|
"""
    )

    print("\nBenvenuto nel setup del sistema insert title here.\n\n")

    input("Premere ENTER per iniziare l'installazione.")

    load_configurazione()

    load_database()
    load_database_utenti()

    print("Installazione completata.")

    print("Per avviare il server di test, eseguire il comando python -m sostituzioni")


if __name__ == "__main__":
    main()
