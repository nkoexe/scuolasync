const ui_evento_html_template = `
<li>
<div class="evento" data-id={id} tabindex="0">
    <div class="evento-testo">{testo}</div>
</div>
</li>`


const ui_eventi_container = document.getElementById("eventi-lista")
// const ui_eventi_messaggio_informativo = document.getElementById("sostituzioni-messaggio-informativo")


function format_evento_to_html(id, pubblicato, urgente, data_ora_inizio, data_ora_fine, testo) {
    return ui_evento_html_template.replace("{id}", id).replace("{testo}", testo)
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
        add_evento_to_ui_list(i, true, false, null, null, `testo evento ${i}`)
    }
}