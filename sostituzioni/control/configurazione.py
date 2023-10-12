"""
Gestione della configurazione del sistema tramite il file configurazione.json
"""

from pathlib import Path
from json import load, dump

from beartype._decor.decormain import beartype
from beartype.typing import List, Dict, Any

from sostituzioni.logger import logger


# todo mettere tutte le variabili di questo tipo in un file separato (databasepath, static ecccc)
CONFIG_FILE = Path(__file__).parent.parent / 'database' / 'configurazione.json'


class Sezione:
    """
    Gruppo di opzioni.
    """
    @beartype
    def __init__(self, id: str, dati: Dict):
        self.id = id
        self.titolo = dati.get('titolo')
        self.descrizione = dati.get('descrizione')
        self.opzioni = []

    def __repr__(self):
        return 'Sezione' + self.id


class Opzione:
    """
    Singola opzione per la configurazione del sistema.
    """

    TESTO = 'testo'
    NUMERO = 'numero'
    NUMERO_UNITA = 'numero_unita'
    BOOLEANO = 'booleano'
    COLORE = 'colore'
    SELEZIONE = 'selezione'

    @beartype
    def __init__(self, id: str, dati: Dict):
        self.id = id

        self.titolo = dati.get('titolo')
        self.descrizione = dati.get('descrizione')
        self.sezione = dati.get('sezione')

        self.tipo = dati.get('tipo')

        match self.tipo:

            case self.TESTO:
                self.lunghezza_massima = dati.get('lunghezza_massima')
                self.default = dati.get('default')
                self.valore = dati.get('valore')

            case self.NUMERO:
                self.intervallo: List[int | None] = dati.get('intervallo')
                self.default: int | float = dati.get('default')
                self.valore: int | float = dati.get('valore')

            case self.NUMERO_UNITA:
                self.intervallo: List[int] = dati.get('intervallo')
                self.scelte_unita: List[str] = dati.get('scelte_unita')
                self.unita_default: str = dati.get('unita_default')
                self.unita: str = dati.get('unita')
                self.default: int | float = dati.get('default')
                self.valore: int | float = dati.get('valore')

            case self.BOOLEANO:
                self.default: bool = dati.get('default')
                self.valore: bool = dati.get('valore')

            case self.COLORE:
                self.default: str = dati.get('default')
                self.valore: str = dati.get('valore')

            case self.SELEZIONE:
                self.scelte: List[str] = dati.get('scelte')
                self.default: int = dati.get('default')
                self.valore: int = dati.get('valore')

            case _:
                logger.error(f'Nel caricamento della configurazione, opzione con id {self.id} non ha un tipo valido ({self.tipo})')

    def __repr__(self):
        return 'Opzione ' + self.id

    @beartype
    def set(self, dati: Any):

        # if not isinstance(valore, type(opzione.valore)):
        #     logger.debug(f"Setter: id {id_opzione}, valore {valore} ({type(valore)}) non accettato, usare {type(opzione.valore)}")
        #     return False

        match self.tipo:

            case self.TESTO:
                assert isinstance(dati, str)

                if (self.lunghezza_massima is not None) and (len(dati) > self.lunghezza_massima):
                    logger.debug(f'Setter {self.id}, valore {dati} sfora la lunghezza massima di {self.lunghezza_massima}')
                    return False

                self.valore = dati
                return True

            case self.NUMERO:
                assert isinstance(dati, (int, float))

                if (self.intervallo is not None) and not (self.intervallo[0] <= dati <= self.intervallo[1]):
                    logger.debug(f'Setter {self.id}, valore {dati} sfora l\'intervallo di {self.intervallo}')
                    return False

                self.valore = dati
                return True

            case self.NUMERO_UNITA:
                self.intervallo
                self.scelte_unita

            case self.BOOLEANO:
                assert isinstance(dati, bool)

                self.valore = dati
                return True

            case self.COLORE:
                pass

            case self.SELEZIONE:
                self.valore = dati

    def esporta(self):
        dati = {
            'titolo': self.titolo,
            'descrizione': self.descrizione,
            'sezione': self.sezione,
            'tipo': self.tipo
        }

        match self.tipo:

            case self.TESTO:
                dati['lunghezza_massima'] = self.lunghezza_massima
                dati['default'] = self.default
                dati['valore'] = self.valore

            case self.NUMERO:
                dati['intervallo'] = self.intervallo
                dati['default'] = self.default
                dati['valore'] = self.valore

            case self.NUMERO_UNITA:
                dati['intervallo'] = self.intervallo
                dati['scelte_unita'] = self.scelte_unita
                dati['unita_default'] = self.unita_default
                dati['unita'] = self.unita
                dati['default'] = self.default
                dati['valore'] = self.valore

            case self.BOOLEANO:
                dati['default'] = self.default
                dati['valore'] = self.valore

            case self.COLORE:
                dati['default'] = self.default
                dati['valore'] = self.valore

            case self.SELEZIONE:
                dati['scelte'] = self.scelte
                dati['default'] = self.default
                dati['valore'] = self.valore

        return dati


class Opzioni(List):
    """
    Lista di opzioni
    Essenzialmente semplicemente una lista, con funzionalità aggiunte di ricerca per id
    """

    def __init__(self):
        super().__init__(self)

    def __getitem__(self, id):
        for opzione in self:
            if opzione.id == id:
                return opzione

        logger.warn(f'Cercando nelle opzioni, nessun id {id} trovato.')
        return None

    def ids(self):
        id_list = []
        for opzione in self:
            id_list.append(opzione.id)

        return id_list


class Configurazione:
    @beartype
    def __init__(self, file: Path = CONFIG_FILE):
        logger.debug('Inizializzazione caricamento configurazione')

        with open(file, encoding='utf-8') as configfile:
            logger.debug('Caricamento file di configurazione..')
            self.data = load(configfile)
            logger.debug(f'Raw data: {self.data}')

        # Todo: controllare validità file

        self.sezioni = []
        self.opzioni = Opzioni()

        for sectionid, sectiondata in self.data.get('sezioni').items():
            sezione = Sezione(sectionid, sectiondata)
            self.sezioni.append(sezione)

        for optionid, optiondata in self.data.get('opzioni').items():
            opzione = Opzione(optionid, optiondata)
            self.opzioni.append(opzione)

        # Tutti i dati sono caricati in oggetti, self.data non verrà aggiornato quindi eliminarlo per sicurezza
        del self.data

    def __repr__(self):
        return 'Configurazione default'

    @beartype
    def get(self, id_opzione: str):
        pass

    @beartype
    def set(self, id_opzione: str, dati: Any):
        if id_opzione not in self.opzioni.ids():
            logger.debug(f"Setter: id {id_opzione} non riconosciuto.")
            return False

        return self.opzioni[id_opzione].set(dati)

        # controllo validità valore

        # if hasattr(opzione, 'lunghezza_massima') and opzione.lunghezza_massima is not None:
        #     if valore > opzione.lunghezza_massima:
        #         logger.debug(f"Setter: id {id_opzione}, valore {valore} sfora la lunghezza massima di {opzione.lunghezza_massima}")
        #         return False

        # if hasattr(opzione, 'intervallo') and opzione.intervallo is not None:
        #     if not (opzione.intervallo[0] <= valore <= opzione.intervallo[1]):
        #         logger.debug(f"Setter: id {id_opzione}, valore {valore} sfora l'intervallo di {opzione.intervallo}")
        #         return False

    @beartype
    def aggiorna(self, configurazione: Dict, salva=True):
        for key, dati in configurazione.items():
            self.set(key, dati)

        if salva:
            self.esporta()

    @beartype
    def esporta(self, file: str | Path = CONFIG_FILE):
        dati = {
            'sezioni': {
                s.id: {'titolo': s.titolo, 'descrizione': s.descrizione} for s in self.sezioni
            },
            'opzioni': {
                o.id: o.esporta() for o in self.opzioni

            }
        }

        with open(file, 'w') as f:
            dump(dati, f, indent=2)


if __name__ == '__main__':  # * test
    c = Configurazione()

    for s in c.sezioni:
        print(s.titolo)

        for o in c.opzioni:
            if o.sezione == s.id:
                print('-', o.titolo)

    print(c.esporta())
