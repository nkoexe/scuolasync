from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view.impostazioni import impostazioni
from sostituzioni.model import aule


@impostazioni.route('/impostazioni')
def main():
    return render_template('impostazioni.html', configurazione=configurazione)


@impostazioni.route('/shell')
def shell():
    return render_template('shell.html')
