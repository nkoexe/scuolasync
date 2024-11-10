from flask import Blueprint

from sostituzioni.model.auth import (
    utenti,
    login_user,
    current_user,
    Utente,
    User,
)


setup = Blueprint("setup", __name__)

# login for temporary setup user
utenti.append(Utente("setup", "amministratore"))


@setup.before_request
def login_setup_user():
    if current_user.is_anonymous:
        login_user(User("setup"))


from sostituzioni.view.setup import routes, events

# some events are the same as the settings page, remember to set namespace to "/impostazioni"
from sostituzioni.view.impostazioni import events
