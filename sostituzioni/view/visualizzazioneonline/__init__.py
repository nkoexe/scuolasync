from flask import Blueprint

online = Blueprint("online", __name__)

from sostituzioni.view.visualizzazioneonline import routes, events
