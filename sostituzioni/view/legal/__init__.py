from flask import render_template

from sostituzioni.view import app


@app.route("/crediti")
def crediti():
    return "crediti wow"


@app.route("/privacy")
def privacy():
    return "privacy"


@app.route("/licenze")
def licenze():
    return "licenze"
