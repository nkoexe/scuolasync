from flask import render_template, request, redirect, url_for

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_user, User
from sostituzioni.view.visualizzazionefisica import fisica


AUTHCODE = "udfh474873kjbuhg455iwejf1654oibnhjhvjzgbzjvhbhudbhfukjbhkfjzhsiud5447650889kugmmbn3253mcbvbhijhkSfgkjlhsi8ut6iut0943utakjderiljkv493u6rtjfg"


@fisica.route("/")
def index():
    if request.args.get("code") == AUTHCODE or True:
        login_user(User("display"))
        return render_template("display.html", configurazione=configurazione)

    return redirect(url_for("auth.login"))
