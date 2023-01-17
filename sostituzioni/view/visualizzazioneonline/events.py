import logging

from flask import session
from flask_socketio import emit

from sostituzioni.view import socketio


@socketio.on('evento')
def evento(data):
    logging.debug(f'ricevuto: {data}')
