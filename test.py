from pathlib import Path
import pandas as pd


class Docenti:
    def from_file(filepath: Path | str):
        data = None

        if isinstance(filepath, str):
            filepath = Path(filepath)

        if not filepath.is_file():
            raise FileNotFoundError(f'File {filepath} not found')

        match filepath.suffix:
            case '.csv':
                data = pd.read_csv(filepath)
            case '.xlsx':
                data = pd.read_excel(filepath)
            case _:
                raise ValueError(f'File type {filepath.suffix} not supported')

        if data is None:
            raise ValueError(f'File {filepath} is empty')

        for index, row in data.iterrows():
            nome, cognome, sure = Docenti.parse_nome_cognome(row['Member Name'])
            print(f'{nome} | {cognome} | {sure}')

    def parse_nome_cognome(nome_cognome: str) -> tuple[str, str, bool]:
        """
        Funzione che tenta di indovinare la suddivisione di nome e cognome a partire da una stringa unica.
        Ritorna: Nome, Cognome, Sicuro
        Il valore è sicuro se la stringa è suddivisibile una volta da uno spazio. "Mario Rossi" -> "Mario", "Rossi"
        Se ci sono incertezze, come secondi nomi, senti io faccio del mio meglio, dato che sicuramente farò errori darò
        all'utente la segnalazione di queste incertezze e la possibilità di modificarle prima dell'inserimento.
        """

        parti = nome_cognome.split(' ')

        if len(parti) == 1:
            nome = ''
            cognome = parti[0]
            return nome, cognome, True

        if len(parti) == 2:
            nome = parti[0]
            cognome = parti[1]
            return nome, cognome, True

        if parti[-2].lower() in ['di', 'da', 'dal', 'dalla', 'dallo', 'dagli', 'dalle', 'dai', 'de', 'del', 'delle', 'dello', 'dei', 'degli', 'van', 'von']:
            nome = ' '.join(parti[:-2])
            cognome = ' '.join(parti[-2:])
            return nome, cognome, False

        if len(parti) >= 4 and (parti[-3] + ' ' + parti[-2]).lower() in ['van der', 'von der', 'van den', 'von den']:
            nome = ' '.join(parti[:-3])
            cognome = ' '.join(parti[-3:])
            return nome, cognome, False

        nome = ' '.join(parti[:-1])
        cognome = parti[-1]
        return nome, cognome, False


if __name__ == '__main__':
    Docenti.from_file(r"C:\Users\nicco\Downloads\Members_02jxsxqh2kqp4nx_11122023_163509.csv.xlsx")
