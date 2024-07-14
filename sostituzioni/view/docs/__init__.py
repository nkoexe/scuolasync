from flask import send_from_directory

from sostituzioni.control.configurazione import configurazione
from sostituzioni.view import app

docsdir = configurazione.get("docsdir").path


@app.route("/docs")
def docs():
    return send_from_directory(docsdir, "index.html")


@app.route("/docs/<path:path>/sidebar.md")
def docs_sidebar(path):
    return send_from_directory(docsdir, "sidebar.md")


@app.route("/docs/<path:path>")
def docs_file(path):
    return send_from_directory(docsdir, path)
