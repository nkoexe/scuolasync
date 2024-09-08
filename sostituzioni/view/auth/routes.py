import logging
from flask import render_template, redirect, url_for, request, flash

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import (
    current_user,
    login_manager,
    login_required,
    sso_login,
    logout_user,
    GOOGLE_SSO_REQ_URI,
)
from sostituzioni.view.auth import auth


logger = logging.getLogger(__name__)


@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("online.index"))

    # 3 lines of development speedup, remove in production pls ty
    # from sostituzioni.model.auth import authenticate_user

    # authenticate_user("niccolo.rag@gmail.com")
    # authenticate_user("bidelleria@gandhimerano.com")
    # return redirect(url_for("online.index"))

    # flash("Questo account non è autorizzato all'accesso al sistema.")
    # flash("Autenticazione annullata.")

    return render_template(
        "login.html",
        configurazione=configurazione,
    )


@auth.route("/googlesso")
def googlessoredirect():
    return redirect(GOOGLE_SSO_REQ_URI)


@auth.route("/loginredirect")
def loginredirect():
    """Richiesta di autorizzazione dopo l'autenticazione con Google"""

    authenticated = sso_login(request)

    if authenticated:
        return redirect(url_for("online.index"))
    else:
        return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
