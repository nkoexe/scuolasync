from flask import render_template, request, redirect, url_for

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import authenticate_user
from sostituzioni.view.visualizzazionefisica import fisica


@fisica.route("/")
def index():
    if request.args.get("code") in configurazione.get("displayauthcodes"):
        return render_template("display.html", configurazione=configurazione)

    return redirect(url_for("auth.login"))
