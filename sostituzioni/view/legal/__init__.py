from flask import render_template

from sostituzioni.view import app


# @app.route("/crediti")
# def crediti():
#     return render_template("crediti.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/licenze")
def licenze():
    return render_template("licenze.html")
