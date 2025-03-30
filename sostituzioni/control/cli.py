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

from flask.cli import AppGroup
import click
import sqlite3

from sostituzioni.control.configurazione import configurazione


def crea_db(nome: str | None = None):
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome
    sqlpath = configurazione.get("scriptsdir").path / "creazione_database.sql"

    if dbpath.exists():
        print("Errore: Database con questo nome già esistente.")
        return

    print("File database:", dbpath)

    try:
        conn = sqlite3.connect(dbpath.as_posix())
        c = conn.cursor()
        c.executescript(sqlpath.read_text())
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Errore nella creazione del database:", e)
        return False

    return True


def imposta_principale(nome: str | None = None):
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    configurazione.set("databasepath", (1, "database/" + nome))
    configurazione.esporta()

    print(f"Database principale impostato: {nome}")

    return True


def inserisci_db(nome: str | None = None):
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome
    sqlpath = configurazione.get("scriptsdir").path / "inserimento_dati_test.sql"

    try:
        conn = sqlite3.connect(dbpath.as_posix())
        c = conn.cursor()
        c.executescript(sqlpath.read_text())
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Errore nell'inserimento dei dati di test:", e)
        return False

    return True


def aggiungi_utente(email: str, ruolo: str | None = None):
    from sostituzioni.model.model import Utente

    if not ruolo:
        ruolo = "amministratore"

    utente = Utente(email, ruolo)
    utente.inserisci()

    return True


def elimina_db(nome: str | None = None):
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    if not dbpath.exists():
        print("Errore: Database con questo nome non esistente.")
        return False

    dbpath.unlink()

    return True


def importa_docenti(file: click.File | object):
    from sostituzioni.control.importer import Docenti

    Docenti.from_buffer(file.read())


def importa_utenti(file: click.File | object):
    from sostituzioni.control.importer import Utenti

    Utenti.from_buffer(file.read())


def esegui_backup():
    from sostituzioni.control.backup import backup

    backup()


# //////////////////////////////


database_cli = AppGroup(
    "database", help="Gestione di dati e database."
)

importer_cli = AppGroup("importa", help="Importa docenti o utenti da file.")

backup_cli = AppGroup(
    "backup", help="Esegue il backup del database e del file di configurazione."
)


@database_cli.command("crea")
@click.argument("nome", type=str, required=False)
def _crea_db(nome):
    """\b
    Crea il database principale.

    Args:
        nome (str): Nome del database. (Default: database.db)
    """

    ok = crea_db(nome)

    if ok:
        print("Database creato.")


@database_cli.command("imposta-principale")
@click.argument("nome", type=str, required=False)
def _imposta_principale(nome):
    """\b
    Imposta il database fornito come database principale. I cambiamenti verranno applicati al riavvio del server se esso è attivo.

    Args:
        nome (str): Nome del database. (Default: database.db)
    """

    imposta_principale(nome)


@database_cli.command("elimina")
@click.argument("nome", type=str, required=False)
def _elimina_db(nome):
    """\b
    Elimina un database.

    Args:
        nome (str): Nome del database da eliminare. (Default: database.db)
    """

    ok = elimina_db(nome)

    if ok:
        print("Database eliminato.")


@database_cli.command("aggiungi-utente")
@click.argument("email", type=str, required=True)
@click.argument("ruolo", type=str, required=False)
def _aggiungi_utente(email, ruolo):
    """\b
    Aggiunge un utente al database.

    Args:
        email (str): Email dell'utente.
        ruolo (str): Ruolo dell'utente. [amministratore, editor, visualizzatore] (Default: amministratore)
    """

    ok = aggiungi_utente(email, ruolo)

    if ok:
        print(f"Utente {email} aggiunto.")


@importer_cli.command("docenti")
@click.argument("file", type=click.File("rb"))
def _importa_docenti(file):
    """\b
    Importa docenti da file.

    Args:
        file: File XLSX o CSV
    """

    importa_docenti(file)


@importer_cli.command("utenti")
@click.argument("file", type=click.File("rb"))
def _importa_utenti(file):
    """\b
    Importa utenti da file.

    Args:
        file: File XLSX o CSV
    """

    importa_utenti(file)


@backup_cli.command("esegui")
def _esegui_backup():
    """\b
    Esegue immediatamente il backup del database e del file di configurazione.
    """

    esegui_backup()
