from datetime import datetime
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import googleapiclient.discovery
import logging
import zipfile

from sostituzioni.control.configurazione import configurazione


logger = logging.getLogger(__name__)


def backup():
    local_backup_dir = configurazione.get("backupdir").path

    # local_file = local_backup(local_backup_dir)
    local_backup_list = get_local_backups(local_backup_dir)
    print(local_backup_list)

    drive_service = service_account_login()
    drive_folder_id = configurazione.get("backupdrivefolderid").valore

    # upload_to_drive(drive_service, local_file, drive_folder_id)
    drive_backup_list = get_drive_backups(drive_service, drive_folder_id)

    print(drive_backup_list)

    # logger.info("Backup completed successfully.")

    # return local_file


def local_backup(directory):
    files = [
        configurazione.get("databasepath").path,
        configurazione.get("authdatabasepath").path,
        configurazione.get("configpath").path,
    ]

    for file in files:
        if not file.is_file():
            logger.error(
                f"File per backup {file} non trovato, impossibile eseguire il backup."
            )

    if not directory.is_dir():
        directory.mkdir()

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = directory / f"backup_{date}.zip"

    logger.debug(f"Compressing files to {backup_file}")

    with zipfile.ZipFile(backup_file, "w") as zip_file:
        for file in files:
            zip_file.write(file, arcname=file.name)

    return backup_file


def get_local_backups(directory):
    files = directory.glob("*.zip")
    valid_files = []

    # check if file is a valid backup and add it to the valid list
    for file in files:
        with zipfile.ZipFile(file, "r") as zip_file:
            # check for file structure, it has to contain a json file and two db
            # todo: improve file checking
            filelist = zip_file.namelist()
            if len(filelist) != 3:
                logger.warning(f"File {file} non è un backup valido.")
                continue
            if not any(
                file.endswith(ext) for ext in [".json", ".db"] for file in filelist
            ):
                logger.warning(f"File {file} non è un backup valido.")
                continue

            valid_files.append(
                {
                    "path": file,
                    "size": file.stat().st_size,
                    "modifiedTime": datetime.fromtimestamp(file.stat().st_mtime),
                    "createdTime": datetime.fromtimestamp(file.stat().st_ctime),
                }
            )

    return valid_files


def service_account_login():
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

    return drive_service


def upload_to_drive(drive_service, backup_file, folder_id):
    logger.debug("Uploading backup to Google Drive..")
    file_name = str(backup_file.name)

    metadata = {"name": file_name, "parents": [folder_id] if folder_id else []}

    media = MediaFileUpload(backup_file, resumable=True)

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


def get_drive_backups(drive_service, folder_id):
    # try:
    #     files = drive_service.files().list(q=f"'{folder_id}' in parents").execute()
    # except googleapiclient.errors.HttpError as error:
    #     logger.error(f"Error retrieving drive files: {error}")
    #     return None

    # return files.get("files", [])

    ## get more info about file
    files = (
        drive_service.files()
        .list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="files(id, name, size, modifiedTime, createdTime)",
        )
        .execute()
    )

    files = files.get("files", [])

    for file in files:
        file["modifiedTime"] = datetime.fromisoformat(file["modifiedTime"])
        file["createdTime"] = datetime.fromisoformat(file["createdTime"])
        file["path"] = f"https://drive.google.com/file/d/{file['id']}/view"

    return files
