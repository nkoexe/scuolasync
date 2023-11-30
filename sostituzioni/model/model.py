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



class VisualizzazioneOnline(Visualizzazione):
    @beartype
    def __init__(self):
        super(VisualizzazioneOnline, self).__init__()


class VisualizzazioneFisica(Visualizzazione):
    @beartype
    def __init__(self):
        super(VisualizzazioneFisica, self).__init__()


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
