const sostituzioni_list = document.getElementById('sostituzioni-lista');
sostituzioni_list.onselectstart = (event) => {
    // todo: nascondere i pulsanti per permettere di selezionare tutto il testo
}


const gestione_dati = document.getElementById('gestione-dati-container');
function mostra_gestione_dati() {
    gestione_dati.style.display = 'flex';
}

function nascondi_gestione_dati() {
    gestione_dati.style.display = 'none';
}