import logging
from flask_socketio import emit

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required
from sostituzioni.view import socketio
from sostituzioni.view.impostazioni.shell import RedirectedStdout

logger = logging.getLogger(__name__)


@socketio.on('applica impostazioni', namespace='/impostazioni')
@login_required
def applica(dati):
    logger.debug(f'ricevuto: {dati}')

    try:
        configurazione.aggiorna(dati)
    except ValueError as e:
        emit('applica impostazioni errore', str(e))

    emit('applica impostazioni successo')


@socketio.on('shell', namespace='/shell')
@login_required
def shell(dati):
    with RedirectedStdout() as out:
        try:
            exec(dati)
        except Exception as e:
            print(e)
        emit('shell', str(out))


@socketio.on('server reboot', namespace='/impostazioni')
@login_required
def reboot():
    import os

    if os.name == 'nt':
        os.system(f'cmd /c {configurazione.get("scriptsdir").path / "reboot.bat"} {os.getpid()}')

    else:
        os.system(f'bash {configurazione.get("scriptsdir").path / "reboot.sh"} {os.getpid()}')
