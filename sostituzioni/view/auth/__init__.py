from flask import Blueprint

auth = Blueprint("auth", __name__)

from sostituzioni.view.auth import routes
