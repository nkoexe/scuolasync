import logging
from flask_socketio import emit

from sostituzioni.model.model import Aula, Classe, Docente, OraPredefinita, Sostituzione, Evento, Notizia
from sostituzioni.model.auth import login_required
from sostituzioni.view import socketio

logger = logging.getLogger(__name__)


@socketio.on('connect')
@login_required
def connect():
    logger.debug('Nuovo client connesso, invio dei dati iniziali.')

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
    """
    filtri:
    { cancellato: true }  // per mostrare anche sostituzioni cancellate
    { data_inizio: 1702767600, data_fine: 1702854000 }  // per sostituzioni comprese in un intervallo
    { data_inizio: 1702767600, data_fine: None }  // per sostituzioni future
    """

    logger.debug(f'Ricevuto segnale richiesta sostituzioni con filtri: {filtri}')

    emit('lista sostituzioni', Sostituzione.load(filtri))


@socketio.on('nuova sostituzione')
@login_required
def nuova_sostituzione(data):
    logger.debug(f'Ricevuto dati per inserimento nuova sostituzione: {data}')

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
    logger.debug(f'Ricevuto dati modifica sostituzione: {data}')

    Sostituzione(id=data.get('id')).modifica(data.get('data'))

    emit('aggiornamento sostituzioni', broadcast=True)


@socketio.on('elimina sostituzione')
@login_required
def elimina_sostituzione(data):
    logger.debug(f'Ricevuto segnale eliminazione sostituzione: {data}')

    Sostituzione(data.get('id')).elimina(data.get('mantieni_in_storico', True))  # usare default di configurazione

    emit('aggiornamento sostituzioni', broadcast=True)


@socketio.on('nuovo evento')
@login_required
def nuovo_evento(data):
    logger.debug(f'Ricevuto dati per inserimento nuovo evento: {data}')

    Evento(urgente=data.get('urgente', False), data_ora_inizio=data.get('data_ora_inizio'), data_ora_fine=data.get('data_ora_fine'), testo=data.get('testo')).inserisci()

    emit('aggiornamento eventi', broadcast=True)


@socketio.on('modifica evento')
@login_required
def modifica_evento(data):
    logger.debug(f'Ricevuto dati modifica evento: {data}')

    Evento(id=data.get('id')).modifica(data.get('data'))

    emit('aggiornamento eventi', broadcast=True)


@socketio.on('elimina evento')
@login_required
def elimina_evento(data):
    logger.debug(f'Ricevuto segnale eliminazione evento: {data}')

    Evento(data.get('id')).elimina()

    emit('aggiornamento eventi', broadcast=True)


@socketio.on('nuova notizia')
@login_required
def nuova_notizia(data: dict):
    logger.debug(f'Ricevuto dati per inserimento nuova notizia: {data}')

    Notizia(data_inizio=data.get('data_inizio'), data_fine=data.get('data_fine'), testo=data.get('testo')).inserisci()

    emit('aggiornamento notizie', broadcast=True)


@socketio.on('modifica notizia')
@login_required
def modifica_notizia(data):
    logger.debug(f'Ricevuto dati modifica notizia: {data}')

    Notizia(id=data.get('id')).modifica(data.get('data'))

    emit('aggiornamento notizie', broadcast=True)


@socketio.on('elimina notizia')
@login_required
def elimina_notizia(data):
    logger.debug(f'Ricevuto segnale eliminazione notizia: {data}')

    Notizia(data.get('id')).elimina()

    emit('aggiornamento notizie', broadcast=True)
