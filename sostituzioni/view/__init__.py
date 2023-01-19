import logging

from flask import Flask
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

from sostituzioni.control.configurazione import Configurazione


configurazione = Configurazione()

app = Flask(__name__)
app.debug = True
app.config.update(
    SECRET_KEY='aaaaa',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

csrf = CSRFProtect(app)
socketio = SocketIO(app)


def main():
    logging.debug('Importing blueprints..')

    from sostituzioni.view.impostazioni import impostazioni as impostazioni_blueprint
    from sostituzioni.view.login import login as login_blueprint
    from sostituzioni.view.visualizzazionefisica import fisica as visualizzazionefisica_blueprint
    from sostituzioni.view.visualizzazioneonline import online as visualizzazioneonline_blueprint

    app.register_blueprint(login_blueprint)
    app.register_blueprint(impostazioni_blueprint)
    app.register_blueprint(visualizzazioneonline_blueprint)
    app.register_blueprint(visualizzazionefisica_blueprint)

    logging.debug('All blueprints registered, starting server.')

    socketio.run(app, '0.0.0.0', debug=True)
