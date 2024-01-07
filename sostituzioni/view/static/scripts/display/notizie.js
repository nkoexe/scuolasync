const ui_notizia_html_template = `<span class="notizia">{testo}</span>`


const ui_notizie_container = document.getElementById("notizie-container")
const ui_notizie_lista = document.getElementById("notizie-lista")

function format_notizia_to_html(id, pubblicato, data_ora_inizio, data_ora_fine, testo) {
    return ui_notizia_html_template.replace("{id}", id).replace("{testo}", testo)
}

function add_notizia_to_ui_list(id, pubblicato, data_ora_inizio, data_ora_fine, testo) {
    let notizia_html = format_notizia_to_html(id, pubblicato, data_ora_inizio, data_ora_fine, testo)
    ui_notizie_lista.innerHTML += notizia_html
}

function ui_modifica_notizia() {
    let id = parseInt(ui_context_menu.dataset.id)
    mostra_modifica_notizia(id)
    ui_context_menu.closingcallback()
}

function refresh_notizie() {
    ui_notizie_lista.innerHTML = ""
    notizie.forEach(element => {
        add_notizia_to_ui_list(element.id, element.pubblicato, element.data_ora_inizio, element.data_ora_fine, element.testo)
    })

   ui_notizie_container.insertAdjacentHTML('beforeend',ui_notizie_container.innerHTML);
}
