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
    img = qrcode.make(url, image_factory=PyPNGImage, box_size=10, border=0)
    img.save(img_bytes)
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype="image/png")
