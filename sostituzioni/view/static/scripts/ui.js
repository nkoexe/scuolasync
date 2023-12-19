const pulsante_logout = document.getElementById('pulsante-logout')


function ui_loading_sostituzioni() {
    ui_sostituzioni_container.innerHTML = ""
    ui_sostituzioni_messaggio_informativo.innerHTML = "<span>Caricamento...</span>"
    ui_sostituzioni_messaggio_informativo.style.display = "flex"
}

// pulsante refresh richiesto dall'utente
function ui_refresh_sostituzioni() {
    ui_loading_sostituzioni()

    s_richiedi_sostituzioni()
}

// logout animation
pulsante_logout.onclick = (e) => {
    let fun = document.getElementById('fun')
    fun.style.top = "-70vh"
    fun.style.right = "-70vw"
    fun.style.height = "200vh"
    fun.style.width = "200vw"

    e.preventDefault()

    setTimeout(() => { location.href = pulsante_logout.href }, 170)
}

const ui_context_menu = document.getElementById("context-menu")
const ui_pulsanti_context_menu = document.getElementById("pulsanti-context-menu")
const ui_conferma_elimina = document.getElementById("dialog-conferma-elimina")


ui_context_menu.onblur = (event) => {
    // if the event target is inside the context menu, do nothing
    if (event.relatedTarget && event.relatedTarget.closest("#context-menu")) {
        return
    }
    ui_context_menu.closingcallback()
}

function ui_modifica_sostituzione() {
    let id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_sostituzione(id)
    ui_context_menu.closingcallback()
}
function ui_duplica_sostituzione() {
    let id = ui_context_menu.dataset.id

    console.log("duplica sostituzione " + id)
    ui_context_menu.closingcallback()
}
function ui_elimina_sostituzione() {
    ui_pulsanti_context_menu.classList.add("hidden")
    ui_conferma_elimina.classList.remove("hidden")
}
function ui_conferma_elimina_sostituzione() {
    let id = ui_context_menu.dataset.id

    s_elimina_sostituzione(id, false)
    ui_context_menu.closingcallback()
}
function ui_annulla_elimina_sostituzione() {
    ui_context_menu.closingcallback()
}

function mostra_context_menu(event, sostituzione) {
    event.preventDefault()

    sostituzione.focus()

    let id = sostituzione.dataset.id

    sostituzione.classList.add("context-menu-active")

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
        sostituzione.classList.remove("context-menu-active")
    }
}


const ui_sostituzioni_filtro_data = document.getElementById("sostituzioni-filtro-data")
const ui_sostituzioni_filtro_data_expandible = document.getElementById("sostituzioni-filtro-data-expandible")
const ui_sostituzioni_filtro_data_oggi = document.getElementById("sostituzioni-filtro-data-oggi")
const ui_sostituzioni_filtro_data_domani = document.getElementById("sostituzioni-filtro-data-domani")
const ui_sostituzioni_filtro_data_future = document.getElementById("sostituzioni-filtro-data-future")
const ui_sostituzioni_filtro_data_data = document.getElementById("sostituzioni-filtro-data-data")
const ui_sostituzioni_filtro_data_mese = document.getElementById("sostituzioni-filtro-data-mese")
const ui_sostituzioni_filtro_data_tutte = document.getElementById("sostituzioni-filtro-data-tutte")

ui_sostituzioni_filtro_data.onfocus = (e) => {
    ui_sostituzioni_filtro_data_expandible.classList.add("active")
}

ui_sostituzioni_filtro_data.onblur = (e) => {
    if (e.relatedTarget && e.relatedTarget.closest("#sostituzioni-filtro-data-expandible")) {
        ui_sostituzioni_filtro_data.focus()
        e.preventDefault()
        e.stopPropagation()
        return
    }

    ui_sostituzioni_filtro_data_expandible.classList.remove("active")
}


ui_sostituzioni_filtro_data_oggi.onclick = (e) => {
    ui_loading_sostituzioni()

    data_inizio = new Date()
    data_inizio.setHours(0, 0, 0, 0)
    data_fine = new Date()
    data_fine.setHours(23, 59, 59, 0)

    filtri = {
        data_inizio: data_inizio.getTime() / 1000,
        data_fine: data_fine.getTime() / 1000
    }

    s_richiedi_sostituzioni(filtri)
}

ui_sostituzioni_filtro_data_domani.onclick = (e) => {
    ui_loading_sostituzioni()

    data_inizio = new Date()
    data_inizio.setDate(data_inizio.getDate() + 1)
    data_inizio.setHours(0, 0, 0, 0)
    data_fine = new Date()
    data_fine.setDate(data_inizio.getDate())
    data_fine.setHours(23, 59, 59, 0)

    filtri = {
        data_inizio: data_inizio.getTime() / 1000,
        data_fine: data_fine.getTime() / 1000
    }

    s_richiedi_sostituzioni(filtri)
}

ui_sostituzioni_filtro_data_future.onclick = (e) => {
    ui_loading_sostituzioni()

    data_inizio = new Date()
    data_inizio.setHours(0, 0, 0, 0)

    filtri = {
        data_inizio: data_inizio.getTime() / 1000,
        data_fine: null
    }

    s_richiedi_sostituzioni(filtri)
}

ui_sostituzioni_filtro_data_data.onchange = (e) => {
    data_inizio = ui_sostituzioni_filtro_data_data.valueAsDate

    if (data_inizio == null || data_inizio == undefined) {
        return
    }

    data_inizio.setHours(0, 0, 0, 0)
    data_fine = new Date()
    data_fine.setDate(data_inizio.getDate())
    data_fine.setHours(23, 59, 59, 0)

    filtri = {
        data_inizio: data_inizio / 1000,
        data_fine: data_fine / 1000
    }

    s_richiedi_sostituzioni(filtri)
}

ui_sostituzioni_filtro_data_mese.onchange = (e) => {
    ui_sostituzioni_filtro_data_mese.value
}

ui_sostituzioni_filtro_data_tutte.onclick = (e) => {
    ui_loading_sostituzioni()

    filtri = {
        data_inizio: null
    }

    
    s_richiedi_sostituzioni(filtri)
}
