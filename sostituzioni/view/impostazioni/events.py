from flask import session
from flask_socketio import emit
from sostituzioni.view import socketio, configurazione
from sostituzioni.logger import logger


@socketio.on('applica')
def applica(dati):
    logger.debug(f'ricevuto: {dati}')

    configurazione.aggiorna(dati)

    emit('applica', 'ok')
