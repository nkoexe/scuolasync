from flask_socketio import emit
from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.database import database
from sostituzioni.view import socketio
from sostituzioni.logger import logger
from sostituzioni.view.impostazioni.shell import RedirectedStdout


@socketio.on('applica impostazioni')
def applica(dati):
    logger.debug(f'ricevuto: {dati}')

    try:
        configurazione.aggiorna(dati)
    except ValueError as e:
        emit('applica impostazioni errore', str(e))

    emit('applica impostazioni successo')


@socketio.on('shell')
def shell(dati):
    with RedirectedStdout() as out:
        try:
            exec(dati)
        except Exception as e:
            print(e)
        emit('shell', str(out))
