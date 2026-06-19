from flask import redirect, url_for, render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view.setup import setup


@setup.route("/")
def index():
    return render_template(
        "setup/ssoinfo.html",
        configurazione=configurazione,
        just_changing_sso_provider=True,
    )


# i need to have these fuckers defined otherwise flask spits at me
@setup.route("/sso")
def sso():
    pass


@setup.route("/next")
def next():
    pass


# override default error handler (so that sostituzioni.view.errorhandlers does not complain)
@setup.app_errorhandler(404)
def error(e):
    return redirect(url_for("setup.index"))
