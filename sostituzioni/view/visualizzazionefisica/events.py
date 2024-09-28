"""
    This file is part of ScuolaSync.

    Copyright (C) 2023-present Niccolò Ragazzi <hi@njco.dev>

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
"""

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

    emit("lista ore predefinite", OraPredefinita.load())
    emit("lista aule", Aula.load())
    emit("lista classi", Classe.load())
    emit("lista docenti", Docente.load())
    emit("lista eventi", Evento.load())
    emit("lista notizie", Notizia.load())
    emit("lista sostituzioni", Sostituzione.load())


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
