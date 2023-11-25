from flask import Flask
from secrets import token_hex
from datetime import timedelta

from sostituzioni.control.configurazione import configurazione

app = Flask(__name__)

app.static_folder = configurazione.get('flaskstaticdir').path
app.template_folder = configurazione.get('flasktemplatedir').path

app.config['SECRET_KEY'] = token_hex(32),
app.config['SESSION_COOKIE_SECURE'] = True,
app.config['SESSION_COOKIE_HTTPONLY'] = True,
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# app.config['PERMANENT_SESSION_LIFETIME '] = timedelta(seconds=5)
# app.config['SESSION_REFRESH_EACH_REQUEST '] = True

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FLASK_ENV'] = 'development'


# @app.before_request
# def before_request():
#     print("before request")
#     app.permanent_session_lifetime = timedelta(seconds=5)
