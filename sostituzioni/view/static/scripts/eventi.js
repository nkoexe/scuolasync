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

    format_options = { day: "numeric", month: "numeric", year: "numeric", hour: "numeric", minute: "numeric" }

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

function ui_modifica_evento() { // incomplete
    let id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_sostituzione(id)
    ui_context_menu.closingcallback()
}
function ui_duplica_evento() {
    let id = ui_context_menu.dataset.id

    console.log("duplica sostituzione " + id)
    ui_context_menu.closingcallback()
}
function ui_elimina_evento() {
    let id = ui_context_menu.dataset.id
    s_elimina_sostituzione(id, true)
    ui_context_menu.closingcallback()
}

function refresh_eventi() {
    ui_eventi_container.innerHTML = ""
    eventi.forEach(element => {
        add_evento_to_ui_list(element.id, element.pubblicato, element.urgente, element.data_ora_inizio, element.data_ora_fine, element.testo)
    })

    for (let i = 0; i < 20; i++) {
        add_evento_to_ui_list(i, true, false, 1703066400, 1703067400, `testo evento ${i}`)
    }
}