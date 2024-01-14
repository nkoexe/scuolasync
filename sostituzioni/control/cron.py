from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from sostituzioni.control.backup import backup

scheduler = BackgroundScheduler()

scheduler.add_job(
    backup,
    trigger=CronTrigger(year="*", month="*", day="*", hour="0", minute="0", second="0"),
    name="backup",
)

scheduler.start()
