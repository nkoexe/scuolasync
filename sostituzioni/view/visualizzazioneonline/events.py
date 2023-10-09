from flask import session
from flask_socketio import emit

from sostituzioni.view import socketio
from sostituzioni.logger import logger


@socketio.on('evento')
def evento(data):
    logger.debug(f'ricevuto: {data}')
