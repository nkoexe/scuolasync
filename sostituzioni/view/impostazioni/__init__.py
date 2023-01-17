from flask import Blueprint

impostazioni = Blueprint('impostazioni', __name__)

from sostituzioni.view.impostazioni import routes, events