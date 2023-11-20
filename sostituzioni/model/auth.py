from flask import abort, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from functools import wraps

from sostituzioni.control.database import database
from sostituzioni.model.app import app

login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.permessi = []
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    '''
    Indica cosa fare con richieste di utenti che non hanno
    ancora fatto il login, a pagine che lo richiedono
    '''
    return redirect(url_for('auth.login'))


class permesso:
    def visualizza_notizie(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.ruoli:
                abort(403)

            return func(*args, **kwargs)
        return wrapper
