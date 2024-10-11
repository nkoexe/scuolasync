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

from flask import render_template, request, redirect, url_for, send_file
from io import BytesIO
import qrcode
from qrcode.image.pure import PyPNGImage

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view.visualizzazionefisica import fisica


@fisica.route("/")
def index():
    authcodes = configurazione.get("displayauthcodes")
    if request.args.get("code") in authcodes or not authcodes:
        return render_template("display.html", configurazione=configurazione)

    return redirect(url_for("auth.login"))


@fisica.route("/qr")
def generate_qrcode():
    url = request.url_root
    img_bytes = BytesIO()
    img = qrcode.make(
        url,
        image_factory=PyPNGImage,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    img.save(img_bytes)
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype="image/png")
