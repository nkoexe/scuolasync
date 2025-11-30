const ui_gestione_dati_sostituzione = document.getElementById('gestione-dati-sostituzione');
const ui_pulsante_terziario_sostituzione = document.getElementById('pulsante-terziario-sostituzione');
const ui_pulsante_secondario_sostituzione = document.getElementById('pulsante-secondario-sostituzione');
const ui_pulsante_principale_sostituzione = document.getElementById('pulsante-primario-sostituzione');

const gestione_dati_sostituzione_data = document.getElementById('gestione-dati-sostituzione-data');
const gestione_dati_sostituzione_ora_inizio = document.getElementById('gestione-dati-sostituzione-ora-inizio');
const gestione_dati_sostituzione_ora_fine = document.getElementById('gestione-dati-sostituzione-ora-fine');


const gestione_dati_sostituzione_ora_predefinita = new Selezione({ query: '#gestione-dati-sostituzione-ora-predefinita', filtra_lista: prendi_ora, render: render_ora_predefinita, autocomplete: true });
const gestione_dati_sostituzione_docente = new Selezione({ query: '#gestione-dati-sostituzione-docente', filtra_lista: prendi_cognome_nome, autocomplete: true });
const gestione_dati_sostituzione_note = new Selezione({ query: '#gestione-dati-sostituzione-note', filtra_lista: prendi_testo });
const gestione_dati_sostituzione_aula = new Selezione({
    query: '#gestione-dati-sostituzione-aula',
    filtra_lista: prendi_numero,
    autocomplete: true,
    callback: (selected) => {
        if (!selected) {
            gestione_dati_sostituzione_aula.modificato_manualmente = false;
            return;
        }
        gestione_dati_sostituzione_aula.modificato_manualmente = true;
    }
});
gestione_dati_sostituzione_aula.modificato_manualmente = false;

const gestione_dati_sostituzione_classe = new Selezione({
    query: '#gestione-dati-sostituzione-classe',
    filtra_lista: prendi_nome,
    autocomplete: true,
    callback: (selected) => {
        if (gestione_dati_sostituzione_aula.modificato_manualmente) {
            return;
        }
        if (!selected) {
            gestione_dati_sostituzione_aula.valore = '';
            return;
        }

        const aule = classi.find(classe => classe.nome == selected).aule_ospitanti;
        if (aule.length > 0) {
            gestione_dati_sostituzione_aula.valore = aule[0];
            gestione_dati_sostituzione_aula.modificato_manualmente = false;
        }
    }
});



function mostra_gestione_sostituzione() {
    s_auth_check()

    gestione_dati_sostituzione_ora_predefinita.aggiorna(ore_predefinite);
    gestione_dati_sostituzione_note.aggiorna(note_standard)
    gestione_dati_sostituzione_docente.aggiorna(docenti);
    gestione_dati_sostituzione_classe.aggiorna(classi);
    gestione_dati_sostituzione_aula.aggiorna(aule);

    gestione_dati_sostituzione_aula.modificato_manualmente = false;;

    ui_gestione_dati.classList.remove('hidden');
    ui_gestione_dati_sostituzione.classList.remove('hidden');
}

function mostra_nuova_sostituzione() {
    mostra_gestione_sostituzione()

    gestione_dati_sostituzione_data.valueAsNumber = fix_date_to_input(new Date());
    gestione_dati_sostituzione_ora_predefinita.valore = '';
    gestione_dati_sostituzione_ora_inizio.value = '';
    gestione_dati_sostituzione_ora_fine.value = '';
    gestione_dati_sostituzione_docente.valore = '';
    gestione_dati_sostituzione_classe.valore = '';
    gestione_dati_sostituzione_aula.valore = '';
    gestione_dati_sostituzione_note.valore = '';

    ui_titolo_gestione_dati.innerHTML = 'Inserimento Nuova Sostituzione';
    ui_pulsante_terziario_sostituzione.classList.remove('hidden');
    ui_pulsante_terziario_sostituzione.innerHTML = 'Annulla';
    ui_pulsante_terziario_sostituzione.onclick = nascondi_gestione_dati;
    ui_pulsante_secondario_sostituzione.innerHTML = 'Inserisci senza pubblicare';
    ui_pulsante_secondario_sostituzione.onclick = () => conferma_nuova_sostituzione(false);
    ui_pulsante_principale_sostituzione.innerHTML = 'Pubblica';
    ui_pulsante_principale_sostituzione.onclick = () => conferma_nuova_sostituzione(true);
}

function conferma_nuova_sostituzione(pubblicato) {
    data = fix_date_from_input(gestione_dati_sostituzione_data.valueAsNumber) / 1000;

    s_nuova_sostituzione({
        pubblicato: pubblicato,
        data: data,
        ora_predefinita: gestione_dati_sostituzione_ora_predefinita.valore,
        ora_inizio: gestione_dati_sostituzione_ora_inizio.value,
        ora_fine: gestione_dati_sostituzione_ora_fine.value,
        docente: gestione_dati_sostituzione_docente.valore,
        nome_classe: gestione_dati_sostituzione_classe.valore,
        numero_aula: gestione_dati_sostituzione_aula.valore,
        note: gestione_dati_sostituzione_note.valore
    });

    nascondi_gestione_dati();
}


function mostra_modifica_sostituzione(id) {
    let sostituzione = sostituzioni.find(element => element.id === id)

    gestione_dati_sostituzione_data.valueAsNumber = fix_date_to_input(new Date(sostituzione.data * 1000));
    gestione_dati_sostituzione_ora_predefinita.valore = sostituzione.ora_predefinita;
    gestione_dati_sostituzione_ora_inizio.value = sostituzione.ora_inizio;
    gestione_dati_sostituzione_ora_fine.value = sostituzione.ora_fine;
    gestione_dati_sostituzione_classe.valore = sostituzione.nome_classe;
    gestione_dati_sostituzione_aula.valore = sostituzione.numero_aula;
    gestione_dati_sostituzione_note.valore = sostituzione.note;
    if (sostituzione.cognome_docente) {
        gestione_dati_sostituzione_docente.valore = sostituzione.cognome_docente + ' ' + sostituzione.nome_docente;
    } else {
        gestione_dati_sostituzione_docente.valore = ''
    }

    mostra_gestione_sostituzione();
    ui_titolo_gestione_dati.innerHTML = 'Modifica Sostituzione';
    ui_pulsante_terziario_sostituzione.classList.add('hidden');
    ui_pulsante_secondario_sostituzione.innerHTML = 'Annulla';
    ui_pulsante_secondario_sostituzione.onclick = () => nascondi_gestione_dati();
    ui_pulsante_principale_sostituzione.innerHTML = 'Applica';
    ui_pulsante_principale_sostituzione.onclick = () => conferma_modifica_sostituzione(id);
}

function conferma_modifica_sostituzione(id) {
    let data = fix_date_from_input(gestione_dati_sostituzione_data.valueAsNumber) / 1000;

    let dati = {
        data: data,
        ora_predefinita: gestione_dati_sostituzione_ora_predefinita.valore,
        ora_inizio: gestione_dati_sostituzione_ora_inizio.value,
        ora_fine: gestione_dati_sostituzione_ora_fine.value,
        docente: gestione_dati_sostituzione_docente.valore,
        nome_classe: gestione_dati_sostituzione_classe.valore,
        numero_aula: gestione_dati_sostituzione_aula.valore,
        note: gestione_dati_sostituzione_note.valore
    }

    s_modifica_sostituzione(id, dati);

    nascondi_gestione_dati();
}

function mostra_duplica_sostituzione(id) {
    let sostituzione = sostituzioni.find(element => element.id === id);

    gestione_dati_sostituzione_data.valueAsNumber = fix_date_to_input(new Date(sostituzione.data * 1000));
    gestione_dati_sostituzione_ora_predefinita.valore = sostituzione.ora_predefinita;
    gestione_dati_sostituzione_ora_inizio.value = sostituzione.ora_inizio;
    gestione_dati_sostituzione_ora_fine.value = sostituzione.ora_fine;
    gestione_dati_sostituzione_classe.valore = sostituzione.nome_classe;
    gestione_dati_sostituzione_aula.valore = sostituzione.numero_aula;
    gestione_dati_sostituzione_note.valore = sostituzione.note;
    if (sostituzione.cognome_docente) {
        gestione_dati_sostituzione_docente.valore = sostituzione.cognome_docente + ' ' + sostituzione.nome_docente;
    } else {
        gestione_dati_sostituzione_docente.valore = ''
    }

    mostra_gestione_sostituzione();
    ui_titolo_gestione_dati.innerHTML = 'Modifica Sostituzione Duplicata';
    ui_pulsante_terziario_sostituzione.classList.remove('hidden');
    ui_pulsante_terziario_sostituzione.innerHTML = 'Annulla';
    ui_pulsante_terziario_sostituzione.onclick = nascondi_gestione_dati;
    ui_pulsante_secondario_sostituzione.innerHTML = 'Inserisci senza pubblicare';
    ui_pulsante_secondario_sostituzione.onclick = () => conferma_nuova_sostituzione(false);
    ui_pulsante_principale_sostituzione.innerHTML = 'Pubblica';
    ui_pulsante_principale_sostituzione.onclick = () => conferma_nuova_sostituzione(true);
}

function pubblica_sostituzione(id, pubblica = true) {
    s_modifica_sostituzione(id, { pubblicato: pubblica });
}
