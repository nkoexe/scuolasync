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
    sostituzione = Sostituzione(id=None, aula=data.get('aula'), classe=data.get('classe'),
                                docente=data.get('docente'), data=data.get('data'),
                                ora_inizio=data.get('ora_inizio'), ora_fine=data.get('ora_fine'),
                                ora_predefinita=data.get('ora_predefinita'), note=data.get('note'),
                                pubblicato=data.get('pubblicato'))
    sostituzione.inserisci()

    emit('aggiornamento sostituzioni', broadcast=True)


@socketio.on('elimina sostituzione')
@login_required
def elimina_sostituzione(data):
    Sostituzione(data.get('id')).elimina()
