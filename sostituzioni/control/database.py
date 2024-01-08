"""
database controller
"""

from beartype import beartype
from beartype.typing import List, Tuple, Dict
import sqlite3
from datetime import datetime
import logging
import re

from sostituzioni.lib.searchablelist import SearchableList
from sostituzioni.control.configurazione import configurazione

logger = logging.getLogger(__name__)


class Where:
    def __init__(self, attribute: str, parent=None) -> None:
        self.attribute = attribute
        self.operator = "="
        self.value: any = None
        self.parent = parent

    def resolve(self):
        # match self.value:
        #     case None:
        #         value = "null"

        #     case list():
        #         value = "(" + ", ".join(str(v) for v in self.value) + ")"

        #     case bool():
        #         value = str(int(self.value))

        #     case int():
        #         value = str(self.value)

        #     case float():
        #         value = str(self.value)

        #     case str():
        #         value = '"' + self.value + '"'

        #     case _:
        #         value = '"' + str(self.value) + '"'

        resolved = str(self.attribute) + self.operator + "?"

        if isinstance(self.parent, Where):
            where, values = self.parent.resolve()
            resolved = where + " AND " + resolved
            values.append(self.value)
        else:
            values = [self.value]

        return resolved, values

    def equals(self, value):
        self.operator = "="
        self.value = value
        return self

    def notequals(self, value):
        self.operator = "!="
        self.value = value
        return self

    def lessthan(self, value):
        self.operator = "<"
        self.value = value
        return self

    def lessthanorequal(self, value):
        self.operator = "<="
        self.value = value
        return self

    def greaterthan(self, value):
        self.operator = ">"
        self.value = value
        return self

    def greaterthanorequal(self, value):
        self.operator = ">="
        self.value = value
        return self

    def LIKE(self, value):
        self.operator = " LIKE "
        self.value = value
        return self

    def NOTLIKE(self, value):
        self.operator = " NOT LIKE "
        self.value = value

    def IN(self, value):
        self.operator = " IN "
        self.value = value
        return self

    def NOTIN(self, value):
        self.operator = " NOT IN "
        self.value = value
        return self

    def AND(self, attribute):
        return Where(attribute, self)


class Database:
    def __init__(self, path):
        self.path = path
        self.connection = None

    def connect(self):
        if not self.connection:
            # logger.debug("Trying to open database connection...")
            try:
                self.connection = sqlite3.connect(self.path)
                # logger.debug("Database connection established.")
                self.connection.execute("PRAGMA foreign_keys = 1")
                self.connection.row_factory = sqlite3.Row

                self.cursor = self.connection.cursor()
                # logger.debug("Database cursor created.")
            except sqlite3.Error as e:
                logger.error(e)
                exit()

    def close(self):
        # logger.debug("Closing connection to database...")
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.connection = None
        # logger.debug("Connection to database closed successfully")

    def execute(self, query: str, values: List | None = None):
        logger.debug("Executing query " + query + " - " + str(values))
        try:
            if values is not None:
                self.cursor.execute(query, list(values))
                self.connection.commit()
            else:
                self.cursor.execute(query)
        except sqlite3.Error as e:
            logger.error(e)
            self.connection.rollback()

    @beartype
    def get(
        self,
        table: str,
        columns: str | Tuple = "*",
        where: Where | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        load_lists: bool = True,
    ) -> SearchableList:
        """
        Esempi:
        database.get('aula', 'numero')
        database.get('aula', ('numero', 'piano'), where=Where('numero').equals(100).AND('cancellato').equals(False))
        database.get('utente', where=Where('email').equals('esempio@gandhimerano.com'), limit=1)
        """

        values = []

        if isinstance(columns, tuple):
            columns = ", ".join(columns)

        query = f"SELECT {columns} from {table}"

        if where is not None:
            where, where_values = where.resolve()

            query += f" WHERE {where}"
            values.extend(where_values)

        if order_by is not None:
            query += f" ORDER BY {order_by}"

        if limit is not None:
            query += f" LIMIT {limit}"

        self.connect()
        self.execute(query, values)

        rows = SearchableList(values=[dict(row) for row in self.cursor.fetchall()])

        self.close()

        if load_lists:
            rows = self.load_lists(table, rows)

        return rows

    def get_one(
        self,
        table: str,
        columns: str | Tuple = "*",
        where: Where | None = None,
        load_lists: bool = True,
    ) -> SearchableList:
        data = self.get(table, columns, where, None, 1, load_lists)

        if len(data) > 0:
            return data[0]
        return None

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
                relazioni = self.get("aula_ospita_classe")

                for classe in rows:
                    classe["aule_ospitanti"] = []

                    aule = relazioni.get(classe["nome"], key="nome_classe")
                    if not aule:
                        continue

                    for aula in aule:
                        classe["aule_ospitanti"].append(aula["numero_aula"])

        return rows

    @beartype
    def insert(self, table: str, or_ignore: bool = False, **data):
        """
        Esempio: database.insert('aula', numero='214', piano='2')
        """
        assert data

        columns = ", ".join(data.keys())
        values = ", ".join("?" for i in data)

        query = f"INSERT {'OR IGNORE ' if or_ignore else ''}INTO {table} ({columns}) VALUES({values});"

        self.connect()
        self.execute(query, data.values())

        self.cursor.execute("SELECT last_insert_rowid();")
        id = self.cursor.fetchone()[0]

        self.close()

        return id

    @beartype
    def update(self, table: str, where: Where | None = None, **values):
        assert values

        # query = f'UPDATE {table} SET {", ".join([f"{column}={value}" for (column, value) in values.items()])}'
        query = f'UPDATE {table} SET {", ".join([f"{column}=?" for column in values.keys()])}'
        values = list(values.values())

        if where is not None:
            where, where_values = where.resolve()

            query += f" WHERE {where}"
            values.extend(where_values)

        self.connect()
        self.execute(query, values)
        self.close()

        return True

    @beartype
    def delete(self, table: str, where: Where):
        where, values = where.resolve()

        query = f"DELETE FROM {table} WHERE {where}"

        self.connect()
        self.execute(query, values)
        self.close()


# -----------------------------------------------


database = Database(configurazione.get("databasepath").path)
authdatabase = Database(configurazione.get("authdatabasepath").path)


# -----------------------------------------------


class ElementoDatabase:
    DATABASE: Database = database
    TABLENAME: str = ""
    KEY: str = ""

    # @staticmethod
    # def load(db, item):
    #     data = db.get(item.TABLENAME)
    #     data.key = item.KEY

    #     return data

    def load(
        item,
        columns: str | Tuple = "*",
        where: Where | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ):
        data = item.DATABASE.get(item.TABLENAME, columns, where, order_by, limit)
        data.key = item.KEY

        return data


class ElementoDatabaseConStorico(ElementoDatabase):
    # def __init__(self, cancellato):
    #     self._cancellato = cancellato

    #     self.elimina = self.cancella = self.__del__

    @beartype
    def elimina(self, mantieni_in_storico: bool = True):
        self.cancellato = True

        if not self.id:
            return False

        if mantieni_in_storico:
            return self.DATABASE.update(
                self.TABLENAME, Where("id").equals(self.id), cancellato=True
            )

        else:
            self.DATABASE.delete(self.TABLENAME, Where("id").equals(self.id))

    @property
    def cancellato(self):
        return self._cancellato

    @beartype
    @cancellato.setter
    def cancellato(self, new: bool | int | None):
        self._cancellato = None
        if new is not None:
            self._cancellato = bool(new)


# -----------------------------------------------


class Aula(ElementoDatabaseConStorico):
    TABLENAME = "aula"
    KEY = "numero"

    def load():
        return ElementoDatabase.load(Aula)

    def trova(numero: str):
        return database.get_one(
            "aula", "numero", where=Where("numero").equals(numero), load_lists=False
        )

    # @beartype
    # def __init__(self, numero: str, piano: str, cancellato: bool):
    #     super(Aula, self).__init__(cancellato)

    #     self.numero = numero
    #     self.piano = piano

    def __repr__(self) -> str:
        return "Aula " + self.numero

    @beartype
    def modifica(self, numero: str | None = None, piano: str | None = None):
        if not any((numero, piano)):
            logger.warning("Nessun parametro passato ad aula.modifica")
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
    TABLENAME = "classe"
    KEY = "nome"

    def load():
        return ElementoDatabase.load(Classe)

    def trova(nome):
        return database.get_one(
            "classe", "nome", where=Where("nome").equals(nome), load_lists=False
        )

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
    TABLENAME = "docente"
    KEY = ("nome", "cognome")

    def load():
        return ElementoDatabase.load(Docente)

    def inserisci(self):
        return self.DATABASE.insert(
            self.TABLENAME,
            nome=self.nome,
            cognome=self.cognome,
            cancellato=self.cancellato,
        )

    @beartype
    def trova(cognome_nome: str):
        return database.get_one(
            "docente",
            ("cognome", "nome"),
            where=Where("(cognome || ' ' || nome)").LIKE(cognome_nome.lower()),
        )

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
    TABLENAME = "ora_predefinita"
    KEY = "numero"

    def load():
        return ElementoDatabase.load(OraPredefinita)

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
    TABLENAME = "sostituzione"
    KEY = "id"

    def __init__(self, id: int):
        # Load data from database
        data = self.DATABASE.get_one(self.TABLENAME, "*", where=Where("id").equals(id))

        if data is None:
            raise ValueError(f"Sostituzione con id {id} non trovata")

        self.id = id
        self.cancellato = data["cancellato"]
        self.pubblicato = data["pubblicato"]
        self.numero_aula = data["numero_aula"]
        self.nome_classe = data["nome_classe"]
        self.nome_docente = data["nome_docente"]
        self.cognome_docente = data["cognome_docente"]
        self.data = data["data"]
        self.ora_predefinita = data["numero_ora_predefinita"]
        self.ora_inizio = data["ora_inizio"]
        self.ora_fine = data["ora_fine"]
        self.note = data["note"]

    def load(filtri: Where | Dict | None = None):
        if filtri is None:
            # default sono le sostituzioni future

            # get todays timestamp at midnight
            today = datetime.today()
            today = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today = int(today.timestamp())

            where = (
                Where("data")
                .greaterthanorequal(today)
                .AND("cancellato")
                .equals(False)
                .AND("pubblicato")
                .equals(True)
            )

            return ElementoDatabase.load(Sostituzione, where=where, order_by="data")

        if isinstance(filtri, Where):
            return ElementoDatabase.load(Sostituzione, where=filtri, order_by="data")

        data_inizio: int = filtri.get(
            "data_inizio",
            int(
                datetime.today()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            ),
        )  # default è oggi
        data_fine: int | None = filtri.get(
            "data_fine", None
        )  # default è nessuna, quindi future

        if data_inizio is None:
            data_inizio = 0

        where = Where("data").greaterthanorequal(data_inizio)

        if data_fine is not None:
            where = where.AND("data").lessthanorequal(data_fine)

        # Se è specificato di caricare anche i cancellati, non impostare un where aggiuntivo
        # Mostrare solo i cancellati non è possibile, le opzioni sono tutti o non cancellati
        cancellato = filtri.get("cancellato", False)
        if not cancellato:
            where = where.AND("cancellato").equals(False)

        # Lo stesso vale per i pubblicati, o tutti o solo pubblicati
        pubblicato = filtri.get("pubblicato", True)
        if pubblicato:
            where = where.AND("pubblicato").equals(True)

        return ElementoDatabase.load(Sostituzione, where=where, order_by="data")

    def inserisci(self):
        id = self.DATABASE.insert(
            self.TABLENAME,
            cancellato=False,
            pubblicato=self.pubblicato,
            numero_aula=self.numero_aula,
            nome_classe=self.nome_classe,
            nome_docente=self.nome_docente,
            cognome_docente=self.cognome_docente,
            data=self.data,
            numero_ora_predefinita=self.ora_predefinita,
            ora_inizio=self.ora_inizio,
            ora_fine=self.ora_fine,
            note=self.note,
        )

        self.id = id

    @beartype
    def modifica(self, dati: Dict):
        if not self.id:
            return False

        if "pubblicato" in dati:
            self.pubblicato = dati["pubblicato"]

        if "aula" in dati:
            self.aula = dati["aula"]

        if "classe" in dati:
            self.classe = dati["classe"]

        if "docente" in dati:
            self.docente = dati["docente"]

        if "data" in dati:
            self.data = dati["data"]

        if "ora_predefinita" in dati:
            self.ora_predefinita = dati["ora_predefinita"]

        if "ora_inizio" in dati:
            self.ora_inizio = dati["ora_inizio"]

        if "ora_fine" in dati:
            self.ora_fine = dati["ora_fine"]

        if "note" in dati:
            self.note = dati["note"]

        return self.aggiorna()

    def aggiorna(self):
        """Update the database record with the object's new data."""
        return self.DATABASE.update(
            self.TABLENAME,
            Where("id").equals(self.id),
            pubblicato=self.pubblicato,
            numero_aula=self.numero_aula,
            nome_classe=self.nome_classe,
            nome_docente=self.nome_docente,
            cognome_docente=self.cognome_docente,
            data=self.data,
            numero_ora_predefinita=self.ora_predefinita,
            ora_inizio=self.ora_inizio,
            ora_fine=self.ora_fine,
            note=self.note,
        )

    # def elimina(self, mantieni_in_storico: bool):
    #     self.cancellato = True

    #     if not self.id:
    #         return False

    #     if mantieni_in_storico:
    #         return self.DATABASE.update(self.TABLENAME, Where('id').equals(self.id), cancellato=True)

    #     else:
    #         self.DATABASE.delete(self.TABLENAME, Where('id').equals(self.id))

    @property
    def id(self):
        return self._id

    @beartype
    @id.setter
    def id(self, new: int | str | None):
        self._id = None

        if isinstance(new, int):
            self._id = new
        elif isinstance(new, str) and new.isdecimal():
            self._id = int(new)

    @property
    def pubblicato(self):
        return self._pubblicato

    @beartype
    @pubblicato.setter
    def pubblicato(self, new: bool | int | None):
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
        self._numero_aula = None

        if not new:
            return

        if isinstance(new, Aula):
            self._aula = new
            self._numero_aula = new.numero
        elif isinstance(new, str):
            aula = Aula.trova(new)
            self._numero_aula = aula["numero"]

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
        self._nome_classe = None

        if not new:
            return

        if isinstance(new, Classe):
            self._classe = new
            self._nome_classe = new.nome
        elif isinstance(new, str):
            classe = Classe.trova(new)
            self._nome_classe = classe["nome"]

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

        if not new:
            return

        if isinstance(new, Docente):
            self._docente = new
            self._nome_docente = new.nome
            self._cognome_docente = new.cognome
        elif isinstance(new, str):
            docente = Docente.trova(new)
            if docente:
                self._nome_docente = docente["nome"]
                self._cognome_docente = docente["cognome"]
            else:
                self._nome_docente = None
                self._cognome_docente = None

    @property
    def data(self):
        return self._data

    @beartype
    @data.setter
    def data(self, new: int | str | None):
        self._data = None

        if not new:
            return

        if isinstance(new, int):
            self._data = new
        elif isinstance(new, str):
            self._data = int(datetime.strptime(new, "%Y-%m-%d").timestamp())

    @property
    def ora_inizio(self):
        return self._ora_inizio

    @beartype
    @ora_inizio.setter
    def ora_inizio(self, new: str | None):
        self._ora_inizio = None

        if not new:
            return

        if isinstance(new, str):
            if re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$", new):
                self._ora_inizio = new
            else:
                raise ValueError(
                    f"Ora_inizio {new} non valida, seguire il formato XX:XX"
                )

    @property
    def ora_fine(self):
        return self._ora_fine

    @beartype
    @ora_fine.setter
    def ora_fine(self, new: str | None):
        self._ora_fine = None

        if not new:
            return

        if isinstance(new, str):
            if re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$", new):
                self._ora_fine = new
            else:
                raise ValueError(f"Ora_fine {new} non valida, seguire il formato XX:XX")

    @property
    def ora_predefinita(self):
        return self._ora_predefinita

    @beartype
    @ora_predefinita.setter
    def ora_predefinita(self, new: str | None):
        self._ora_predefinita = None

        if not new:
            return

        # trasforma da "1a ora" a "1"
        if new.endswith("a ora"):
            new = new[0]

        self._ora_predefinita = new

    @property
    def note(self):
        return self._note

    @beartype
    @note.setter
    def note(self, new: str | None):
        self._note = new


class Evento(ElementoDatabaseConStorico):
    TABLENAME = "evento"
    KEY = "id"

    def load(filtri: Where | Dict | None = None):
        if filtri is None:
            # carica gli eventi futuri non cancellati

            # get todays timestamp at midnight
            today = datetime.today()
            today = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today = int(today.timestamp())

            where = (
                Where("data_ora_fine")
                .greaterthanorequal(today)
                .AND("cancellato")
                .equals(False)
            )

            return ElementoDatabase.load(
                Evento, where=where, order_by="data_ora_inizio"
            )

        if isinstance(filtri, Where):
            return ElementoDatabase.load(
                Evento, where=filtri, order_by="data_ora_inizio"
            )

        data_ora_inizio: int | None = filtri.get(
            "data_ora_inizio", int(datetime.today().timestamp())
        )  # default è oggi
        data_ora_fine: int | None = filtri.get(
            "data_fine", None
        )  # default è nessuna, quindi future

        if data_ora_inizio is None:
            data_ora_inizio = 0

        where = Where("data").greaterthanorequal(data_ora_inizio)

        if data_ora_fine is not None:
            where = where.AND("data").lessthanorequal(data_ora_fine)

        # Se è specificato di caricare anche i cancellati, non impostare un where aggiuntivo
        cancellato = filtri.get("cancellato", False)

        if not cancellato:
            where = where.AND("cancellato").equals(False)

        return ElementoDatabase.load(Evento, where=where, order_by="data")

    def inserisci(self):
        id = self.DATABASE.insert(
            self.TABLENAME,
            cancellato=False,
            urgente=self.urgente,
            data_ora_inizio=self.data_ora_inizio,
            data_ora_fine=self.data_ora_fine,
            testo=self.testo,
        )

        self.id = id

    @beartype
    def modifica(self, dati: Dict):
        if not self.id:
            return

        if "urgente" in dati:
            self.urgente = dati["urgente"]

        if "data_ora_inizio" in dati:
            self.data_ora_inizio = dati["data_ora_inizio"]

        if "data_ora_fine" in dati:
            self.data_ora_fine = dati["data_ora_fine"]

        if "testo" in dati:
            self.testo = dati["testo"]

        return self.aggiorna()

    def aggiorna(self):
        if not self.id:
            return

        return self.DATABASE.update(
            self.TABLENAME,
            Where("id").equals(self.id),
            urgente=self.urgente,
            data_ora_inizio=self.data_ora_inizio,
            data_ora_fine=self.data_ora_fine,
            testo=self.testo,
        )

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

    @property
    def id(self):
        return self._id

    @beartype
    @id.setter
    def id(self, new: int | str | None):
        self._id = None

        if isinstance(new, int):
            self._id = new
        elif isinstance(new, str) and new.isdecimal():
            self._id = int(new)

    @property
    def urgente(self):
        return self._urgente

    @beartype
    @urgente.setter
    def urgente(self, new: bool | None):
        self._urgente = new

    @property
    def data_ora_inizio(self):
        return self._data_ora_inizio

    @beartype
    @data_ora_inizio.setter
    def data_ora_inizio(self, new: int | None):
        self._data_ora_inizio = new

    @property
    def data_ora_fine(self):
        return self._data_ora_fine

    @beartype
    @data_ora_fine.setter
    def data_ora_fine(self, new: int | None):
        self._data_ora_fine = new

    @property
    def testo(self):
        return self._testo

    @beartype
    @testo.setter
    def testo(self, new: str | None):
        self._testo = new


class Notizia(ElementoDatabaseConStorico):
    TABLENAME = "notizia"
    KEY = "id"

    @beartype
    def load(filtri: Where | Dict | None = None):
        if filtri is None:
            # carica le notizie non cancellate comprese nell'intervallo di data

            # get todays timestamp
            today = int(datetime.today().timestamp())

            where = (
                Where("data_inizio")
                .lessthanorequal(today)
                .AND("data_fine")
                .greaterthanorequal(today)
                .AND("cancellato")
                .equals(False)
            )

            return ElementoDatabase.load(Notizia, where=where, order_by="data_inizio")

        if isinstance(filtri, Where):
            return ElementoDatabase.load(Notizia, where=filtri, order_by="data_inizio")

        # todo completare, decidere come far filtrare notizie, se per data o aggiungere un pulsante "tutte" boh
        logger.warning(
            "Notizia.load(filtri) non ancora implementato, questo non sarebbe dovuto succedere"
        )
        return ElementoDatabase.load(Notizia, order_by="data_inizio")

    def inserisci(self):
        id = self.DATABASE.insert(
            self.TABLENAME,
            cancellato=False,
            data_inizio=self.data_inizio,
            data_fine=self.data_fine,
            testo=self.testo,
        )

        self.id = id

    def modifica(self, dati: Dict):
        if not self.id:
            return

        if "data_inizio" in dati:
            self.data_inizio = dati["data_inizio"]

        if "data_fine" in dati:
            self.data_fine = dati["data_fine"]

        if "testo" in dati:
            self.testo = dati["testo"]

        return self.aggiorna()

    def aggiorna(self):
        if not self.id:
            return

        return self.DATABASE.update(
            self.TABLENAME,
            Where("id").equals(self.id),
            data_inizio=self.data_inizio,
            data_fine=self.data_fine,
            testo=self.testo,
        )

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
    #     self.data_inizio = (data_inizio,)
    #     self.data_fine = data_fine

    @property
    def id(self):
        return self._id

    @beartype
    @id.setter
    def id(self, new: int | str | None):
        self._id = None

        if isinstance(new, int):
            self._id = new
        elif isinstance(new, str) and new.isdecimal():
            self._id = int(new)

    @property
    def data_inizio(self):
        return self._data_inizio

    @beartype
    @data_inizio.setter
    def data_inizio(self, new: int | None):
        self._data_inizio = new

    @property
    def data_fine(self):
        return self._data_fine

    @beartype
    @data_fine.setter
    def data_fine(self, new: int | None):
        self._data_fine = new

    @property
    def testo(self):
        return self._testo

    @beartype
    @testo.setter
    def testo(self, new: str | None):
        self._testo = new


class Visualizzazione(ElementoDatabase):
    TABLENAME = "visualizzazione"
    KEY = "id"

    def load():
        return ElementoDatabase.load(Visualizzazione)

    @beartype
    def __init__(self):
        super(Visualizzazione, self).__init__()


# --------------------


class Ruolo(ElementoDatabase):
    DATABASE = authdatabase
    TABLENAME = "ruolo"
    KEY = "nome"

    def load(*args, **kwargs):
        return ElementoDatabase.load(Ruolo, *args, **kwargs)

    def __init__(self, nome: str):
        self.nome = nome
        self.nomi_permesso = []

        class permessi:
            class notizie:
                read = False
                write = False

            class eventi:
                read = False
                write = False

            class sostituzioni:
                read = False
                write = False

            class impostazioni:
                write = False

        self.permessi = permessi()

        for relazione in self.DATABASE.get("permesso_per_ruolo"):
            if relazione["nome_ruolo"] == self.nome:
                self.nomi_permesso.append(relazione["permesso_ruolo"])

                permesso, livello = relazione["permesso_ruolo"].split(".")
                setattr(getattr(self.permessi, permesso), livello, True)


class Utente(ElementoDatabase):
    DATABASE = authdatabase
    TABLENAME = "utente"
    KEY = "email"

    def load(*args, **kwargs):
        return ElementoDatabase.load(Utente, *args, **kwargs)

    def inserisci(self):
        id = self.DATABASE.insert(
            self.TABLENAME, email=self.email, ruolo=self.ruolo.nome, or_ignore=True
        )

        self.id = id

    @beartype
    def __init__(self, email: str, ruolo: Ruolo | str):
        super(Utente, self).__init__()

        if isinstance(ruolo, str):
            ruolo = Ruolo(ruolo)

        self.email = email
        self.ruolo = ruolo

    @property
    def email(self):
        return self._email

    @beartype
    @email.setter
    def email(self, new: str):
        self._email = new

    @property
    def ruolo(self):
        return self._ruolo

    @beartype
    @ruolo.setter
    def ruolo(self, new: Ruolo):
        self._ruolo = new


# For efficiency purposes, handle users in memory
ruoli = SearchableList("nome", [Ruolo(r["nome"]) for r in Ruolo.load()])
utenti = SearchableList(
    "email", [Utente(u["email"], ruoli.get(u["ruolo"])) for u in Utente.load()]
)
# Visualizzazione fisica
utenti.append(Utente("display", "visualizzatore"))
