const ui_eventi_container = document.getElementById("eventi-container")

let altezza_container_eventi = 0
let altezza_lista_eventi = 0
let current_scroll_eventi = 0


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

setInterval(() => {
    current_scroll_eventi += altezza_container_eventi
    if (current_scroll_eventi >= altezza_lista_eventi) { current_scroll_eventi = 0 }
    ui_eventi_container.scroll({ top: current_scroll_eventi, behavior: "smooth" })
}, tempo_scroll_eventi)
