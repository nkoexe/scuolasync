import pandas as pd

from sostituzioni.model.model import Sostituzione


def esporta(filtri):
    sostituzioni = Sostituzione.load()

    # Creazione di liste di tutti gli attributi
    dati = {}
    for sostituzione in sostituzioni:
        for key, value in sostituzione.items():
            if key not in dati:
                dati[key] = []
            dati[key].append(value)

    dataframe = pd.DataFrame(
        {
            "Data": dati["data"],
            "Ora Predefinita": dati["numero_ora_predefinita"],
            "Ora Inizio": dati["ora_inizio"],
            "Ora Fine": dati["ora_fine"],
            "Classe": dati["nome_classe"],
            "Aula": dati["numero_aula"],
            "Nome Docente": dati["nome_docente"],
            "Cognome Docente": dati["cognome_docente"],
            "Note": dati["note"],
        }
    )
    print(dataframe)

    dataframe.to_excel("export.xlsx", "Sostituzioni")
    return ""
