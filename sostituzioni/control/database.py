"""
database controller
"""

from beartype.typing import List
from beartype._decor.decormain import beartype
from datetime import date, datetime, time
import logging
import sqlite3

from sostituzioni.control.configurazione import configurazione


class Database:
    def __init__(self):
        self.path = configurazione.get('databasepath').path

    def connect(self):
        self.con = sqlite3.connect(self.path)

    def crea_database(self):
        pass


# -----------------------------------------------


class ElementoDatabase():
    def __init__(self):
        super().__init__()

    def modifica(self):
        pass

    def salva(self):
        pass


class ElementoConStorico(ElementoDatabase):
    def __init__(self):
        self._cancellato = False

        self.elimina = self.cancella = self.__del__

    def __del__(self, mantieni_in_storico: bool = True):
        self._cancellato = True

    @property
    def cancellato(self):
        return self._cancellato


# -----------------------------------------------


class Aula(ElementoDatabase, ElementoConStorico):
    @beartype
    def __init__(self, numero: str, piano: str):
        ElementoDatabase.__init__(self)
        ElementoConStorico.__init__(self)

        self.numero = numero
        self.piano = piano

    @beartype
    def modifica(self, numero: str | None = None, piano: str | None = None):
        if not any((numero, piano)):
            logging.debug('Nessun parametro passato ad aula.modifica, ')
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


class Classe(ElementoDatabase, ElementoConStorico):
    @beartype
    def __init__(self, nome: str, aule_ospitanti: List[Aula]):
        ElementoDatabase.__init__(self)
        ElementoConStorico.__init__(self)

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


class Docente(ElementoDatabase, ElementoConStorico):
    @beartype
    def __init__(self, nome: str, cognome: str):
        ElementoDatabase.__init__(self)
        ElementoConStorico.__init__(self)

        self.nome = nome
        self.cognome = cognome

    @property
    def nome(self):
        return self._nome

    @beartype
    @nome.setter
    def nome(self, new):
        self._nome = new

    @property
    def cognome(self):
        return self._cognome

    @beartype
    @cognome.setter
    def cognome(self, new):
        self._cognome = new


class OraPredefinita(ElementoDatabase):
    @beartype
    def __init__(self, numero: int, ora_inizio: time, ora_fine: time):
        ElementoDatabase.__init__(self)

        self.numero = numero
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine

    @property
    def ora_inizio(self):
        return self._ora_inizio

    @beartype
    @ora_inizio.setter
    def ora_inizio(self, new):
        self._ora_inizio = new

    @property
    def nome(self):
        return self._nome

    @beartype
    @nome.setter
    def nome(self, new):
        self._nome = new


class Sostituzione(ElementoDatabase, ElementoConStorico):
    @beartype
    def __init__(
        self,
        id: int,
        aula: Aula,
        classe: Classe,
        docente: Docente | None = None,
        data: date | None = None,
        ora_inizio: time | None = None,
        ora_fine: time | None = None,
        ora_predefinita: OraPredefinita | None = None,
        note: str | None = None,
        pubblicato: bool = False,
    ):
        ElementoDatabase.__init__(self)
        ElementoConStorico.__init__(self)

        self._id = id
        self.aula = aula
        self.classe = classe
        self.docente = docente
        self.data = data
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine
        self.ora_predefinita = ora_predefinita
        self.note = note
        self.pubblicato = pubblicato


class Evento(ElementoDatabase, ElementoConStorico):
    @beartype
    def __init__(
        self,
        id: int,
        testo: str,
        data_ora_inizio: datetime | None = None,
        data_ora_fine: datetime | None = None,
        urgente: bool = False,
    ):
        ElementoDatabase.__init__(self)
        ElementoConStorico.__init__(self)

        self._id = id
        self.testo = testo
        self.data_ora_inizio = data_ora_inizio
        self.data_ora_fine = data_ora_fine
        self.urgente = urgente


class Notizia(ElementoDatabase, ElementoConStorico):
    @beartype
    def __init__(
        self,
        id: int,
        testo: str,
        data_ora_inizio: datetime | None = None,
        data_ora_fine: datetime | None = None,
    ):
        ElementoDatabase.__init__(self)
        ElementoConStorico.__init__(self)

        self._id = id
        self.testo = testo
        self.data_ora_inizio = (data_ora_inizio,)
        self.data_ora_fine = data_ora_fine


class Visualizzazione(ElementoDatabase):
    @beartype
    def __init__(self):
        ElementoDatabase.__init__(self)


class VisualizzazioneOnline(Visualizzazione):
    @beartype
    def __init__(self):
        ElementoDatabase.__init__(self)


class VisualizzazioneFisica(Visualizzazione):
    @beartype
    def __init__(self):
        ElementoDatabase.__init__(self)


database = Database()
