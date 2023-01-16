import logging

from flask import Flask, request
from flask_socketio import SocketIO


logging.getLogger('werkzeug').setLevel(logging.ERROR)

socketio = SocketIO()


@socketio.on('connect')
def connect():
    # print(f'dispositivo connesso: {request.remote_addr}')
    pass


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'aaaaa'

    from .impostazioni import impostazioni as impostazioni_blueprint
    from .login import login as login_blueprint
    from .visualizzazionefisica import \
        fisica as visualizzazionefisica_blueprint
    from .visualizzazioneonline import \
        online as visualizzazioneonline_blueprint

    app.register_blueprint(login_blueprint)
    app.register_blueprint(impostazioni_blueprint)
    app.register_blueprint(visualizzazioneonline_blueprint)
    app.register_blueprint(visualizzazionefisica_blueprint)

    socketio.init_app(app)

    return app
