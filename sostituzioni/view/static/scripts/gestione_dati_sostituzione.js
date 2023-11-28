const ui_gestione_dati_sostituzione = document.getElementById('gestione-dati-sostituzione');

const ui_gestione_dati_sostituzione_data = document.getElementById('gestione-dati-sostituzione-data');
const ui_gestione_dati_sostituzione_ora_predefinita = document.getElementById('gestione-dati-sostituzione-ora-predefinita');
const ui_gestione_dati_sostituzione_ora_inizio = document.getElementById('gestione-dati-sostituzione-ora-inizio');
const ui_gestione_dati_sostituzione_ora_fine = document.getElementById('gestione-dati-sostituzione-ora-fine');
const ui_gestione_dati_sostituzione_docente = document.getElementById('gestione-dati-sostituzione-docente');
const ui_gestione_dati_sostituzione_classe = document.getElementById('gestione-dati-sostituzione-classe');
const ui_gestione_dati_sostituzione_aula = document.getElementById('gestione-dati-sostituzione-aula');
const ui_gestione_dati_sostituzione_note = document.getElementById('gestione-dati-sostituzione-note');
const ui_gestione_dati_sostituzione_pubblicato = document.getElementById('gestione-dati-sostituzione-pubblicato');


function mostra_gestione_sostituzione() {
    ui_gestione_dati.classList.remove('hidden');
    ui_gestione_dati_sostituzione.classList.remove('hidden');
}

function mostra_nuova_sostituzione() {
    mostra_gestione_sostituzione()
    ui_pulsante_applica_gestione_dati.onclick = conferma_nuova_sostituzione
}

function conferma_nuova_sostituzione() {
    carica_nuova_sostituzione(
        ui_gestione_dati_sostituzione_pubblicato.value,
        ui_gestione_dati_sostituzione_data.value,
        ui_gestione_dati_sostituzione_ora_predefinita.value,
        ui_gestione_dati_sostituzione_ora_inizio.value,
        ui_gestione_dati_sostituzione_ora_fine.value,
        ui_gestione_dati_sostituzione_docente.value,
        ui_gestione_dati_sostituzione_classe.value,
        ui_gestione_dati_sostituzione_aula.value,
        ui_gestione_dati_sostituzione_note.value
    )
}



function mostra_modifica_sostituzione(id) {
    let sostituzione = sostituzioni.find(element => element.id === id)

    ui_gestione_dati_sostituzione_data.value = sostituzione.data
    ui_gestione_dati_sostituzione_ora.value = sostituzione.ora_predefinita
    ui_gestione_dati_sostituzione_docente.value = sostituzione.nome_docente
    ui_gestione_dati_sostituzione_classe.value = classi.findIndex(element => element.nome === sostituzione.nome_classe)
    ui_gestione_dati_sostituzione_aula.value = aule.findIndex(element => element.numero === sostituzione.numero_aula)
    ui_gestione_dati_sostituzione_note.value = sostituzione.note

    mostra_gestione_sostituzione()
    ui_pulsante_applica_gestione_dati.onclick = () => console.log('modifica')
}