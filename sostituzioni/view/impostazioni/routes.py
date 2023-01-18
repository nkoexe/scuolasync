from flask import render_template

from sostituzioni.view import configurazione
from sostituzioni.view.impostazioni import impostazioni


@impostazioni.route('/impostazioni')
def main():
    return render_template('impostazioni.html', impostazioni=configurazione.configurazione)
