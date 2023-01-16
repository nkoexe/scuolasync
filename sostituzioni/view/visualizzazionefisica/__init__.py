from flask import Blueprint

fisica = Blueprint('fisica', __name__)

from . import routes, events