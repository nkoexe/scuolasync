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

from secrets import token_hex
from flask import Flask
from os import environ

try:
    from sostituzioni.control.configurazione import configurazione
except FileNotFoundError:
    environ["SCUOLASYNC_SETUP"] = "1"

    # reimport the module loading the default config file
    from sostituzioni.control.configurazione import configurazione

try:
    import sostituzioni.control.database
except FileNotFoundError:
    environ["SCUOLASYNC_SETUP"] = "2"

    # reimport the module creating the database first
    import sostituzioni.control.database


from sostituzioni.control.cli import database_cli, importer_cli, backup_cli
import sostituzioni.control.cron

app = Flask(__name__)

# File statici - css, js, icone
app.static_folder = configurazione.get("flaskstaticdir").path
# Template html
app.template_folder = configurazione.get("flasktemplatedir").path


# 0 = In produzione
# 1 = In manutenzione
# 2 = In sviluppo
sysstate = configurazione.get("sysstate")

# Debug se in manutenzione o in sviluppo
app.config["DEBUG"] = sysstate >= 1
# Testing se in sviluppo
app.config["TESTING"] = sysstate >= 2

# Se la secret key non è stata impostata, genera una casuale
app.config["SECRET_KEY"] = configurazione.get("flasksecretkey") or token_hex(32)

# Impostazioni di sessione
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 6 * 60 * 60

# Timeout della sessione, in minuti
session_lifetime = configurazione.get("flasksessionlifetime")
if session_lifetime == -1:
    # disabilita il logout automatico
    # o almeno facciamo finta
    session_lifetime = 60 * 60 * 24 * 365 * 10
app.config["PERMANENT_SESSION_LIFETIME"] = session_lifetime * 60

# il countdown viene ripristinato ad ogni richiesta
# ! attenzione, non si applica a socketio, soltanto a richieste http
app.config["SESSION_REFRESH_EACH_REQUEST"] = True


# Comandi per controllo da terminale
app.cli.add_command(database_cli)
app.cli.add_command(importer_cli)
app.cli.add_command(backup_cli)
