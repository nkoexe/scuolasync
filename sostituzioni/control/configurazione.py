"""
Gestione della configurazione del sistema tramite il file configurazione.json
"""

from pathlib import Path
from json import load, dump
import logging

from beartype._decor.decormain import beartype
from beartype.typing import List, Dict, Any

import sostituzioni.control.logging
from sostituzioni.lib.searchablelist import SearchableList

logger = logging.getLogger(__name__)


ROOT_PATH = Path(__file__).parent.parent
CONFIG_FILE = ROOT_PATH / "database" / "configurazione.json"


def parsepath(pathstring: str) -> Path:
    pathstring = pathstring.replace("%ROOT%", str(ROOT_PATH))

    return Path(pathstring)


class Sezione:
    """
    Gruppo di opzioni.
    """

    @beartype
    def __init__(self, id: str, dati: Dict):
        self.id = id
        self.titolo = dati.get("titolo")
        self.descrizione = dati.get("descrizione")
        self.opzioni = []

    def __repr__(self):
        return "Sezione" + self.id


class Opzione:
    """
    Singola opzione per la configurazione del sistema.
    """

    TESTO = "testo"
    NUMERO = "numero"
    NUMERO_UNITA = "numero_unita"
    BOOLEANO = "booleano"
    COLORE = "colore"
    SELEZIONE = "selezione"
    PERCORSO = "percorso"

    @beartype
    def __init__(self, id: str, dati: Dict):
        self.id = id

        self.titolo: str = dati.get("titolo", "Titolo Opzione")
        self.descrizione: str = dati.get("descrizione", "Descrizione Opzione")
        self.sezione: str = dati.get("sezione", "test")
        self.disabilitato: bool = dati.get("disabilitato", False)
        self.nascosto: bool = dati.get("nascosto", False)

        self.tipo: str = dati.get("tipo")

        match self.tipo:
            case self.TESTO:
                self.lunghezza_massima = dati.get("lunghezza_massima")
                self.default = dati.get("default")
                self.valore = dati.get("valore")

            case self.NUMERO:
                self.intervallo: List[int | None] = dati.get("intervallo")
                self.default: int | float = dati.get("default")
                self.valore: int | float = dati.get("valore")

            case self.NUMERO_UNITA:
                self.intervallo: List[int | None] = dati.get("intervallo")
                self.scelte_unita: List[str] = dati.get("scelte_unita")
                self.unita_default: int = dati.get("unita_default")
                self.unita: int = dati.get("unita")
                self.default: int | float = dati.get("default")
                self.valore: int | float = dati.get("valore")

            case self.BOOLEANO:
                self.default: bool = dati.get("default")
                self.valore: bool = dati.get("valore")

            case self.COLORE:
                self.default: str = dati.get("default")
                self.valore: str = dati.get("valore")

            case self.SELEZIONE:
                self.scelte: List[str] = dati.get("scelte")
                self.default: int = dati.get("default")
                self.valore: int = dati.get("valore")

            case self.PERCORSO:
                self.radice: int = dati.get("radice")
                self.scelte_radice: List[str] = dati.get("scelte_radice")
                self.default: str = dati.get("default")
                self.valore: str = dati.get("valore")

                self.path = parsepath(self.scelte_radice[self.radice]) / parsepath(
                    self.valore
                )

            case _:
                logger.error(
                    f"Nel caricamento della configurazione, opzione con id {self.id} non ha un tipo valido ({self.tipo})"
                )

    def __repr__(self):
        return self.valore

    @beartype
    def set(self, dati: Any, force: bool = False):
        logger.debug(f"Setter {self.id}: {dati}")

        if not force and (self.disabilitato or self.nascosto):
            logger.debug("Setter disabilitato, impossibile aggiornare l'opzione.")
            return False

        match self.tipo:
            case self.TESTO:
                if not isinstance(dati, str):
                    raise TypeError(
                        f"Dati non validi, fornire stringa, non {type(dati)}"
                    )

                if (self.lunghezza_massima is not None) and (
                    len(dati) > self.lunghezza_massima
                ):
                    logger.debug(
                        f"Setter {self.id}, valore {dati} sfora la lunghezza massima di {self.lunghezza_massima}"
                    )
                    return False

                self.valore = dati
                return True

            case self.NUMERO:
                if not isinstance(dati, (int, float)):
                    raise TypeError(
                        f"Dati non validi, fornire int o float, non {type(dati)}"
                    )

                if (
                    (self.intervallo[0] is not None)
                    and not (self.intervallo[0] <= dati)
                ) or (
                    (self.intervallo[1] is not None)
                    and not (dati <= self.intervallo[1])
                ):
                    logger.error(
                        f"Valore {dati} sfora l'intervallo di {self.intervallo}"
                    )
                    return False

                self.valore = dati
                return True

            case self.NUMERO_UNITA:
                if not isinstance(dati, (list, tuple)) or len(dati) != 2:
                    raise ValueError(
                        f"Dati {dati} non validi, per numero con unità fornire (valore, index_unita)"
                    )
                if not isinstance(dati[0], (int, float)):
                    raise TypeError(
                        "Valore del numero deve essere di tipo int o float, non "
                        + str(type(dati[0]))
                    )
                if not isinstance(dati[1], int):
                    raise TypeError(
                        "L'indice dell'unità deve essere di tipo int, non "
                        + str(type(dati[1]))
                    )
                if not 0 <= dati[1] < len(self.scelte_unita):
                    raise ValueError(
                        f"L'indice dell'unità {dati[1]} non è valido, deve essere compreso tra 0 e {len(self.scelte_unita) - 1}"
                    )

                if (
                    (self.intervallo[0] is not None)
                    and not (self.intervallo[0] <= dati[0])
                ) and (
                    (self.intervallo[1] is not None)
                    and not (dati[0] <= self.intervallo[1])
                ):
                    logger.warning(
                        f"Valore {dati[0]} sfora l'intervallo di {self.intervallo}"
                    )
                    return False

                self.valore = dati[0]
                self.unita = dati[1]
                return True

            case self.BOOLEANO:
                if not isinstance(dati, bool):
                    raise TypeError(
                        "Valore deve essere di tipo bool, non " + str(type(dati))
                    )

                self.valore = dati
                return True

            case self.COLORE:
                pass

            case self.SELEZIONE:
                if not isinstance(dati, int):
                    raise TypeError(
                        "Valore deve essere di tipo int, non " + str(type(dati))
                    )
                if not 0 <= dati < len(self.scelte):
                    raise ValueError(
                        f"Valore {dati} non valido, deve essere compreso tra 0 e {len(self.scelte) - 1}"
                    )

                self.valore = dati
                return True

            case self.PERCORSO:
                if not isinstance(dati, (list, tuple)) or len(dati) != 2:
                    raise ValueError(
                        "Dati non validi, per percorso fornire (index_radice, percorso)"
                    )
                if not isinstance(dati[0], int):
                    raise TypeError(
                        "L'indice della radice deve essere di tipo int, non "
                        + str(type(dati[0]))
                    )
                if not isinstance(dati[1], (str, Path)):
                    raise TypeError(
                        "Il percorso deve essere di tipo str o Path, non "
                        + str(type(dati[1]))
                    )
                if not 0 <= dati[0] < len(self.scelte_radice):
                    raise ValueError(
                        f"L'indice della radice {dati[0]} non è valido, deve essere compreso tra 0 e {len(self.scelte_radice) - 1}"
                    )

                if isinstance(dati[1], Path):
                    dati[1] = dati[1].as_posix()

                self.radice = dati[0]
                self.valore = dati[1]

                self.path = parsepath(self.scelte_radice[self.radice]) / parsepath(
                    self.valore
                )

                return True

    def esporta(self):
        dati = {
            "titolo": self.titolo,
            "descrizione": self.descrizione,
            "sezione": self.sezione,
            "disabilitato": self.disabilitato,
            "nascosto": self.nascosto,
            "tipo": self.tipo,
        }

        match self.tipo:
            case self.TESTO:
                dati["lunghezza_massima"] = self.lunghezza_massima
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.NUMERO:
                dati["intervallo"] = self.intervallo
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.NUMERO_UNITA:
                dati["intervallo"] = self.intervallo
                dati["scelte_unita"] = self.scelte_unita
                dati["unita_default"] = self.unita_default
                dati["unita"] = self.unita
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.BOOLEANO:
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.COLORE:
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.SELEZIONE:
                dati["scelte"] = self.scelte
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.PERCORSO:
                dati["radice"] = self.radice
                dati["scelte_radice"] = self.scelte_radice
                dati["default"] = str(self.default)
                dati["valore"] = str(self.valore)

        return dati


class Configurazione:
    @beartype
    def __init__(self, file: Path = CONFIG_FILE):
        logger.debug("Inizializzazione caricamento configurazione")

        with open(file, encoding="utf-8") as configfile:
            logger.debug("Caricamento file di configurazione..")
            self.data = load(configfile)
            logger.debug(f"Raw data: {self.data}")

        # Todo: controllare validità file

        self.sezioni = []
        self.opzioni = SearchableList()

        for sectionid, sectiondata in self.data.get("sezioni").items():
            sezione = Sezione(sectionid, sectiondata)
            self.sezioni.append(sezione)

        for optionid, optiondata in self.data.get("opzioni").items():
            opzione = Opzione(optionid, optiondata)
            self.opzioni.append(opzione)

        # Tutti i dati sono caricati in oggetti, self.data non verrà aggiornato quindi eliminarlo per sicurezza
        del self.data

        # Aggiorna il percorso base di sistema e quello del file di configurazione
        self.set("rootpath", [0, str(ROOT_PATH)], force=True)
        self.set("configpath", [0, str(CONFIG_FILE)], force=True)

    def __repr__(self):
        return "Configurazione default"

    @beartype
    def get(self, id_opzione: str) -> Opzione | None:
        """
        La funzione get recupera un oggetto Opzione in base al suo ID o restituisce None se l'ID non è trovato.

        :param id_opzione: Il parametro id_opzione è una stringa che rappresenta l'ID di un'opzione.
        :type id_opzione: str

        :return: Il metodo get restituisce un'istanza della classe Opzione se l'id_opzione è
        trovato nel dizionario self.opzioni. Se l'id_opzione non viene trovato, restituisce None.
        """
        if self.opzioni.get(id_opzione) is None:
            logger.warning(f"Getter: id {id_opzione} non trovato.")
            return None

        return self.opzioni.get(id_opzione)

    @beartype
    def set(self, id_opzione: str, dati: Any, force: bool = False) -> bool:
        """
        La funzione verifica se l'ID dell'opzione fornito è valido e imposta il valore di quell'opzione se lo è.

        :param id_opzione: Il parametro id_opzione è una stringa che rappresenta l'ID di un'opzione.
        :type id_opzione: str

        :param dati: Il valore o i valori che verranno inseriti. A dipendere dal tipo dell'opzione, questo parametro può
                     essere un testo, un numero, un booleano, o una lista di valori se l'opzione è composta.

        :param force: Forza l'aggiornamento di un'impostazione, anche se essa è disabilitata.

        :return: Success. Se l'id_opzione non è riconosciuto, restituisce False. In caso contrario,
                 chiama il metodo set dell'oggetto opzioni[id_opzione] con il parametro dati e restituisce il risultato.
        """

        if id_opzione not in self.opzioni.keys():
            logger.warning(f"Setter: id {id_opzione} non riconosciuto.")
            return False

        return self.opzioni.get(id_opzione).set(dati, force)

    @beartype
    def aggiorna(self, configurazione: Dict, salva=True) -> bool:
        """
        Questa funzione aggiorna le impostazioni di configurazione utilizzando un dizionario 'configurazione' che
        contiene coppie chiave-valore, dove ogni chiave rappresenta l'id di un'opzione e il valore (singolo o multiplo)
        corrispondente rappresenta il nuovo valore per quell'opzione.

        :param configurazione: Dizionario contenente i dati di configurazione da aggiornare.
        :type configurazione: dict

        :param salva: Un flag booleano che determina se la configurazione aggiornata deve essere esportata su file.
                      (valore predefinito: True)
        :type salva: bool
        """

        for key, dati in configurazione.items():
            ok = self.set(key, dati)

            if not ok:
                return False

        if salva:
            self.esporta()

        return True

    @beartype
    def esporta(self, file: str | Path = CONFIG_FILE):
        """
        La funzione esporta esporta i dati di configurazione in un file nel formato JSON.

        :param file: Il parametro file rappresenta il percorso del file in cui i dati verranno esportati.
        :type file: str | Path
        """

        dati = {
            "sezioni": {
                s.id: {"titolo": s.titolo, "descrizione": s.descrizione}
                for s in self.sezioni
            },
            "opzioni": {o.id: o.esporta() for o in self.opzioni},
        }

        with open(file, "w") as f:
            dump(dati, f, indent=2)


configurazione = Configurazione()
