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

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view import app


# @app.route("/crediti")
# def crediti():
#     return render_template("crediti.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", configurazione=configurazione)


@app.route("/license")
@app.route("/licenze")
def licenze():
    return render_template("licenze.html", configurazione=configurazione)
