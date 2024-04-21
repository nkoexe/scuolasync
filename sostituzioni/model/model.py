"""
descr
"""

from beartype._decor.decormain import beartype
from datetime import datetime
import logging

from sostituzioni.lib.searchablelist import SearchableList
from sostituzioni.control.database import (
    Aula,
    Classe,
    Docente,
    OraPredefinita,
    NotaStandard,
    Sostituzione,
    Evento,
    Notizia,
    Visualizzazione,
    Utente,
    Ruolo,
)


logger = logging.getLogger(__name__)


class Docente(Docente):
    def __init__(
        self,
        nome: str | None = None,
        cognome: str | None = None,
        cancellato: bool = False,
    ):
        self.nome = nome
        self.nome = nome
        self.cognome = cognome
        self.cancellato = cancellato


class Sostituzione(Sostituzione):
    def __init__(
        self,
        # id: int | None = None,
        # aula: Aula | None = None,
        # classe: Classe | None = None,
        # docente: Docente | None = None,
        # data: int | None = None,
        # ora_inizio: str | None = None,
        # ora_fine: str | None = None,
        # ora_predefinita: OraPredefinita | None = None,
        # note: str | None = None,
        # pubblicato: bool = False,
        dati: dict,
    ):
        super(Sostituzione, self).__init__()

        self.incompleta: bool = False
        self.sovrapposizioni: bool = False
        self.elemento_sovrapposizione: str | None = None

        # if id is not None:
        #     super().__init__(id)
        # elif dati is not None:
        #     super().__init__(None, dati)
        # else:
        # self.aula = aula
        # self.classe = classe
        # self.docente = docente
        # self.data = data
        # self.ora_inizio = ora_inizio
        # self.ora_fine = ora_fine
        # self.ora_predefinita = ora_predefinita
        # self.note = note
        # self.pubblicato = pubblicato

        if "id" in dati:
            # Sostituzione esistente dato che l'id è presente

            # Controlla che i dati inseriti siano validi
            if not all(
                [
                    attr in dati
                    for attr in [
                        "cancellato",
                        "pubblicato",
                        "numero_aula",
                        "nome_classe",
                        "nome_docente",
                        "cognome_docente",
                        "data",
                        "ora_predefinita",
                        "ora_inizio",
                        "ora_fine",
                        "note",
                    ]
                ]
            ):
                raise ValueError(f"Sostituzione con id {id} ha dati invalidi - {dati}")

            self.id = dati.get("id", None)
            self.cancellato = dati["cancellato"]
            self.pubblicato = dati["pubblicato"]
            self.numero_aula = dati["numero_aula"]
            self.nome_classe = dati["nome_classe"]
            self.nome_docente = dati["nome_docente"]
            self.cognome_docente = dati["cognome_docente"]
            self.data = dati["data"]
            self.ora_predefinita = dati["ora_predefinita"]
            self.ora_inizio = dati["ora_inizio"]
            self.ora_fine = dati["ora_fine"]
            self.note = dati["note"]
        else:
            # Sostituzione nuova

            # Controlla che i dati inseriti siano validi
            if not all(
                [
                    attr in dati
                    for attr in [
                        "pubblicato",
                        "numero_aula",
                        "nome_classe",
                        "docente",
                        "data",
                        "ora_predefinita",
                        "ora_inizio",
                        "ora_fine",
                        "note",
                    ]
                ]
            ):
                raise ValueError(f"Inserimento Sostituzione con dati invalidi - {dati}")

            self.id = None
            self.pubblicato = dati["pubblicato"]
            self.numero_aula = dati["numero_aula"]
            self.nome_classe = dati["nome_classe"]
            self.docente = dati["docente"]
            self.data = dati["data"]
            self.ora_predefinita = dati["ora_predefinita"]
            self.ora_inizio = dati["ora_inizio"]
            self.ora_fine = dati["ora_fine"]
            self.note = dati["note"]

    def __repr__(self):
        return f"<Sostituzione({self.id}, {self.cancellato}, {self.pubblicato}, {self.numero_aula}, {self.nome_classe}, {self.nome_docente} {self.cognome_docente}, {self.data}, {self.ora_predefinita}, {self.ora_inizio}, {self.ora_fine}, {self.note})>"

    def __str__(self):
        return f"Sostituzione {self.id if self.id is not None else '(nuova)'} - ({self.numero_aula}, {self.nome_classe}, {self.nome_docente} {self.cognome_docente}, {self.data}, {self.ora_predefinita}, {self.ora_inizio}, {self.ora_fine}, {self.note})"


class Evento(Evento):
    def __init__(
        self,
        id: int | None = None,
        urgente: bool | None = None,
        data_ora_inizio: int | None = None,
        data_ora_fine: int | None = None,
        testo: str | None = None,
    ):
        self.id = id
        self.urgente = urgente
        self.data_ora_inizio = data_ora_inizio
        self.data_ora_fine = data_ora_fine
        self.testo = testo


class Notizia(Notizia):
    def __init__(
        self,
        id: int | None = None,
        data_inizio: int | None = None,
        data_fine: int | None = None,
        testo: str | None = None,
    ):
        self.id = id
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.testo = testo


# class VisualizzazioneOnline(Visualizzazione):
#     def __init__(self):
#         pass


# class VisualizzazioneFisica(Visualizzazione):
#     def __init__(self):
#         pass


# //////////////////////////////////


class Sostituzioni(SearchableList):
    def __init__(self):
        super().__init__(key_name="id")

    def load(self):
        self.extend([Sostituzione(data) for data in Sostituzione.load()])
        self.check_errors()

    def to_json(self):
        descrizioni_sovrapposizioni = {
            "docente": "Errore: Il docente ha una supplenza alla stessa ora.",
            "aula": "Errore: Questa aula ha due supplenze in contemporanea.",
            "classe": "Errore: Questa classe ha due supplenze in contemporanea.",
        }
        return [
            {
                "id": sostituzione.id,
                "cancellato": sostituzione.cancellato,
                "pubblicato": sostituzione.pubblicato,
                "numero_aula": sostituzione.numero_aula,
                "nome_classe": sostituzione.nome_classe,
                "nome_docente": sostituzione.nome_docente,
                "cognome_docente": sostituzione.cognome_docente,
                "data": sostituzione.data,
                "ora_predefinita": sostituzione.ora_predefinita,
                "ora_inizio": sostituzione.ora_inizio,
                "ora_fine": sostituzione.ora_fine,
                "note": sostituzione.note,
                "incompleta": sostituzione.incompleta,
                "sovrapposizioni": sostituzione.sovrapposizioni,
                "descrizione_sovrapposizione": descrizioni_sovrapposizioni.get(
                    sostituzione.elemento_sovrapposizione, None
                ),
            }
            for sostituzione in self
        ]

    @staticmethod
    @beartype
    def check_incompleta(sostituzione: Sostituzione):
        return not all(
            (
                sostituzione.data,
                (
                    sostituzione.ora_predefinita
                    or (sostituzione.ora_inizio and sostituzione.ora_fine)
                ),
                sostituzione.numero_aula,
                sostituzione.nome_classe,
                sostituzione.nome_docente,
                sostituzione.cognome_docente,
            )
        )

    @beartype
    def check_sovrapposizioni(
        self, sostituzione: Sostituzione
    ) -> tuple[bool, str | None]:
        """
        Controlla se una sostituzione ha errori di sovrapposizione
        Sono considerati errori:
        - Stessa data e ora, e stessa aula
        - Stessa data e ora, stessa classe
        - Stessa data e ora, stesso docente

        Ritorna un tuple con il risultato e il motivo dell'errore
        """

        for sostituzione_altra in self:
            if (
                sostituzione_altra.id != sostituzione.id
                and sostituzione.cancellato == False
                and sostituzione_altra.cancellato == False
                and sostituzione_altra.data == sostituzione.data
                and (
                    sostituzione_altra.ora_predefinita == sostituzione.ora_predefinita
                    if (
                        sostituzione_altra.ora_predefinita is not None
                        and sostituzione.ora_predefinita is not None
                    )
                    else (
                        sostituzione_altra.ora_inizio is not None
                        and (
                            sostituzione_altra.ora_inizio == sostituzione.ora_inizio
                            or sostituzione_altra.ora_fine == sostituzione.ora_fine
                        )
                        # Todo: check per ora_inizio2 > ora_fine1 oppure ora_inizio1 > ora_fine2
                    )
                )
            ):
                if sostituzione.nome_classe is not None and (
                    sostituzione_altra.nome_classe == sostituzione.nome_classe
                ):
                    return True, "classe"
                if sostituzione.numero_aula is not None and (
                    sostituzione_altra.numero_aula == sostituzione.numero_aula
                ):
                    return True, "aula"
                if (
                    sostituzione.nome_docente
                    and (
                        sostituzione_altra.nome_docente == sostituzione.nome_docente
                        and sostituzione_altra.cognome_docente
                    )
                    == sostituzione.cognome_docente
                ):
                    return True, "docente"

        return False, None

    def check_errors(self, sostituzione: Sostituzione | None = None):
        if sostituzione is None:
            for sostituzione in self:
                sostituzione.incompleta = self.check_incompleta(sostituzione)

                sostituzione.sovrapposizioni, sostituzione.elemento_sovrapposizione = (
                    self.check_sovrapposizioni(sostituzione)
                )
        else:
            sostituzione.incompleta = self.check_incompleta(sostituzione)

            sostituzione.sovrapposizioni, sostituzione.elemento_sovrapposizione = (
                self.check_sovrapposizioni(sostituzione)
            )

    @beartype
    def filtra(self, filtri: dict | None = None):
        """
        filtri:
        `{ cancellato: true }`  // per mostrare anche sostituzioni cancellate
        `{ non_pubblicato: true }`  // per mostrare anche sostituzioni non pubblicate
        `{ data_inizio: 1702767600, data_fine: 1702854000 }`  // per sostituzioni comprese in un intervallo
        `{ data_inizio: 1702767600, data_fine: None }`  // per sostituzioni future
        """

        if filtri is None:
            return self.to_json()

        # filtri: dict
        lista_filtrata = Sostituzioni()

        data_inizio: int | None = filtri.get(
            "data_inizio",
            int(
                datetime.today()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            ),
        )  # default è oggi

        data_fine: int | None = filtri.get(
            "data_fine", None
        )  # default è nessuna, quindi future

        if data_inizio is None:
            data_inizio = 0

        # Mostra anche i cancellati
        cancellato = filtri.get("cancellato", False)
        non_pubblicato = filtri.get("non_pubblicato", False)

        for sostituzione in self:
            if (
                (data_inizio is None or sostituzione.data >= data_inizio)
                and (data_fine is None or sostituzione.data <= data_fine)
                and (
                    (sostituzione.cancellato is False) if cancellato else True
                )  # Includi anche le sostituzioni cancellate se
                and ((sostituzione.pubblicato is True) if not non_pubblicato else True)
            ):
                lista_filtrata.append(sostituzione)

        return lista_filtrata.to_json()

    @beartype
    def inserisci(self, sostituzione: Sostituzione):
        try:
            sostituzione.inserisci()
        except Exception as e:
            logger.error(
                f"Errore durante l'inserimento della sostituzione {sostituzione}"
            )
            raise e

        self.append(sostituzione)
        # self.check_errors(sostituzione)
        self.check_errors()

    @beartype
    def modifica(self, id: int, data: dict):
        sostituzione = self.get(id)
        try:
            sostituzione.modifica(data)
        except Exception as e:
            logger.error(
                f"Errore durante la modifica della sostituzione {sostituzione}"
            )
            raise e

        # self.check_errors(sostituzione)
        self.check_errors()

    @beartype
    def elimina(self, id: int, mantieni_in_storico: bool = True):
        # todo: usare default mantieniinstorico di configurazione

        sostituzione = self.get(id)
        try:
            sostituzione.elimina(mantieni_in_storico)
        except Exception as e:
            logger.error(
                f"Errore durante l'eliminazione della sostituzione {sostituzione}"
            )
            raise e

        self.remove(sostituzione)
        self.check_errors()


sostituzioni = Sostituzioni()
sostituzioni.load()

# print(sostituzioni[0].id)
# print(sostituzioni.get((375)))
# print(sostituzioni.filtra({"cancellato": True}))
