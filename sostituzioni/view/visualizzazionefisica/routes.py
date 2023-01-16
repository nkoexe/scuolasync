from flask import render_template
from . import fisica


@fisica.route('/fisica')
def index():
    return render_template('index.html')
