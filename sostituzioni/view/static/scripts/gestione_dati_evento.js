const ui_gestione_dati_evento = document.getElementById("gestione-dati-evento");
const ui_pulsante_principale_evento = document.getElementById("pulsante-principale-evento");

const gestione_dati_evento_data_inizio = document.getElementById("gestione-dati-evento-data-inizio");
const gestione_dati_evento_data_fine = document.getElementById("gestione-dati-evento-data-fine");
const gestione_dati_evento_testo = document.getElementById("gestione-dati-evento-testo");
const gestione_dati_evento_urgente = document.getElementById("gestione-dati-evento-urgente");


function mostra_gestione_evento() {
    s_auth_check()

    ui_gestione_dati.open();
    ui_gestione_dati_evento.classList.remove("hidden");
}

function mostra_nuovo_evento() {
    mostra_gestione_evento();

    today = new Date();
    today.setHours(0, 0, 0, 0);
    today = fix_date_to_input(today);

    gestione_dati_evento_data_inizio.valueAsNumber = today;
    gestione_dati_evento_data_fine.valueAsNumber = today;
    gestione_dati_evento_testo.value = "";
    gestione_dati_evento_urgente.checked = false;

    ui_titolo_gestione_dati.innerHTML = "Inserimento Nuovo Evento";
    ui_pulsante_principale_evento.innerHTML = "Pubblica";
    ui_pulsante_principale_evento.onclick = conferma_nuovo_evento;
}

function conferma_nuovo_evento() {
    data_ora_inizio = fix_date_from_input(gestione_dati_evento_data_inizio.valueAsNumber) / 1000;
    data_ora_fine = fix_date_from_input(gestione_dati_evento_data_fine.valueAsNumber) / 1000;

    testo = gestione_dati_evento_testo.value;
    testo = testo.trim();
    testo = testo.replace(/\n/g, '<br>');


    if (testo.length == 0) {
        notyf.error("Inserire un testo");
        return;
    };
    if (data_ora_inizio >= data_ora_fine) {
        notyf.error("Date non valide");
        return;
    };

    s_nuovo_evento({
        data_ora_inizio: data_ora_inizio,
        data_ora_fine: data_ora_fine,
        testo: testo,
        urgente: gestione_dati_evento_urgente.checked
    });

    nascondi_gestione_dati();
}


function mostra_modifica_evento(id) {
    let evento = eventi.find(element => element.id === id);

    gestione_dati_evento_data_inizio.valueAsNumber = fix_date_to_input(new Date(evento.data_ora_inizio * 1000));
    gestione_dati_evento_data_fine.valueAsNumber = fix_date_to_input(new Date(evento.data_ora_fine * 1000));
    gestione_dati_evento_testo.value = evento.testo;
    gestione_dati_evento_urgente.checked = evento.urgente;

    mostra_gestione_evento()
    ui_titolo_gestione_dati.innerHTML = "Modifica Evento";
    ui_pulsante_principale_evento.innerHTML = "Applica";
    ui_pulsante_principale_evento.onclick = () => conferma_modifica_evento(id);
}

function conferma_modifica_evento(id) {
    data_ora_inizio = fix_date_from_input(gestione_dati_evento_data_inizio.valueAsNumber) / 1000;
    data_ora_fine = fix_date_from_input(gestione_dati_evento_data_fine.valueAsNumber) / 1000;

    testo = gestione_dati_evento_testo.value;
    testo = testo.trim();
    testo = testo.replace(/\n/g, '<br>');

    if (testo.length == 0) {
        notyf.error("Inserire un testo");
        return;
    };

    if (data_ora_inizio >= data_ora_fine) {
        return
    };

    s_modifica_evento(
        id, {
        data_ora_inizio: data_ora_inizio,
        data_ora_fine: data_ora_fine,
        testo: testo,
        urgente: gestione_dati_evento_urgente.checked
    });

    nascondi_gestione_dati();
}


function mostra_duplica_evento(id) {
    let evento = eventi.find(element => element.id === id);

    gestione_dati_evento_data_inizio.valueAsNumber = fix_date_to_input(new Date(evento.data_ora_inizio * 1000));
    gestione_dati_evento_data_fine.valueAsNumber = fix_date_to_input(new Date(evento.data_ora_fine * 1000));
    gestione_dati_evento_testo.value = evento.testo;
    gestione_dati_evento_urgente.checked = evento.urgente;

    mostra_gestione_evento()
    ui_titolo_gestione_dati.innerHTML = "Modifica Evento Duplicato";
    ui_pulsante_principale_evento.innerHTML = "Pubblica";
    ui_pulsante_principale_evento.onclick = conferma_nuovo_evento;
}