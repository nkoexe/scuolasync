const ui_gestione_dati_sostituzione = document.getElementById('gestione-dati-sostituzione');

const gestione_dati_sostituzione_data = document.getElementById('gestione-dati-sostituzione-data');
const gestione_dati_sostituzione_ora_inizio = document.getElementById('gestione-dati-sostituzione-ora-inizio');
const gestione_dati_sostituzione_ora_fine = document.getElementById('gestione-dati-sostituzione-ora-fine');
const gestione_dati_sostituzione_pubblicato = document.getElementById('gestione-dati-sostituzione-pubblicato');


const gestione_dati_sostituzione_ora_predefinita = new Selezione({ id: 'gestione-dati-sostituzione-ora-predefinita' })
const gestione_dati_sostituzione_docente = new Selezione({ id: 'gestione-dati-sostituzione-docente' })
const gestione_dati_sostituzione_classe = new Selezione({ id: 'gestione-dati-sostituzione-classe' })
const gestione_dati_sostituzione_aula = new Selezione({ id: 'gestione-dati-sostituzione-aula' })
const gestione_dati_sostituzione_note = new Selezione({ id: 'gestione-dati-sostituzione-note' })

gestione_dati_sostituzione_ora_predefinita.filtra_lista = prendi_ora
gestione_dati_sostituzione_docente.filtra_lista = prendi_nome_cognome
gestione_dati_sostituzione_classe.filtra_lista = prendi_nome
gestione_dati_sostituzione_aula.filtra_lista = prendi_numero


function mostra_gestione_sostituzione() {
    gestione_dati_sostituzione_ora_predefinita.aggiorna(ore_predefinite)
    gestione_dati_sostituzione_docente.aggiorna(docenti)
    gestione_dati_sostituzione_classe.aggiorna(classi)
    gestione_dati_sostituzione_aula.aggiorna(aule)

    ui_gestione_dati.classList.remove('hidden')
    ui_gestione_dati_sostituzione.classList.remove('hidden')
}

function mostra_nuova_sostituzione() {
    mostra_gestione_sostituzione()

    gestione_dati_sostituzione_data.valueAsDate = new Date();

    ui_pulsante_applica_gestione_dati.onclick = conferma_nuova_sostituzione
}

function conferma_nuova_sostituzione() {
    carica_nuova_sostituzione(
        gestione_dati_sostituzione_pubblicato.checked,
        gestione_dati_sostituzione_data.value,
        gestione_dati_sostituzione_ora_predefinita.valore,
        gestione_dati_sostituzione_ora_inizio.value,
        gestione_dati_sostituzione_ora_fine.value,
        gestione_dati_sostituzione_docente.valore,
        gestione_dati_sostituzione_classe.valore,
        gestione_dati_sostituzione_aula.valore,
        gestione_dati_sostituzione_note.valore
    )
}



function mostra_modifica_sostituzione(id) {
    let sostituzione = sostituzioni.find(element => element.id === id)

    gestione_dati_sostituzione_data.valueAsDate = new Date(sostituzione.data)
    gestione_dati_sostituzione_ora_predefinita.valore = sostituzione.numero_ora_predefinita
    gestione_dati_sostituzione_ora_inizio.value = sostituzione.ora_inizio
    gestione_dati_sostituzione_ora_fine.value = sostituzione.ora_fine
    gestione_dati_sostituzione_docente.valore = sostituzione.nome_docente + ' ' + sostituzione.cognome_docente
    gestione_dati_sostituzione_classe.valore = sostituzione.nome_classe
    gestione_dati_sostituzione_aula.valore = sostituzione.numero_aula
    gestione_dati_sostituzione_note.valore = sostituzione.note

    mostra_gestione_sostituzione()
    ui_pulsante_applica_gestione_dati.onclick = () => console.log('modifica')
}