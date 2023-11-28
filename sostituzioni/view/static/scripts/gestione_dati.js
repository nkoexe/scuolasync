const ui_gestione_dati = document.getElementById('gestione-dati-container');
const ui_gestione_dati_sostituzione = document.getElementById('gestione-dati-sostituzione');
const ui_gestione_dati_evento = document.getElementById('gestione-dati-evento');
const ui_gestione_dati_notizia = document.getElementById('gestione-dati-notizia');
const ui_pulsante_applica_gestione_dati = document.getElementById('pulsante-applica-gestione-dati');

const ui_gestione_dati_sostituzione_data = document.getElementById('gestione-dati-sostituzione-data');
const ui_gestione_dati_sostituzione_ora = document.getElementById('gestione-dati-sostituzione-ora');
const ui_gestione_dati_sostituzione_docente = document.getElementById('gestione-dati-sostituzione-docente');
const ui_gestione_dati_sostituzione_classe = document.getElementById('gestione-dati-sostituzione-classe');
const ui_gestione_dati_sostituzione_aula = document.getElementById('gestione-dati-sostituzione-aula');
const ui_gestione_dati_sostituzione_note = document.getElementById('gestione-dati-sostituzione-note');


function nascondi_gestione_dati() {
    ui_gestione_dati.classList.add('hidden');
    ui_gestione_dati_sostituzione.classList.add('hidden');
    ui_gestione_dati_evento.classList.add('hidden');
    ui_gestione_dati_notizia.classList.add('hidden');
    ui_pulsante_applica_gestione_dati.onclick = null;
}

function mostra_gestione_sostituzione() {
    ui_gestione_dati.classList.remove('hidden');
    ui_gestione_dati_sostituzione.classList.remove('hidden');
}

function mostra_modifica_sostituzione(id) {
    let sostituzione = sostituzioni.find(element => element.id === id)

    console.log(sostituzione)

    ui_gestione_dati_sostituzione_data.value = sostituzione.data
    ui_gestione_dati_sostituzione_ora.value = sostituzione.ora_predefinita
    ui_gestione_dati_sostituzione_docente.value = sostituzione.nome_docente
    ui_gestione_dati_sostituzione_classe.value = classi.findIndex(element => element.nome === sostituzione.nome_classe)
    ui_gestione_dati_sostituzione_aula.value = aule.findIndex(element => element.numero === sostituzione.numero_aula)
    // ui_gestione_dati_sostituzione_note.value = sostituzione.note

    mostra_gestione_sostituzione()
    ui_pulsante_applica_gestione_dati.onclick = () => console.log('modifica')
}