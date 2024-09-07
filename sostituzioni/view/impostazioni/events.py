import logging
import subprocess
import os
import re
from datetime import datetime, timedelta
from flask import url_for
from flask_socketio import emit

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.cron import scheduler
from sostituzioni.control.importer import Docenti
from sostituzioni.model.model import (
    Aula,
    Classe,
    Docente,
    OraPredefinita,
    NotaStandard,
    Utente,
)
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


@socketio.on("carica file", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def carica_file(dati):
    logger.debug(f"ricevuto: {dati}")

    ext = dati["name"].split(".")[-1]

    if dati["id"] == "schoolmainlogo":
        file_name = "logo." + ext
        file_path = "images/" + file_name
        file = configurazione.get("flaskstaticdir").path / file_path

    elif dati["id"] == "schoolheaderlogo":
        file_name = "logo_white." + ext
        file_path = "images/" + file_name
        file = configurazione.get("flaskstaticdir").path / file_path

    else:
        emit("carica file errore", "id opzione non valido")
        return

    try:
        file.write_bytes(dati["data"])
        configurazione.set(dati["id"], file_path)
    except ValueError as e:
        emit("carica file errore", str(e))
        return

    emit(
        "carica file successo",
        {"id": dati["id"], "path": url_for("static", filename=file_path)},
    )


# //////////////////////////////


@socketio.on("check update", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def check_update():

    try:
        aggiornamento = configurazione.check_update()
    except Exception as e:
        emit("check update errore", str(e))
        return

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

    # Se l'email inserita è diversa da quella attualmente in uso e questa esiste
    # già nel database, avvisare, ma se le mail sono le stesse allora l'utente
    # sta cercando di modificare il ruolo
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


@socketio.on("modifica docente", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_docente(dati):
    """
    dati = {
        "nome": (str),
        "cognome": (str),
        "new_nome": (str),
        "new_cognome": (str)
    }
    """

    nome = dati["nome"].strip()
    cognome = dati["cognome"].strip()
    new_nome = dati["new_nome"].strip()
    new_cognome = dati["new_cognome"].strip()

    if new_nome == "":
        emit(
            "modifica docente errore",
            {"nome": nome, "cognome": cognome, "error": "Inserire un nome valido"},
        )
        return

    if new_cognome == "":
        emit(
            "modifica docente errore",
            {"nome": nome, "cognome": cognome, "error": "Inserire un cognome valido"},
        )
        return

    if Docente.trova(new_cognome + " " + new_nome):
        emit(
            "modifica docente errore",
            {"nome": nome, "cognome": cognome, "error": "Questo docente esiste già"},
        )
        return

    # inserimento nuovo docente
    if nome == "":
        try:
            docente = Docente(new_nome, new_cognome)
            docente.inserisci()
        except Exception as e:
            emit(
                "modifica docente errore",
                {"nome": nome, "cognome": cognome, "error": str(e)},
            )
            return

    # modifica docente esistente
    else:
        try:
            docente = Docente(nome, cognome)
            docente.modifica({"cognome": new_cognome, "nome": new_nome})
        except Exception as e:
            emit(
                "modifica docente errore",
                {"nome": nome, "cognome": cognome, "error": str(e)},
            )
            return

    emit("modifica docente successo", dati)


@socketio.on("elimina docente", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_docente(nome, cognome):
    if nome == "":
        emit("elimina docente successo", "")
        return

    docente = Docente(nome, cognome)

    if not docente.in_database:
        emit(
            "elimina docente errore",
            {"nome": nome, "cognome": cognome, "error": "Docente non trovato"},
        )
        return

    try:
        docente.elimina()
    except Exception as e:
        emit(
            "elimina docente errore",
            {"nome": nome, "cognome": cognome, "error": str(e)},
        )
        return

    logger.debug(f"docente {nome} {cognome} eliminato")

    emit("elimina docente successo", {"nome": nome, "cognome": cognome})


@socketio.on("elimina tutti docenti", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_tutti_docenti():
    def actually_elimina():
        try:
            Docente.elimina_tutti()
        except Exception as e:
            logger.error(f"Errore durante l'eliminazione di tutti i docenti: {e}")

    scheduler.add_job(
        actually_elimina,
        "date",
        run_date=datetime.now() + timedelta(seconds=10),
        id="eliminazione_docenti",
        replace_existing=True,
        max_instances=1,
    )

    emit("elimina tutti docenti in corso", 10)
    logger.debug(
        "Eliminazione di tutti i docenti iniziata. L'utente ha 10 secondi per annullare l'operazione"
    )


@socketio.on("elimina tutti docenti annulla", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_tutti_docenti_annulla():
    scheduler.remove_job("eliminazione_docenti")
    emit("elimina tutti docenti annulla successo", "")
    logger.debug("Eliminazione di tutti i docenti annullata.")


@socketio.on("importa docenti", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def importa_docenti(data):
    file_type = data["type"]
    file_bytearray = data["data"]
    res = Docenti.from_buffer(file_bytearray, file_type)
    emit("importa docenti risultato", res)


# //////////////////////////////


@socketio.on("modifica nota", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_nota(dati):
    """
    dati = {
        "testo": (str),
        "new_testo": (str)
    }
    """

    testo = dati["testo"].strip()
    new_testo = dati["new_testo"].strip()

    if new_testo == "":
        emit(
            "modifica nota errore",
            {"testo": testo, "error": "Inserire un testo valido"},
        )
        return

    if NotaStandard.trova(new_testo):
        emit(
            "modifica nota errore",
            {"testo": testo, "error": "Questa nota esiste già"},
        )
        return

    # inserimento nuova nota
    if testo == "":
        try:
            nota = NotaStandard(new_testo)
            nota.inserisci()
        except Exception as e:
            emit("modifica nota errore", {"testo": testo, "error": str(e)})
            return

    # modifica nota esistente
    else:
        try:
            nota = NotaStandard(testo)
            nota.modifica({"testo": new_testo})
        except Exception as e:
            emit("modifica nota errore", {"testo": testo, "error": str(e)})
            return

    emit("modifica nota successo", dati)


@socketio.on("elimina nota", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_nota(testo):
    if testo == "":
        emit("elimina nota successo", "")
        return

    nota = NotaStandard(testo)

    if not nota.in_database:
        emit("elimina nota errore", {"testo": testo, "error": "Nota non trovata"})
        return

    try:
        nota.elimina()
    except Exception as e:
        emit("elimina nota errore", {"testo": testo, "error": str(e)})
        return

    logger.debug(f"nota {testo} eliminata")

    emit("elimina nota successo", testo)


# //////////////////////////////


@socketio.on("modifica aula", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_aula(dati):
    """
    dati = {
        "numero_aula": (str),
        "new_numero_aula": (str),
        "new_piano_aula": (str)
    }
    """

    numero_aula = dati["numero_aula"].strip()
    new_numero_aula = dati["new_numero_aula"].strip()
    new_piano_aula = dati["new_piano_aula"].strip()

    if new_piano_aula == "":
        new_piano_aula = 0

    if new_numero_aula == "":
        emit(
            "modifica aula errore",
            {"numero_aula": numero_aula, "error": "Inserire un valido numero di aula"},
        )
        return

    if Aula.trova(new_numero_aula) and new_numero_aula != numero_aula:
        emit(
            "modifica aula errore",
            {"numero_aula": numero_aula, "error": "Questa aula esiste già"},
        )
        return

    # inserimento nuova aula
    if numero_aula == "":
        try:
            aula = Aula(new_numero_aula, new_piano_aula)
            aula.inserisci()
        except Exception as e:
            emit("modifica aula errore", {"numero_aula": numero_aula, "error": str(e)})
            return
    else:
        try:
            aula = Aula(numero_aula)
            aula.modifica({"numero": new_numero_aula, "piano": new_piano_aula})
        except Exception as e:
            emit("modifica aula errore", {"numero_aula": numero_aula, "error": str(e)})
            return

    emit("modifica aula successo", dati)


@socketio.on("elimina aula", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_aula(numero_aula):
    if numero_aula == "":
        emit("elimina aula successo", "")
        return

    aula = Aula(numero_aula)

    if not aula.in_database:
        emit(
            "elimina aula errore",
            {"numero_aula": numero_aula, "error": "Aula non trovata"},
        )
        return

    try:
        aula.elimina()
    except Exception as e:
        emit("elimina aula errore", {"numero_aula": numero_aula, "error": str(e)})
        return

    logger.debug(f"aula {numero_aula} eliminata")

    emit("elimina aula successo", numero_aula)


# //////////////////////////////


@socketio.on("modifica classe", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_classe(dati):
    """
    dati = {
        "nome": (str),
        "new_nome": (str),
        "new_aule": (list),
    }
    """

    nome = dati["nome"].strip()
    new_nome = dati["new_nome"].strip()
    aule_ospitanti = dati["new_aule"]

    if new_nome == "":
        emit(
            "modifica classe errore",
            {"nome": nome, "error": "Inserire un nome valido"},
        )
        return

    if not isinstance(aule_ospitanti, list):
        emit(
            "modifica classe errore",
            {"nome": nome, "error": "Inserire una lista di aule valide"},
        )
        return

    if Classe.trova(new_nome) and new_nome != nome:
        emit(
            "modifica classe errore",
            {"nome": nome, "error": "Questa classe esiste già"},
        )
        return

    # inserimento nuova classe
    if nome == "":
        try:
            classe = Classe(new_nome, aule_ospitanti)
            classe.inserisci()
        except Exception as e:
            emit(
                "modifica classe errore",
                {"nome": nome, "error": str(e)},
            )
            return

    # modifica classe esistente
    else:
        try:
            classe = Classe(nome)
            classe.modifica({"nome": new_nome, "aule_ospitanti": aule_ospitanti})
        except Exception as e:
            emit(
                "modifica classe errore",
                {"nome": nome, "error": str(e)},
            )
            return

    emit("modifica classe successo", dati)


@socketio.on("elimina classe", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_classe(nome_classe):
    if nome_classe == "":
        emit("elimina classe successo", "")
        return

    classe = Classe(nome_classe)

    if not classe.in_database:
        emit(
            "elimina classe errore",
            {"nome_classe": nome_classe, "error": "Classe non trovata"},
        )
        return

    try:
        classe.elimina()
    except Exception as e:
        emit(
            "elimina classe errore",
            {"nome_classe": nome_classe, "error": str(e)},
        )
        return

    emit("elimina classe successo", nome_classe)


# //////////////////////////////


@socketio.on("modifica ora", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def modifica_ora(dati):
    """
    dati = {
        "numero": (str),
        "new_numero": (str),
        "new_ora_inizio": (str),
        "new_ora_fine": (str)
    }
    """

    numero = dati["numero"].strip()
    new_numero = dati["new_numero"].strip()
    new_ora_inizio = dati["new_ora_inizio"].strip()
    new_ora_fine = dati["new_ora_fine"].strip()

    if not new_numero:
        emit(
            "modifica ora errore",
            {"numero": numero, "error": "Inserire un numero valido"},
        )
        return

    if not new_ora_inizio:
        emit(
            "modifica ora errore",
            {"numero": numero, "error": "Inserire un orario valido"},
        )
        return

    if not new_ora_fine:
        emit(
            "modifica ora errore",
            {"numero": numero, "error": "Inserire un orario valido"},
        )
        return

    if new_numero != numero and OraPredefinita.trova(new_numero):
        emit(
            "modifica ora errore",
            {"numero": numero, "error": "Questa ora predefinita esiste già"},
        )
        return

    # inserimento nuova ora
    if numero == "":
        try:
            ora = OraPredefinita(new_numero, new_ora_inizio, new_ora_fine)
            ora.inserisci()
        except Exception as e:
            emit("modifica ora errore", {"numero": numero, "error": str(e)})
            return

    # modifica ora esistente
    else:
        try:
            ora = OraPredefinita(numero)
            ora.modifica(
                {
                    "numero": new_numero,
                    "ora_inizio": new_ora_inizio,
                    "ora_fine": new_ora_fine,
                }
            )
        except Exception as e:
            emit("modifica ora errore", {"numero": numero, "error": str(e)})
            return

    emit("modifica ora successo", dati)


@socketio.on("elimina ora", namespace="/impostazioni")
@login_required
@role_required("impostazioni.write")
def elimina_ora(numero):
    if numero == "":
        emit("elimina ora successo", "")
        return

    ora = OraPredefinita(numero)

    if not ora.in_database:
        emit("elimina ora errore", {"numero": numero, "error": "Ora non trovata"})
        return

    try:
        ora.elimina()
    except Exception as e:
        emit("elimina ora errore", {"numero": numero, "error": str(e)})
        return

    logger.debug(f"ora {numero} eliminata")

    emit("elimina ora successo", numero)
