from flask_socketio import emit
import json
from sostituzioni.model.model import aule, classi, docenti, ore_predefinite, sostituzioni, eventi, notizie
from sostituzioni.model.auth import login_required, current_user
from sostituzioni.view import socketio
from sostituzioni.logger import logger


@socketio.on('test')
def evento(data):
    logger.debug(f'ricevuto: {data}')


@socketio.on('connect')
@login_required
def connect():
    print(sostituzioni())
    emit('lista sostituzioni', json.dumps(sostituzioni(), default=str))
    # emit('lista eventi', eventi())
    # emit('lista notizie', notizie())
    # emit('lista aule', aule())
    # emit('lista classi', classi())
    # emit('lista docenti', docenti())
    # emit('lista ore predefinite', ore_predefinite())
