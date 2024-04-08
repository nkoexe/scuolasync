const ui_ora = document.getElementById("ora")
const ui_giorno = document.getElementById("giorno")
const ui_data = document.getElementById("data")

let altezza_container_eventi = 0
let altezza_lista_eventi = 0
let current_scroll_eventi = 0

// Cose da fare in un determinato momento
// struttura: { unixtimestamp: func }
let tasks = {}


options_ora = { 'hour': '2-digit', 'minute': '2-digit', 'second': '2-digit' }
options_giorno = { 'day': '2-digit' }
options_data = { 'month': 'long', 'year': 'numeric' }

setInterval(() => {
    const now = new Date()
    ui_ora.innerText = now.toLocaleTimeString('it-IT', options_ora)
    ui_giorno.innerText = now.toLocaleDateString('it-IT', options_giorno)
    ui_data.innerText = now.toLocaleDateString('it-IT', options_data)

    // execute all past tasks
    for (const timestamp in tasks) {
        if (timestamp < now.getTime()) {
            tasks[timestamp]()
            delete tasks[timestamp]
        }
    }
}, 1000);


setInterval(() => {
    let containerscroll = ui_sostituzioni_container.scrollTop
    containerscroll += ui_sostituzioni_container.offsetHeight
    if (containerscroll >= ui_sostituzioni_lista.offsetHeight) { containerscroll = 0 }
    ui_sostituzioni_container.scroll({ top: containerscroll, behavior: "smooth" })
}, 12000)

setInterval(() => {
    current_scroll_eventi += altezza_container_eventi
    if (current_scroll_eventi >= altezza_lista_eventi) { current_scroll_eventi = 0 }
    ui_eventi_container.scroll({ top: current_scroll_eventi, behavior: "smooth" })
}, 10000)
