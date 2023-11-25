from flask import Flask
from datetime import timedelta

app = Flask(__name__)

# app.config['PERMANENT_SESSION_LIFETIME '] = timedelta(seconds=5)
# app.config['SESSION_REFRESH_EACH_REQUEST '] = True

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FLASK_ENV'] = 'development'


# @app.before_request
# def before_request():
#     print("before request")
#     app.permanent_session_lifetime = timedelta(seconds=5)
