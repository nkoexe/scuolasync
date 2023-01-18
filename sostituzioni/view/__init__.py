import logging

from flask import Flask, request
from flask_socketio import SocketIO

from sostituzioni.control.configurazione import Configurazione

logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

configurazione = Configurazione()

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'aaaaa'

socketio = SocketIO(app)

from sostituzioni.view.impostazioni import impostazioni as impostazioni_blueprint
from sostituzioni.view.login import login as login_blueprint
from sostituzioni.view.visualizzazionefisica import fisica as visualizzazionefisica_blueprint
from sostituzioni.view.visualizzazioneonline import online as visualizzazioneonline_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(impostazioni_blueprint)
app.register_blueprint(visualizzazioneonline_blueprint)
app.register_blueprint(visualizzazionefisica_blueprint)


def main():
    socketio.run(app, '0.0.0.0', debug=True)
