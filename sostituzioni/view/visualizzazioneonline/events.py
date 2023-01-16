from flask import session
from flask_socketio import emit
from .. import socketio

import logging


@socketio.on('evento')
def evento(data):
    logging.debug(f'ricevuto: {data}')
