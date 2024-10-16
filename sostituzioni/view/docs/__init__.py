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

from flask import send_from_directory

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view import app

docsdir = configurazione.get("docsdir").path


@app.route("/docs")
def docs():
    return send_from_directory(docsdir, "index.html")


# @app.route("/docs/<path:path>/sidebar.md")
# def docs_sidebar(path):
#     return send_from_directory(docsdir, "sidebar.md")


@app.route("/docs/<path:path>")
def docs_file(path):
    return send_from_directory(docsdir, path)
