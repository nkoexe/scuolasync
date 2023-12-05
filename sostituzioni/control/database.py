"""
database controller
"""

from beartype.typing import List, Tuple
from beartype._decor.decormain import beartype
import sqlite3
from datetime import datetime
import re

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
    def get(self, table: str, columns: str | Tuple = '*', where: str | Tuple | None = None, limit: int | None = None, load_lists: bool = True) -> SearchableList:
        """
        Esempi:
        database.get('aula', 'numero')
        database.get('aula', ('numero', 'piano'), where=('numero=100', 'cancellato=0'))
        database.get('utente', where='email="esempio@gandhimerano.com"', limit=1)
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

        rows = SearchableList(values=[dict(row) for row in self.cursor.fetchall()])

        self.close()

        if load_lists:
            rows = self.load_lists(table, rows)

        return rows

    def get_one(self, table: str, columns: str | Tuple = '*', where: str | Tuple | None = None, load_lists: bool = True) -> SearchableList:
        return self.get(table, columns, where, 1, load_lists)[0]

    def load_lists(self, table_name: str, rows: SearchableList):
        """
        Carica liste da diverse tabelle
        """

        match table_name:
            # Questa funzione convertiva le date degli oggetti da stringhe a oggetti datetime.
            # Date le arzigogolature le date vengono ora gestite come timestamp UNIX, fino alla loro visualizzazione.

            # Serve convertire gli orari da stringhe a qualcos'altro?
            # case OraPredefinita.TABLENAME:
            #     for row in rows:
            #         row['ora_inizio_default'] = 0
            #         row['ora_fine_default'] = 0

            # case Sostituzione.TABLENAME:
            #     for row in rows:
            #         row['data'] = datetime.fromtimestamp(row['data'])
            #         # row['ora_inizio'] =
            #         # row['ora_fine'] =

            # case Evento.TABLENAME:
            #     for row in rows:
            #         row['data_ora_inizio'] = datetime.fromtimestamp(row['data_ora_inizio'])
            #         row['data_ora_fine'] = datetime.fromtimestamp(row['data_ora_fine'])

            # case Notizia.TABLENAME:
            #     for row in rows:
            #         row['data_ora_inizio'] = datetime.fromtimestamp(row['data_ora_inizio'])
            #         row['data_ora_fine'] = datetime.fromtimestamp(row['data_ora_fine'])

            case Classe.TABLENAME:
                relazioni = self.get('aula_ospita_classe')

                for classe in rows:
                    classe['aule_ospitanti'] = []

                    aule = relazioni.get(classe['nome'], key='nome_classe')
                    if not aule:
                        continue

                    for aula in aule:
                        classe['aule_ospitanti'].append(aula['numero_aula'])

        return rows

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
    def update(self, table: str, where: str | Tuple | None = None, **values):
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
    def delete(self, table: str, where: str | Tuple):
        if isinstance(where, tuple):
            where = ' AND '.join(where)

        query = f'DELETE FROM {table} WHERE {where}'

        self.connect()
        self.execute(query)
        self.close()


# -----------------------------------------------


database = Database(configurazione.get('databasepath').path)
authdatabase = Database(configurazione.get('authdatabasepath').path)


# -----------------------------------------------


class ElementoDatabase:
    DATABASE: Database = database
    TABLENAME: str = ''
    KEY: str = ''

    # @staticmethod
    # def load(db, item):
    #     data = db.get(item.TABLENAME)
    #     data.key = item.KEY

    #     return data

    def load(item, columns: str | Tuple = '*', where: str | Tuple | None = None, limit: int | None = None):
        data = item.DATABASE.get(item.TABLENAME, columns, where, limit)
        data.key = item.KEY

        return data

    def modifica(self):
        pass

    def inserisci(self, **data):
        self.DATABASE.insert(self.TABLENAME, **data)


class ElementoDatabaseConStorico(ElementoDatabase):
    # def __init__(self, cancellato):
    #     self._cancellato = cancellato

    #     self.elimina = self.cancella = self.__del__

    def elimina(self, mantieni_in_storico: bool = True):
        return self.__del__(mantieni_in_storico)

    def __del__(self, mantieni_in_storico: bool = True):
        self._cancellato = True

    @property
    def cancellato(self):
        return self._cancellato


# -----------------------------------------------


class Aula(ElementoDatabaseConStorico):
    TABLENAME = 'aula'
    KEY = 'numero'

    def load(): return ElementoDatabase.load(Aula)

    def trova(numero):
        return database.get_one('aula', 'numero', where=f'numero="{numero}"', load_lists=False)

    # @beartype
    # def __init__(self, numero: str, piano: str, cancellato: bool):
    #     super(Aula, self).__init__(cancellato)

    #     self.numero = numero
    #     self.piano = piano

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

    def load(): return ElementoDatabase.load(Classe)

    def trova(nome):
        return database.get_one('classe', 'nome', where=f'nome="{nome}"', load_lists=False)

    # @beartype
    # def __init__(self, nome: str, aule_ospitanti: List[Aula], cancellato: bool):
    #     super(Classe, self).__init__(cancellato)

    #     self.nome = nome
    #     self.aule_ospitanti = aule_ospitanti

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

    def load(): return ElementoDatabase.load(Docente)

    def trova(nome_cognome):
        return database.get_one('docente', ('nome', 'cognome'), where=f'(nome || " " || cognome)="{nome_cognome}"')

    # @beartype
    # def __init__(self, nome: str, cognome: str, cancellato: bool):
    #     super(Docente, self).__init__(cancellato)

    #     self._nome = nome
    #     self._cognome = cognome

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

    def load(): return ElementoDatabase.load(OraPredefinita)

    # @beartype
    # def __init__(self, numero: int, ora_inizio: time, ora_fine: time):
    #     super(OraPredefinita, self).__init__()

    #     self._numero = numero
    #     self._ora_inizio = ora_inizio
    #     self._ora_fine = ora_fine

    @property
    def numero(self):
        return self._numero

    @beartype
    @numero.setter
    def numero(self, new: str):
        self._numero = new

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

    def load(): return ElementoDatabase.load(Sostituzione)

    def inserisci(self):

        super().inserisci(cancellato=False, pubblicato=self.pubblicato,
                          numero_aula=self.numero_aula, nome_classe=self.nome_classe,
                          nome_docente=self.nome_docente, cognome_docente=self.cognome_docente, data=self.data,
                          numero_ora_predefinita=self.ora_predefinita, ora_inizio=self.ora_inizio, ora_fine=self.ora_fine,
                          note=self.note)

    # @beartype
    # def __init__(
    #     self,
    #     id: int,
    #     cancellato: bool,
    #     aula: Aula,
    #     classe: Classe,
    #     docente: Docente | None = None,
    #     data: int | None = None,
    #     ora_inizio: str | None = None,
    #     ora_fine: str | None = None,
    #     ora_predefinita: OraPredefinita | None = None,
    #     note: str | None = None,
    #     pubblicato: bool = False
    # ):
    #     super(Sostituzione, self).__init__(cancellato)

    #     self._id = id
    #     self._aula = aula
    #     self._classe = classe
    #     self._docente = docente
    #     self._data = data
    #     self._ora_inizio = ora_inizio
    #     self._ora_fine = ora_fine
    #     self._ora_predefinita = ora_predefinita
    #     self._note = note
    #     self._pubblicato = pubblicato

    @property
    def pubblicato(self):
        return self._pubblicato

    @beartype
    @pubblicato.setter
    def pubblicato(self, new: bool):
        self._pubblicato = new

    @property
    def numero_aula(self):
        return self._numero_aula

    @beartype
    @numero_aula.setter
    def numero_aula(self, new: str | None):
        self._numero_aula = new

    @property
    def aula(self):
        return self._aula

    @beartype
    @aula.setter
    def aula(self, new: str | Aula | None):
        self._aula = None

        if isinstance(new, Aula):
            self._aula = new
            self._numero_aula = new.numero
        elif isinstance(new, str):
            aula = Aula.trova(new)
            self._numero_aula = aula['numero']

    @property
    def nome_classe(self):
        return self._nome_classe

    @beartype
    @nome_classe.setter
    def nome_classe(self, new: str | None):
        self._nome_classe = new

    @property
    def classe(self):
        return self._classe

    @beartype
    @classe.setter
    def classe(self, new: str | Classe | None):
        self._classe = None

        if isinstance(new, Classe):
            self._classe = new
            self._nome_classe = new.nome
        elif isinstance(new, str):
            classe = Classe.trova(new)
            print(classe)
            self._nome_classe = classe['nome']

    @property
    def nome_docente(self):
        return self._nome_docente

    @beartype
    @nome_docente.setter
    def nome_docente(self, new: str | None):
        self._nome_docente = new

    @property
    def cognome_docente(self):
        return self._cognome_docente

    @beartype
    @cognome_docente.setter
    def cognome_docente(self, new: str | None):
        self._cognome_docente = new

    @property
    def docente(self):
        return self._docente

    @beartype
    @docente.setter
    def docente(self, new: str | Docente | None):
        self._docente = None
        self._nome_docente = None
        self._cognome_docente = None

        if isinstance(new, Docente):
            self._docente = new
            self._nome_docente = new.nome
            self._cognome_docente = new.cognome
        elif isinstance(new, str):
            docente = Docente.trova(new)
            self._nome_docente = docente['nome']
            self._cognome_docente = docente['cognome']

    @property
    def data(self):
        return self._data

    @beartype
    @data.setter
    def data(self, new: int | str | None):
        self._data = None

        if isinstance(new, int):
            self._data = new
        elif isinstance(new, str):
            self._data = int(datetime.strptime(new, '%Y-%m-%d').timestamp())

    @property
    def ora_inizio(self):
        return self._ora_inizio

    @beartype
    @ora_inizio.setter
    def ora_inizio(self, new: str | None):
        self._ora_inizio = None

        if isinstance(new, str):
            if not new:
                self._ora_inizio = None

            elif re.match(r'^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$', new):
                self._ora_inizio = new
            else:
                raise ValueError(f'Ora_inizio {new} non valida, seguire il formato XX:XX')

    @property
    def ora_fine(self):
        return self._ora_fine

    @beartype
    @ora_fine.setter
    def ora_fine(self, new: str | None):
        self._ora_fine = None

        if isinstance(new, str):
            if not new:
                self._ora_inizio = None

            elif re.match(r'^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$', new):
                self._ora_fine = new
            else:
                raise ValueError(f'Ora_fine {new} non valida, seguire il formato XX:XX')

    @property
    def ora_predefinita(self):
        return self._ora_predefinita

    @beartype
    @ora_predefinita.setter
    def ora_predefinita(self, new: int | str | None):
        self._ora_predefinita = new

        if isinstance(new, str):
            self._ora_predefinita = int(new)

    @property
    def note(self):
        return self._note

    @beartype
    @note.setter
    def note(self, new: str | None):
        self._note = new


class Evento(ElementoDatabaseConStorico):
    TABLENAME = 'evento'
    KEY = 'id'

    def load(): return ElementoDatabase.load(Evento)

    # @beartype
    # def __init__(
    #     self,
    #     id: int,
    #     cancellato: bool,
    #     testo: str,
    #     data_ora_inizio: datetime | None = None,
    #     data_ora_fine: datetime | None = None,
    #     urgente: bool = False,
    # ):
    #     super(Evento, self).__init__(cancellato)

    #     self._id = id
    #     self.testo = testo
    #     self.data_ora_inizio = data_ora_inizio
    #     self.data_ora_fine = data_ora_fine
    #     self.urgente = urgente


class Notizia(ElementoDatabaseConStorico):
    TABLENAME = 'notizia'
    KEY = 'id'

    def load(): return ElementoDatabase.load(Notizia)

    # @beartype
    # def __init__(
    #     self,
    #     id: int,
    #     cancellato: bool,
    #     testo: str,
    #     data_ora_inizio: datetime | None = None,
    #     data_ora_fine: datetime | None = None,
    # ):
    #     super(Notizia, self).__init__(cancellato)

    #     self._id = id
    #     self.testo = testo
    #     self.data_ora_inizio = (data_ora_inizio,)
    #     self.data_ora_fine = data_ora_fine


class Visualizzazione(ElementoDatabase):
    TABLENAME = 'visualizzazione'
    KEY = 'id'

    def load(): return ElementoDatabase.load(Visualizzazione)

    @beartype
    def __init__(self):
        super(Visualizzazione, self).__init__()


# --------------------


class Utente(ElementoDatabase):
    DATABASE = authdatabase
    TABLENAME = 'utente'
    KEY = 'email'

    def load(*args, **kwargs): return ElementoDatabase.load(Utente, *args, **kwargs)

    @beartype
    def __init__(self, email: str, ):
        super(Utente, self).__init__()

        self.email = email
