"""
    This file is part of ScuolaSync.

    Copyright (C) 2023-present Niccolò Ragazzi <hi@njco.dev>

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
"""

import logging
import signal
from os import environ

from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from sostituzioni.model.app import app

logger = logging.getLogger(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

csrf = CSRFProtect(app)
socketio = SocketIO(app, manage_session=False)

import sostituzioni.view.errorhandlers
import sostituzioni.view.legal
import sostituzioni.view.docs

logger.debug("Importing blueprints..")

if "SCUOLASYNC_SETUP" in environ:
    from sostituzioni.view.setup import setup as setup_blueprint

    app.register_blueprint(setup_blueprint)
    logger.debug("Setup blueprint registered.")

else:
    from sostituzioni.view.impostazioni import impostazioni as impostazioni_blueprint
    from sostituzioni.view.auth import auth as auth_blueprint
    from sostituzioni.view.visualizzazionefisica import (
        fisica as visualizzazionefisica_blueprint,
    )
    from sostituzioni.view.visualizzazioneonline import (
        online as visualizzazioneonline_blueprint,
    )

    app.register_blueprint(impostazioni_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(visualizzazionefisica_blueprint)
    app.register_blueprint(visualizzazioneonline_blueprint)


def exit_handler(signal, frame):
    logger.info("Shutting down")
    # todo: velocizzare il shutdown di socketio
    # socketio.emit("shutdown") per qualche motivo non funziona, clients non lo ricevono
    exit(0)


signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

logger.debug("All blueprints registered")
logger.info("System ready")
