"""
descr
"""
from beartype._decor.decormain import beartype

from sostituzioni.control.database import (database, ElementoDatabase,
                                           Aula, Classe, Docente, OraPredefinita,
                                           Sostituzione, Evento, Notizia,
                                           Visualizzazione, Utente)


class Sostituzione(Sostituzione):
    def __init__(self,
                 id: int | None = None,
                 aula: Aula | None = None,
                 classe: Classe | None = None,
                 docente: Docente | None = None,
                 data: int | None = None,
                 ora_inizio: str | None = None,
                 ora_fine: str | None = None,
                 ora_predefinita: OraPredefinita | None = None,
                 note: str | None = None,
                 pubblicato: bool = False
                 ):

        self.id = id
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
    def __init__(self,
                 id: int | None = None,
                 urgente: bool | None = None,
                 data_ora_inizio: int | None = None,
                 data_ora_fine: int | None = None,
                 testo: str | None = None
                 ):

        self.id = id
        self.urgente = urgente
        self.data_ora_inizio = data_ora_inizio
        self.data_ora_fine = data_ora_fine
        self.testo = testo


class Notizia(Notizia):
    def __init__(self,
                 id: int | None = None,
                 data_inizio: int | None = None,
                 data_fine: int | None = None,
                 testo: str | None = None
                 ):

        self.id = id
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.testo = testo


class VisualizzazioneOnline(Visualizzazione):
    def __init__(self):
        pass


class VisualizzazioneFisica(Visualizzazione):
    def __init__(self):
        pass


# from time import time
# print('start', time())
# total = 0
# for i in range(10000):
#     start_time = time()
#     database.get('permesso', where=f'nome="permesso{i}"')
#     end_time = time()
#     total += end_time - start_time
# print('total', total)
# print('average', total / 10000)
