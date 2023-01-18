"""
Gestione della configurazione del sistema tramite il file configurazione.ini
"""

from pathlib import Path
from json import load

from beartype._decor.decormain import beartype
from beartype.typing import List

# un file singolo o file di configurazione per ogni categoria?
CONFIG_FILE = Path(__file__).parent.parent / 'database' / 'configurazione.json'


class Sezione:
    """
    Gruppo di opzioni.
    """
    @beartype
    def __init__(self, id: str, titolo: str, descrizione: str | None = None, opzioni: List = []):
        self.titolo = titolo
        self.id = titolo.replace(' ', '').lower()
        self.descrizione = descrizione
        self.opzioni = opzioni


class Opzione:
    """
    Singola opzione per la configurazione del sistema.
    """
    @beartype
    def __init__(self, id: str, titolo: str | None = None, descrizione: str | None = None):
        self.titolo = titolo
        self.descrizione = descrizione
        self.tipo = None

    @beartype
    def testo(self, valore: str):
        self.tipo = 'testo'
        self.valore = valore

        return self

    @beartype
    def booleano(self, valore: bool):
        self.tipo = 'bool'
        self.valore = valore

        return self

    @beartype
    def lista(self, lista: List):
        self.tipo = 'lista'
        self.valori = lista

        return self


class Configurazione:
    @beartype
    def __init__(self, file: Path = CONFIG_FILE):
        with open(file) as configfile:
            self.data = load(configfile)

        self.configurazione = []

        for sectionid, sectiondata in self.data.items():
            sezione = Sezione(sectionid, sectiondata.get('title', sectiondata.get('descr')))

            for optionid, optiondata in sectiondata.get('options').items():
                opzione = Opzione(optionid, optiondata.get('title'), optiondata.get('descr'))

        # configurazione di test


if __name__ == '__main__':
    c = Configurazione()