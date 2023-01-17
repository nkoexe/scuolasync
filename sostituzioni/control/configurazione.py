"""
Gestione della configurazione del sistema tramite il file configurazione.ini
"""

from pathlib import Path

from beartype._decor.decormain import beartype
from beartype.typing import List

# un file singolo o file di configurazione per ogni categoria?
CONFIG_FILE = Path(__file__).parent.parent / 'database' / ''


class Sezione:
    """
    Gruppo di opzioni.
    """
    def __init__(self, titolo: str, descrizione: str | None = None, opzioni: List | None = None):
        self.titolo = titolo
        self.id = titolo.replace(' ', '').lower()
        self.descrizione = descrizione
        self.opzioni = opzioni


class Opzione:
    """
    Singola opzione per la configurazione del sistema.
    """
    @beartype
    def __init__(self, titolo: str | None = None, descrizione: str | None = None):
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
    def __init__(self, file: Path = CONFIG_FILE):
        #* Leggere da config file

        # configurazione di test
        self.configurazione = [
            Sezione(
                'Test sezione1',
                opzioni=[
                    Opzione('Testo', 'Esempio di campo di testo.').testo('testone'),
                    Opzione('Prova 2', 'Esempio di campo di testo.').testo('testone due'),
                    Opzione('Prova 3', 'Esempio di campo di testo.').testo('testone'),
                    Opzione('Prova 4', 'Esempio di campo di testo.').testo('testone'),
                    Opzione('Vero o falso??', 'Non so dimmi tu.').booleano(False),
                    Opzione('Vero o falso??', 'Non so dimmi tu.').booleano(True)
                ]
            ),
            Sezione(
                'Note standard',
                opzioni=[
                    Opzione(
                        'Note Standard',
                        'Descrizione bla bla imposta le note standard di sistema.',
                    ).lista(
                        [Opzione().testo('Nota standard #1'),
                         Opzione().testo('Nota standard #2')]
                    )
                ]
            )
        ]


configurazione = Configurazione()