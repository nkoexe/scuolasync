from flask import Flask
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from secrets import token_hex

from sostituzioni.logger import logger
from sostituzioni.control.configurazione import Configurazione


configurazione = Configurazione()


app = Flask(__name__)
app.debug = True
app.config.update(
    SECRET_KEY=token_hex(32),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

csrf = CSRFProtect(app)
socketio = SocketIO(app)

logger.debug('Importing blueprints..')
from sostituzioni.view.impostazioni import impostazioni as impostazioni_blueprint
from sostituzioni.view.auth import auth as auth_blueprint
from sostituzioni.view.visualizzazionefisica import fisica as visualizzazionefisica_blueprint
from sostituzioni.view.visualizzazioneonline import online as visualizzazioneonline_blueprint

app.register_blueprint(impostazioni_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(visualizzazionefisica_blueprint)
app.register_blueprint(visualizzazioneonline_blueprint)

logger.debug('All blueprints registered')
