const ui_evento_html_template = `
<li>
<div class="evento" data-id={id} tabindex="0">
    <div class="evento-data">
        <span>{data_inizio}</span>
        <span class="separator">-</span>
        <span>{data_fine}</span>
    </div>
    <div class="evento-testo">{testo}</div>
</div>
</li>`


const ui_eventi_container = document.getElementById("eventi-lista")
// const ui_eventi_messaggio_informativo = document.getElementById("sostituzioni-messaggio-informativo")

function format_date(data_ora_inizio, data_ora_fine) {
    // format date objects to single string
    // if the year is the same do not display it

    if (data_ora_inizio == null || data_ora_inizio == undefined
        || data_ora_fine == null || data_ora_fine == undefined) {
        return ["", ""]
    }

    let now = new Date()

    data_ora_inizio = new Date(data_ora_inizio * 1000)
    data_ora_fine = new Date(data_ora_fine * 1000)

    format_options = { day: "numeric", month: "short", year: "numeric", hour: "numeric", minute: "numeric" }

    if (data_ora_inizio.getFullYear() == now.getFullYear() && now.getFullYear() == data_ora_fine.getFullYear()) {
        format_options.year = undefined
    }
    return [data_ora_inizio.toLocaleString(Intl.NumberFormat().resolvedOptions().locale, format_options), data_ora_fine.toLocaleString(Intl.NumberFormat().resolvedOptions().locale, format_options)]
}

function format_evento_to_html(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo) {
    [data_ora_inizio, data_ora_fine] = format_date(data_ora_inizio, data_ora_fine)

    return ui_evento_html_template.replace("{id}", id).replace("{testo}", testo).replace("{data_inizio}", data_ora_inizio).replace("{data_fine}", data_ora_fine)
}

function add_evento_to_ui_list(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo) {
    let evento_html = format_evento_to_html(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo)
    ui_eventi_container.innerHTML += evento_html
}

function ui_modifica_evento() {
    let id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_evento(id)
    ui_context_menu.closingcallback()
}

function refresh_eventi() {
    ui_eventi_container.innerHTML = ""
    eventi.forEach(element => {
        add_evento_to_ui_list(element.id, element.pubblicato, element.urgente, element.data_ora_inizio, element.data_ora_fine, element.testo)
    })

    if (eventi_write) {
      for (const evento of document.getElementsByClassName("evento")) {
        evento.oncontextmenu = (e) => { mostra_context_menu_evento(e, evento) }
      }
    }
}
