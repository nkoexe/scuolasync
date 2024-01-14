from datetime import datetime
from shutil import copyfile

from sostituzioni.control.configurazione import configurazione


def backup():
    database_file = configurazione.get("databasepath").path
    backup_dir = configurazione.get("backupdir").path

    if not database_file.is_file():
        return FileNotFoundError(f"Database file {database_file} not found.")

    if not backup_dir.is_dir():
        backup_dir.mkdir()

    database_name = database_file.stem
    database_ext = database_file.suffix
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = backup_dir / f"backup_{database_name}_{date}{database_ext}"

    print(f"Backing up database to {backup_file}")

    copyfile(database_file, backup_file)

    return backup_file
