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

import logging
from flask import render_template, redirect, url_for, request, flash

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import (
    current_user,
    login_manager,
    login_required,
    sso_login,
    logout_user,
    SSO_REQ_URI,
)
from sostituzioni.view.auth import auth


logger = logging.getLogger(__name__)


@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("online.index"))

    # 3 lines of development speedup, remove in production pls ty
    from sostituzioni.model.auth import authenticate_user

    authenticate_user("niccolo.rag@gmail.com")
    # authenticate_user("bidelleria@gandhimerano.com")
    return redirect(url_for("online.index"))

    # flash("Questo account non è autorizzato all'accesso al sistema.")
    # flash("Autenticazione annullata.")

    return render_template(
        "login.html",
        configurazione=configurazione,
    )


@auth.route("/sso")
def ssoredirect():
    return redirect(SSO_REQ_URI)


@auth.route("/loginredirect")
def loginredirect():
    """Richiesta di autorizzazione dopo l'autenticazione con Google"""

    authenticated = sso_login(request)

    if authenticated:
        return redirect(url_for("online.index"))
    else:
        return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
