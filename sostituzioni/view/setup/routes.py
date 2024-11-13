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
    return render_template("setup/admin.html", configurazione=configurazione)


@setup.route("/info")
def info():
    return render_template("setup/info.html", configurazione=configurazione)


@setup.route("/scuola")
def scuola():
    return render_template("setup/scuola.html", configurazione=configurazione)


@setup.route("/sso")
def sso():
    return render_template("setup/sso.html", configurazione=configurazione)


@setup.route("/ssoinfo")
def ssoinfo():
    return render_template("setup/ssoinfo.html", configurazione=configurazione)


@setup.route("/next")
def next():
    admin_ready = False
    school_img_ready = False
    school_info_ready = False
    sso_ready = False

    admin_ready = bool(configurazione.admin_email)

    school_img_ready = (
        configurazione.get("schoolmainlogo").valore.path.exists()
        and configurazione.get("schoolhederlogo").valore.path.exists()
    )

    school_info_ready = (
        bool(configurazione.get("supportemail"))
        and bool(configurazione.get("schoollink"))
        and bool(configurazione.get("schoolprivacylink"))
    )

    match configurazione.get("ssochoice"):
        case 0:
            sso_ready = bool(configurazione.get("gclientid")) and bool(
                configurazione.get("gclientsecret")
            )

        case 1:
            sso_ready = bool(configurazione.get("msclientid")) and bool(
                configurazione.get("msclientsecret")
            )

    return render_template(
        "setup/next.html",
        configurazione=configurazione,
        admin=admin_ready,
        school_img=school_img_ready,
        school_info=school_info_ready,
        sso=sso_ready,
    )


# override default error handler (so that sostituzioni.view.errorhandlers does not complain)
@setup.app_errorhandler(404)
def error(e):
    return redirect(url_for("setup.index"))
