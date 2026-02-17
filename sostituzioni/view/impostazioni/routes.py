"""
    This file is part of ScuolaSync.

    Copyright (C) 2023-present Niccolò Ragazzi <hi@njco.dev>

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
"""

from flask import render_template
import re
from datetime import datetime

from sostituzioni.control.logging import file
from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.updater import updater
from sostituzioni.model.auth import login_required, role_required, utenti
from sostituzioni.model.model import Classe, Aula, Docente, OraPredefinita, NotaStandard
from sostituzioni.view.impostazioni import impostazioni


@impostazioni.route("/impostazioni")
@login_required
@role_required("impostazioni.write")
def main():
    return render_template(
        "impostazioni.html",
        configurazione=configurazione,
    )


@impostazioni.route("/impostazioni/utenti")
@login_required
@role_required("impostazioni.write")
def gestione_utenti():
    lista_utenti = [(u.email, u.ruolo.nome) for u in utenti]
    return render_template(
        "gestione_impostazioni/utenti.html",
        configurazione=configurazione,
        utenti=lista_utenti,
    )


@impostazioni.route("/impostazioni/docenti")
@login_required
@role_required("impostazioni.write")
def gestione_docenti():
    lista_docenti = [
        (d["nome"], d["cognome"]) for d in Docente.load() if not d["cancellato"]
    ]
    return render_template(
        "gestione_impostazioni/docenti.html",
        configurazione=configurazione,
        docenti=lista_docenti,
    )


@impostazioni.route("/impostazioni/classi")
@login_required
@role_required("impostazioni.write")
def gestione_classi():
    lista_classi = [
        (c["nome"], c["aule_ospitanti"]) for c in Classe.load() if not c["cancellato"]
    ]
    lista_aule = [a["numero"] for a in Aula.load() if not a["cancellato"]]
    return render_template(
        "gestione_impostazioni/classi.html",
        configurazione=configurazione,
        classi=lista_classi,
        aule=lista_aule,
    )


@impostazioni.route("/impostazioni/aule")
@login_required
@role_required("impostazioni.write")
def gestione_aule():
    lista_aule = [(a["numero"], a["piano"]) for a in Aula.load() if not a["cancellato"]]
    return render_template(
        "gestione_impostazioni/aule.html",
        configurazione=configurazione,
        aule=lista_aule,
    )


@impostazioni.route("/impostazioni/ore")
@login_required
@role_required("impostazioni.write")
def gestione_ore():
    lista_ore = [
        (o["numero"], [o["ora_inizio_default"], o["ora_fine_default"]])
        for o in OraPredefinita.load()
    ]
    return render_template(
        "gestione_impostazioni/ore.html", configurazione=configurazione, ore=lista_ore
    )


@impostazioni.route("/impostazioni/note")
@login_required
@role_required("impostazioni.write")
def gestione_note():
    note = [n["testo"] for n in NotaStandard.load()]
    return render_template(
        "gestione_impostazioni/note.html", configurazione=configurazione, note=note
    )


@impostazioni.route("/reboot")
@login_required
@role_required("impostazioni.write")
def reboot():
    return render_template(
        "updater.html",
        version=updater.version,
        configurazione=configurazione,
        reboot=True,
    )


@impostazioni.route("/update")
@login_required
@role_required("impostazioni.write")
def update():
    return render_template(
        "updater.html",
        version=updater.version,
        configurazione=configurazione,
        reboot=False,  # indica semplicemente che non è la pagina di reboot
    )


@impostazioni.route("/version")
def version():
    return updater.version


@impostazioni.route("/log")
# @login_required
# @role_required("impostazioni.write")
def log():
    logdata = open(file, "r").read()

    log_entries = []
    for line in logdata.splitlines()[-200:]:
        match = re.match(
            r"^(?P<level>\w+) - (?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<module>[\w\.]+) - (?P<message>.+)$",
            line,
        )
        if match:
            level = match.group("level")
            datetime_str = match.group("datetime")
            module = match.group("module")
            message = match.group("message")
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S,%f")
            log_entries.append((level, datetime_obj, module, message))

    return render_template("log.html", log=log_entries)
