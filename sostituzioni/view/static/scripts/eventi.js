const ui_evento_html_template = `
<li>
<div class="evento {urgente}" data-id={id} tabindex="0">
    <div class="evento-data">
        <span>{data}</span>
    </div>
    <div class="evento-testo">{testo}</div>
</div>
</li>`


const ui_eventi_lista = document.getElementById("eventi-lista")
// const ui_eventi_messaggio_informativo = document.getElementById("sostituzioni-messaggio-informativo")

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

    return data_ora_inizio.toLocaleString(userLocale, format_options_inizio) + " - " + data_ora_fine.toLocaleString(userLocale, format_options_fine)
}

function format_evento_to_html(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo) {
    data = format_date(data_ora_inizio, data_ora_fine)

    urgente = urgente ? "urgente" : ""

    return ui_evento_html_template.replace("{id}", id).replace("{urgente}", urgente).replace("{testo}", testo).replace("{data}", data)
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

    if (eventi_write) {
        for (const evento of document.getElementsByClassName("evento")) {
            evento.oncontextmenu = (e) => { mostra_context_menu_evento(e, evento) }
        }
    }
}

function ordina_eventi() {
    eventi.sort((a, b) => {
        if (a.urgente && !b.urgente) return -1
        if (!a.urgente && b.urgente) return 1
        if (a.urgente && b.urgente) return a.data_ora_inizio - b.data_ora_inizio
        if (!a.urgente && !b.urgente) return a.data_ora_inizio - b.data_ora_inizio
    })
}