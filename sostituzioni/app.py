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
