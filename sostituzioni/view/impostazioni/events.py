from flask_socketio import emit

from sostituzioni.logger import logger
from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required
from sostituzioni.view import socketio
from sostituzioni.view.impostazioni.shell import RedirectedStdout


@socketio.on('applica impostazioni')
@login_required
def applica(dati):
    logger.debug(f'ricevuto: {dati}')

    try:
        configurazione.aggiorna(dati)
    except ValueError as e:
        emit('applica impostazioni errore', str(e))

    emit('applica impostazioni successo')


@socketio.on('shell')
@login_required
def shell(dati):
    with RedirectedStdout() as out:
        try:
            exec(dati)
        except Exception as e:
            print(e)
        emit('shell', str(out))
