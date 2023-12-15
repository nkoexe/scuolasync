import logging

from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

from sostituzioni.model.app import app

logger = logging.getLogger(__name__)

csrf = CSRFProtect(app)
socketio = SocketIO(app, manage_session=True)

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
logger.info('System ready')
