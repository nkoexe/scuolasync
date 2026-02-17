import logging
import subprocess
from packaging import version

from sostituzioni.control.configurazione import configurazione


logger = logging.getLogger(__name__)


class Updater:
    class Commands:
        GET_LOCAL_VERSION = "git describe --tags --abbrev=0"
        GET_REMOTE_VERSION = "git fetch --tags --quiet && git tag -l --sort=-v:refname"
        GET_RELEASE_NOTES = "git fetch --tags --quiet && git tag -l --sort=-v:refname --format='%(contents)'"

    def __init__(self):
        # "/scuolasync/sostituzioni", git è un livello più alto
        self.repo = configurazione.get("rootpath").path.parent

        # Validate git repository
        if not (self.repo / '.git').exists():
            logger.error("Not a git repository")
            self.version = "err"
            configurazione.set("version", self.version, force=True)
            self.aggiornamento_disponibile = False
            return

        self.version = self.get_local_version()
        configurazione.set("version", self.version, force=True)

        self.aggiornamento_disponibile = False

    def get_local_version(self):
        try:
            result = subprocess.run(
                self.Commands.GET_LOCAL_VERSION,
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'ottenimento della versione locale")
            return "err"

        if result.returncode != 0:
            stderr = result.stderr.decode('utf-8')
            # Handle repository with no tags
            if "No names found" in stderr or "no tags" in stderr.lower():
                logger.warning("Nessun tag trovato nel repository")
                return "untagged"
            logger.error(f"Errore durante l'ottenimento della versione locale: {stderr}")
            return "err"

        return result.stdout.decode("utf-8").strip()

    def get_remote_version(self):
        try:
            result = subprocess.run(
                self.Commands.GET_REMOTE_VERSION,
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'ottenimento della versione remota")
            return "err"

        if result.returncode != 0:
            logger.error(f"Errore durante l'ottenimento della versione remota: {result.stderr.decode('utf-8')}")
            return "err"

        # Parse output to get only the first (latest) tag
        tags = result.stdout.decode("utf-8").strip().split('\n')
        if not tags or not tags[0]:
            logger.warning("Nessun tag remoto trovato")
            return "err"
        
        return tags[0]

    def get_release_notes(self):
        """Get release notes for the latest remote tag"""
        try:
            result = subprocess.run(
                self.Commands.GET_RELEASE_NOTES,
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'ottenimento delle note di rilascio")
            return "Timeout durante l'ottenimento delle note di rilascio."

        if result.returncode != 0:
            logger.error(f"Errore durante l'ottenimento delle note di rilascio: {result.stderr.decode('utf-8')}")
            return "Errore durante l'ottenimento delle note di rilascio."

        # Parse output to get only the first tag's notes (latest)
        all_notes = result.stdout.decode("utf-8").strip()
        if not all_notes:
            return "Nessuna nota di rilascio disponibile."
        
        # Split by tags - first entry is the latest tag's notes
        notes_list = all_notes.split('\n\n')
        latest_notes = notes_list[0] if notes_list else all_notes
        
        return latest_notes if latest_notes else "Nessuna nota di rilascio disponibile."


    def check_update(self):
        local_version = self.get_local_version()
        remote_version = self.get_remote_version()

        logger.info(f"Versione locale: {local_version}")
        logger.info(f"Versione remota: {remote_version}")

        # Handle error states
        if local_version == "err" or remote_version == "err" or local_version == "untagged":
            self.aggiornamento_disponibile = False
            return False

        # Strip 'v' prefix and handle detached HEAD versions (e.g., v1.0.0-5-g1234abc)
        local_clean = local_version.lstrip('v').split('-')[0]
        remote_clean = remote_version.lstrip('v')

        try:
            # Use semantic version comparison
            self.aggiornamento_disponibile = version.parse(remote_clean) > version.parse(local_clean)
        except Exception as e:
            logger.error(f"Errore nel parsing delle versioni: {e}")
            self.aggiornamento_disponibile = False

        return self.aggiornamento_disponibile
    
    def update(self):
        # Store current version for rollback
        current_version = self.get_local_version()
        
        try:
            # Get latest tag (this also fetches)
            latest_tag = self.get_remote_version()
            if latest_tag == "err":
                raise Exception("Impossibile ottenere l'ultima versione")

            # Checkout that tag
            result = subprocess.run(
                f"git checkout {latest_tag}",
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )

            if result.returncode != 0:
                logger.error(f"Errore durante l'aggiornamento: {result.stderr.decode('utf-8')}")
                raise Exception("Errore durante l'aggiornamento")

            logger.info("Aggiornamento completato con successo.")

            self.version = self.get_local_version()
            configurazione.set("version", self.version, force=True)
            self.aggiornamento_disponibile = False
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'aggiornamento")
            self._rollback(current_version)
            raise Exception("Timeout durante l'aggiornamento")
        except Exception as e:
            logger.error(f"Aggiornamento fallito: {e}")
            self._rollback(current_version)
            raise
    
    def _rollback(self, target_version):
        """Rollback to a previous version in case of update failure"""
        if target_version == "err" or target_version == "untagged":
            logger.warning("Impossibile eseguire rollback: versione target non valida")
            return
        
        logger.warning(f"Tentativo di rollback alla versione {target_version}")
        try:
            result = subprocess.run(
                f"git checkout {target_version}",
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
            if result.returncode == 0:
                logger.info(f"Rollback alla versione {target_version} completato")
            else:
                logger.error(f"Rollback fallito: {result.stderr.decode('utf-8')}")
        except Exception as e:
            logger.error(f"Errore durante il rollback: {e}")


    def auto_update(self):
        if not configurazione.get("autoupdate"):
            return

        if self.check_update():
            logger.info("Aggiornamento disponibile, avviando processo di aggiornamento...")
            try:
                self.update()
            except Exception as e:
                logger.error(f"Auto-aggiornamento fallito: {e}")


updater = Updater()
