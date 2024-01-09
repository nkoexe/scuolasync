from flask import render_template, request

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required, role_required, current_user
from sostituzioni.view.visualizzazioneonline import online


code = "my85nyh5724025g740389ny91cf6ntynm5ynm89346y86y30h6yn0g6ny832yn7fkuy84532gdsfhiofg78432n5fayht4nh78523th789treaju89f32gb5ayhn89rewbn679532yj8953ayn79532yj89weuj088"


@online.route("/infopoint/frontend")
def test():
    if request.args.get("code") == code:
        return "infopoint!!!! wowow!!!"

    return "no"


@online.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        title=configurazione.get("systitle"),
        configurazione=configurazione,
        utente=current_user,
    )
