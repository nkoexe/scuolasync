const ui_gestione_dati_evento = document.getElementById('gestione-dati-evento');
const ui_pulsante_principale_evento = document.getElementById('pulsante-principale-evento');

const gestione_dati_evento_testo = document.getElementById('gestione-dati-evento-testo');



function mostra_gestione_evento() {
    ui_gestione_dati.classList.remove('hidden')
    ui_gestione_dati_evento.classList.remove('hidden')
}

function mostra_nuovo_evento() {
    mostra_gestione_evento()

    ui_titolo_gestione_dati.innerHTML = 'Inserimento Nuovo Evento'
    ui_pulsante_principale_evento.innerHTML = 'Pubblica'
    ui_pulsante_principale_evento.onclick = () => conferma_nuovo_evento(true)
}

function conferma_nuovo_evento() {
    s_nuovo_evento({
        testo: gestione_dati_evento_testo.value
    })

    nascondi_gestione_dati()
}


function mostra_modifica_evento(id) {
    let evento = eventi.find(element => element.id === id)

    gestione_dati_evento_testo.value = evento.value

    mostra_gestione_evento()
    ui_titolo_gestione_dati.innerHTML = 'Modifica Evento'
    ui_pulsante_principale_evento.innerHTML = 'Applica'
    ui_pulsante_principale_evento.onclick = () => conferma_modifica_evento(id)
}

function conferma_modifica_evento(id) {
    s_modifica_evento(
        id, {
        testo: gestione_dati_evento_testo.value,
    })

    nascondi_gestione_dati()
}