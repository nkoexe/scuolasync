from flask_socketio import emit
from sostituzioni.model.model import aule, classi, docenti, ore_predefinite, sostituzioni, eventi, notizie
from sostituzioni.view import socketio
from sostituzioni.logger import logger


@socketio.on('test')
def evento(data):
    logger.debug(f'ricevuto: {data}')


@socketio.on('connect')
def connect():
    emit('lista sostituzioni', sostituzioni())
    emit('lista eventi', eventi())
    emit('lista notizie', notizie())
    emit('lista aule', aule())
    emit('lista classi', classi())
    emit('lista docenti', docenti())
    emit('lista ore predefinite', ore_predefinite())
