from flask import render_template

from sostituzioni.view.visualizzazioneonline import online


@online.route('/')
def index():
    return render_template('index.html')
