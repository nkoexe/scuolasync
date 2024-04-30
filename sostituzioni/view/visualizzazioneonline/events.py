import logging
from flask_socketio import emit
from time import time

from sostituzioni.control.exporter import Exporter
from sostituzioni.model.model import (
    Aula,
    Classe,
    Docente,
    OraPredefinita,
    NotaStandard,
    Sostituzione,
    Evento,
    Notizia,
    sostituzioni,
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

    emit("lista ore predefinite", OraPredefinita.load())
    emit("lista note standard", NotaStandard.load())
    emit("lista aule", Aula.load())
    emit("lista classi", Classe.load())
    emit("lista docenti", Docente.load())
    richiesta_notizie()
    richiesta_eventi()
    richiesta_sostituzioni({"non_pubblicato": True})


# @socketio.on("disconnect")
# def disconnect():
#     #! does not work at the moment
#     logout_user()


@socketio.on("auth check")
@login_required
def auth_check():
    return True


@socketio.on("richiesta sostituzioni")
@login_required
def richiesta_sostituzioni(filtri: dict | None = None):
    """
    filtri:
    `{ cancellato: true }`  // per mostrare anche sostituzioni cancellate
    `{ non_pubblicato: true }`  // per mostrare anche sostituzioni non pubblicate
    `{ data_inizio: 1702767600, data_fine: 1702854000 }`  // per sostituzioni comprese in un intervallo
    `{ data_inizio: 1702767600, data_fine: None }`  // per sostituzioni future
    """

    # start_time = time()

    #! fix temporaneo finché non si implementa il filtro per le sostituzioni non pubblicate
    if isinstance(filtri, dict):
        filtri["non_pubblicato"] = True

    logger.debug(f"Ricevuto segnale richiesta sostituzioni con filtri: {filtri}")

    # Check se l'utente ha permessi per visualizzare dati speciali.
    # Il filtro per data è accessibile da tutti
    if "cancellato" in filtri and not current_user.permessi.sostituzioni.write:
        filtri.pop("cancellato")
    if "non_pubblicato" in filtri and not current_user.permessi.sostituzioni.write:
        filtri.pop("non_pubblicato")

    emit("lista sostituzioni", sostituzioni.filtra(filtri))

    # print(f"GET SOSTITUZIONI - {time() - start_time:.6f}")


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

    if filtri is None and current_user.permessi.notizie.write:
        filtri = {"solo_attivo": False}

    emit("lista notizie", Notizia.load(filtri))


# ////////////////////////////////////


@socketio.on("nuova sostituzione")
@login_required
@role_required("sostituzioni.write")
def nuova_sostituzione(data):
    logger.debug(f"Ricevuto dati per inserimento nuova sostituzione: {data}")

    sostituzione = Sostituzione(
        # id=None,
        # aula=data.get("aula"),
        # classe=data.get("classe"),
        # docente=data.get("docente"),
        # data=data.get("data"),
        # ora_inizio=data.get("ora_inizio"),
        # ora_fine=data.get("ora_fine"),
        # ora_predefinita=data.get("ora_predefinita"),
        # note=data.get("note"),
        # pubblicato=data.get("pubblicato"),
        dati=data,
    )
    try:
        sostituzioni.inserisci(sostituzione)
    except Exception as e:
        emit("errore inserimento sostituzione", str(e))
        return

    emit("aggiornamento sostituzioni", broadcast=True)
    emit("aggiornamento sostituzioni", broadcast=True, namespace="/display")


@socketio.on("modifica sostituzione")
@login_required
@role_required("sostituzioni.write")
def modifica_sostituzione(data):
    logger.debug(f"Ricevuto dati modifica sostituzione: {data}")

    id, dati = data.get("id"), data.get("data")

    if not isinstance(id, int) or not isinstance(dati, dict):
        logger.error(
            f"Modifica sostituzione: errore nel formato dei dati ricevuti - id: {id}, dati: {dati}"
        )
        emit("errore modifica sostituzione", "Errore nella modifica della sostituzione")
        return

    try:
        sostituzioni.modifica(data.get("id"), data.get("data"))
    except Exception as e:
        logger.error(f"Errore durante la modifica della sostituzione: {e}")
        emit("errore modifica sostituzione", str(e))
        return

    emit("aggiornamento sostituzioni", broadcast=True)
    emit("aggiornamento sostituzioni", broadcast=True, namespace="/display")


@socketio.on("elimina sostituzione")
@login_required
@role_required("sostituzioni.write")
def elimina_sostituzione(data):
    logger.debug(f"Ricevuto segnale eliminazione sostituzione: {data}")

    # todo usare default mantieniinstorico di configurazione
    sostituzioni.elimina(data.get("id"), data.get("mantieni_in_storico", True))

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


# ////////////////////////////////////


@socketio.on("esporta sostituzioni")
@login_required
@role_required("sostituzioni.write")
def esporta_sostituzioni(filtri: dict | None = None):
    """
    filtri: stessi della funzione per richiesta sostituzioni
    """

    logger.debug(f"Ricevuto segnale per esportazione sostituzioni con filtri: {filtri}")

    try:
        Exporter.esporta(filtri)
    except Exporter.EmptyError:
        emit(
            "errore esportazione",
            "Nessuna sostituzione trovata per i filtri impostati.",
        )
        return
    except Exporter.FormatError as e:
        emit("errore esportazione", str(e))
        return
    except Exception as e:
        emit("errore esportazione", "Errore: " + str(e))
        return

    emit("esportazione completata")
