from flask import render_template
from . import impostazioni


@impostazioni.route('/impostazioni')
def main():
    return render_template('impostazioni.html')
