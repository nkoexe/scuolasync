from flask import Blueprint

fisica = Blueprint('fisica', __name__, url_prefix='/display')

from sostituzioni.view.visualizzazionefisica import routes, events