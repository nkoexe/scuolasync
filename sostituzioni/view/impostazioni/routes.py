from flask import render_template
import os, subprocess

from sostituzioni.control.configurazione import configurazione
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
    )


@impostazioni.route("/impostazioni/utenti")
@login_required
@role_required("impostazioni.write")
def gestione_utenti():
    from sostituzioni.model.auth import utenti

    lista_utenti = [(u.email, u.ruolo.nome) for u in utenti]
    return render_template("gestione_utenti.html", utenti=lista_utenti)


@impostazioni.route("/reboot")
@login_required
@role_required("impostazioni.write")
def reboot(render: bool = True):
    if os.name == "nt":
        subprocess.Popen(
            [
                "cmd",
                "/c",
                str(configurazione.get("scriptsdir").path / "reboot.bat"),
                str(os.getpid()),
            ]
        )
    else:
        subprocess.Popen(
            ["/bin/bash", str(configurazione.get("scriptsdir").path / "reboot.sh")]
        )

    if not render:
        return

    return render_template("reboot.html", operazione="Riavvio")


@impostazioni.route("/update")
@login_required
@role_required("impostazioni.write")
def update():
    rootpath = configurazione.get("rootpath").path

    # "/sostituzioni/sostituzioni", git è un livello più alto
    repopath = rootpath.parent

    os.chdir(repopath)

    if os.name == "nt":
        subprocess.check_call(
            ["cmd", "/c", str(configurazione.get("scriptsdir").path / "update.bat")]
        )
    else:
        subprocess.check_call(
            ["/bin/bash", str(configurazione.get("scriptsdir").path / "update.sh")]
        )

    os.chdir(rootpath)

    reboot(render=False)

    return render_template("reboot.html", operazione="Aggiornamento")


@impostazioni.route("/log")
@login_required
@role_required("impostazioni.write")
def log():
    import subprocess

    return subprocess.check_output(
        ["/usr/bin/journalctl", "-u", "sostituzioni", "-n", "1000", "--no-pager"]
    )
