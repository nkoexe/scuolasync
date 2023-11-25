"""
database controller
"""

from beartype.typing import List, Dict, Tuple
from beartype._decor.decormain import beartype
from datetime import date, datetime, time
import sqlite3

from sostituzioni.lib.searchablelist import SearchableList
from sostituzioni.logger import logger
from sostituzioni.control.configurazione import configurazione


class Database:
    def __init__(self, path):
        self.path = path
        self.connection = None

    def connect(self):
        if not self.connection:
            try:
                self.connection = sqlite3.connect(self.path)
                self.connection.execute('PRAGMA foreign_keys = 1')
                self.connection.row_factory = sqlite3.Row

                self.cursor = self.connection.cursor()
            except sqlite3.Error as e:
                logger.error(e)
                exit()

    def close(self):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.connection = None

    def execute(self, query: str, values: List | None = None):
        try:
            if values is not None:
                self.cursor.execute(query, list(values))
                self.connection.commit()
            else:
                self.cursor.execute(query)
        except sqlite3.Error as e:
            logger.error(e)
            self.connection.rollback()

    # def get_all_from(self, table: str) -> List[Dict]:
    #     self.execute('SELECT * FROM ' + table)

    #     return [dict(row) for row in self.cursor.fetchall()]

    @beartype
    def get(self, table: str, columns: str | Tuple[str] = '*', where: str | Tuple[str] | None = None, limit: int | None = None) -> SearchableList:
        """
        Esempi:
        database.get('aula', 'numero')
        database.get('aula', ('numero', 'piano'), where=('numero=100', 'cancellato=0'))
        database.get('utente', where='email=esempio@gandhimerano.com', limit=1)
        """

        if isinstance(columns, tuple):
            columns = ', '.join(columns)

        query = f'SELECT {columns} from {table}'

        if where is not None:
            if isinstance(where, tuple):
                where = ' AND '.join(where)

            query += f' WHERE {where}'

        if limit is not None:
            query += f' LIMIT {limit}'

        self.connect()
        self.execute(query)

        result = SearchableList(values=[dict(row) for row in self.cursor.fetchall()])

        self.close()

        return result

    @beartype
    def insert(self, table: str, **data):
        """
        Esempio: database.insert('aula', numero='214', piano='2')
        """
        assert data

        columns = ', '.join(data.keys())
        values = ', '.join('?' for i in data)

        query = f'INSERT INTO {table} ({columns}) VALUES({values});'

        self.connect()
        self.execute(query, data.values())
        self.close()

    @beartype
    def update(self, table: str, where: str | Tuple[str] | None = None, **values):
        assert where
        assert values

        query = f'UPDATE {table} SET {", ".join([f"{column} = {value}" for (column, value) in values.items()])}'

        if where is not None:
            if isinstance(where, tuple):
                where = ' AND '.join(where)

            query += f' WHERE {where}'

        self.connect()
        self.execute(query)
        self.close()

    @beartype
    def delete(self, table: str, where: str | Tuple[str]):
        if isinstance(where, tuple):
            where = ' AND '.join(where)

        query = f'DELETE FROM {table} WHERE {where}'

        self.connect()
        self.execute(query)
        self.close()

    # def load_all(self):
    #     aule = SearchableList('numero')
    #     classi = SearchableList('nome')
    #     docenti = SearchableList()  # quale cazzo è l'id in questo caso??????? modifico per includere anche chiavi tuple????
    #     ore_predefinite = SearchableList()
    #     sostituzioni = SearchableList()
    #     eventi = SearchableList()
    #     notizie = SearchableList()
    #     visualizzazioni_online = SearchableList()
    #     visualizzazioni_fisiche = SearchableList()

    #     db_aule = database.get_all_from('aula')
    #     for db_aula in db_aule:
    #         aula = Aula(db_aula['numero'], db_aula['piano'], bool(db_aula['cancellato']))
    #         aule.append(aula)

    #     db_classi = database.get_all_from('classe')
    #     for db_classe in db_classi:
    #         # Istanziare con attributo aule_ospitanti vuoto, in quanto lo aggiungiamo in seguito
    #         classe = Classe(db_classe['nome'], [], bool(db_classe['cancellato']))
    #         classi.append(classe)

    #     db_aule_classi = database.get_all_from('aula_ospita_classe')
    #     for db_aula_classe in db_aule_classi:
    #         classi[db_aula_classe['nome_classe']].aule_ospitanti.append(db_aula_classe['numero_aula'])

    #     db_docenti = database.get_all_from('docente')
    #     for db_docente in db_docenti:
    #         docente = Docente(db_docente['nome'], db_docente['cognome'], bool(db_docente['cancellato']))
    #         docenti.append(docente)

    #     # db_ore_predefinite = database.get_all_from('ora_predefinita')
    #     # for db_ora_predefinita in db_ore_predefinite:
    #     #     ora_predefinita = OraPredefinita(db_ora_predefinita['numero'], db_ora_predefinita['ora_inizio'], db_ora_predefinita['ora_fine'])
    #     #     ore_predefinite.append(ora_predefinita)

    #     # db_sostituzioni = database.get_all_from('aula')
    #     # for db_aula in db_sostituzioni:
    #     #     aula = Aula(db_aula['numero'], db_aula['piano'], bool(db_aula['cancellato']))
    #     #     sostituzioni.append(aula)

    #     return aule, classi, docenti, ore_predefinite, sostituzioni, eventi, notizie, visualizzazioni_online, visualizzazioni_fisiche


# -----------------------------------------------


class ElementoDatabase:
    def __init__(self):
        super().__init__()

    def modifica(self):
        pass

    def salva(self):
        pass


class ElementoDatabaseConStorico(ElementoDatabase):
    def __init__(self, cancellato):
        self._cancellato = cancellato

        self.elimina = self.cancella = self.__del__

    def __del__(self, mantieni_in_storico: bool = True):
        self._cancellato = True

    @property
    def cancellato(self):
        return self._cancellato


# -----------------------------------------------


class Aula(ElementoDatabaseConStorico):
    TABLENAME = 'aula'
    KEY = 'numero'

    def load():
        aule = database.get(Aula.TABLENAME)
        aule.key = Aula.KEY

        return aule

    @beartype
    def __init__(self, numero: str, piano: str, cancellato: bool):
        super(Aula, self).__init__(cancellato)

        self.numero = numero
        self.piano = piano

    def __repr__(self) -> str:
        return 'Aula ' + self.numero

    @beartype
    def modifica(self, numero: str | None = None, piano: str | None = None):
        if not any((numero, piano)):
            logger.warning('Nessun parametro passato ad aula.modifica')
            return

        if numero:
            self.numero = numero

        if piano:
            self.piano = piano

    @property
    def numero(self):
        return self._numero

    @beartype
    @numero.setter
    def numero(self, new: str):
        self._numero = new

    @property
    def piano(self):
        return self._piano

    @beartype
    @piano.setter
    def piano(self, new: str):
        self._piano = new


class Classe(ElementoDatabaseConStorico):
    TABLENAME = 'classe'
    KEY = 'nome'

    def load():
        classi = database.get(Classe.TABLENAME)
        classi.key = Classe.KEY

        for classe in classi:
            classe['aule_ospitanti'] = []

        for relazione in database.get('aula_ospita_classe'):
            classi[relazione['nome_classe']]['aule_ospitanti'].append(relazione['numero_aula'])

        return classi

    @beartype
    def __init__(self, nome: str, aule_ospitanti: List[Aula], cancellato: bool):
        super(Classe, self).__init__(cancellato)

        self.nome = nome
        self.aule_ospitanti = aule_ospitanti

    @property
    def nome(self):
        return self._nome

    @beartype
    @nome.setter
    def nome(self, new):
        self._nome = new

    @property
    def aule_ospitanti(self):
        return self._aule_ospitanti

    @beartype
    @aule_ospitanti.setter
    def aule_ospitanti(self, new):
        self._aule_ospitanti = new


class Docente(ElementoDatabaseConStorico):
    TABLENAME = 'docente'
    KEY = ('nome', 'cognome')

    def load():
        docenti = database.get(Docente.TABLENAME)
        docenti.key = Docente.KEY

        return docenti

    @beartype
    def __init__(self, nome: str, cognome: str, cancellato: bool):
        super(Docente, self).__init__(cancellato)

        self._nome = nome
        self._cognome = cognome

    @property
    def nome(self):
        return self._nome

    @beartype
    @nome.setter
    def nome(self, new: str):
        self._nome = new

    @property
    def cognome(self):
        return self._cognome

    @beartype
    @cognome.setter
    def cognome(self, new: str):
        self._cognome = new


class OraPredefinita(ElementoDatabase):
    TABLENAME = 'ora_predefinita'
    KEY = 'numero'

    def load():
        ore_predefinite = database.get(OraPredefinita.TABLENAME)
        ore_predefinite.key = OraPredefinita.KEY

        return ore_predefinite

    @beartype
    def __init__(self, numero: int, ora_inizio: time, ora_fine: time):
        super(OraPredefinita, self).__init__()

        self._numero = numero
        self._ora_inizio = ora_inizio
        self._ora_fine = ora_fine

    @property
    def ora_inizio(self):
        return self._ora_inizio

    @beartype
    @ora_inizio.setter
    def ora_inizio(self, new):
        self._ora_inizio = new

    @property
    def ora_fine(self):
        return self._ora_fine

    @beartype
    @ora_fine.setter
    def ora_fine(self, new):
        self._ora_fine = new


class Sostituzione(ElementoDatabaseConStorico):
    TABLENAME = 'sostituzione'
    KEY = 'id'

    def load():
        return database.get(Sostituzione.TABLENAME)

    @beartype
    def __init__(
        self,
        id: int,
        cancellato: bool,
        aula: Aula,
        classe: Classe,
        docente: Docente | None = None,
        data: date | None = None,
        ora_inizio: time | None = None,
        ora_fine: time | None = None,
        ora_predefinita: OraPredefinita | None = None,
        note: str | None = None,
        pubblicato: bool = False
    ):
        super(Sostituzione, self).__init__(cancellato)

        self._id = id
        self._aula = aula
        self._classe = classe
        self._docente = docente
        self._data = data
        self._ora_inizio = ora_inizio
        self._ora_fine = ora_fine
        self._ora_predefinita = ora_predefinita
        self._note = note
        self._pubblicato = pubblicato


class Evento(ElementoDatabaseConStorico):
    TABLENAME = 'evento'
    KEY = 'id'

    def load():
        return database.get(Evento.TABLENAME)

    @beartype
    def __init__(
        self,
        id: int,
        cancellato: bool,
        testo: str,
        data_ora_inizio: datetime | None = None,
        data_ora_fine: datetime | None = None,
        urgente: bool = False,
    ):
        super(Evento, self).__init__(cancellato)

        self._id = id
        self.testo = testo
        self.data_ora_inizio = data_ora_inizio
        self.data_ora_fine = data_ora_fine
        self.urgente = urgente


class Notizia(ElementoDatabaseConStorico):
    TABLENAME = 'notizia'
    KEY = 'id'

    def load():
        return database.get(Notizia.TABLENAME)

    @beartype
    def __init__(
        self,
        id: int,
        cancellato: bool,
        testo: str,
        data_ora_inizio: datetime | None = None,
        data_ora_fine: datetime | None = None,
    ):
        super(Notizia, self).__init__(cancellato)

        self._id = id
        self.testo = testo
        self.data_ora_inizio = (data_ora_inizio,)
        self.data_ora_fine = data_ora_fine


class Visualizzazione(ElementoDatabase):
    @beartype
    def __init__(self):
        super(Visualizzazione, self).__init__()


class VisualizzazioneOnline(Visualizzazione):
    @beartype
    def __init__(self):
        super(VisualizzazioneOnline, self).__init__()


class VisualizzazioneFisica(Visualizzazione):
    @beartype
    def __init__(self):
        super(VisualizzazioneFisica, self).__init__()


# --------------------


class Utente(ElementoDatabase):
    TABLENAME = 'utente'
    KEY = 'email'

    # Trovare un modo per mettere una singola funzione load nella classe Elementodatabase
    def load(columns: str | Tuple[str] = '*', where: str | Tuple[str] | None = None, limit: int | None = None):
        return authdatabase.get(Utente.TABLENAME, columns, where, limit)

    @beartype
    def __init__(self, email: str, ):
        super(Utente, self).__init__()

        self.email = email


# --------------------


database = Database(configurazione.get('databasepath').path)
authdatabase = Database(configurazione.get('authdatabasepath').path)
