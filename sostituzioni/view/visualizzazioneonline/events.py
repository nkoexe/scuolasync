import logging
from flask_socketio import emit

from sostituzioni.model.model import (
    Aula,
    Classe,
    Docente,
    OraPredefinita,
    Sostituzione,
    Evento,
    Notizia,
)
from sostituzioni.model.auth import (
    login_required,
    role_required,
    logout_user,
    current_user,
)
from sostituzioni.view import socketio

logger = logging.getLogger(__name__)


@socketio.on("connect")
@login_required
def connect():
    logger.debug("Nuovo client connesso, invio dei dati iniziali.")

    emit("lista aule", Aula.load())
    emit("lista classi", Classe.load())
    emit("lista docenti", Docente.load())
    emit("lista ore predefinite", OraPredefinita.load())
    richiesta_notizie()
    richiesta_eventi()
    richiesta_sostituzioni({"pubblicato": False})


@socketio.on("disconnect")
def disconnect():
    #! does not work at the moment
    logout_user()


@socketio.on("richiesta sostituzioni")
@login_required
def richiesta_sostituzioni(filtri: dict | None = None):
    """
    filtri:
    { cancellato: true }  // per mostrare anche sostituzioni cancellate
    { pubblicato: false }  // per mostrare anche sostituzioni non pubblicate
    { data_inizio: 1702767600, data_fine: 1702854000 }  // per sostituzioni comprese in un intervallo
    { data_inizio: 1702767600, data_fine: None }  // per sostituzioni future
    """

    logger.debug(f"Ricevuto segnale richiesta sostituzioni con filtri: {filtri}")

    # check if user has necessary permissions for non default view
    if "cancellato" in filtri and not current_user.permessi.sostituzioni.write:
        filtri.pop("cancellato")
    if "pubblicato" in filtri and not current_user.permessi.sostituzioni.write:
        filtri.pop("pubblicato")

    emit("lista sostituzioni", Sostituzione.load(filtri))


@socketio.on("richiesta eventi")
@login_required
def richiesta_eventi(filtri: dict | None = None):
    """
    filtri:
    { cancellato: true }  // per mostrare anche eventi cancellati
    { data_inizio: 1702767600, data_fine: 1702854000 }  // per eventi compresi in un intervallo
    { data_inizio: 1702767600, data_fine: None }  // per eventi futuri
    """

    logger.debug(f"Ricevuto segnale richiesta eventi con filtri: {filtri}")

    emit("lista eventi", Evento.load(filtri))


@socketio.on("richiesta notizie")
@login_required
def richiesta_notizie(filtri: dict | None = None):
    """
    Todo:
    decidere come far filtrare notizie, se per data o se aggiungere pulsante 'tutte' idk
    """

    logger.debug(f"Ricevuto segnale richiesta notizie con filtri: {filtri}")
    emit("lista notizie", Notizia.load(filtri))


# ////////////////////////////////////


@socketio.on("nuova sostituzione")
@login_required
@role_required("sostituzioni.write")
def nuova_sostituzione(data):
    logger.debug(f"Ricevuto dati per inserimento nuova sostituzione: {data}")

    sostituzione = Sostituzione(
        id=None,
        aula=data.get("aula"),
        classe=data.get("classe"),
        docente=data.get("docente"),
        data=data.get("data"),
        ora_inizio=data.get("ora_inizio"),
        ora_fine=data.get("ora_fine"),
        ora_predefinita=data.get("ora_predefinita"),
        note=data.get("note"),
        pubblicato=data.get("pubblicato"),
    )
    sostituzione.inserisci()

    emit("aggiornamento sostituzioni", broadcast=True)
    emit("aggiornamento sostituzioni", broadcast=True, namespace="/display")


@socketio.on("modifica sostituzione")
@login_required
@role_required("sostituzioni.write")
def modifica_sostituzione(data):
    logger.debug(f"Ricevuto dati modifica sostituzione: {data}")

    Sostituzione(id=data.get("id")).modifica(data.get("data"))

    emit("aggiornamento sostituzioni", broadcast=True)
    emit("aggiornamento sostituzioni", broadcast=True, namespace="/display")


@socketio.on("elimina sostituzione")
@login_required
@role_required("sostituzioni.write")
def elimina_sostituzione(data):
    logger.debug(f"Ricevuto segnale eliminazione sostituzione: {data}")

    Sostituzione(data.get("id")).elimina(
        data.get("mantieni_in_storico", True)
    )  # usare default di configurazione

    emit("aggiornamento sostituzioni", broadcast=True)
    emit("aggiornamento sostituzioni", broadcast=True, namespace="/display")


@socketio.on("nuovo evento")
@login_required
@role_required("eventi.write")
def nuovo_evento(data):
    logger.debug(f"Ricevuto dati per inserimento nuovo evento: {data}")

    Evento(
        urgente=data.get("urgente", False),
        data_ora_inizio=data.get("data_ora_inizio"),
        data_ora_fine=data.get("data_ora_fine"),
        testo=data.get("testo"),
    ).inserisci()

    emit("aggiornamento eventi", broadcast=True)
    emit("aggiornamento eventi", broadcast=True, namespace="/display")


@socketio.on("modifica evento")
@login_required
@role_required("eventi.write")
def modifica_evento(data):
    logger.debug(f"Ricevuto dati modifica evento: {data}")

    Evento(id=data.get("id")).modifica(data.get("data"))

    emit("aggiornamento eventi", broadcast=True)
    emit("aggiornamento eventi", broadcast=True, namespace="/display")


@socketio.on("elimina evento")
@login_required
@role_required("eventi.write")
def elimina_evento(data):
    logger.debug(f"Ricevuto segnale eliminazione evento: {data}")

    Evento(data.get("id")).elimina()

    emit("aggiornamento eventi", broadcast=True)
    emit("aggiornamento eventi", broadcast=True, namespace="/display")


@socketio.on("nuova notizia")
@login_required
@role_required("notizie.write")
def nuova_notizia(data: dict):
    logger.debug(f"Ricevuto dati per inserimento nuova notizia: {data}")

    Notizia(
        data_inizio=data.get("data_inizio"),
        data_fine=data.get("data_fine"),
        testo=data.get("testo"),
    ).inserisci()

    emit("aggiornamento notizie", broadcast=True)
    emit("aggiornamento notizie", broadcast=True, namespace="/display")


@socketio.on("modifica notizia")
@login_required
@role_required("notizie.write")
def modifica_notizia(data):
    logger.debug(f"Ricevuto dati modifica notizia: {data}")

    Notizia(id=data.get("id")).modifica(data.get("data"))

    emit("aggiornamento notizie", broadcast=True)
    emit("aggiornamento notizie", broadcast=True, namespace="/display")


@socketio.on("elimina notizia")
@login_required
@role_required("notizie.write")
def elimina_notizia(data):
    logger.debug(f"Ricevuto segnale eliminazione notizia: {data}")

    Notizia(data.get("id")).elimina()

    emit("aggiornamento notizie", broadcast=True)
    emit("aggiornamento notizie", broadcast=True, namespace="/display")
