import logging
import subprocess

from sostituzioni.control.configurazione import configurazione


logger = logging.getLogger(__name__)


class Updater:
    class Commands:
        GET_LOCAL_COMMIT = "git rev-parse HEAD"
        GET_REMOTE_COMMIT = "git fetch origin demo --quiet && git rev-parse origin/demo"
        GET_RELEASE_NOTES = "git fetch origin demo --quiet && git log origin/demo -1 --pretty=format:'%B'"

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

        # Always return "demo" as version for display
        self.version = "demo"
        configurazione.set("version", self.version, force=True)

        self.aggiornamento_disponibile = False

    def get_local_version(self):
        """Always return 'demo' for display purposes"""
        return "demo"
    
    def get_local_commit(self):
        """Get actual local commit hash for comparison"""
        try:
            result = subprocess.run(
                self.Commands.GET_LOCAL_COMMIT,
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'ottenimento del commit locale")
            return "err"

        if result.returncode != 0:
            logger.error(f"Errore durante l'ottenimento del commit locale: {result.stderr.decode('utf-8')}")
            return "err"

        return result.stdout.decode("utf-8").strip()

    def get_remote_version(self):
        """Get latest commit hash from remote demo branch"""
        try:
            result = subprocess.run(
                self.Commands.GET_REMOTE_COMMIT,
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'ottenimento del commit remoto")
            return "err"

        if result.returncode != 0:
            logger.error(f"Errore durante l'ottenimento del commit remoto: {result.stderr.decode('utf-8')}")
            return "err"

        return result.stdout.decode("utf-8").strip()

    def get_release_notes(self):
        """Get release notes from latest commit message"""
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

        notes = result.stdout.decode("utf-8").strip()
        return notes if notes else "Nessuna nota di rilascio disponibile."


    def check_update(self):
        local_commit = self.get_local_commit()
        remote_commit = self.get_remote_version()

        logger.info(f"Commit locale: {local_commit[:8] if local_commit != 'err' else local_commit}")
        logger.info(f"Commit remoto: {remote_commit[:8] if remote_commit != 'err' else remote_commit}")

        # Handle error states
        if local_commit == "err" or remote_commit == "err":
            self.aggiornamento_disponibile = False
            return False

        # Update available if commits differ
        self.aggiornamento_disponibile = local_commit != remote_commit

        return self.aggiornamento_disponibile
    
    def update(self):
        # Store current commit for rollback
        current_commit = self.get_local_commit()
        
        try:
            # Get latest commit from demo branch (also fetches)
            latest_commit = self.get_remote_version()
            if latest_commit == "err":
                raise Exception("Impossibile ottenere l'ultimo commit")

            # Pull from demo branch
            result = subprocess.run(
                "git fetch origin demo --quiet && git reset --hard origin/demo",
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )

            if result.returncode != 0:
                logger.error(f"Errore durante l'aggiornamento: {result.stderr.decode('utf-8')}")
                raise Exception("Errore durante l'aggiornamento")

            logger.info("Aggiornamento completato con successo.")

            # Version stays "demo"
            configurazione.set("version", "demo", force=True)
            self.aggiornamento_disponibile = False
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout durante l'aggiornamento")
            self._rollback(current_commit)
            raise Exception("Timeout durante l'aggiornamento")
        except Exception as e:
            logger.error(f"Aggiornamento fallito: {e}")
            self._rollback(current_commit)
            raise
    
    def _rollback(self, target_commit):
        """Rollback to a previous commit in case of update failure"""
        if target_commit == "err":
            logger.warning("Impossibile eseguire rollback: commit target non valido")
            return
        
        logger.warning(f"Tentativo di rollback al commit {target_commit[:8]}")
        try:
            result = subprocess.run(
                f"git reset --hard {target_commit}",
                cwd=self.repo,
                capture_output=True,
                shell=True,
                timeout=30,
            )
            if result.returncode == 0:
                logger.info(f"Rollback al commit {target_commit[:8]} completato")
            else:
                logger.error(f"Rollback fallito: {result.stderr.decode('utf-8')}")
        except Exception as e:
            logger.error(f"Errore durante il rollback: {e}")



updater = Updater()
