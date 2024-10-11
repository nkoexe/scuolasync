"""
    This file is part of ScuolaSync.

    Copyright (C) 2023-present Niccolò Ragazzi <hi@njco.dev>

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
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


class Classe(Classe):
    def __init__(
        self,
        nome: str = "",
        aule_ospitanti: list = [],
        cancellato: bool = False,
    ):
        self.nome = nome
        self.aule_ospitanti = aule_ospitanti
        self.cancellato = cancellato
        self.in_database = False

        dati = self.load({"nome": nome})
        if dati:
            self.in_database = True
            self.aule_ospitanti = dati[0]["aule_ospitanti"]
            self.cancellato = dati[0]["cancellato"]

    def elimina(self, mantieni_in_storico: bool = False):
        super().elimina(mantieni_in_storico)
        self.in_database = False


class Aula(Aula):
    def __init__(
        self,
        numero: str = "",
        piano: str = "0",
        cancellato: bool = False,
    ):
        self.numero = numero
        self.piano = piano
        self.cancellato = cancellato
        self.in_database = False

        dati = self.load({"numero": numero})
        if dati:
            self.in_database = True
            self.piano = dati[0]["piano"]
            self.cancellato = dati[0]["cancellato"]

    def elimina(self, mantieni_in_storico: bool = False):
        super().elimina(mantieni_in_storico)
        self.in_database = False


class Docente(Docente):
    def __init__(
        self,
        nome: str = "",
        cognome: str = "",
        cancellato: bool = False,
    ):
        self.nome = nome
        self.cognome = cognome
        self.cancellato = cancellato
        self.in_database = False

        dati = self.load({"nome": nome, "cognome": cognome})
        if dati:
            self.in_database = True
            self.cancellato = dati[0]["cancellato"]

    def elimina(self, mantieni_in_storico: bool = False):
        super().elimina(mantieni_in_storico)
        self.in_database = False


class OraPredefinita(OraPredefinita):
    def __init__(self, numero: str, ora_inizio: str = "", ora_fine: str = ""):
        self.numero = numero
        self.ora_inizio = ora_inizio
        self.ora_fine = ora_fine
        self.in_database = False

        dati = self.load(
            {"numero": numero, "ora_inizio": ora_inizio, "ora_fine": ora_fine}
        )
        if dati:
            self.in_database = True
            self.ora_inizio = dati[0]["ora_inizio_default"]
            self.ora_fine = dati[0]["ora_fine_default"]

    def elimina(self):
        super().elimina()
        self.in_database = False


class NotaStandard(NotaStandard):
    def __init__(self, testo: str):
        self.testo = testo
        self.in_database = False

        dati = self.load({"testo": testo})
        if dati:
            self.in_database = True

    def elimina(self):
        super().elimina()
        self.in_database = False


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
        self.sovrapposizioni: list = []
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
        self.indice_per_data = {}

    def load(self):
        self.extend(
            [
                Sostituzione(data)
                for data in Sostituzione.load(
                    {
                        "data_inizio": 0,
                        "data_fine": None,
                        "non_pubblicato": True,
                        "cancellato": True,
                    }
                )
            ]
        )

        for sostituzione in self:
            if not sostituzione.cancellato:
                self.aggiungi_a_indice(sostituzione)

        self.check_errori()

    def aggiungi_a_indice(self, sostituzione: Sostituzione):
        if sostituzione.data not in self.indice_per_data:
            self.indice_per_data[sostituzione.data] = []

        self.indice_per_data[sostituzione.data].append(sostituzione)

    def rimuovi_da_indice(self, sostituzione: Sostituzione):
        if sostituzione.data in self.indice_per_data:
            self.indice_per_data[sostituzione.data].remove(sostituzione)
            if len(self.indice_per_data[sostituzione.data]) == 0:
                del self.indice_per_data[sostituzione.data]

    def to_json(self):
        descrizioni_sovrapposizione = {
            "docente": "Il docente ha una supplenza alla stessa ora.",
            "aula": "Questa aula ha due supplenze in contemporanea.",
            "classe": "Questa classe ha due supplenze in contemporanea.",
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
                # idea: mandare la lista di sovrapposizioni, on hover l'altra sostituzione con errore lampeggia
                "sovrapposizioni": len(sostituzione.sovrapposizioni) > 0,
                "descrizione_sovrapposizione": descrizioni_sovrapposizione.get(
                    sostituzione.elemento_sovrapposizione, None
                ),
            }
            for sostituzione in self
        ]

    @staticmethod
    @beartype
    def check_incompleta(sostituzione: Sostituzione):
        sostituzione.incompleta = not all(
            (
                sostituzione.data,
                (
                    # Controlla che ci sia ora predefinita oppure ora manuale
                    sostituzione.ora_predefinita
                    or (sostituzione.ora_inizio and sostituzione.ora_fine)
                ),
                (
                    # Se l'ora predefinita é una pausa non è necessario che ci sia una classe
                    sostituzione.nome_classe
                    if (
                        sostituzione.ora_predefinita
                        and ("Pausa" not in sostituzione.ora_predefinita)
                    )
                    else True
                ),
                sostituzione.numero_aula,
                sostituzione.nome_docente,
                sostituzione.cognome_docente,
            )
        )

    @beartype
    def check_sovrapposizioni(
        self,
        sostituzione: Sostituzione,
        contrassegna_altre: bool = False,
    ):
        """
        Controlla se una sostituzione ha errori di sovrapposizione
        Sono considerati errori:
        - Stessa data e ora, e stessa aula
        - Stessa data e ora, stessa classe
        - Stessa data e ora, stesso docente
        """

        if sostituzione.data not in self.indice_per_data:
            return False, None

        for sostituzione_altra in self.indice_per_data[sostituzione.data]:
            # Controllo per supplenze contemporanee
            if (
                # Non devono essere cancellate e non devono essere la stessa sostituzione
                # Il controllo avviene anche alle sostituzioni non pubblicate
                sostituzione_altra.id != sostituzione.id
                and not sostituzione.cancellato
                and not sostituzione_altra.cancellato
                and (
                    # Se entrambe le sostituzioni hanno ora_predefinita, controlla che siano uguali
                    sostituzione_altra.ora_predefinita == sostituzione.ora_predefinita
                    if (
                        sostituzione_altra.ora_predefinita
                        and sostituzione.ora_predefinita
                    )
                    else (
                        # Altrimenti controlla che la ora d'inizio di una sia anteriore all'altra
                        (
                            sostituzione.ora_inizio
                            and sostituzione_altra.ora_fine
                            and (sostituzione.ora_inizio < sostituzione_altra.ora_fine)
                        )
                        # Oppure che la ora di fine sia posteriore all'altra
                        or (
                            sostituzione.ora_fine
                            and sostituzione_altra.ora_inizio
                            and (sostituzione.ora_fine > sostituzione_altra.ora_inizio)
                        )
                    )
                )
            ):
                # Controlli per sostituzioni contemporanee, riordinare gli if per stabilire la gerarchia
                # In una sostituzione che ha sovrapposizioni sia di classe sia di docente, se l'if di classe
                # è antecedente, il messaggio mostrato sarà per la classe.

                # Stessa classe
                if sostituzione.nome_classe and (
                    sostituzione_altra.nome_classe == sostituzione.nome_classe
                ):
                    if contrassegna_altre:
                        sostituzione_altra.sovrapposizioni.append(sostituzione)
                        sostituzione_altra.elemento_sovrapposizione = "classe"

                    sostituzione.sovrapposizioni.append(sostituzione_altra)
                    sostituzione.elemento_sovrapposizione = "classe"

                    return True

                # Stessa aula
                elif sostituzione.numero_aula and (
                    sostituzione_altra.numero_aula == sostituzione.numero_aula
                ):
                    if contrassegna_altre:
                        sostituzione_altra.sovrapposizioni.append(sostituzione)
                        sostituzione_altra.elemento_sovrapposizione = "aula"

                    sostituzione.sovrapposizioni.append(sostituzione_altra)
                    sostituzione.elemento_sovrapposizione = "aula"

                    return True

                # Stesso docente
                elif (
                    sostituzione.nome_docente
                    and (
                        sostituzione_altra.nome_docente == sostituzione.nome_docente
                        and sostituzione_altra.cognome_docente
                    )
                    == sostituzione.cognome_docente
                ):
                    if contrassegna_altre:
                        sostituzione_altra.sovrapposizioni.append(sostituzione)
                        sostituzione_altra.elemento_sovrapposizione = "docente"

                    sostituzione.sovrapposizioni.append(sostituzione_altra)
                    sostituzione.elemento_sovrapposizione = "docente"

                    return True

        sostituzione.sovrapposizioni = []
        sostituzione.elemento_sovrapposizione = None

        return False

    @beartype
    def rimuovi_altre_sovrapposizioni(self, sostituzione: Sostituzione):
        for sostituzione_altra in sostituzione.sovrapposizioni:
            self.check_sovrapposizioni(sostituzione_altra)

    @beartype
    def check_errori(
        self,
        sostituzione: Sostituzione | None = None,
    ):

        if sostituzione:
            self.check_incompleta(sostituzione)
            self.check_sovrapposizioni(sostituzione, contrassegna_altre=True)

        else:
            # totaltimeincompleta = 0
            # totaltimesovrapposizioni = 0

            for sostituzione in self:
                # start_time = time()
                self.check_incompleta(sostituzione)
                # incompleta_time = time()

                self.check_sovrapposizioni(sostituzione)
                # sovrapposizioni_time = time()

                # totaltimeincompleta += incompleta_time - start_time
                # totaltimesovrapposizioni += sovrapposizioni_time - incompleta_time

            # print(f"incompleta - {totaltimeincompleta:.6f}")
            # print(f"sovrapposizioni - {totaltimesovrapposizioni:.6f}")

    @beartype
    def filtra(self, filtri: dict | None = None):
        """
        filtri:
        `{ cancellato: true }`  // per mostrare anche sostituzioni cancellate
        `{ non_pubblicato: true }`  // per mostrare anche sostituzioni non pubblicate
        `{ data_inizio: 1702767600, data_fine: 1702854000 }`  // per sostituzioni comprese in un intervallo
        `{ data_inizio: 1702767600, data_fine: None }`  // per sostituzioni future
        """

        if not isinstance(filtri, dict):
            filtri = {}

        # Questa roba salva letteralmente 1ms shit aint worth it
        # if str(filtri) in self.json_salvati:
        # return self.json_salvati[str(filtri)]

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
                (sostituzione.data >= data_inizio)
                and ((data_fine is None) or (sostituzione.data <= data_fine))
                # Filtra solo per sostituzioni non cancellate, altrimenti includi anche quelle cancellate
                and ((not sostituzione.cancellato) if not cancellato else True)
                # Filtra solo per le sostituzioni pubblicate se non_pubblicato è false, altrimenti includi tutte
                and ((sostituzione.pubblicato) if not non_pubblicato else True)
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
        self.aggiungi_a_indice(sostituzione)
        self.check_errori(sostituzione)

    @beartype
    def modifica(self, id: int, data: dict):
        # start_time = time()

        sostituzione: Sostituzione = self.get(id)

        self.rimuovi_da_indice(sostituzione)

        try:
            sostituzione.modifica(data)
        except Exception as e:
            logger.error(
                f"Errore durante la modifica della sostituzione {sostituzione}"
            )
            raise e

        # print(f"modifica - {time() - start_time:.6f}")

        self.aggiungi_a_indice(sostituzione)

        self.rimuovi_altre_sovrapposizioni(sostituzione)
        self.check_errori(sostituzione)

        # print(f"errori - {time() - start_time:.6f}")

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
        self.rimuovi_altre_sovrapposizioni(sostituzione)
        self.rimuovi_da_indice(sostituzione)

        del sostituzione


sostituzioni = Sostituzioni()
sostituzioni.load()

# print(sostituzioni[0].id)
# print(sostituzioni.get((375)))
# print(sostituzioni.filtra({"cancellato": True}))
