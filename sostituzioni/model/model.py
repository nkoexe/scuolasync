#!/usr/bin/env python

"""
descr
"""

from typing import List
from datetime import _Time as Time, _Date as Date, datetime


class Aula:
    def __init__(self, numero: str, piano: int):
        self._numero = numero
        self._piano  = piano


class Classe:
    def __init__(self, nome: str, aule_ospitanti: List[Aula]):
        self._nome = nome
        self._aule_ospitanti = aule_ospitanti
        self._cancellato = False


class Docente:
    def __init__(self, nome: str, cognome: str):
        self._nome = nome
        self._cognome = cognome
        self._cancellato = False


class OraPredefinita:
    def __init__(self, numero: int, oraInizio: Time, oraFine: Time):
        self._numero = numero
        self._oraInizio = oraInizio
        self._oraFine = oraFine


class Sostituzione:
    def __init__(
        self,
        id: int,
        aula: Aula,
        classe: Classe,
        docente: Docente | None = None,
        data: Date | None = None,
        oraInizio: Time | None = None,
        oraFine: Time | None = None,
        oraPredefinita: OraPredefinita | None = None,
        note: str | None = None,
        pubblicato: bool = False,
        cancellato: bool = False,
    ):
        self._cancellato = False


class Evento:
    def __init__(
        self,
        id: int,
        testo: str,
        data_ora_inizio: datetime | None = None,
        data_ora_fine: datetime | None = None,
        urgente: bool = False,
    ):
        self._id, self._testo, self._data_ora_inizio, self._data_ora_fine, urgente = (
            id,
            testo,
            data_ora_inizio,
            data_ora_fine,
            urgente,
        )
        self._cancellato = False


class Notizia:
    def __init__(
        self,
        id: int,
        testo: str,
        data_ora_inizio: datetime | None = None,
        data_ora_fine: datetime | None = None,
    ):
        self._id = id
        self._testo = testo
        self._data_ora_inizio = (data_ora_inizio,)
        self._data_ora_fine = data_ora_fine
        self._cancellato = False


class Visualizzazione:
    def __init__(self,):
        pass


class VisualizzazioneOnline:
    def __init__(self,):
        pass


class VisualizzazioneFisica:
    def __init__(self,):
        pass
