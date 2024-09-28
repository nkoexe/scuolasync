"""
    This file is part of ScuolaSync.

    Copyright (C) 2023-present Niccolò Ragazzi <hi@njco.dev>

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
"""

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


def select_input(question: str, options: list):
    while True:
        print(question)
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        answer = input("> ")

        if answer.isdigit():
            try:
                answer = int(answer)
            except ValueError:
                print("Inserisci un numero valido.")
                continue
            if answer < 1 or answer > len(options):
                print("Inserisci un numero valido.")
                continue
            return options[answer - 1]

        elif answer in options:
            return answer

        else:
            print("Inserisci un numero valido.")
            continue


# //////////////////////////////


def load_configurazione():
    print(
        """
╔═════════════════════════════════════════╗
║ Configurazione del sistema              ║
╚═════════════════════════════════════════╝
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
    configurazione.load(CONFIG_TEMPLATE)

    print("Inizializzazione configurazione di sistema.\n")

    sso_choice = select_input(
        "Quale gestore di Single Sign On vuoi utilizzare?", ["Google", "Microsoft"]
    )

    if sso_choice == "Google":
        configurazione.set("ssochoice", 0)

        client_id = text_input("OAuth 2.0 Client ID di Google: ")
        configurazione.set("gclientid", client_id)

        client_secret = text_input("OAuth 2.0 Client Secret di Google: ")
        configurazione.set("gclientsecret", client_secret)

    elif sso_choice == "Microsoft":
        configurazione.set("ssochoice", 1)

        client_id = text_input("OAuth 2.0 Client ID di Microsoft: ")
        configurazione.set("msclientid", client_id)

        client_secret = text_input("OAuth 2.0 Client Secret di Microsoft: ")
        configurazione.set("msclientsecret", client_secret)

    support_email = text_input(
        "Indirizzo email che verrà indicato come contatto di supporto: ",
        allow_empty=True,
    )
    configurazione.set("supportemail", support_email)

    configurazione.esporta(CONFIG_FILE)

    print("\nConfigurazione di sistema completata.")


# //////////////////////////////


def load_database():

    print(
        """
╔═════════════════════════════════════════╗
║ Configurazione del database             ║
╚═════════════════════════════════════════╝
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
╔═════════════════════════════════════════╗
║ Configurazione del database di utenti   ║
╚═════════════════════════════════════════╝
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
    utente_admin = text_input(
        "Inserisci l'email del primo amministratore che eseguirà l'accesso: "
    )
    aggiungi_utente(utente_admin)


# //////////////////////////////


def main():
    global ROOT_PATH, CONFIG_FILE, CONFIG_TEMPLATE, configurazione
    environ["SCUOLASYNC_SETUP"] = "1"

    from sostituzioni.control.configurazione import (
        ROOT_PATH,
        CONFIG_FILE,
        CONFIG_TEMPLATE,
        configurazione,
    )

    print(
        """
╔═════════════════════════════════════════╗
║            ScuolaSync Setup             ║
╚═════════════════════════════════════════╝
"""
    )

    input("Premere ENTER per iniziare l'installazione.")

    load_configurazione()

    load_database()
    load_database_utenti()

    print("\n\nInstallazione completata!")

    print("Per avviare il server di test, eseguire il comando `python -m sostituzioni`")


if __name__ == "__main__":
    main()
