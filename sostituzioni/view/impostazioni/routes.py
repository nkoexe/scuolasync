from flask import render_template

from sostituzioni.control.configurazione import configurazione
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
def reboot():
    return render_template(
        "updater.html",
        version=configurazione.get("version").valore,
        reboot=True,
    )


@impostazioni.route("/update")
@login_required
@role_required("impostazioni.write")
def update():
    return render_template(
        "updater.html",
        version=configurazione.get("version").valore,
        reboot=False,  # indica semplicemente che non è la pagina di reboot
    )


@impostazioni.route("/version")
def version():
    return configurazione.get("version").valore


@impostazioni.route("/log")
@login_required
@role_required("impostazioni.write")
def log():
    import subprocess

    return (
        subprocess.check_output(
            [
                "/usr/bin/journalctl",
                "--output",
                "cat",
                "-u",
                "sostituzioni",
                "-n",
                "2000",
                "--no-pager",
            ],
            stderr=subprocess.STDOUT,
        )
        .decode("utf-8")
        .replace("\n", "<br>")
    )
