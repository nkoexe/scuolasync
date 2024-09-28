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

from random import choice

from flask import render_template, redirect, url_for

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import current_user
from sostituzioni.view import app


@app.route("/offline")
def offline():
    support_email = configurazione.get("supportemail")

    return render_template(
        "error.html",
        code="////",
        offline=True,
        support_email=support_email,
    )


@app.errorhandler(404)
def not_found(e):
    if current_user.is_authenticated:
        homepage = url_for("online.index")

        description = choice(
            [
                "Non preoccuparti, succede ai migliori. Torna alla {homepage} o riprova.",
                "Sembra che questa pagina sia scappata. Torna alla {homepage} e vediamo se riusciamo a ritrovarla.",
                "Questa pagina ha deciso di prendersi una pausa. Torna alla {homepage} per continuare a navigare.",
                "La pagina che cerchi sembra essere sparita nel nulla. Forse la {homepage} può aiutarti.",
                "Sembra che questa pagina si sia nascosta bene. Forse la {homepage} può aiutarti.",
                "La pagina che cerchi è attualmente in vacanza. Forse la {homepage} può aiutarti.",
                "Ho controllato due volte, ma non c'è nulla qui. Forse la {homepage} può aiutarti.",
                "Hai trovato la tana del Bianconiglio, ma senza Bianconiglio. Torna alla {homepage} per vedere cos'altro c'è nel Paese delle Meraviglie.",
                "Hai trovato un angolo nascosto di Internet. Torniamo alla {homepage}?",
                "Sei in un vicolo cieco digitale. Torna alla {homepage} per riprendere la retta via.",
                "Questa pagina è in gita scolastica. Forse la {homepage} può aiutarti.",
                "Questa pagina ha firmato un'uscita anticipata. Forse la {homepage} può aiutarti.",
            ]
        )

        description = description.format(homepage=f'<a href="{homepage}">Homepage</a>')

        return (
            render_template(
                "error.html", code=404, title="Non trovato.", description=description
            ),
            404,
        )

    return redirect(url_for("auth.login"))


@app.errorhandler(500)
def internal_error(e):
    support_email = configurazione.get("supportemail")

    return (
        render_template(
            "error.html",
            code=500,
            title="Errore interno.",
            description=f"Qualquadra non cosa. Contatta <a href='mailto:{support_email}'>{support_email}</a> e descrivi cosa è successo: potresti aver scovato un errore nel codice.",
        ),
        500,
    )


@app.errorhandler(401)
def unauthorized(e):
    if current_user.is_authenticated:
        return (
            render_template(
                "error.html",
                code=401,
                title="Non autorizzato.",
                description="Non hai accesso a questa pagina. Hai fatto il login con l'account {current_user.id}, prova con un altro account.",
            ),
            401,
        )
    else:
        return redirect(url_for("auth.login"))
