import logging
import subprocess
import os
from flask_socketio import emit

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.importer import Docenti
from sostituzioni.model.model import Utente
from sostituzioni.model.auth import login_required, role_required, utenti
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


@socketio.on("server reboot", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def reboot():
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


@socketio.on("server update", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def update():
    rootpath = configurazione.get("rootpath").path

    # "/sostituzioni/sostituzioni", git è un livello più alto
    repopath = rootpath.parent

    os.chdir(repopath)
    subprocess.check_call(["/usr/bin/git", "pull"])
    os.chdir(rootpath)
    reboot()


@socketio.on("importa docenti", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def importa_docenti(file_bytearray):
    Docenti.from_buffer(file_bytearray)


@socketio.on("modifica utente", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_utente(dati):
    # inserimento nuovo utente
    if dati["email"] == "":
        try:
            utente = Utente(dati["new_email"], dati["ruolo"])
            utente.inserisci()
            utenti.append(utente)
        except ValueError as e:
            emit("modifica utente errore", {"email": dati["email"], "error": str(e)})
            return

    # modifica utente esistente
    else:
        try:
            utente = utenti.get(dati["email"])
            utente.modifica({"email": dati["new_email"], "ruolo": dati["ruolo"]})
        except ValueError as e:
            emit("modifica utente errore", {"email": dati["email"], "error": str(e)})
            return

    emit("modifica utente successo", dati)


@socketio.on("elimina utente", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_utente(email):
    if email == "":
        emit("elimina utente successo", "")
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
