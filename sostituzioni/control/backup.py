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

    # create the new backup
    local_file = local_backup(local_backup_dir)

    logger.info("Local backup completed successfully.")

    # get the previous backups
    local_backup_list = get_local_backups(local_backup_dir)

    # delete the old backups, duration can be set in the configuration
    logger.debug("Deleting old backups from local storage..")
    delete_old_local_backups(local_backup_list)


    # upload to Google Drive
    drive_service = service_account_login()

    if not drive_service:
        logger.error("Errore nell'autenticazione con Google Drive")
        return local_file

    drive_folder_id = configurazione.get("backupdrivefolderid").valore

    logger.debug("Uploading backup to Google Drive..")
    upload_to_drive(drive_service, local_file, drive_folder_id)

    logger.info("Backup to Google Drive completed successfully.")

    logger.debug("Deleting old backups from Google Drive..")
    drive_backup_list = get_drive_backups(drive_service, drive_folder_id)

    delete_old_drive_backups(drive_service, drive_backup_list)

    return local_file


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


def delete_old_backups(file_list):
    # function to get the backups to delete from a list.

    # get the number of days to keep backups
    days_to_keep = configurazione.get("maxbackupdays").valore

    # user has disabled backup deletion
    if (days_to_keep) < 0:
        return []

    # if there's only one backup left for some reason, keep it
    if len(file_list) <= 1:
        return []

    to_delete = []

    for file in file_list:
        now = datetime.now(file["modifiedTime"].tzinfo)
        # print(now.tzinfo, file["modifiedTime"].tzinfo)
        if (now - file["modifiedTime"]).days > days_to_keep:
            to_delete.append(file)

    return to_delete


def delete_old_local_backups(file_list):
    to_delete = delete_old_backups(file_list)

    for file in to_delete:
        logger.debug(f"Deleting backup {file['path']}")
        file["path"].unlink()


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
        "drive", "v3", credentials=credentials, cache_discovery=False
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


def delete_old_drive_backups(drive_service, file_list):
    to_delete = delete_old_backups(file_list)

    for file in to_delete:
        logger.debug(f"Deleting Drive backup {file['path']}")
        drive_service.files().delete(fileId=file["id"]).execute()
        logger.debug(f"Backup {file['path']} deleted successfully.")

    return to_delete
