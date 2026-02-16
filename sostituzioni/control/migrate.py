from sostituzioni.control.configurazione import configurazione
from sostituzioni.control.database import database
import sqlite3
import logging
import shutil

logger = logging.getLogger(__name__)

versione_db = configurazione.get("databaseversion")


def migrate_v1_to_v2():
    """Merge user database into main database."""

    user_db = configurazione.get("authdatabasepath").path
    
    if not user_db.exists():
        logger.warning(f"User database not found at {user_db}, skipping migration")
        return True

    try:
        # Update schema in main database
        script = configurazione.get("scriptsdir").path / "creazione_database.sql"
        database.connect()
        database.cursor.executescript(script.read_text())

        # Connect to user database
        user_conn = sqlite3.connect(user_db)
        user_cursor = user_conn.cursor()


        # Migrate permissions
        user_cursor.execute("SELECT nome, descrizione FROM permesso")
        permessi = user_cursor.fetchall()
        for nome, descrizione in permessi:
            database.execute(
                "INSERT OR IGNORE INTO permesso (nome, descrizione) VALUES (?, ?)",
                (nome, descrizione)
            )
        logger.info(f"Migrated {len(permessi)} permessi")
        
        # Migrate roles
        user_cursor.execute("SELECT nome FROM ruolo")
        ruoli = user_cursor.fetchall()
        for (nome,) in ruoli:
            database.execute(
                "INSERT OR IGNORE INTO ruolo (nome) VALUES (?)",
                (nome,)
            )
        logger.info(f"Migrated {len(ruoli)} ruoli")

        # Migrate role-permission mappings
        user_cursor.execute("SELECT nome_ruolo, permesso_ruolo FROM permesso_per_ruolo")
        ruolo_permessi = user_cursor.fetchall()
        for nome_ruolo, permesso_ruolo in ruolo_permessi:
            database.execute(
                "INSERT OR IGNORE INTO permesso_per_ruolo (nome_ruolo, permesso_ruolo) VALUES (?, ?)",
                (nome_ruolo, permesso_ruolo)
            )
        logger.info(f"Migrated {len(ruolo_permessi)} ruolo-permesso mappings")
        
        # Migrate users
        user_cursor.execute("SELECT email, ruolo FROM utente")
        utenti = user_cursor.fetchall()
        for email, ruolo in utenti:
            database.execute(
                "INSERT OR IGNORE INTO utente (email, ruolo) VALUES (?, ?)",
                (email, ruolo)
            )
        logger.info(f"Migrated {len(utenti)} utenti")
        
        # Clean up connections
        database.close()
        user_conn.close()
        
        # Update database version
        configurazione.set("databaseversion", 2)
        configurazione.esporta()
        
        logger.info("Migration v1 to v2 completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return False


if versione_db == 1 and configurazione.get("authdatabasepath") is not None:
    migrate_v1_to_v2()
