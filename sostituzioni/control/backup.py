from datetime import datetime
from pathlib import Path
from shutil import copyfile
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import googleapiclient.discovery
import logging
import zipfile

from sostituzioni.control.configurazione import configurazione


logger = logging.getLogger(__name__)


def backup():
    files = [
        configurazione.get("databasepath").path,
        configurazione.get("authdatabasepath").path,
        configurazione.get("configpath").path,
    ]

    backup_dir = configurazione.get("backupdir").path

    for file in files:
        if not file.is_file():
            return FileNotFoundError(f"File per backup {file} not found.")

    if not backup_dir.is_dir():
        backup_dir.mkdir()

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = backup_dir / f"backup_{date}.zip"

    logger.debug(f"Compressing files to {backup_file}")

    with zipfile.ZipFile(backup_file, "w") as zip_file:
        for file in files:
            zip_file.write(file, arcname=file.name)

    logger.debug("Uploading backup to Google Drive..")
    upload_to_drive(backup_file)

    logger.info("Backup completed successfully.")

    return backup_file


def upload_to_drive(backup_file):
    file_name = str(backup_file.name)
    folder_id = configurazione.get("backupdrivefolderid").valore

    metadata = {"name": file_name, "parents": [folder_id] if folder_id else []}

    media = MediaFileUpload(backup_file, resumable=True)

    chiave_account_servizio = configurazione.get("backupserviceaccountkey").path

    if not chiave_account_servizio.is_file():
        logger.warning(
            f"Chiave per l'account di servizio non trovata, non è possibile eseguire il backup su Google Drive. ({chiave_account_servizio})"
        )
        return None

    credentials = service_account.Credentials.from_service_account_file(
        chiave_account_servizio, scopes=["https://www.googleapis.com/auth/drive.file"]
    )

    drive_service = googleapiclient.discovery.build(
        "drive", "v3", credentials=credentials
    )

    try:
        file = (
            drive_service.files()
            .create(body=metadata, media_body=media, fields="id")
            .execute()
        )
    except googleapiclient.errors.HttpError as error:
        logger.error(f"Error uploading backup file: {error}")
        return None

    logger.debug(f"File uploaded with ID: {file['id']}")
    return file["id"]
