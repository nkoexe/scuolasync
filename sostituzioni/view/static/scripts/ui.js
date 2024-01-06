const pulsante_logout = document.getElementById('pulsante-logout')

const ui_context_menu = document.getElementById("context-menu")
const ui_pulsanti_context_menu = document.getElementById("pulsanti-context-menu")
const ui_conferma_elimina = document.getElementById("dialog-conferma-elimina")
const ui_conferma_elimina_titolo = document.getElementById("dialog-conferma-elimina-titolo")
const ui_conferma_elimina_storico_container = document.getElementById("dialog-conferma-elimina-storico-container")
const ui_conferma_elimina_storico = document.getElementById("dialog-conferma-elimina-storico")
const ui_conferma_elimina_per_reale = document.getElementById("dialog-conferma-elimina-per-reale")


// ----------------------------------


function fix_date_to_input(date) {
    return date.getTime() - date.getTimezoneOffset() * 60 * 1000
}

function fix_date_from_input(value) {
    return value + new Date().getTimezoneOffset() * 60 * 1000
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

    filtri = sostituzioni_filtra_data()
    s_richiedi_sostituzioni(filtri)
}

// logout animation
pulsante_logout.onclick = (e) => {
    let fun = document.getElementById('fun')
    fun.style.top = "-70vh"
    fun.style.right = "-70vw"
    fun.style.height = "200vh"
    fun.style.width = "200vw"

    e.preventDefault()

    setTimeout(() => { location.href = pulsante_logout.href }, 210)
}


// ----------------------------------


ui_context_menu.onblur = (event) => {
    // if the event target is inside the context menu, do nothing
    if (event.relatedTarget && event.relatedTarget.closest("#context-menu")) {
        ui_context_menu.focus()
        return
    }
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
    s_elimina_sostituzione(id, false)
    ui_context_menu.closingcallback()
}
function ui_modifica_evento() {
    id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_evento(id)
    ui_context_menu.closingcallback()
}
function ui_duplica_evento() {
    id = parseInt(ui_context_menu.dataset.id)
    console.log("Duplica evento: " + id)
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


for (const element of document.getElementsByClassName("tooltip")) {
    let rect = element.getBoundingClientRect();

    if (rect.right > window.innerWidth) {
        // move the tooltip to the left but leave the after element in its place
        element.style.translate = "-" + (rect.width / 2 + (rect.right - window.innerWidth)) + "px" + " 0";
    }
}