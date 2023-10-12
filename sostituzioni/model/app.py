from flask import Flask

from sostituzioni.control.database import Database
from sostituzioni.control.configurazione import Configurazione


app = Flask(__name__)

configurazione = Configurazione()
database = Database(app)
