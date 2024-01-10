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


@auth.route("/richiedi-accesso")
def fottiti():
    return 'Qui ci sarà il form per richiedere l\'accesso al sistema, con opportune minacce. Per il momento, in caso di problemi di accesso, scrivere a <a href="mailto:niccolo.ragazzi@gandhimerano.com">niccolo.ragazzi@gandhimerano.com</a>'


@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("online.index"))

    # 3 lines of development speedup, remove in production pls ty
    # from sostituzioni.model.auth import authenticate_user

    # authenticate_user("testa")
    # return redirect(url_for("online.index"))

    # flash("Questo account non è autorizzato all'accesso al sistema.")

    return render_template(
        "login.html",
        title=configurazione.get("systitle"),
        bottomparagraph=configurazione.get("loginpageparagraph"),
        paragraph=configurazione.get("loginpageparagraph"),
        supportemail=configurazione.get("supportemail"),
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
