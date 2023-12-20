const ui_gestione_dati_evento = document.getElementById("gestione-dati-evento");
const ui_pulsante_principale_evento = document.getElementById("pulsante-principale-evento");

const gestione_dati_evento_data_inizio = document.getElementById("gestione-dati-evento-data-inizio")
const gestione_dati_evento_data_fine = document.getElementById("gestione-dati-evento-data-fine")
const gestione_dati_evento_testo = document.getElementById("gestione-dati-evento-testo");



function mostra_gestione_evento() {
    ui_gestione_dati.classList.remove("hidden")
    ui_gestione_dati_evento.classList.remove("hidden")
}

function mostra_nuovo_evento() {
    mostra_gestione_evento()

    // today = new Date()
    // today.setHours(0, 0, 0, 0)
    // today.setMinutes(today.getMinutes() - today.getTimezoneOffset());

    // gestione_dati_evento_data_inizio.value = today.toISOString().slice(0, 16);
    // gestione_dati_evento_data_fine.value = today.toISOString().slice(0, 16);
    // gestione_dati_evento_testo.value = ""

    ui_titolo_gestione_dati.innerHTML = "Inserimento Nuovo Evento"
    ui_pulsante_principale_evento.innerHTML = "Pubblica"
    ui_pulsante_principale_evento.onclick = () => conferma_nuovo_evento(true)
}

function conferma_nuovo_evento() {
    // adjust for timezone
    // data_ora_inizio = new Date(gestione_dati_evento_data_inizio.value)
    // data_ora_inizio.setMinutes(data_ora_inizio.getMinutes() - data_ora_inizio.getTimezoneOffset());
    // data_ora_inizio = data_ora_inizio.getTime() / 1000;

    // data_ora_fine = new Date(gestione_dati_evento_data_fine.value)
    // data_ora_fine.setMinutes(data_ora_fine.getMinutes() - data_ora_fine.getTimezoneOffset());
    // data_ora_fine = data_ora_fine.getTime() / 1000;

    data_ora_inizio = gestione_dati_evento_data_inizio.valueAsNumber / 1000;
    data_ora_fine = gestione_dati_evento_data_fine.valueAsNumber / 1000;

    if (data_ora_inizio > data_ora_fine) {
        return
    }

    s_nuovo_evento({
        data_ora_inizio: data_ora_inizio,
        data_ora_fine: data_ora_fine,
        testo: gestione_dati_evento_testo.value
    })

    nascondi_gestione_dati()
}


function mostra_modifica_evento(id) {
    let evento = eventi.find(element => element.id === id)

    gestione_dati_evento_testo.value = evento.value

    mostra_gestione_evento()
    ui_titolo_gestione_dati.innerHTML = "Modifica Evento"
    ui_pulsante_principale_evento.innerHTML = "Applica"
    ui_pulsante_principale_evento.onclick = () => conferma_modifica_evento(id)
}

function conferma_modifica_evento(id) {
    s_modifica_evento(
        id, {
        testo: gestione_dati_evento_testo.value,
    })

    nascondi_gestione_dati()
}