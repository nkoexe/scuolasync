import logging
import subprocess
import os
import re
from datetime import datetime, timedelta
from flask_socketio import emit

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.cron import scheduler
from sostituzioni.control.importer import Docenti
from sostituzioni.model.model import Utente
from sostituzioni.model.auth import (
    login_required,
    role_required,
    current_user,
    utenti,
    load_utenti,
)
from sostituzioni.view import socketio


logger = logging.getLogger(__name__)


@socketio.on("applica impostazioni", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def applica(dati):
    logger.debug(f"ricevuto: {dati}")

    try:
        configurazione.aggiorna(dati)
    except ValueError as e:
        emit("applica impostazioni errore", str(e))

    emit("applica impostazioni successo")


@socketio.on("importa docenti", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def importa_docenti(file_bytearray):
    Docenti.from_buffer(file_bytearray)


# //////////////////////////////


@socketio.on("check update", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def check_update():
    rootpath = configurazione.get("rootpath").path

    # "/sostituzioni/sostituzioni", git è un livello più alto
    repopath = rootpath.parent

    try:
        new_version = (
            subprocess.run(
                configurazione.shell_commands["check_update"],
                cwd=repopath,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .split("\t")[0]
            .strip()
        )
    except Exception as e:
        logger.error(f"Errore durante il controllo dell'aggiornamento: {e}")
        emit("check update errore", str(e))
        return

    if new_version == configurazione.get("version").valore:
        aggiornamento = False
    else:
        aggiornamento = True

    emit("check update successo", {"value": aggiornamento})


@socketio.on("update", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def update():
    rootpath = configurazione.get("rootpath").path

    # "/sostituzioni/sostituzioni", git è un livello più alto
    repopath = rootpath.parent

    subprocess.run(configurazione.shell_commands["update"], cwd=repopath)

    reboot()


@socketio.on("reboot", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def reboot():
    subprocess.Popen(configurazione.shell_commands["reboot"], cwd=os.getcwd())


# //////////////////////////////


@socketio.on("modifica utente", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_utente(dati):
    """
    dati = {
        "email": <email> (str),
        "new_email": <email> (str),
        "ruolo": visualizzatore | editor | amministratore (str),
    }
    """

    email = dati["email"].lower().strip()
    new_email = dati["new_email"].lower().strip()
    ruolo = dati["ruolo"]

    if email == current_user.email:
        emit(
            "modifica utente errore",
            {
                "email": email,
                "error": "Non è possibile modificare l'utente attualmente in uso. Eseguire il login con un altro account.",
            },
        )
        return

    if new_email == "":
        emit(
            "modifica utente errore",
            {"email": email, "error": "Inserire un indirizzo email."},
        )
        return

    # Se l'email è la stessa, l'utente sta cercando di modificare il ruolo
    if utenti.get(new_email) and new_email != email:
        emit(
            "modifica utente errore",
            {"email": email, "error": "Questo indirizzo email è già in uso."},
        )
        return

    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", new_email):
        emit(
            "modifica utente errore",
            {"email": email, "error": f"L'indirizzo '{new_email}' non è valido."},
        )
        return

    # inserimento nuovo utente
    if email == "":
        try:
            utente = Utente(new_email, ruolo)
            utente.inserisci()
            utenti.append(utente)
        except ValueError as e:
            emit("modifica utente errore", {"email": email, "error": str(e)})
            return

    # modifica utente esistente
    else:
        try:
            utente = utenti.get(email)
            utente.modifica({"email": new_email, "ruolo": ruolo})
        except ValueError as e:
            emit("modifica utente errore", {"email": email, "error": str(e)})
            return

    emit("modifica utente successo", dati)


@socketio.on("elimina utente", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_utente(email):
    if email == "":
        emit("elimina utente successo", "")
        return

    if email == current_user.email:
        emit(
            "elimina utente errore",
            {
                "email": email,
                "error": "Non è possibile eliminare l'utente attualmente in uso. Eseguire il login con un altro account.",
            },
        )
        return

    utente = utenti.get(email)

    if not utente:
        emit("elimina utente errore", {"email": email, "error": "Utente non trovato"})
        return

    try:
        utente.elimina()
        utenti.remove(utente)
    except Exception as e:
        emit("elimina utente errore", {"email": email, "error": str(e)})
        return

    logger.debug(f"utente {email} eliminato")

    emit("elimina utente successo", email)


@socketio.on("elimina tutti utenti", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_tutti_utenti():
    def actually_elimina(email_da_mantenere: list):
        try:
            # elimina tutti gli utenti dal database
            Utente.elimina_tutti(email_da_mantenere)
            # rigenera la lista di utenti
            load_utenti()
        except Exception as e:
            logger.error(f"Errore durante l'eliminazione di tutti gli utenti: {e}")

    scheduler.add_job(
        actually_elimina,
        "date",
        run_date=datetime.now() + timedelta(seconds=10),
        args=[[current_user.email]],
        id="eliminazione_utenti",
        replace_existing=True,
        max_instances=1,
    )

    emit("elimina tutti utenti in corso", 10)
    logger.debug(
        "Eliminazione di tutti gli utenti iniziata. L'utente ha 10 secondi per annullare l'operazione"
    )


@socketio.on("elimina tutti utenti annulla", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_tutti_utenti_annulla():
    scheduler.remove_job("eliminazione_utenti")
    emit("elimina tutti utenti annulla successo", "")
    logger.debug("Eliminazione di tutti gli utenti annullata.")


# //////////////////////////////
