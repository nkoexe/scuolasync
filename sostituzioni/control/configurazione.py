"""
Gestione della configurazione del sistema tramite il file configurazione.json
"""

from pathlib import Path
from json import load

from beartype._decor.decormain import beartype
from beartype.typing import List, Dict

import logging


# un file singolo o file di configurazione per ogni categoria?
CONFIG_FILE = Path(__file__).parent.parent / 'database' / 'configurazione.json'


class Sezione:
    """
    Gruppo di opzioni.
    """
    @beartype
    def __init__(self, id: str, title: str, descr: str | None = None):
        self.id = id
        self.title = title
        self.descr = descr
        self.options = []


class Opzione:
    """
    Singola opzione per la configurazione del sistema.
    """

    TESTO = 'text'
    NUMERO = 'num'
    NUMERO_UNITA = 'unitnum'
    BOOLEANO = 'bool'
    COLORE = 'color'
    SELEZIONE = 'select'

    @beartype
    def __init__(self, id: str, title: str | None = None, descr: str | None = None):
        self.id = id
        self.title = title
        self.descr = descr

    @beartype
    def testo(self, configurazione: Dict):
        self.type = self.TESTO
        self.default = configurazione.get('default')
        self.max_lenght = configurazione.get('max_lenght')
        self.value = configurazione.get('value')

    @beartype
    def numero(self, configurazione: Dict):
        self.type = self.NUMERO
        self.interval: List[int | None] = configurazione.get('interval')
        self.default: int = configurazione.get('default')
        self.value: int = configurazione.get('value')

    @beartype
    def numero_unita(self, configurazione: Dict):
        self.type = self.NUMERO_UNITA
        self.interval: List[int] = configurazione.get('interval')
        self.default: int = configurazione.get('default')
        self.value: int = configurazione.get('value')
        self.units: List[str] = configurazione.get('units')
        self.default_unit: str = configurazione.get('default_unit')
        self.unit: str = configurazione.get('unit')

    @beartype
    def booleano(self, configurazione: Dict):
        self.type = self.BOOLEANO
        self.default: bool = configurazione.get('default')
        self.value: bool = configurazione.get('value')

    @beartype
    def colore(self, configurazione: Dict):
        self.type = self.TESTO
        self.default: str = configurazione.get('default')
        self.value: str = configurazione.get('value')

    @beartype
    def selezione(self, configurazione: Dict):
        self.type = self.SELEZIONE
        self.choices: List[str] = configurazione.get('choices')
        self.default: int = configurazione.get('default')
        self.value: int = configurazione.get('value')


class Configurazione:
    @beartype
    def __init__(self, file: Path = CONFIG_FILE):
        logging.debug('Inizializzazione caricamento configurazione')

        with open(file, encoding='utf-8') as configfile:
            logging.debug('Caricamento file di configurazione..')
            self.data = load(configfile)
            logging.debug(f'Raw data: {self.data}')

        # Todo: controllare validità file

        self.configurazione = []

        for sectionid, sectiondata in self.data.items():
            sezione = Sezione(sectionid, sectiondata.get('title'), sectiondata.get('descr'))

            for optionid, optiondata in sectiondata.get('options').items():
                opzione = Opzione(optionid, optiondata.get('title'), optiondata.get('descr'))

                config = optiondata.get('config')

                match config.get('type'):

                    case Opzione.TESTO:
                        opzione.testo(config)

                    case Opzione.NUMERO:
                        opzione.numero(config)

                    case Opzione.NUMERO_UNITA:
                        opzione.numero_unita(config)

                    case Opzione.BOOLEANO:
                        opzione.booleano(config)

                    case Opzione.COLORE:
                        opzione.colore(config)

                    case Opzione.SELEZIONE:
                        opzione.selezione(config)

                    case _:
                        logging.warning(f'Nel caricamento della configurazione, opzione con id {optionid} non ha un tipo valido.')

                sezione.options.append(opzione)

            self.configurazione.append(sezione)


if __name__ == '__main__':  # * test
    logging.basicConfig(level=logging.DEBUG)
    c = Configurazione()

    for s in c.configurazione:
        print(s.title)

        for o in s.options:
            print('-', o.title)
