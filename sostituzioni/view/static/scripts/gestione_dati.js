const ui_gestione_dati = new Popup({ query: "#gestione-dati-container" });
const ui_titolo_gestione_dati = document.querySelector('#gestione-dati-titolo');


ui_gestione_dati.addEventListener("close", () => {
    ui_gestione_dati_sostituzione.classList.add('hidden');
    ui_gestione_dati_evento.classList.add('hidden');
    ui_gestione_dati_notizia.classList.add('hidden');
});

function nascondi_gestione_dati() {
    ui_gestione_dati.close();
}
