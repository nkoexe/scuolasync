from flask_socketio import emit
from sostituzioni.model.model import Aula, Classe, Docente, OraPredefinita, Sostituzione, Evento, Notizia
from sostituzioni.model.auth import login_required
from sostituzioni.view import socketio
from sostituzioni.logger import logger


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


@socketio.on('nuova sostituzione')
@login_required
def nuova_sostituzione(data):
    print(data)
