from flask import render_template
from sostituzioni.view.visualizzazionefisica import fisica


@fisica.route('/fisica')
def index():
    return render_template('index.html')
