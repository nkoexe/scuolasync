from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required
from sostituzioni.view.visualizzazioneonline import online


@online.route('/')
@login_required
def index():
    return render_template('index.html', configurazione=configurazione)
