"""
descr
"""

from beartype._decor.decormain import beartype
from beartype.typing import Tuple

from sostituzioni.lib.searchablelist import SearchableList
from sostituzioni.control.database import (
    Aula,
    Classe,
    Docente,
    OraPredefinita,
    NotaStandard,
    Sostituzione,
    Evento,
    Notizia,
    Visualizzazione,
    Utente,
    Ruolo,
)


class Docente(Docente):
    def __init__(
        self,
        nome: str | None = None,
        cognome: str | None = None,
        cancellato: bool = False,
    ):
        self.nome = nome
        self.nome = nome
        self.cognome = cognome
        self.cancellato = cancellato


class Sostituzione(Sostituzione):
    def __init__(
        self,
        id: int | None = None,
        aula: Aula | None = None,
        classe: Classe | None = None,
        docente: Docente | None = None,
        data: int | None = None,
        ora_inizio: str | None = None,
        ora_fine: str | None = None,
        ora_predefinita: OraPredefinita | None = None,
        note: str | None = None,
        pubblicato: bool = False,
    ):
        if id is not None:
            super().__init__(id)
        else:
            self.aula = aula
            self.classe = classe
            self.docente = docente
            self.data = data
            self.ora_inizio = ora_inizio
            self.ora_fine = ora_fine
            self.ora_predefinita = ora_predefinita
            self.note = note
            self.pubblicato = pubblicato


class Evento(Evento):
    def __init__(
        self,
        id: int | None = None,
        urgente: bool | None = None,
        data_ora_inizio: int | None = None,
        data_ora_fine: int | None = None,
        testo: str | None = None,
    ):
        self.id = id
        self.urgente = urgente
        self.data_ora_inizio = data_ora_inizio
        self.data_ora_fine = data_ora_fine
        self.testo = testo


class Notizia(Notizia):
    def __init__(
        self,
        id: int | None = None,
        data_inizio: int | None = None,
        data_fine: int | None = None,
        testo: str | None = None,
    ):
        self.id = id
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.testo = testo


# class VisualizzazioneOnline(Visualizzazione):
#     def __init__(self):
#         pass


# class VisualizzazioneFisica(Visualizzazione):
#     def __init__(self):
#         pass


# //////////////////////////////////


class Sostituzioni(SearchableList):
    def __init__(self):
        super().__init__(key_name="id")

    def filtra(filtri: dict):
        pass

    def add(sostituzione: Sostituzione):
        pass

    def check_errors():
        pass


sostituzioni = Sostituzioni()
