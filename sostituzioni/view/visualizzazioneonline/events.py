import logging
from flask_socketio import emit

from sostituzioni.model.model import Aula, Classe, Docente, OraPredefinita, Sostituzione, Evento, Notizia
from sostituzioni.model.auth import login_required
from sostituzioni.view import socketio

logger = logging.getLogger(__name__)


@socketio.on('test')
def evento(data):
    logger.debug(f'ricevuto: {data}')


@socketio.on('connect')
@login_required
def connect():
    emit('lista sostituzioni', Sostituzione.load())
    emit('lista eventi', Evento.load())
    emit('lista notizie', Notizia.load())
    emit('lista aule', Aula.load())
    emit('lista classi', Classe.load())
    emit('lista docenti', Docente.load())
    emit('lista ore predefinite', OraPredefinita.load())


@socketio.on('richiesta sostituzioni')
@login_required
def richiesta_sostituzioni(filtri):
    emit('lista sostituzioni', Sostituzione.load())


@socketio.on('nuova sostituzione')
@login_required
def nuova_sostituzione(data):
    sostituzione = Sostituzione(id=None, aula=data.get('aula'), classe=data.get('classe'),
                                docente=data.get('docente'), data=data.get('data'),
                                ora_inizio=data.get('ora_inizio'), ora_fine=data.get('ora_fine'),
                                ora_predefinita=data.get('ora_predefinita'), note=data.get('note'),
                                pubblicato=data.get('pubblicato'))
    sostituzione.inserisci()

    emit('aggiornamento sostituzioni', broadcast=True)


@socketio.on('modifica sostituzione')
@login_required
def modifica_sostituzione(data):
    Sostituzione(id=data.get('id')).modifica(data.get('data'))

    emit('aggiornamento sostituzioni', broadcast=True)


@socketio.on('elimina sostituzione')
@login_required
def elimina_sostituzione(data: dict):
    Sostituzione(data.get('id')).elimina(data.get('mantieni_in_storico', True))  # usare default di configurazione

    emit('aggiornamento sostituzioni', broadcast=True)


@socketio.on('nuova notizia')
@login_required
def nuova_notizia(data: dict):
    Notizia(id=None, testo=data.get('testo')).inserisci()

    emit('aggiornamento notizie', broadcast=True)
