from flask import Blueprint

online = Blueprint('online', __name__)

from . import routes, events