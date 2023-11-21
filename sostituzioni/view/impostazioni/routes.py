from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required
from sostituzioni.view.impostazioni import impostazioni


@impostazioni.route('/impostazioni')
@login_required
def main():
    return render_template('impostazioni.html', configurazione=configurazione)


@impostazioni.route('/shell')
@login_required
def shell():
    return render_template('shell.html')
