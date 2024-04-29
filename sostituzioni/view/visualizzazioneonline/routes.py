from flask import render_template, request, send_file
from datetime import datetime

from sostituzioni.control.exporter import Exporter
from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required, role_required, current_user
from sostituzioni.view.visualizzazioneonline import online


@online.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        title=configurazione.get("systitle"),
        configurazione=configurazione,
        utente=current_user,
    )


@online.route("/export")
@login_required
def export():
    if Exporter.exported_buffer is None:
        return "Nessun file."

    if Exporter.exported_buffer.closed:
        # print("closed")
        return "Nessun file."

    match Exporter.exported_mimetype:
        case "text/csv":
            exported_ext = ".csv"
        case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            exported_ext = ".xlsx"
        case _:
            exported_ext = ""

    return send_file(
        Exporter.exported_buffer,
        as_attachment=True,
        download_name="export_sostituzioni_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + exported_ext,
    )


@online.route("/testone")
@login_required
@role_required("sostituzioni.write")
def testone():
    from random import choice, randint
    from datetime import datetime, timedelta
    from sostituzioni.model.model import (
        Aula,
        Docente,
        Classe,
        OraPredefinita,
        Sostituzione,
        sostituzioni,
    )

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
            {
                "data": data,
                "numero_aula": aula,
                "nome_classe": classe,
                "docente": docente,
                "ora_predefinita": orapredefinita,
                "ora_inizio": None,
                "ora_fine": None,
                "note": None,
                "pubblicato": True,
                "cancellato": False,
            }
        )

        sostituzioni.inserisci(sostituzione)

    return "ok"
