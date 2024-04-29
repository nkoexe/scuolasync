import click
from flask.cli import AppGroup
from os import system

from sostituzioni.control.configurazione import configurazione


database_cli = AppGroup("database")

database_utenti_cli = AppGroup("utenti")
database_cli.add_command(database_utenti_cli)

importer_cli = AppGroup("importa")

backup_cli = AppGroup("backup")


@database_cli.command("crea")
@click.argument("nome", type=str, required=False)
def crea_db(nome):
    sqlpath = configurazione.get("scriptsdir").path / "creazione_database.sql"
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    if dbpath.exists():
        print("Errore: Database con questo nome già esistente.")
        return

    print("File database:", dbpath)

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print("Errore nella creazione del database")
        return

    print("Database principale creato.")


@database_utenti_cli.command("crea")
@click.argument("nome", type=str, required=False)
def crea_db_utenti(nome):
    sqlpath = configurazione.get("scriptsdir").path / "creazione_database_utenti.sql"
    if not nome:
        nome = "utenti.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    if dbpath.exists():
        print("Errore: Database con questo nome già esistente.")
        return

    print("File database:", dbpath)

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print("Errore nella creazione del database")
        return

    print("Database utenti creato.")


@database_cli.command("imposta-principale")
@click.argument("nome", type=str, required=False)
def imposta_principale(nome):
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    configurazione.set("databasepath", (1, "database/" + nome))
    configurazione.esporta()

    print(f"Database principale impostato su {nome}")


@database_utenti_cli.command("imposta-principale")
@click.argument("nome", type=str, required=False)
def imposta_principale_utenti(nome):
    if not nome:
        nome = "utenti.db"
    elif "." not in nome:
        nome = nome + ".db"

    configurazione.set("authdatabasepath", (1, "database/" + nome))
    configurazione.esporta()

    print(f"Database utenti impostato su {nome}")


@database_cli.command("inserisci-test")
@click.argument("nome", type=str, required=False)
def inserisci_db(nome):
    sqlpath = configurazione.get("scriptsdir").path / "inserimento_dati_test.sql"

    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print("Errore nell'inserimento dei dati di test.")
        return

    print("Dati di test inseriti nel database principale.")


@database_utenti_cli.command("aggiungi-utente")
@click.argument("email", type=str, required=True)
@click.argument("ruolo", type=str, required=False)
def aggiungi_utente(email, ruolo):
    from sostituzioni.model.model import Utente

    if not ruolo:
        ruolo = "amministratore"

    utente = Utente(email, ruolo)
    utente.inserisci()

    print("Utente aggiunto.")


@database_utenti_cli.command("inserisci-test")
@click.argument("nome", type=str, required=False)
def inserisci_db_utenti(nome):
    sqlpath = configurazione.get("scriptsdir").path / "inserimento_dati_utenti_test.sql"

    if not nome:
        nome = "utenti.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print("Errore nell'inserimento dei dati di test.")
        return

    print("Dati di test inseriti nel database utenti.")


@database_cli.command("elimina")
@click.argument("nome", type=str, required=False)
def elimina_db(nome):
    if not nome:
        nome = "database.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    if not dbpath.exists():
        print("Errore: Database con questo nome non esistente.")
        return

    dbpath.unlink()

    print("Database eliminato.")


@database_utenti_cli.command("elimina")
@click.argument("nome", type=str, required=False)
def elimina_db_utenti(nome):
    if not nome:
        nome = "utenti.db"
    elif "." not in nome:
        nome = nome + ".db"

    dbpath = configurazione.get("rootpath").path / "database" / nome

    if not dbpath.exists():
        print("Errore: Database con questo nome non esistente.")
        return

    dbpath.unlink()

    print("Database eliminato.")


@importer_cli.command("docenti")
@click.argument("file", type=click.File("rb"))
def importa_docenti(file):
    from sostituzioni.control.importer import Docenti

    Docenti.from_buffer(file.read())


@importer_cli.command("utenti")
@click.argument("file", type=click.File("rb"))
def importa_utenti(file):
    from sostituzioni.control.importer import Utenti

    Utenti.from_buffer(file.read())


@backup_cli.command("esegui")
def esegui_backup():
    from sostituzioni.control.backup import backup

    backup()
