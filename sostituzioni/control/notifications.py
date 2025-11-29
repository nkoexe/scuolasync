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
from datetime import datetime, timedelta
from json import dumps
from threading import Thread
from pywebpush import webpush, WebPushException

from sostituzioni.control.configurazione import configurazione
from sostituzioni.model.model import Sostituzione, sostituzioni


logger = logging.getLogger(__name__)


class Notification:
    def __init__(self, sostituzione: Sostituzione):
        if sostituzione.ora_predefinita is not None:
            ora = (
                f"{sostituzione.ora_predefinita}a ora"
                if sostituzione.ora_predefinita.isdigit()
                else sostituzione.ora_predefinita
            )
            self.title = f"Supplenza alla {ora}"
        elif sostituzione.ora_inizio is not None and sostituzione.ora_fine is not None:
            self.title = (
                f"Supplenza oggi {sostituzione.ora_inizio}-{sostituzione.ora_fine}"
            )
        else:
            self.title = "Supplenza oggi"

        self.body = f"In {sostituzione.nome_classe} (aula {sostituzione.numero_aula})"

        if sostituzione.note:
            self.body += f"\nNote: {sostituzione.note}"


class NotificationManager:
    def __init__(self):
        Thread(target=test_notification, daemon=True).start()

        self.private_key = configurazione.get("vapidprivatekey").valore
        self.public_key = configurazione.get("vapidpublickey").valore

        if not self.private_key or not self.public_key:
            logger.warning("VAPID keys not found, notifications will not work.")

    def send_upcoming(self):
        after = (
            datetime.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        )
        before = after + timedelta(days=1).total_seconds()

        s = sostituzioni.filtra({"data_inizio": after, "data_fine": before})
        logger.info(f"Found {len(s)} upcoming sostituzioni")

        for sostituzione in s:
            # todo get list of user subscriptions
            # if any subscription.docente == sostituzione.docente
            # foreach subscription send notification

            for user, info in configurazione.temp_utenti.items():
                logger.info(f"Sending notification to {user}")
                self.send(info, Notification(sostituzione))

        logger.info("Sent all notifications")

    def send(self, user, notification: Notification):
        data = dumps(
            {
                "title": notification.title,
                "body": notification.body,
            }
        )

        webpush(
            subscription_info=user,
            data=data,
            vapid_private_key=self.private_key,
            vapid_claims={
                "sub": "mailto:test@example.org",
            },
        )


def test_notification():
    from time import sleep

    sleep(10)

    while True:
        notificationmanager.send_upcoming()
        sleep(20)


notificationmanager = NotificationManager()
