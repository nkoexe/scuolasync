from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view import app


# @app.route("/crediti")
# def crediti():
#     return render_template("crediti.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", configurazione=configurazione)


@app.route("/license")
@app.route("/licenze")
def licenze():
    return render_template("licenze.html", configurazione=configurazione)


@app.route("/yourschool")
def demo_school():
    return "Pagina principale del tuo Istituto Scolastico"


@app.route("/yourschool/privacy")
def demo_privacy():
    return "Pagina Privacy del tuo Istituto Scolastico"
