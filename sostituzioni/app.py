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

try:
    from sostituzioni.view import app

except ImportError as e:
    from logging import getLogger

    logger = getLogger(__name__)
    logger.error("Errori di importazione dei moduli richiesti: " + str(e))
    logger.info("Tentativo di installazione automatica dei moduli richiesti...")

    from subprocess import run
    from pathlib import Path
    import sys

    root = Path(__file__).parent.parent
    requirements = root / "requirements.txt"
    logger.debug("File requirements.txt: " + str(requirements))

    if not requirements.exists():
        logger.error(
            "File requirements.txt non trovato. Impossibile installare automaticamente i moduli richiesti, intervento manuale richiesto."
        )
        sys.exit(1)

    result = run(["pip", "install", "-r", str(requirements)], capture_output=True)
    if result.returncode != 0:
        logger.error(
            "Impossibile installare i moduli richiesti, intervento manuale richiesto:\n"
            + result.stderr.decode("utf-8")
        )
        sys.exit(1)

    logger.info("Moduli richiesti installati con successo. Tentativo di riavvio...")

    from sostituzioni.view import app
