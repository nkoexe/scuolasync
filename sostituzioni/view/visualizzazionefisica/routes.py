from flask import render_template, request, redirect, url_for

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import authenticate_user
from sostituzioni.view.visualizzazionefisica import fisica


AUTHCODES = [
    "udfh474873kjbuhg455iwejf1654oibnhjhvjzgbzjvhbhudbhfukjbhkfjzhsiud5447650889kugmmbn3253mcbvbhijhkSfgkjlhsi8ut6iut0943utakjderiljkv493u6rtjfg",
    "test",
]


@fisica.route("/")
def index():
    if request.args.get("code") in AUTHCODES:
        return render_template("display.html", configurazione=configurazione)

    return redirect(url_for("auth.login"))
