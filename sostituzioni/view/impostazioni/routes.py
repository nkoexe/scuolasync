from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.database import utenti
from sostituzioni.model.model import Docente
from sostituzioni.model.auth import login_required, role_required
from sostituzioni.view.impostazioni import impostazioni


@impostazioni.route("/impostazioni")
@login_required
@role_required("impostazioni.write")
def main():
    return render_template(
        "impostazioni.html",
        configurazione=configurazione,
        utenti=utenti,
        docenti=Docente.load(),
    )
