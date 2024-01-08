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


@impostazioni.route("/update")
@login_required
@role_required("impostazioni.write")
def update():
    rootpath = configurazione.get("rootpath").path

    # "/sostituzioni/sostituzioni", git è un livello più alto
    repopath = rootpath.parent

    import os, subprocess

    os.chdir(repopath)
    subprocess.check_call(["/usr/bin/git", "pull"])
    os.chdir(rootpath)

    if os.name == "nt":
        subprocess.check_call(
            [
                "cmd",
                "/c",
                str(configurazione.get("scriptsdir").path / "reboot.bat"),
                os.getpid(),
            ]
        )
    else:
        subprocess.check_call(
            [
                "/bin/bash",
                str(configurazione.get("scriptsdir").path / "reboot.sh"),
                "&",
                "disown",
            ]
        )

    return "Updating////////"


@impostazioni.route("/log")
@login_required
@role_required("impostazioni.write")
def log():
    import subprocess

    return subprocess.check_output(
        ["/usr/bin/journalctl", "-u", "sostituzioni", "-n", "1000", "--no-pager"]
    )
