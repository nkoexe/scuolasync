// const ui_pulsante_help = document.querySelector('#pulsante-help')
let installPrompt = null;
const ui_pulsante_installa = document.querySelector('#pulsante-installa')
// const ui_help_container = document.querySelector('#help-container')

const ui_pulsante_refresh_sostituzioni = document.querySelector('#pulsante-refresh-sostituzioni')

const ui_context_menu = document.querySelector("#context-menu")
const ui_pulsanti_context_menu = document.querySelector("#pulsanti-context-menu")
const ui_conferma_elimina = document.querySelector("#dialog-conferma-elimina")
const ui_conferma_elimina_titolo = document.querySelector("#dialog-conferma-elimina-titolo")
const ui_conferma_elimina_storico_container = document.querySelector("#dialog-conferma-elimina-storico-container")
const ui_conferma_elimina_storico = document.querySelector("#dialog-conferma-elimina-storico")
const ui_conferma_elimina_per_reale = document.querySelector("#dialog-conferma-elimina-per-reale")

// set theme color
document.head.querySelector("meta[name=theme-color]").content = getComputedStyle(document.body).getPropertyValue('--color-accent')


// ----------------------------------


const userLocale =
    navigator.languages && navigator.languages.length
        ? navigator.languages[0]
        : navigator.language;


// ----------------------------------


function fix_date_to_input(date) {
    return date.getTime() - date.getTimezoneOffset() * 60 * 1000
}

function fix_date_from_input(value) {
    return value + new Date(value).getTimezoneOffset() * 60 * 1000
}


// ----------------------------------


function ui_loading_sostituzioni() {
    ui_sostituzioni_lista.innerHTML = ""
    ui_sostituzioni_messaggio_informativo.innerHTML = "<span>Caricamento...</span>"
    ui_sostituzioni_messaggio_informativo.style.display = "flex"
}

// pulsante refresh richiesto dall'utente
function ui_refresh_sostituzioni() {
    ui_loading_sostituzioni()

    ui_pulsante_refresh_sostituzioni.style.animation = 'none';
    ui_pulsante_refresh_sostituzioni.offsetHeight; /* trigger reflow and restart animation */
    ui_pulsante_refresh_sostituzioni.style.animation = null;

    filtri = sostituzioni_filtra_data()
    // temporaneo, rimuovere quanod si crea il filtro 'pubblicato'
    filtri.non_pubblicato = true
    s_richiedi_sostituzioni(filtri)
}

// ui_pulsante_help.onclick = () => {
//     ui_help_container.classList.remove("hidden")
// }


// ----------------------------------


ui_context_menu.onblur = (event) => {
    // if the event target is inside the context menu, do nothing
    if (event.relatedTarget && event.relatedTarget.closest("#context-menu")) {
        ui_context_menu.focus()
        return
    }
    ui_context_menu.closingcallback()
}
function ui_nascondi_sostituzione() {
    id = parseInt(ui_context_menu.dataset.id)
    pubblica_sostituzione(id, false)
    ui_context_menu.closingcallback()
}
function ui_pubblica_sostituzione() {
    id = parseInt(ui_context_menu.dataset.id)
    pubblica_sostituzione(id, true)
    ui_context_menu.closingcallback()
}
function ui_modifica_sostituzione() {
    id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_sostituzione(id)
    ui_context_menu.closingcallback()
}
function ui_duplica_sostituzione() {
    id = parseInt(ui_context_menu.dataset.id)
    mostra_duplica_sostituzione(id)
    ui_context_menu.closingcallback()
}
function ui_conferma_elimina_sostituzione() {
    id = parseInt(ui_context_menu.dataset.id)
    s_elimina_sostituzione(id, !(ui_conferma_elimina_storico.checked))
    ui_context_menu.closingcallback()
}
function ui_informa_docente() {
    const id = parseInt(ui_context_menu.dataset.id)
    const sostituzione = sostituzioni.find(x => x.id == id)
    const docente = sostituzione.nome_docente + " " + sostituzione.cognome_docente
    const classe = sostituzione.nome_classe
    const aula = sostituzione.numero_aula
    const data = new Date(sostituzione.data * 1000).toLocaleDateString()
    const ora = sostituzione.ora_predefinita ? render_ora_predefinita(sostituzione.ora_predefinita) : sostituzione.ora_inizio + "-" + sostituzione.ora_fine
    const oggetto = oggetto_mail_informa_docente.replaceAll("{docente}", docente).replaceAll("{classe}", classe).replaceAll("{aula}", aula).replaceAll("{data}", data).replaceAll("{ora}", ora)
    const corpo = corpo_mail_informa_docente.replaceAll("{docente}", docente).replaceAll("{classe}", classe).replaceAll("{aula}", aula).replaceAll("{data}", data).replaceAll("{ora}", ora)
    const url = "mailto:?to=&subject=" + oggetto + "&body=" + corpo
    window.open(url, '_blank').focus();
}
function ui_modifica_evento() {
    id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_evento(id)
    ui_context_menu.closingcallback()
}
function ui_duplica_evento() {
    id = parseInt(ui_context_menu.dataset.id)
    mostra_duplica_evento(id)
    ui_context_menu.closingcallback()
}
function ui_conferma_elimina_evento() {
    id = parseInt(ui_context_menu.dataset.id)
    s_elimina_evento(id)
    ui_context_menu.closingcallback()
}
function ui_modifica_notizia() {
    id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_notizia(id)
    ui_context_menu.closingcallback()
}
function ui_conferma_elimina_notizia() {
    id = parseInt(ui_context_menu.dataset.id)
    s_elimina_notizia(id)
    ui_context_menu.closingcallback()
}
function ui_elimina() {
    ui_pulsanti_context_menu.classList.add("hidden")
    ui_conferma_elimina.classList.remove("hidden")
    // check if context menu is outside window, move it in case
    const rect = ui_conferma_elimina.getBoundingClientRect()
    if (rect.right > window.innerWidth) {
        ui_context_menu.style.left = window.innerWidth - rect.width + "px"
    }
    if (rect.bottom > window.innerHeight) {
        ui_context_menu.style.top = window.innerHeight - rect.height + "px"
    }
}
function ui_annulla_elimina() {
    ui_context_menu.closingcallback()
}

// -----------
// CONTEXT MENU

function pulsante(funzione, icona, testo) {
    return `<button onclick="${funzione}()" class="pulsante-context-menu" tabindex="0"><span class="material-symbols-rounded">${icona}</span><span>${testo}</span></button>`
}

function mostra_context_menu_sostituzione(event, sostituzione) {
    event.preventDefault()

    ui_conferma_elimina_titolo.innerHTML = "Eliminare Sostituzione?"
    ui_conferma_elimina_storico_container.classList.remove("hidden")
    ui_conferma_elimina_per_reale.onclick = ui_conferma_elimina_sostituzione

    ui_pulsanti_context_menu.innerHTML =
        pulsante("ui_modifica_sostituzione", "edit", "Modifica")
        + pulsante("ui_duplica_sostituzione", "content_copy", "Duplica")
        + (sostituzione.classList.contains("non-pubblicato") ? pulsante("ui_pubblica_sostituzione", "visibility", "Pubblica") : pulsante("ui_nascondi_sostituzione", "visibility_off", "Nascondi"))
        + (mostra_link_informa_docente ? pulsante("ui_informa_docente", "email", "Avvisa Docente") : "")
        + pulsante("ui_elimina", "delete", "Elimina")

    mostra_context_menu(sostituzione)
}

function mostra_context_menu_evento(event, evento) {
    event.preventDefault()

    ui_conferma_elimina_titolo.innerHTML = "Eliminare Evento?"
    ui_conferma_elimina_storico_container.classList.add("hidden")
    ui_conferma_elimina_per_reale.onclick = ui_conferma_elimina_evento

    ui_pulsanti_context_menu.innerHTML =
        pulsante("ui_modifica_evento", "edit", "Modifica")
        + pulsante("ui_duplica_evento", "content_copy", "Duplica")
        + pulsante("ui_elimina", "delete", "Elimina")

    mostra_context_menu(evento)
}

function mostra_context_menu_notizia(event, notizia) {
    event.preventDefault()

    ui_conferma_elimina_titolo.innerHTML = "Eliminare Notizia?"
    ui_conferma_elimina_storico_container.classList.add("hidden")
    ui_conferma_elimina_per_reale.onclick = ui_conferma_elimina_notizia

    ui_pulsanti_context_menu.innerHTML =
        pulsante("ui_modifica_notizia", "edit", "Modifica")
        + pulsante("ui_elimina", "delete", "Elimina")

    mostra_context_menu(notizia)
}

function mostra_context_menu(elemento) {
    elemento.focus()

    let id = elemento.dataset.id

    elemento.classList.add("context-menu-active")

    ui_context_menu.dataset.id = id
    ui_context_menu.classList.remove("hidden");

    if (event.clientX + ui_context_menu.offsetWidth > window.innerWidth) {
        ui_context_menu.style.left = (window.innerWidth - ui_context_menu.offsetWidth) + "px";
    } else if (event.clientX < 0) {
        ui_context_menu.style.left = "0px";
    } else {
        ui_context_menu.style.left = event.clientX + "px";
    }
    if (event.clientY + ui_context_menu.offsetHeight > window.innerHeight) {
        ui_context_menu.style.top = (window.innerHeight - ui_context_menu.offsetHeight) + "px";
    } else if (event.clientY < 0) {
        ui_context_menu.style.top = "0px";
    } else {
        ui_context_menu.style.top = event.clientY + "px";
    }

    ui_context_menu.focus()
    ui_context_menu.closingcallback = () => {
        ui_context_menu.classList.add("hidden")
        ui_pulsanti_context_menu.classList.remove("hidden")
        ui_conferma_elimina.classList.add("hidden")
        elemento.classList.remove("context-menu-active")
    }
}


// PWA

navigator.serviceWorker && navigator.serviceWorker.register("service-worker.js")
    .then((registration) => {
    })
    .catch((err) => {
    });


window.onbeforeinstallprompt = function (e) {
    installPrompt = e;
    e.preventDefault()
    ui_pulsante_installa.classList.remove("hidden");
    if (navigator.userAgent.match(/Android/i) || navigator.userAgent.match(/webOS/i) || navigator.userAgent.match(/iPhone/i) || navigator.userAgent.match(/iPad/i) || navigator.userAgent.match(/iPod/i) || navigator.userAgent.match(/BlackBerry/i) || navigator.userAgent.match(/Windows Phone/i)) {
        ui_pulsante_installa.querySelector("span").innerHTML = "install_mobile";
    } else {
        ui_pulsante_installa.querySelector("span").innerHTML = "install_desktop";
    }
}

ui_pulsante_installa.onclick = (e) => {
    if (!installPrompt) {
        return;
    }

    installPrompt.prompt();
    installPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
            location.reload();
        }
    });
    installPrompt = null;
}