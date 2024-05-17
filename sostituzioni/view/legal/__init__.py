from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view import app


# @app.route("/crediti")
# def crediti():
#     return render_template("crediti.html")


@app.route("/privacy")
def privacy():
    return render_template(
        "privacy.html", logintimeout=configurazione.get("flasksessionlifetime")
    )


@app.route("/licenze")
def licenze():
    return render_template("licenze.html")
