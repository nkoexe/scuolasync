## Da mettere nella documentazione:

del obj, obj.elimina() e obj.cancella() sono la stessa cosa

init chiama setter di attributo per mettere tutto in un posto, beartype controlla type di attributo e nella funzione setter definisco io altri filtri

## Idee:

per aggiornare la vista js non riceve raw data ma html gia renderizzato da flask (server notifica disponibilità, cli richiede aggiornamento, server fa un render template della parte richiesta e la manda a cli, cli rimpiazza html interno di div)

## Todo:

modificare sql creazione database per mettere piano aula come stringa
macro impostazioni di: numero, dropdown (scelta multipla), color
sezione in impostazioni per impostare lista aule, classi, docenti ecc hardcoded, unica cosa modulare è il blocco personalizzato 'docente' o 'classe' (con selezione per aula preferita e lista)
