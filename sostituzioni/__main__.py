"""
durante la fase di sviluppo eseguire questo file tramite python -m sostituzioni
"""

from sostituzioni.app import app
from sostituzioni.view import socketio


if __name__ == "__main__":
    socketio.run(app, use_reloader=True, log_output=False)
