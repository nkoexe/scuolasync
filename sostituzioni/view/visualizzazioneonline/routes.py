from flask import render_template, request

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required, current_user
from sostituzioni.model.model import Sostituzione, Aula, Docente, Classe, OraPredefinita
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


@online.route("/testone")
@login_required
def testone():
    from random import choice, randint
    from datetime import datetime, timedelta

    aule = Aula.load()
    docenti = Docente.load()
    classi = Classe.load()
    orapredefinite = OraPredefinita.load()

    for i in range(100):
        aula = choice(aule)["numero"]
        docente = choice(docenti)
        docente = docente["cognome"] + " " + docente["nome"]
        classe = choice(classi)["nome"]
        orapredefinita = choice(orapredefinite)["numero"]
        data = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=randint(0, 30))
        data = int(data.timestamp())

        sostituzione = Sostituzione(
            None, aula, classe, docente, data, None, None, orapredefinita, None, True
        )
        sostituzione.inserisci()

    return "ok"
