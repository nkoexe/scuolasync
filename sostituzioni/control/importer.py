from pathlib import Path
from io import BytesIO
import pandas as pd
import pylibmagic
import magic
from beartype import beartype

from sostituzioni.model.model import Docente, Utente, Ruolo


class Docenti:
    @beartype
    def from_file(filepath: Path | str):
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if not filepath.is_file():
            raise FileNotFoundError(f"File {filepath} not found")

        return Docenti.from_buffer(filepath.read_bytes())

    @beartype
    def from_buffer(buffer: bytes | BytesIO, file_type: str | None = None):
        data = None

        if isinstance(buffer, bytes):
            buffer = BytesIO(buffer)

        if file_type is None:
            match magic.from_buffer(buffer, mime=True):
                case "text/csv":
                    file_type = "csv"
                case (
                    "application/vnd.ms-excel"
                    | "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ):
                    file_type = "xlsx"
                case (
                    "application/vnd.oasis.opendocument.spreadsheet"
                ):
                    file_type = "ods"

        if file_type == "csv" or file_type == "text/csv":
            data = pd.read_csv(buffer)
        elif file_type == "xlsx" or file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file_type == "application/vnd.ms-excel":
            data = pd.read_excel(buffer)
        elif file_type == "ods" or file_type == "application/vnd.oasis.opendocument.spreadsheet":
            data = pd.read_excel(buffer, engine="odf")
        else:
            # tenta comunque di aprirlo yolo
            data = pd.read_excel(buffer)
            if data is None:
                data = pd.read_csv(buffer)
            if data is None:
                raise ValueError(f"File di tipo {file_type} non supportato")

        col_nome = None
        col_cognome = None

        for nome in ["Nome", "Name", "Member Name"]:
            if nome in data.columns:
                col_nome = nome
                break

        for cognome in ["Cognome", "Surname", "Member Surname"]:
            if cognome in data.columns:
                col_cognome = cognome
                break

        if col_nome and col_cognome:
            for index, row in data.iterrows():
                nome = row[col_nome]
                cognome = row[col_cognome]
                Docente(nome, cognome).inserisci()

        elif col_nome:
            for index, row in data.iterrows():
                nome, cognome, sure = Docenti.parse_nome_cognome(row[col_nome])
                Docente(nome, cognome).inserisci()

        else:
            raise ValueError("Nessuna colonna di nome o cognome trovata")

        return True

    def parse_nome_cognome(nome_cognome: str) -> tuple[str, str, bool]:
        """
        Funzione che tenta di indovinare la suddivisione di nome e cognome a partire da una stringa unica.
        Ritorna: Nome, Cognome, Sicuro
        Il valore è sicuro se la stringa è suddivisibile una volta da uno spazio. "Mario Rossi" -> "Mario", "Rossi"
        Se ci sono incertezze, come secondi nomi, senti io faccio del mio meglio, dato che sicuramente farò errori darò
        all'utente la segnalazione di queste incertezze e la possibilità di modificarle prima dell'inserimento.
        """

        parti = nome_cognome.split(" ")

        if len(parti) == 1:
            nome = ""
            cognome = parti[0]
            return nome, cognome, True

        if len(parti) == 2:
            nome = parti[0]
            cognome = parti[1]
            return nome, cognome, True

        if parti[-2].lower() in [
            "di",
            "da",
            "dal",
            "dalla",
            "dallo",
            "dagli",
            "dalle",
            "dai",
            "de",
            "del",
            "delle",
            "dello",
            "dei",
            "degli",
            "van",
            "von",
        ]:
            nome = " ".join(parti[:-2])
            cognome = " ".join(parti[-2:])
            return nome, cognome, False

        if len(parti) >= 4 and (parti[-3] + " " + parti[-2]).lower() in [
            "van der",
            "von der",
            "van den",
            "von den",
        ]:
            nome = " ".join(parti[:-3])
            cognome = " ".join(parti[-3:])
            return nome, cognome, False

        nome = " ".join(parti[:-1])
        cognome = parti[-1]
        return nome, cognome, False


class Utenti:
    def from_file(filepath: Path | str):
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if not filepath.is_file():
            raise FileNotFoundError(f"File {filepath} not found")

        return Utenti.from_buffer(filepath.read_bytes())

    def from_buffer(buffer: bytes):
        data = None

        match magic.from_buffer(buffer, mime=True):
            case "text/csv":
                data = pd.read_csv(buffer)
            case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                data = pd.read_excel(buffer)
            case "application/vnd.ms-excel":
                data = pd.read_excel(buffer)
            case _:
                # tenta comunque di aprirlo yolo
                data = pd.read_excel(buffer)
                if data is None:
                    data = pd.read_csv(buffer)
                if data is None:
                    raise ValueError(
                        f"File di tipo {magic.from_buffer(buffer, mime=True)} non supportato"
                    )

        ruolo_default = Ruolo("visualizzatore")

        for index, row in data.iterrows():
            Utente(row["Member Email"], ruolo_default).inserisci()
