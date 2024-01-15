import logging
from flask import request
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
from sostituzioni.view import socketio

logger = logging.getLogger(__name__)


@socketio.on("connect", namespace="/display")
def connect():
    # request.args.get("authcode")

    logger.debug("Nuovo client connesso, invio dei dati iniziali.")

    emit("lista sostituzioni", Sostituzione.load())
    emit("lista eventi", Evento.load())
    emit("lista notizie", Notizia.load())
    emit("lista aule", Aula.load())
    emit("lista classi", Classe.load())
    emit("lista docenti", Docente.load())
    emit("lista ore predefinite", OraPredefinita.load())


@socketio.on("richiesta sostituzioni", namespace="/display")
def richiesta_sostituzioni():
    logger.debug("Ricevuto segnale da visualizzazione fisica: richiesta sostituzioni")

    emit("lista sostituzioni", Sostituzione.load())


@socketio.on("richiesta eventi", namespace="/display")
def richiesta_eventi():
    logger.debug("Ricevuto segnale da visualizzazione fisica: richiesta eventi")

    emit("lista eventi", Evento.load())


@socketio.on("richiesta notizie", namespace="/display")
def richiesta_notizie():
    logger.debug("Ricevuto segnale da visualizzazione fisica: richiesta notizie")
    emit("lista notizie", Notizia.load())
