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

import re
import logging
import sqlite3
from os import environ
from datetime import datetime
from beartype import beartype
from beartype.typing import Any

from sostituzioni.lib.searchablelist import SearchableList
from sostituzioni.control.configurazione import configurazione

logger = logging.getLogger(__name__)


class Where:
    def __init__(self, attribute: str, parent=None) -> None:
        self.attribute: str = attribute
        self.operator: str = "="
        self.value: any = None
        self.value_is_list: bool = False
        self.parent: Where | None = parent

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

        query_marks = "?"
        if self.value_is_list:
            query_marks = "(" + ", ".join("?" for _ in self.value) + ")"

        resolved = str(self.attribute) + self.operator + query_marks

        if isinstance(self.parent, Where):
            where, values = self.parent.resolve()
            resolved = where + " AND " + resolved
            if self.value_is_list:
                values += self.value
            else:
                values.append(self.value)
        else:
            if self.value_is_list:
                values = self.value
            else:
                values = [self.value]

        return resolved, values

    @beartype
    def equals(self, value: Any):
        self.operator = "="
        self.value = value
        return self

    @beartype
    def notequals(self, value: Any):
        self.operator = "!="
        self.value = value
        return self

    @beartype
    def lessthan(self, value: int | float):
        self.operator = "<"
        self.value = value
        return self

    @beartype
    def lessthanorequal(self, value: int | float):
        self.operator = "<="
        self.value = value
        return self

    @beartype
    def greaterthan(self, value: int | float):
        self.operator = ">"
        self.value = value
        return self

    @beartype
    def greaterthanorequal(self, value: int | float):
        self.operator = ">="
        self.value = value
        return self

    @beartype
    def LIKE(self, value: str):
        self.operator = " LIKE "
        self.value = value
        return self

    @beartype
    def NOTLIKE(self, value: str):
        self.operator = " NOT LIKE "
        self.value = value

    @beartype
    def IN(self, value: list | tuple):
        self.operator = " IN "
        self.value = value
        self.value_is_list = True
        return self

    @beartype
    def NOTIN(self, value: list | tuple):
        self.operator = " NOT IN "
        self.value = value
        self.value_is_list = True
        return self

    @beartype
    def AND(self, attribute: str):
        return Where(attribute, self)


class Database:
    def __init__(self, path):
        self.path = path
        self.connection = None

    def connect(self):
        if not self.connection:
            # logger.debug("Trying to open database connection...")
            try:
                self.connection = sqlite3.connect(
                    self.path
                )  # check_same_thread=False ?
                # logger.debug("Database connection established.")
                # self.connection.execute("PRAGMA foreign_keys = 1")
                self.connection.row_factory = sqlite3.Row

                self.cursor = self.connection.cursor()
                # logger.debug("Database cursor created.")
            except sqlite3.Error as e:
                logger.error(e)
                raise e

    def close(self):
        # logger.debug("Closing connection to database...")
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.connection = None
        # logger.debug("Connection to database closed successfully")

    @beartype
    def execute(self, query: str, values: Any | None = None):
        logger.debug("Executing query " + query + " - " + str(values))
        try:
            if values is not None:
                self.cursor.execute(query, list(values))
                self.connection.commit()
            else:
                self.cursor.execute(query)
        except sqlite3.Error as e:
            self.connection.rollback()
            logger.error(e)
            raise e

    @beartype
    def get(
        self,
        table: str,
        columns: str | tuple = "*",
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

    @beartype
    def get_one(
        self,
        table: str,
        columns: str | tuple = "*",
        where: Where | None = None,
        load_lists: bool = True,
    ) -> dict | None:
        data = self.get(table, columns, where, None, 1, load_lists)

        if len(data) > 0:
            return data[0]
        return None

    @beartype
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

                    if not isinstance(aule, list):
                        classe["aule_ospitanti"].append(aule["numero_aula"])

                    else:
                        for aula in aule:
                            classe["aule_ospitanti"].append(aula["numero_aula"])
                            if aula["predefinito"]:
                                # L'aula predefinita è il primo elemento della lista.
                                # L'inserimento automatico del frontend selezionerà questo elemento
                                classe["aule_ospitanti"].insert(
                                    0, classe["aule_ospitanti"].pop()
                                )

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


databasepath = configurazione.get("databasepath").path

if "SCUOLASYNC_SETUP" in environ:
    from sostituzioni.control.cli import crea_db

    if not databasepath.exists():
        crea_db()

else:
    if not databasepath.exists():
        raise FileNotFoundError(f"Database {databasepath} non trovato.")


database = Database(databasepath)


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

    @staticmethod
    @beartype
    def load(
        item,
        columns: str | tuple = "*",
        where: Where | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ):
        data = item.DATABASE.get(item.TABLENAME, columns, where, order_by, limit)
        data.key = item.KEY

        return data

    def elimina(self):
        self.DATABASE.delete(self.TABLENAME, Where(self.KEY).equals(self.id))

    @staticmethod
    @beartype
    def trova(item, value: Any = None, where: Where | None = None):
        """
        Funzione usata nell'inserimento di dati per verificare che
        l'elemento esiste nella relativa tabella, caricandone la chiave.
        Esempio di uso è il cercare per docente, una singola stringa con
        cognome in maiuscolo, ed ottenere l'effettiva chiave (nome, cognome).
        """
        where = where or Where(item.KEY).equals(value)
        return item.DATABASE.get_one(
            item.TABLENAME,
            item.KEY,
            where=where,
            load_lists=False,
        )


class ElementoDatabaseConStorico(ElementoDatabase):
    def __init__(self, cancellato: bool = False):
        self._cancellato = cancellato

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

    @beartype
    def elimina_tutti(self, mantieni_in_storico: bool = True):
        if mantieni_in_storico:
            self.DATABASE.update(
                self.TABLENAME,
                Where("cancellato").equals(False),
                cancellato=True,
            )

        else:
            self.DATABASE.delete(self.TABLENAME, Where("cancellato").equals(False))

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

    @staticmethod
    def load(filtri: Where | dict | None = None):
        where = None

        if isinstance(filtri, Where):
            where = filtri

        elif isinstance(filtri, dict):
            numero = filtri.get("numero", None)
            piano = filtri.get("piano", None)
            cancellato = filtri.get("cancellato", False)

            if numero:
                where = Where("numero").equals(numero)

            if piano:
                if where:
                    where = where.AND("piano").equals(piano)
                else:
                    where = Where("piano").equals(piano)

            # L'attributo cancellato è usato per visualizzare anche i cancellati
            # Se non viene specificato, vengono caricati solo i non cancellati
            if not cancellato:
                if where:
                    where = where.AND("cancellato").equals(False)
                else:
                    where = Where("cancellato").equals(False)

        else:
            # default sono le aule non cancellate

            where = Where("cancellato").equals(False)

        return ElementoDatabase.load(Aula, where=where, order_by="numero")

    @staticmethod
    @beartype
    def trova(numero: str):
        return ElementoDatabase.trova(Aula, numero)

    def inserisci(self):
        return self.DATABASE.insert(
            self.TABLENAME,
            numero=self.numero,
            piano=self.piano,
            cancellato=self.cancellato,
        )

    @beartype
    def modifica(self, dati: dict):
        old_numero = self.numero

        if "numero" in dati:
            self.numero = dati["numero"]

        if "piano" in dati:
            self.piano = dati["piano"]

        return self.DATABASE.update(
            self.TABLENAME,
            Where("numero").equals(old_numero),
            numero=self.numero,
            piano=self.piano,
        )

    def aggiorna(self):
        return self.DATABASE.update(
            self.TABLENAME,
            Where("numero").equals(self.numero),
            numero=self.numero,
            piano=self.piano,
            cancellato=self.cancellato,
        )

    @beartype
    def elimina(self, mantieni_in_storico: bool = False):
        self.cancellato = True

        if mantieni_in_storico:
            return self.DATABASE.update(
                self.TABLENAME,
                Where("numero").equals(self.numero),
                cancellato=True,
            )

        else:
            self.DATABASE.delete(
                self.TABLENAME,
                Where("numero").equals(self.numero),
            )

    def __repr__(self) -> str:
        return "Aula " + self.numero

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

    @staticmethod
    @beartype
    def load(filtri: Where | dict | None = None):
        where = None

        if isinstance(filtri, Where):
            where = filtri

        elif isinstance(filtri, dict):
            nome = filtri.get("nome", None)
            cancellato = filtri.get("cancellato", False)

            if nome:
                where = Where("nome").equals(nome)

            if not cancellato:
                if where:
                    where = where.AND("cancellato").equals(False)
                else:
                    where = Where("cancellato").equals(False)

        else:
            # default sono le classi non cancellate
            where = Where("cancellato").equals(False)

        return ElementoDatabase.load(Classe, where=where, order_by="nome")

    @beartype
    def trova(nome: str):
        return ElementoDatabase.trova(Classe, nome)

    def inserisci(self):
        self.DATABASE.insert(
            self.TABLENAME,
            nome=self.nome,
            cancellato=self.cancellato,
        )

        if self.aule_ospitanti:
            for i in range(len(self.aule_ospitanti)):
                self.DATABASE.insert(
                    "aula_ospita_classe",
                    numero_aula=self.aule_ospitanti[i],
                    nome_classe=self.nome,
                    predefinito=(i == 0),
                )

        return True

    @beartype
    def modifica(self, dati: dict):
        old_nome = self.nome

        if "nome" in dati:
            self.nome = dati["nome"]

        if "aule_ospitanti" in dati:
            self.aule_ospitanti = dati["aule_ospitanti"]

        self.DATABASE.update(
            self.TABLENAME, Where("nome").equals(old_nome), nome=self.nome
        )
        self.DATABASE.delete(
            "aula_ospita_classe", Where("nome_classe").equals(old_nome)
        )
        for i in range(len(self.aule_ospitanti)):
            self.DATABASE.insert(
                "aula_ospita_classe",
                numero_aula=self.aule_ospitanti[i],
                nome_classe=self.nome,
                predefinito=(i == 0),
            )

        return True

    @beartype
    def elimina(self, mantieni_in_storico: bool = False):
        self.cancellato = True

        if mantieni_in_storico:
            self.DATABASE.update(
                self.TABLENAME, Where("nome").equals(self.nome), cancellato=True
            )
            self.DATABASE.delete(
                "aula_ospita_classe", Where("nome_classe").equals(self.nome)
            )

        else:
            self.DATABASE.delete(self.TABLENAME, Where("nome").equals(self.nome))
            self.DATABASE.delete(
                "aula_ospita_classe", Where("nome_classe").equals(self.nome)
            )

        return True

    @property
    def nome(self):
        return self._nome

    @beartype
    @nome.setter
    def nome(self, new: str):
        self._nome = new

    @property
    def aule_ospitanti(self):
        return self._aule_ospitanti

    @beartype
    @aule_ospitanti.setter
    def aule_ospitanti(self, new: list):
        self._aule_ospitanti = new


class Docente(ElementoDatabaseConStorico):
    TABLENAME = "docente"
    KEY = ("nome", "cognome")

    @staticmethod
    @beartype
    def load(filtri: Where | dict | None = None):
        where = None

        if isinstance(filtri, Where):
            where = filtri

        elif isinstance(filtri, dict):
            nome = filtri.get("nome", None)
            cognome = filtri.get("cognome", None)
            cancellato = filtri.get("cancellato", False)

            if nome:
                where = Where("nome").equals(nome)

            if cognome:
                if where:
                    where = where.AND("cognome").equals(cognome)
                else:
                    where = Where("cognome").equals(cognome)

            # L'attributo cancellato è usato solo per visualizzare solo anche i docenti cancellati
            # Se non viene specificato, vengono caricati solo i docenti non cancellati
            if not cancellato:
                if where:
                    where = where.AND("cancellato").equals(False)
                else:
                    where = Where("cancellato").equals(False)

        else:
            # default sono i docenti non cancellati
            where = Where("cancellato").equals(False)

        return ElementoDatabase.load(Docente, where=where)

    @staticmethod
    @beartype
    def trova(cognome_nome: str):
        return ElementoDatabase.trova(
            Docente,
            cognome_nome,
            where=Where("(cognome || ' ' || nome)").LIKE(cognome_nome.lower()),
        )

    def inserisci(self):
        return self.DATABASE.insert(
            self.TABLENAME,
            nome=self.nome,
            cognome=self.cognome,
            cancellato=self.cancellato,
        )

    @beartype
    def modifica(self, dati: dict):
        # todo: terribile, utilizzare id per docenti
        old_nome = self.nome
        old_cognome = self.cognome

        if "nome" in dati:
            self.nome = dati["nome"]

        if "cognome" in dati:
            self.cognome = dati["cognome"]

        return self.DATABASE.update(
            self.TABLENAME,
            Where("nome").equals(old_nome).AND("cognome").equals(old_cognome),
            nome=self.nome,
            cognome=self.cognome,
            cancellato=self.cancellato,
        )

    @beartype
    def aggiorna(self):
        return self.DATABASE.update(
            self.TABLENAME,
            Where("nome").equals(self.nome).AND("cognome").equals(self.cognome),
            nome=self.nome,
            cognome=self.cognome,
            cancellato=self.cancellato,
        )

    @beartype
    def elimina(self, mantieni_in_storico: bool = False):
        self.cancellato = True

        if mantieni_in_storico:
            return self.DATABASE.update(
                self.TABLENAME,
                Where("nome").equals(self.nome).AND("cognome").equals(self.cognome),
                cancellato=True,
            )

        else:
            self.DATABASE.delete(
                self.TABLENAME,
                Where("nome").equals(self.nome).AND("cognome").equals(self.cognome),
            )

    @staticmethod
    @beartype
    def elimina_tutti():
        Docente.DATABASE.delete(Docente.TABLENAME, Where("cancellato").equals(False))

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

    @staticmethod
    def load(filtri: Where | dict | None = None):
        where = None

        if isinstance(filtri, Where):
            where = filtri

        elif isinstance(filtri, dict):
            numero = filtri.get("numero", None)
            ora_inizio = filtri.get("ora_inizio", None)
            ora_fine = filtri.get("ora_fine", None)

            if numero:
                where = Where("numero").equals(numero)

            if ora_inizio:
                if where:
                    where = where.AND("ora_inizio_default").equals(ora_inizio)
                else:
                    where = Where("ora_inizio_default").equals(ora_inizio)

            if ora_fine:
                if where:
                    where = where.AND("ora_fine_default").equals(ora_fine)
                else:
                    where = Where("ora_fine_default").equals(ora_fine)

        # Default: nessun filtro

        return ElementoDatabase.load(
            OraPredefinita, where=where, order_by="ora_inizio_default"
        )

    @beartype
    def trova(numero: str):
        return ElementoDatabase.trova(OraPredefinita, numero)

    @beartype
    def inserisci(self):
        return self.DATABASE.insert(
            self.TABLENAME,
            numero=self.numero,
            ora_inizio_default=self.ora_inizio,
            ora_fine_default=self.ora_fine,
        )

    @beartype
    def modifica(self, dati: dict):
        old_numero = self.numero

        if "numero" in dati:
            self.numero = dati["numero"]

        if "ora_inizio" in dati:
            self.ora_inizio = dati["ora_inizio"]

        if "ora_fine" in dati:
            self.ora_fine = dati["ora_fine"]

        return self.DATABASE.update(
            self.TABLENAME,
            Where("numero").equals(old_numero),
            numero=self.numero,
            ora_inizio_default=self.ora_inizio,
            ora_fine_default=self.ora_fine,
        )

    def elimina(self):
        self.DATABASE.delete(self.TABLENAME, Where("numero").equals(self.numero))

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


class NotaStandard(ElementoDatabaseConStorico):
    TABLENAME = "nota_standard"
    KEY = "testo"

    @staticmethod
    def load(filtri: Where | dict | None = None):
        where = None

        if isinstance(filtri, Where):
            where = filtri

        elif isinstance(filtri, dict):
            testo: str = filtri.get("testo", None)

            if testo:
                where = Where("testo").equals(testo)

        return ElementoDatabase.load(NotaStandard, where=where)

    @staticmethod
    def trova(testo: str):
        return ElementoDatabase.trova(NotaStandard, testo)

    def __repr__(self) -> str:
        return "Nota standard " + self.testo

    def inserisci(self):
        return self.DATABASE.insert(
            self.TABLENAME,
            testo=self.testo,
        )

    def modifica(self, dati: dict):
        # todo: stessa roba qui, terribile. usare id.
        old_testo = self.testo
        if "testo" in dati:
            self.testo = dati["testo"]

        return self.DATABASE.update(
            self.TABLENAME,
            Where("testo").equals(old_testo),
            testo=self.testo,
        )

    def elimina(self):
        self.DATABASE.delete(self.TABLENAME, Where("testo").equals(self.testo))

    @property
    def testo(self):
        return self._testo

    @beartype
    @testo.setter
    def testo(self, new: str):
        self._testo = new


class Sostituzione(ElementoDatabaseConStorico):
    TABLENAME = "sostituzione"
    KEY = "id"

    @beartype
    def __init__(
        self,
        # id: int,
        # aula: Aula | None = None,
        # classe: Classe | None = None,
        # docente: Docente | None = None,
        # data: int | None = None,
        # ora_inizio: str | None = None,
        # ora_fine: str | None = None,
        # ora_predefinita: OraPredefinita | None = None,
        # note: str | None = None,
        # pubblicato: bool = False,
    ):
        super(Sostituzione, self).__init__()
        """
        Questa classe rappresenta una sostituzione esistente nel database.
        Nota per futuro nico: non serve letteralmente mai utilizzare questa classe.
        I dati vengono caricati nella classe del model

        Se viene passato solamente l'id, i dati verranno caricati dal database.
        Se vengono passati anche tutti i dati,
        """

        # dati = None
        # if dati is None:
        #     # Carica i dati da database
        #     dati = self.DATABASE.get_one(
        #         self.TABLENAME, "*", where=Where("id").equals(id)
        #     )

        #     # Id della sostituzione non esiste nel database
        #     if dati is None:
        #         raise ValueError(f"Sostituzione con id {id} non trovata")

        # # Controlla che i dati inseriti siano validi
        # if not all(
        #     [
        #         attr in dati
        #         for attr in [
        #             "cancellato",
        #             "pubblicato",
        #             "numero_aula",
        #             "nome_classe",
        #             "nome_docente",
        #             "cognome_docente",
        #             "data",
        #             "ora_predefinita",
        #             "ora_inizio",
        #             "ora_fine",
        #             "note",
        #         ]
        #     ]
        # ):
        #     raise ValueError(
        #         f"Sostituzione con id {id} non valida. Dati inseriti: {dati}"
        #     )

        # self.id = id
        # self.cancellato = dati["cancellato"]
        # self.pubblicato = dati["pubblicato"]
        # self.numero_aula = dati["numero_aula"]
        # self.nome_classe = dati["nome_classe"]
        # self.nome_docente = dati["nome_docente"]
        # self.cognome_docente = dati["cognome_docente"]
        # self.data = dati["data"]
        # self.ora_predefinita = dati["ora_predefinita"]
        # self.ora_inizio = dati["ora_inizio"]
        # self.ora_fine = dati["ora_fine"]
        # self.note = dati["note"]

    @staticmethod
    @beartype
    def load(filtri: Where | dict | None = None):
        if isinstance(filtri, Where):
            where = filtri

        elif isinstance(filtri, dict):
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
            pubblicato = filtri.get("non_pubblicato", False)
            if not pubblicato:
                where = where.AND("pubblicato").equals(True)

        else:
            # default sono le sostituzioni future

            # timestap della mezzanotte passata
            today = datetime.today()
            today = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today = int(today.timestamp())

            # Sostituzioni future pubblicate (visualizzazione di un docente)
            where = (
                Where("data")
                .greaterthanorequal(today)
                .AND("cancellato")
                .equals(False)
                .AND("pubblicato")
                .equals(True)
            )

        # Carica le sostituzioni dal database
        sostituzioni = ElementoDatabase.load(Sostituzione, where=where, order_by="data")

        # Modifica nome attributo perché sono stupido e mi piace crearmi problemi
        # numero_ora_predefinita viene usato nel database
        # ora_predefinita viene usato sia nel server che in frontend
        for sostituzione in sostituzioni:
            sostituzione["ora_predefinita"] = sostituzione.pop("numero_ora_predefinita")

        return sostituzioni

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
    def modifica(self, dati: dict):
        if not self.id:
            return False

        if "pubblicato" in dati:
            self.pubblicato = dati["pubblicato"]

        if "numero_aula" in dati:
            self.numero_aula = dati["numero_aula"]

        if "nome_classe" in dati:
            self.nome_classe = dati["nome_classe"]

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

        if not new:
            self._numero_aula = None

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

        if not new:
            self._nome_classe = None

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
        self._note = new if new else None


class Evento(ElementoDatabaseConStorico):
    TABLENAME = "evento"
    KEY = "id"

    @staticmethod
    @beartype
    def load(filtri: Where | dict | None = None):
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

        # filtri: dict

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
    def modifica(self, dati: dict):
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

    @staticmethod
    @beartype
    def load(filtri: Where | dict | None = None):
        if filtri is None:
            # carica le notizie non cancellate comprese nell'intervallo di data

            # get todays timestamp
            today = int(
                datetime.today()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )

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

        # filtri: dict
        solo_attivo = filtri.get("solo_attivo", True)
        cancellato = filtri.get("cancellato", False)

        today = int(
            datetime.today()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        )

        if solo_attivo:
            where = (
                Where("data_inizio")
                .lessthanorequal(today)
                .AND("data_fine")
                .greaterthanorequal(today)
            )
        else:
            where = Where("data_fine").greaterthanorequal(today)

        if not cancellato:
            where = where.AND("cancellato").equals(False)

        return ElementoDatabase.load(Notizia, where=where, order_by="data_inizio")

    def inserisci(self):
        id = self.DATABASE.insert(
            self.TABLENAME,
            cancellato=False,
            data_inizio=self.data_inizio,
            data_fine=self.data_fine,
            testo=self.testo,
        )

        self.id = id

    @beartype
    def modifica(self, dati: dict):
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


class Ruolo(ElementoDatabase):
    DATABASE = database
    TABLENAME = "ruolo"
    KEY = "nome"

    @staticmethod
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
    DATABASE = database
    TABLENAME = "utente"
    KEY = "email"

    def load(*args, **kwargs):
        return ElementoDatabase.load(Utente, *args, **kwargs)

    @beartype
    def elimina_tutti(users_to_keep: list | None = None):
        return Utente.DATABASE.delete(
            Utente.TABLENAME,
            Where("email").NOTIN(users_to_keep),
        )

    def elimina(self):
        return self.DATABASE.delete(self.TABLENAME, Where("email").equals(self.email))

    def inserisci(self):
        self.DATABASE.insert(
            self.TABLENAME, email=self.email, ruolo=self.ruolo.nome, or_ignore=True
        )

        return self.email

    @beartype
    def modifica(self, dati: dict):
        old_email = self.email

        if "email" in dati:
            self.email = dati["email"]

        if "ruolo" in dati:
            self.ruolo = dati["ruolo"]

        return self.DATABASE.update(
            self.TABLENAME,
            Where("email").equals(old_email),
            email=self.email,
            ruolo=self.ruolo.nome,
        )

    def aggiorna(self):
        if not self.email:
            return

        return self.DATABASE.update(
            self.TABLENAME,
            Where("email").equals(self.email),
            email=self.email,
            ruolo=self.ruolo.nome,
        )

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
    def ruolo(self, new: Ruolo | str):
        if isinstance(new, str):
            new = Ruolo(new)
        self._ruolo = new
