from flask import render_template, redirect, url_for

from sostituzioni.view import app
from sostituzioni.model.auth import current_user


@app.errorhandler(404)
def not_found(e):
    if current_user.is_authenticated:
        return "Non trovato", 404

    return redirect(url_for("auth.login"))


# @app.errorhandler(500)
# def internal_error(e):
#     return "Errore interno", 500


@app.errorhandler(401)
def unauthorized(e):
    if current_user.is_authenticated:
        return (
            f"Non hai accesso a questa pagina. Hai fatto il login con l'account {current_user.id}, prova con un altro account.",
            401,
        )
    else:
        return redirect(url_for("auth.login"))
