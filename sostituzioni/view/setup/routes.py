from flask import redirect, url_for, render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view.setup import setup
from sostituzioni.model.auth import current_user

configurazione.admin_email = ""

@setup.route("/")
def index():
    return render_template("setup/index.html", configurazione=configurazione)


@setup.route("/admin")
def admin():
    return render_template(
        "setup/admin.html", configurazione=configurazione
    )


@setup.route("/info")
def info():
    return render_template("setup/info.html", configurazione=configurazione)


# override default error handler (so that sostituzioni.view.errorhandlers does not complain)
@setup.app_errorhandler(404)
def error(e):
    return redirect(url_for("setup.index"))
