from flask import Blueprint

login = Blueprint('login', __name__)

from sostituzioni.view.login import routes