from time import time
from threading import Thread

from pywebpush import webpush
from sostituzioni.model.model import Sostituzione, sostituzioni


class Notification:
    def __init__(self, sostituzione: Sostituzione):
        self.sostituzione = sostituzione

    @property
    def title(self):
        return f"Nuova supplenza in {self.sostituzione.nome_classe}"

    @property
    def body(self):
        return f"Oggi alla {self.sostituzione.ora_predefinita} in {self.sostituzione.nome_classe} ({self.sostituzione.numero_aula})"


class NotificationManager:
    def __init__(self):
        Thread(target=test_notification, daemon=True).start()

    def send_upcoming(self):
        print("Sending upcoming notifications")
        after = int(time())
        before = after + 200 * 60

        s = sostituzioni.filtra({"data_inizio": after, "data_fine": before})

        for sostituzione in s:
            # todo get list of user subscriptions
            # if any subscription.docente == sostituzione.docente
            # foreach subscription send notification

            from sostituzioni.control.configurazione import configurazione
            for info in configurazione.temp_utenti.values():
                self.send(info, Notification(sostituzione))

        print("Sent all notifications")

    def send(self, user, notification: Notification):
        webpush(
            subscription_info=user,
            data=f'{{"title": "{notification.title}", "body": "{notification.body}" }}',
            vapid_private_key="KfKu2UKkx2wKuS0OPvpaZL0Ebj9hLl9_b_5zyegnKN0",
            vapid_claims={
                "sub": "mailto:test@example.org",
            },
            ttl=10,
            timeout=5
        )


def test_notification():
    while True:
        from time import sleep
        sleep(30)
        notificationmanager.send_upcoming()


notificationmanager = NotificationManager()
