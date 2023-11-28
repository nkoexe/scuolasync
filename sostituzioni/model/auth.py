from flask import abort, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from functools import wraps
import requests
from oauthlib import oauth2
import json

from sostituzioni.control.database import authdatabase, Utente
from sostituzioni.model.app import app


OAUTH_CLIENT_ID = '824960094253-vlhoqf37teg8i307fkeui4041tmu2lk9.apps.googleusercontent.com'
OAUTH_CLIENT_SECRET = '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'

OAUTH_CLIENT = oauth2.WebApplicationClient(OAUTH_CLIENT_ID)
GOOGLE_SSO_REQ_URI = OAUTH_CLIENT.prepare_request_uri(
    uri='https://accounts.google.com/o/oauth2/v2/auth',
    redirect_uri='http://localhost:5000/loginredirect',
    scope='https://www.googleapis.com/auth/userinfo.email',
    prompt='consent'
)


login_manager = LoginManager(app)


class User(UserMixin, Utente):
    def __init__(self, id):
        self.id = id
        self.ruolo = ''
        self.permessi = []

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True


def sso_login(request):
    code = request.args.get('code')

    token_url, headers, body = OAUTH_CLIENT.prepare_token_request(
        'https://oauth2.googleapis.com/token',
        authorisation_response=request.url,
        redirect_url=request.base_url,
        code=code)

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET))

    OAUTH_CLIENT.parse_request_body_response(json.dumps(token_response.json()))

    uri, headers, body = OAUTH_CLIENT.add_token('https://www.googleapis.com/oauth2/v3/userinfo')

    response_user_info = requests.get(uri, headers=headers, data=body)
    info = response_user_info.json()

    result = authenticate_user(info['email'])

    if result:
        return True
    else:
        flash('Questo account non è autorizzato all\'accesso al sistema.')


def authenticate_user(email):
    userdata = User.load(where=f"email='{email}'")

    if not userdata:
        return False

    session.permanent = True

    login_user(User(email))

    return True


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


class permesso:
    def visualizza_notizie(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.ruoli:
                abort(403)

            return func(*args, **kwargs)
        return wrapper
