from functools import wraps
from oauthlib import oauth2
import logging
import requests
import json

from flask import abort, redirect, url_for, flash, session, request
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from flask_socketio import emit


from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.database import Where, Ruolo, Utente, SearchableList
from sostituzioni.model.app import app

logger = logging.getLogger(__name__)


OAUTH_CLIENT_ID = configurazione.get("oauthclientid")
OAUTH_CLIENT_SECRET = configurazione.get("oauthclientsecret")

OAUTH_CLIENT = oauth2.WebApplicationClient(OAUTH_CLIENT_ID)
GOOGLE_SSO_REQ_URI = OAUTH_CLIENT.prepare_request_uri(
    uri="https://accounts.google.com/o/oauth2/v2/auth",
    redirect_uri=configurazione.get("redirecturi"),
    scope="https://www.googleapis.com/auth/userinfo.email",
    prompt="select_account",
)


def load_utenti():
    global ruoli, utenti

    ruoli = SearchableList("nome", [Ruolo(r["nome"]) for r in Ruolo.load()])
    utenti = SearchableList(
        "email", [Utente(u["email"], ruoli.get(u["ruolo"])) for u in Utente.load()]
    )


login_manager = LoginManager(app)
load_utenti()


class User(UserMixin, Utente):
    def __init__(self, id):
        utente = utenti.get(id)

        self.id = id
        self.email = utente.email
        self.ruolo = utente.ruolo
        self.permessi = utente.ruolo.permessi

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True


def role_required(role):
    """
    Usage:
    ```
    @login_requided
    @role_required("sostituzioni.write")
    def protected():
        ...
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if role in current_user.ruolo.nomi_permesso:
                return func(*args, **kwargs)
            return abort(401)

        return wrapper

    return decorator


def sso_login(request):
    code = request.args.get("code")

    token_url, headers, body = OAUTH_CLIENT.prepare_token_request(
        "https://oauth2.googleapis.com/token",
        authorisation_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    try:
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET),
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore durante l'autenticazione: {e}")
        flash("Si è verificato un errore durante l'autenticazione.")
        return False

    try:
        OAUTH_CLIENT.parse_request_body_response(json.dumps(token_response.json()))
    except oauth2.OAuth2Error as e:
        logger.error(
            f"Errore durante l'autenticazione, probabilmente annullata dall'utente: {e}"
        )
        flash("Autenticazione annullata.")
        return False

    uri, headers, body = OAUTH_CLIENT.add_token(
        "https://www.googleapis.com/oauth2/v3/userinfo"
    )

    response_user_info = requests.get(uri, headers=headers, data=body)
    info = response_user_info.json()

    print(info)

    # Struttura info utente:
    # {
    #   email: ...
    #
    # }

    result = authenticate_user(info["email"])

    if result:
        return True
    else:
        flash("Questo account non è autorizzato all'accesso al sistema.")
        return False


def authenticate_user(email):
    logger.debug(f"Autenticazione utente {email}")

    email = "niccolo.ragazzi@gandhimerano.com"

    userdata = User.load(where=Where("email").equals(email))

    if not userdata:
        logger.info(
            f"Utente {email} ha cercato di effettuare l'accesso, non autorizzato"
        )
        return False

    user = User(email)

    logger.info(f"Utente {email} ({user.ruolo.nome}) ha eseguito l'accesso al sistema.")

    session.permanent = True
    login_user(user)

    return True


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    # check if request was sent with socketio
    if hasattr(request, "namespace"):
        emit("unauthorized")
        return
    return redirect(url_for("auth.login"))
