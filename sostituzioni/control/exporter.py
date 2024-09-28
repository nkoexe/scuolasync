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

import pandas as pd
import io
from datetime import datetime

from sostituzioni.model.model import Sostituzione


class Exporter:
    exported_buffer = None
    exported_mimetype = None

    class EmptyError(Exception):
        pass

    class FormatError(Exception):
        pass

    def esporta(filtri):
        sostituzioni = Sostituzione.load(filtri)

        # Creazione di liste di tutti gli attributi
        dati = {}
        for sostituzione in sostituzioni:
            for key, value in sostituzione.items():
                if key not in dati:
                    dati[key] = []
                dati[key].append(value)

        if not dati:
            Exporter.exported_buffer = None
            Exporter.exported_mimetype = None
            raise Exporter.EmptyError("Nessuna sostituzione trovata")

        for i in range(len(dati["data"])):
            dati["data"][i] = datetime.fromtimestamp(dati["data"][i]).date()
            dati["pubblicato"][i] = bool(dati["pubblicato"][i])
            dati["cancellato"][i] = bool(dati["cancellato"][i])

        dataframe = pd.DataFrame(
            {
                "Data": dati["data"],
                "Ora Predefinita": dati["ora_predefinita"],
                "Ora Inizio": dati["ora_inizio"],
                "Ora Fine": dati["ora_fine"],
                "Classe": dati["nome_classe"],
                "Aula": dati["numero_aula"],
                "Nome Docente": dati["nome_docente"],
                "Cognome Docente": dati["cognome_docente"],
                "Note": dati["note"],
                "Pubblicato": dati["pubblicato"],
                "Cancellato": dati["cancellato"],
            }
        )

        if filtri.get("formato") == "csv":
            Exporter.exported_buffer = io.StringIO()
            dataframe.to_csv(Exporter.exported_buffer, index=False)
            Exporter.exported_buffer.seek(0)
            Exporter.exported_mimetype = "text/csv"

            # Convert from stringio to bytesio
            bytesio = io.BytesIO()
            bytesio.write(Exporter.exported_buffer.getvalue().encode())
            bytesio.seek(0)
            Exporter.exported_buffer = bytesio

        elif filtri.get("formato") == "xlsx":
            Exporter.exported_buffer = io.BytesIO()
            writer = pd.ExcelWriter(Exporter.exported_buffer, date_format="dd/mm/yyyy")
            dataframe.style.set_properties(**{"text-align": "right"})
            dataframe.to_excel(writer, "Sostituzioni", index=False)

            border_format = writer.book.add_format({"border": 1})

            columns = len(dataframe.columns)
            rows = len(dataframe.index)
            writer.sheets["Sostituzioni"].conditional_format(
                "A2:" + chr(ord("A") + columns - 1) + str(rows + 1),
                {"type": "no_errors", "format": border_format},
            )

            for column in dataframe:
                column_width = (
                    max(dataframe[column].astype(str).map(len).max(), len(column)) + 3
                )
                col_idx = dataframe.columns.get_loc(column)
                writer.sheets["Sostituzioni"].set_column(col_idx, col_idx, column_width)

            writer.close()

            Exporter.exported_buffer.seek(0)
            Exporter.exported_mimetype = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            Exporter.exported_buffer = None
            Exporter.exported_mimetype = None
            raise Exporter.FormatError("Formato non supportato")

        return Exporter.exported_buffer, Exporter.exported_mimetype
