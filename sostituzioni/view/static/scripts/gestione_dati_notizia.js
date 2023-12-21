const ui_gestione_dati_notizia = document.getElementById('gestione-dati-notizia');
const ui_pulsante_principale_notizia = document.getElementById('pulsante-principale-notizia');

const gestione_dati_notizia_data_inizio = document.getElementById('gestione-dati-notizia-data-inizio');
const gestione_dati_notizia_data_fine = document.getElementById('gestione-dati-notizia-data-fine');
const gestione_dati_notizia_testo = document.getElementById('gestione-dati-notizia-testo');



function mostra_gestione_notizia() {
    ui_gestione_dati.classList.remove('hidden')
    ui_gestione_dati_notizia.classList.remove('hidden')
}

function mostra_nuova_notizia() {
    mostra_gestione_notizia()

    ui_titolo_gestione_dati.innerHTML = 'Inserimento Nuova Notizia'
    ui_pulsante_principale_notizia.innerHTML = 'Pubblica'
    ui_pulsante_principale_notizia.onclick = () => conferma_nuova_notizia(true)
}

function conferma_nuova_notizia() {
    data_inizio = gestione_dati_evento_data_inizio.valueAsNumber / 1000;
    data_fine = gestione_dati_evento_data_fine.valueAsNumber / 1000;

    if (data_inizio > data_fine) {
        return
    }

    s_nuova_notizia({
        data_inizio: data_inizio,
        data_fine: data_fine,
        testo: gestione_dati_notizia_testo.value
    })

    nascondi_gestione_dati()
}


function mostra_modifica_notizia(id) {
    let notizia = notizie.find(element => element.id === id)

    gestione_dati_notizia_data_inizio.value = new Date(notizia.data_inizio * 1000).toISOString().slice(0, 16)
    gestione_dati_notizia_data_fine.value = new Date(notizia.data_fine * 1000).toISOString().slice(0, 16)
    gestione_dati_notizia_testo.value = notizia.testo

    mostra_gestione_notizia()
    ui_titolo_gestione_dati.innerHTML = 'Modifica Notizia'
    ui_pulsante_principale_notizia.innerHTML = 'Applica'
    ui_pulsante_principale_notizia.onclick = () => conferma_modifica_notizia(id)
}

function conferma_modifica_notizia(id) {
    s_modifica_notizia(
        id, {
        testo: gestione_dati_notizia_testo.value,
    })

    nascondi_gestione_dati()
}