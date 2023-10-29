"""
database controller
"""

from beartype.typing import List, Dict
from beartype._decor.decormain import beartype
from datetime import date, datetime, time
import logging
import sqlite3

from sostituzioni.lib.searchablelist import SearchableList
from sostituzioni.logger import logger
from sostituzioni.control.configurazione import configurazione


class Database:
    def __init__(self):
        self.path = configurazione.get('databasepath').path
        self.connection = None

    def connect(self):
        if not self.connection:
            try:
                self.connection = sqlite3.connect(self.path)
                self.connection.execute('PRAGMA foreign_keys = 1')
                self.connection.row_factory = sqlite3.Row

                self.cursor = self.connection.cursor()
            except Exception as e:
                logger.error(e)

    def execute(self, sql):
        self.connect()
        self.cursor.execute(sql)

    def get_all_from(self, table: str) -> List[Dict]:
        self.execute('SELECT * FROM ' + table)

        return [dict(row) for row in self.cursor.fetchall()]

    def load_all(self):
        aule = SearchableList('numero')
        classi = SearchableList('nome')
        docenti = SearchableList()  # quale cazzo è l'id in questo caso??????? modifico per includere anche chiavi tuple????
        ore_predefinite = SearchableList()
        sostituzioni = SearchableList()
        eventi = SearchableList()
        notizie = SearchableList()
        visualizzazioni_online = SearchableList()
        visualizzazioni_fisiche = SearchableList()

        db_aule = database.get_all_from('aula')
        for db_aula in db_aule:
            aula = Aula(db_aula['numero'], db_aula['piano'], bool(db_aula['cancellato']))
            aule.append(aula)

        db_classi = database.get_all_from('classe')
        for db_classe in db_classi:
            # Istanziare con attributo aule_ospitanti vuoto, in quanto lo aggiungiamo in seguito
            classe = Classe(db_classe['nome'], [], bool(db_classe['cancellato']))
            classi.append(classe)

        db_aule_classi = database.get_all_from('aula_ospita_classe')
        for db_aula_classe in db_aule_classi:
            classi[db_aula_classe['nome_classe']].aule_ospitanti.append(db_aula_classe['numero_aula'])

        db_docenti = database.get_all_from('docente')
        for db_docente in db_docenti:
            docente = Docente(db_docente['nome'], db_docente['cognome'], bool(db_docente['cancellato']))
            docenti.append(docente)

        # db_ore_predefinite = database.get_all_from('ora_predefinita')
        # for db_ora_predefinita in db_ore_predefinite:
        #     ora_predefinita = OraPredefinita(db_ora_predefinita['numero'], db_ora_predefinita['ora_inizio'], db_ora_predefinita['ora_fine'])
        #     ore_predefinite.append(ora_predefinita)

        # db_sostituzioni = database.get_all_from('aula')
        # for db_aula in db_sostituzioni:
        #     aula = Aula(db_aula['numero'], db_aula['piano'], bool(db_aula['cancellato']))
        #     sostituzioni.append(aula)

        return aule, classi, docenti, ore_predefinite, sostituzioni, eventi, notizie, visualizzazioni_online, visualizzazioni_fisiche


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
            logging.warning('Nessun parametro passato ad aula.modifica')
            return

        if numero:
            self.numero = numero

        if piano:
            self.piano = piano

    @property
    def numero(self):
        print('get numero')
        return self._numero

    @beartype
    @numero.setter
    def numero(self, new: str):
        print('set numero')
        self._numero = new

    @property
    def piano(self):
        return self._piano

    @beartype
    @piano.setter
    def piano(self, new: str):
        self._piano = new


class Classe(ElementoDatabaseConStorico):
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


database = Database()
