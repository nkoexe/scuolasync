from flask import Flask

app = Flask(__name__)

# todo rimuovere yeah
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_PERMANENT'] = True
app.config['FLASK_ENV'] = "development"
