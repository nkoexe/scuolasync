from flask import render_template

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.auth import login_required, role_required, utenti
from sostituzioni.model.model import Aula, Docente, NotaStandard
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
    lista_utenti = [(u.email, u.ruolo.nome) for u in utenti]
    return render_template("gestione_impostazioni/utenti.html", utenti=lista_utenti)


@impostazioni.route("/impostazioni/docenti")
@login_required
@role_required("impostazioni.write")
def gestione_docenti():
    lista_docenti = [
        (d["nome"], d["cognome"]) for d in Docente.load() if not d["cancellato"]
    ]
    return render_template("gestione_impostazioni/docenti.html", docenti=lista_docenti)


@impostazioni.route("/impostazioni/classi")
@login_required
@role_required("impostazioni.write")
def gestione_classi():
    return render_template("gestione_impostazioni/classi.html")


@impostazioni.route("/impostazioni/aule")
@login_required
@role_required("impostazioni.write")
def gestione_aule():
    lista_aule = [(a["numero"], a["piano"]) for a in Aula.load() if not a["cancellato"]]
    return render_template("gestione_impostazioni/aule.html", aule=lista_aule)


@impostazioni.route("/impostazioni/ore")
@login_required
@role_required("impostazioni.write")
def gestione_ore():
    return render_template("gestione_impostazioni/ore.html")


@impostazioni.route("/impostazioni/note")
@login_required
@role_required("impostazioni.write")
def gestione_note():
    note = [n["testo"] for n in NotaStandard.load()]
    return render_template("gestione_impostazioni/note.html", note=note)


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
                "1000",
                "--no-pager",
            ],
            stderr=subprocess.STDOUT,
        )
        .decode("utf-8")
        .replace("\n", "<br>")
    )
