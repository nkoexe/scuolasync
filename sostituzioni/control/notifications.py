from time import time
from json import dumps
from threading import Thread

from pywebpush import webpush
from sostituzioni.model.model import Sostituzione, sostituzioni


class Notification:
    def __init__(self, sostituzione: Sostituzione):
        if sostituzione.ora_predefinita is not None:
            self.title = f"Supplenza alla {sostituzione.ora_predefinita}a ora"
        elif sostituzione.ora_inizio is not None and sostituzione.ora_fine is not None:
            self.title = (
                f"Supplenza oggi {sostituzione.ora_inizio}-{sostituzione.ora_fine}"
            )

        self.body = f"In {sostituzione.nome_classe} (aula {sostituzione.numero_aula})"

        if sostituzione.note:
            self.body += f"\nNote: {sostituzione.note}"


class NotificationManager:
    def __init__(self):
        # Thread(target=test_notification, daemon=True).start()
        pass

    def send_upcoming(self):
        after = int(time())
        before = after + 24 * 60 * 60

        s = sostituzioni.filtra({"data_inizio": after, "data_fine": before})
        print(f"Found {len(s)} upcoming sostituzioni")

        for sostituzione in s:
            # todo get list of user subscriptions
            # if any subscription.docente == sostituzione.docente
            # foreach subscription send notification

            from sostituzioni.control.configurazione import configurazione

            print(f"Sending {len(configurazione.temp_utenti.keys())} notifications")
            for info in configurazione.temp_utenti.values():
                self.send(info, Notification(sostituzione))

        print("Sent all notifications")

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
            vapid_private_key="KfKu2UKkx2wKuS0OPvpaZL0Ebj9hLl9_b_5zyegnKN0",
            vapid_claims={
                "sub": "mailto:test@example.org",
            },
        )


def test_notification():
    while True:
        from time import sleep

        sleep(10)
        notificationmanager.send_upcoming()


notificationmanager = NotificationManager()
