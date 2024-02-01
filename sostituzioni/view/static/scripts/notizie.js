const ui_notizia_html_template = `
<li>
<div class="notizia {futura}" data-id={id} tabindex="0">
    <div class="notizia-testo">{testo}</div>
</div>
</li>`


const ui_notizie_container = document.getElementById("notizie-container")
const ui_notizie_messaggio_informativo = document.getElementById("notizie-messaggio-informativo")
const ui_notizie_lista = document.getElementById("notizie-lista")

function format_notizia_to_html(id, data_inizio, data_fine, testo) {
    const futura = (data_inizio * 1000 > new Date()) ? "futura" : ""

    return ui_notizia_html_template.replace("{id}", id).replace("{futura}", futura).replace("{testo}", testo)
}

function add_notizia_to_ui_list(id, data_inizio, data_fine, testo) {
    let notizia_html = format_notizia_to_html(id, data_inizio, data_fine, testo)
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
        add_notizia_to_ui_list(element.id, element.data_inizio, element.data_fine, element.testo)
    })


    ui_notizie_messaggio_informativo.classList.add("hidden")
    if (notizie.length === 0) {
        ui_notizie_messaggio_informativo.innerHTML = "<span>Niente di nuovo qui.</span>"
        ui_notizie_messaggio_informativo.classList.remove("hidden")
    }

    if (notizie_write) {
        for (const notizia of document.getElementsByClassName("notizia")) {
            notizia.oncontextmenu = (e) => { mostra_context_menu_notizia(e, notizia) }
        }
    }
}
