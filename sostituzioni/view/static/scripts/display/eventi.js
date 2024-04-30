const ui_evento_html_template = `
<li>
<div class="evento {urgente}">
    <div class="evento-data">
        <span>{data}</span>
    </div>
    <div class="evento-testo">{testo}</div>
</div>
</li>`


const ui_eventi_container = document.getElementById("eventi-container")
const ui_eventi_lista = document.getElementById("eventi-lista")
// const ui_eventi_messaggio_informativo = document.getElementById("eventi-messaggio-informativo")

let altezza_container_eventi = 0
let altezza_lista_eventi = 0
let current_scroll_eventi = 0




setInterval(() => {
    current_scroll_eventi += altezza_container_eventi
    if (current_scroll_eventi >= altezza_lista_eventi) { current_scroll_eventi = 0 }
    ui_eventi_container.scroll({ top: current_scroll_eventi, behavior: "smooth" })
}, 10000)

function format_date(data_ora_inizio, data_ora_fine) {
    // format date objects to single string
    // if the year is the same do not display it

    if (data_ora_inizio == null || data_ora_inizio == undefined
        || data_ora_fine == null || data_ora_fine == undefined) {
        return ""
    }

    let now = new Date()

    data_ora_inizio = new Date(data_ora_inizio * 1000)
    data_ora_fine = new Date(data_ora_fine * 1000)

    format_options_inizio = { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }
    format_options_fine = { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }

    if (data_ora_inizio.getFullYear() == now.getFullYear() && now.getFullYear() == data_ora_fine.getFullYear()) {
        format_options_inizio.year = undefined
        format_options_fine.year = undefined
    }
    if (data_ora_inizio.getMonth() == data_ora_fine.getMonth() && data_ora_inizio.getDay() == data_ora_fine.getDay()) {
        format_options_fine.day = undefined
        format_options_fine.month = undefined
    }

    return data_ora_inizio.toLocaleString(Intl.NumberFormat().resolvedOptions().locale, format_options_inizio) + " - " + data_ora_fine.toLocaleString(Intl.NumberFormat().resolvedOptions().locale, format_options_fine)
}

function format_evento_to_html(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo) {
    data = format_date(data_ora_inizio, data_ora_fine)

    urgente = urgente ? "urgente" : ""

    return ui_evento_html_template.replace("{urgente}", urgente).replace("{testo}", testo).replace("{data}", data)
}

function add_evento_to_ui_list(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo) {
    let evento_html = format_evento_to_html(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo)
    ui_eventi_lista.innerHTML += evento_html
}

function ui_modifica_evento() {
    let id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_evento(id)
    ui_context_menu.closingcallback()
}

function refresh_eventi() {
    ordina_eventi()

    ui_eventi_lista.innerHTML = ""
    eventi.forEach(element => {
        add_evento_to_ui_list(element.id, element.pubblicato, element.urgente, element.data_ora_inizio, element.data_ora_fine, element.testo)
    })

    altezza_container_eventi = ui_eventi_container.offsetHeight
    altezza_lista_eventi = ui_eventi_lista.offsetHeight
    current_scroll_eventi = 10 ** 10
}

function ordina_eventi() {
    eventi.sort((a, b) => {
        if (a.urgente && !b.urgente) return -1
        if (!a.urgente && b.urgente) return 1
        if (a.urgente && b.urgente) return a.data_ora_inizio - b.data_ora_inizio
        if (!a.urgente && !b.urgente) return a.data_ora_inizio - b.data_ora_inizio
    })
}


setInterval(() => {
    current_scroll_eventi += altezza_container_eventi
    if (current_scroll_eventi >= altezza_lista_eventi) { current_scroll_eventi = 0 }
    ui_eventi_container.scroll({ top: current_scroll_eventi, behavior: "smooth" })
}, 10000)
