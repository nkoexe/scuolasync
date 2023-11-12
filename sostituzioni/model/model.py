"""
descr
"""

from sostituzioni.control.database import (database, ElementoDatabase,
                                           Aula, Classe, Docente, OraPredefinita,
                                           Sostituzione, Evento, Notizia,
                                           VisualizzazioneOnline, VisualizzazioneFisica)


def load(data: ElementoDatabase, filtri=None):
    return data.load()


def sostituzioni():
    return load(Sostituzione)


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
