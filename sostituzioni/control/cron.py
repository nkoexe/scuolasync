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

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.updater import updater
from sostituzioni.control.backup import backup
from sostituzioni.control.database import database

scheduler = BackgroundScheduler()

# Backup del sistema - ogni giorno a mezzanotte
scheduler.add_job(
    backup,
    trigger=CronTrigger(year="*", month="*", day="*", hour="0", minute="0", second="0"),
    name="backup",
)

# Controllo aggiornamento - ogni due ore
scheduler.add_job(
    updater.check_update,
    trigger=CronTrigger(
        year="*", month="*", day="*", hour="*/2", minute="0", second="0"
    ),
    name="check_update",
)


# temi stagionali
def update_seasonal_themes():
    if "halloween" in configurazione.extra_themes:
        configurazione.extra_themes.remove("halloween")
    if "xmas" in configurazione.extra_themes:
        configurazione.extra_themes.remove("xmas")

    if not configurazione.get("seasonalthemes"):
        return

    now = datetime.now()

    # halloween theme
    if (
        datetime(now.year, 10, 30, 0, 0, 0)
        <= now
        <= datetime(now.year, 10, 31, 23, 59, 59)
    ):
        configurazione.extra_themes.append("halloween")

    # xmas theme
    if (
        datetime(now.year, 12, 15, 0, 0, 0)
        <= now
        <= datetime(now.year, 12, 31, 23, 59, 59)
    ):
        configurazione.extra_themes.append("xmas")


update_seasonal_themes()

scheduler.add_job(
    update_seasonal_themes,
    trigger=CronTrigger(year="*", month="*", day="*", hour="0", minute="0", second="0"),
    name="update_seasonal_themes",
)

scheduler.start()
