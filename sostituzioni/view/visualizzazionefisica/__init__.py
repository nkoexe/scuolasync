from flask import Blueprint

fisica = Blueprint('fisica', __name__)

from sostituzioni.view.visualizzazionefisica import routes, events