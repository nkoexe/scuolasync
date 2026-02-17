import logging
import subprocess

from sostituzioni.control.configurazione import configurazione


logger = logging.getLogger(__name__)


class Updater:
    class Commands:
        GET_LOCAL_VERSION = "git describe --tags --abbrev=0"
        GET_REMOTE_VERSION = "git ls-remote --tags origin"
        UPDATE = "git pull"


    def __init__(self):
        # "/scuolasync/sostituzioni", git è un livello più alto
        self.repo = configurazione.get("rootpath").path.parent

        self.version = self.get_local_version()
        configurazione.set("version", self.version, force=True)

        self.aggiornamento_disponibile = False

    def get_local_version(self):
        result = subprocess.run(
            self.Commands.GET_LOCAL_VERSION,
            cwd=self.repo,
            capture_output=True,
            shell=True,
        )

        if result.returncode != 0:
            logger.error(f"Errore durante l'ottenimento della versione locale: {result.stderr.decode('utf-8')}")
            return "err"

        return result.stdout.decode("utf-8").strip()

    def get_remote_version(self):
        result = subprocess.run(
            self.Commands.GET_REMOTE_VERSION,
            cwd=self.repo,
            capture_output=True,
            shell=True,
        )

        if result.returncode != 0:
            logger.error(f"Errore durante l'ottenimento della versione remota: {result.stderr.decode('utf-8')}")
            return "err"

        return result.stdout.decode("utf-8").strip()

    def check_update(self):
        local_version = self.get_local_version()
        remote_version = self.get_remote_version()

        logger.info(f"Versione locale: {local_version}")
        logger.info(f"Versione remota: {remote_version}")

        self.aggiornamento_disponibile = (
            remote_version != local_version
            and remote_version != "err"
            and local_version != "err"
        )

        return self.aggiornamento_disponibile
    
    def update(self):
        result = subprocess.run(
            self.Commands.UPDATE,
            cwd=self.repo,
            capture_output=True,
            shell=True,
        )

        if result.returncode != 0:
            logger.error(f"Errore durante l'aggiornamento: {result.stderr.decode('utf-8')}")
            raise Exception("Errore durante l'aggiornamento")

        logger.info("Aggiornamento completato con successo.")
        self.version = self.get_local_version()
        configurazione.set("version", self.version, force=True)
        self.aggiornamento_disponibile = False



updater = Updater()
