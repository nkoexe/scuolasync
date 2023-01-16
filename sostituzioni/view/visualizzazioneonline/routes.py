from flask import render_template
from . import online


@online.route('/')
def index():
    return render_template('index.html')
