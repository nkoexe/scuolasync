import re
from flask_socketio import emit

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import (
    login_required,
    role_required,
    current_user,
    login_user,
    logout_user,
    utenti,
    Utente,
    User,
)
from sostituzioni.view import socketio


@socketio.on("test", namespace="/impostazioni")
def test():
    return "ok"


@socketio.on("admin email", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def admin_email(email):
    if email == "" or not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
        return

    configurazione.admin_email = email


@socketio.on("sso choice", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def sso_choice(choice):
    if not isinstance(choice, int):
        if not isinstance(choice, str) or not choice.isdigit():
            return

    configurazione.set("ssochoice", int(choice))


@socketio.on("setup done", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def setup_done():
    configurazione.esporta()

    from sostituzioni.control.cli import aggiungi_utente

    aggiungi_utente(configurazione.admin_email, "amministratore")

    from sostituzioni.view.impostazioni.events import reboot

    reboot()
