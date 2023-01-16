from flask import Blueprint

impostazioni = Blueprint('impostazioni', __name__)

from . import routes, events