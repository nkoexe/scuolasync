from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.backup import backup

scheduler = BackgroundScheduler()

# Backup del sistema - ogni giorno a mezzanotte
scheduler.add_job(
    backup,
    trigger=CronTrigger(year="*", month="*", day="*", hour="0", minute="0", second="0"),
    name="backup",
)

# Controllo aggiornamento - ogni due ore
scheduler.add_job(
    configurazione.check_update,
    trigger=CronTrigger(
        year="*", month="*", day="*", hour="*/2", minute="0", second="0"
    ),
    name="check_update",
)

# Passaggio a nuovo anno scolastico - definito nella configurazione
giorno = configurazione.get("newyeardate").valore
mese = configurazione.get("newyeardate").unita + 1

scheduler.add_job(
    lambda: print("Passaggio a nuovo anno scolastico"),
    trigger=CronTrigger(
        year="*", month=mese, day=giorno, hour="0", minute="0", second="0"
    ),
    name="new_school_year",
)

scheduler.start()
