const ui_gestione_dati_sostituzione = document.getElementById('gestione-dati-sostituzione');
const ui_pulsante_secondario_sostituzione = document.getElementById('pulsante-applica-sostituzione');
const ui_pulsante_principale_sostituzione = document.getElementById('pulsante-pubblica-sostituzione');

const gestione_dati_sostituzione_data = document.getElementById('gestione-dati-sostituzione-data');
const gestione_dati_sostituzione_ora_inizio = document.getElementById('gestione-dati-sostituzione-ora-inizio');
const gestione_dati_sostituzione_ora_fine = document.getElementById('gestione-dati-sostituzione-ora-fine');


const gestione_dati_sostituzione_ora_predefinita = new Selezione({ id: 'gestione-dati-sostituzione-ora-predefinita', filtra_lista: prendi_ora })
const gestione_dati_sostituzione_docente = new Selezione({ id: 'gestione-dati-sostituzione-docente', filtra_lista: prendi_nome_cognome })
const gestione_dati_sostituzione_classe = new Selezione({ id: 'gestione-dati-sostituzione-classe', filtra_lista: prendi_nome })
const gestione_dati_sostituzione_aula = new Selezione({ id: 'gestione-dati-sostituzione-aula', filtra_lista: prendi_numero })
const gestione_dati_sostituzione_note = new Selezione({ id: 'gestione-dati-sostituzione-note' })



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

    ui_pulsante_secondario_sostituzione.innerHTML = 'Inserisci senza pubblicare'
    ui_pulsante_secondario_sostituzione.onclick = () => conferma_nuova_sostituzione(false)
    ui_pulsante_principale_sostituzione.innerHTML = 'Pubblica'
    ui_pulsante_principale_sostituzione.onclick = () => conferma_nuova_sostituzione(true)
}

function conferma_nuova_sostituzione(pubblicato) {
    s_nuova_sostituzione({
        pubblicato: pubblicato,
        data: gestione_dati_sostituzione_data.value,
        ora_predefinita: gestione_dati_sostituzione_ora_predefinita.valore,
        ora_inizio: gestione_dati_sostituzione_ora_inizio.value,
        ora_fine: gestione_dati_sostituzione_ora_fine.value,
        docente: gestione_dati_sostituzione_docente.valore,
        classe: gestione_dati_sostituzione_classe.valore,
        aula: gestione_dati_sostituzione_aula.valore,
        note: gestione_dati_sostituzione_note.valore
    })

    nascondi_gestione_dati()
}


function mostra_modifica_sostituzione(id) {
    let sostituzione = sostituzioni.find(element => element.id === id)

    gestione_dati_sostituzione_data.valueAsDate = new Date(sostituzione.data * 1000)
    gestione_dati_sostituzione_ora_predefinita.valore = sostituzione.numero_ora_predefinita
    gestione_dati_sostituzione_ora_inizio.value = sostituzione.ora_inizio
    gestione_dati_sostituzione_ora_fine.value = sostituzione.ora_fine
    gestione_dati_sostituzione_docente.valore = sostituzione.nome_docente + ' ' + sostituzione.cognome_docente
    gestione_dati_sostituzione_classe.valore = sostituzione.nome_classe
    gestione_dati_sostituzione_aula.valore = sostituzione.numero_aula
    gestione_dati_sostituzione_note.valore = sostituzione.note

    mostra_gestione_sostituzione()
    ui_pulsante_secondario_sostituzione.innerHTML = 'Annulla'
    ui_pulsante_secondario_sostituzione.onclick = () => nascondi_gestione_dati()
    ui_pulsante_principale_sostituzione.innerHTML = 'Applica'
    ui_pulsante_principale_sostituzione.onclick = () => conferma_modifica_sostituzione(id)
}

function conferma_modifica_sostituzione(id) {
    s_modifica_sostituzione(
        id, {
        data: gestione_dati_sostituzione_data.value,
        ora_predefinita: gestione_dati_sostituzione_ora_predefinita.valore,
        ora_inizio: gestione_dati_sostituzione_ora_inizio.value,
        ora_fine: gestione_dati_sostituzione_ora_fine.value,
        docente: gestione_dati_sostituzione_docente.valore,
        classe: gestione_dati_sostituzione_classe.valore,
        aula: gestione_dati_sostituzione_aula.valore,
        note: gestione_dati_sostituzione_note.valore
    })

    nascondi_gestione_dati()
}