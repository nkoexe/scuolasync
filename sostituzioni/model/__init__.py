from sostituzioni.model.model import database


aule, classi, docenti, ore_predefinite, sostituzioni, eventi, notizie, visualizzazioni_online, visualizzazioni_fisiche = database.load_all()


for i in classi:
    print(i.aule_ospitanti)

for i in docenti:
    print(i.nome, i.cognome)
