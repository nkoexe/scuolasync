const ui_gestione_dati = document.getElementById('gestione-dati-container');

const ui_gestione_dati_evento = document.getElementById('gestione-dati-evento');
const ui_gestione_dati_notizia = document.getElementById('gestione-dati-notizia');

function nascondi_gestione_dati() {
    ui_gestione_dati.classList.add('hidden');
    ui_gestione_dati_sostituzione.classList.add('hidden');
    ui_gestione_dati_evento.classList.add('hidden');
    ui_gestione_dati_notizia.classList.add('hidden');
}
