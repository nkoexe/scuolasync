import click
from flask.cli import AppGroup
from os import system

from sostituzioni.control.configurazione import configurazione


database_cli = AppGroup('database')

database_utenti_cli = AppGroup('utenti')
database_cli.add_command(database_utenti_cli)


@database_cli.command('crea')
@click.argument('nome', type=str, required=False)
def crea_db(nome):
    sqlpath = configurazione.get('scriptsdir').path / 'creazione_database.sql'
    if not nome:
        nome = 'database.db'
    elif '.' not in nome:
        nome = nome + '.db'

    dbpath = configurazione.get('rootpath').path / 'database' / nome

    if dbpath.exists():
        print('ErroreL: Database con questo nome già esistente.')
        return

    print('File database:', dbpath)

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print('Errore nella creazione del database')
        return

    print('Database principale creato.')


@database_utenti_cli.command('crea')
@click.argument('nome', type=str, required=False)
def crea_db_utenti(nome):

    sqlpath = configurazione.get('scriptsdir').path / 'creazione_database_utenti.sql'
    if not nome:
        nome = 'utenti.db'
    elif '.' not in nome:
        nome = nome + '.db'

    dbpath = configurazione.get('rootpath').path / 'database' / nome

    if dbpath.exists():
        print('Errore: Database con questo nome già esistente.')
        return

    print('File database:', dbpath)

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print('Errore nella creazione del database')
        return

    print('Database utenti creato.')


@database_cli.command('imposta-principale')
@click.argument('nome', type=str, required=False)
def imposta_principale(nome):
    if not nome:
        nome = 'database.db'

    configurazione.set('databasepath', (1, 'database' / nome))

    print(f'Database principale impostato su {nome}')


@database_utenti_cli.command('imposta-principale')
@click.argument('nome', type=str, required=False)
def imposta_principale_utenti(nome):
    if not nome:
        nome = 'utenti.db'

    configurazione.set('authdatabasepath', (1, 'database' / nome))

    print(f'Database utenti impostato su {nome}')


@database_cli.command("inserisci-test")
@click.argument("nome", type=str, required=False)
def inserisci_db(nome):

    sqlpath = configurazione.get('scriptsdir').path / 'inserimento_dati_test.sql'

    if not nome:
        nome = 'database.db'

    dbpath = configurazione.get('rootpath').path / 'database' / nome

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print('Errore nell\'inserimento dei dati di test.')
        return

    print('Dati di test inseriti nel database principale.')


@database_utenti_cli.command("inserisci-test")
@click.argument("nome", type=str, required=False)
def inserisci_db_utenti(nome):

    sqlpath = configurazione.get('scriptsdir').path / 'inserimento_dati_utenti_test.sql'
    if not nome:
        nome = 'utenti.db'

    dbpath = configurazione.get('rootpath').path / 'database' / nome

    result = system(f'sqlite3 {dbpath.as_posix()} ".read {sqlpath.as_posix()}"')

    if result != 0:
        print('Errore nell\'inserimento dei dati di test.')
        return

    print('Dati di test inseriti nel database utenti.')
