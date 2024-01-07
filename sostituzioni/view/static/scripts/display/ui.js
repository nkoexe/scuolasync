const ui_ora = document.getElementById("ora")
const ui_giorno = document.getElementById("giorno")
const ui_data = document.getElementById("data")

let altezza_container_sostituzioni = 0
let altezza_lista_sostituzioni = 0
let current_scroll_sostituzioni = 0

let altezza_container_eventi = 0
let altezza_lista_eventi = 0
let current_scroll_eventi = 0

const notizie_scroll_speed = 0.7;
let notizie_marginleft = 0;

options_ora = { 'hour': '2-digit', 'minute': '2-digit', 'second': '2-digit' }
options_giorno = { 'day': '2-digit' }
options_data = { 'month': 'long', 'year': 'numeric' }

setInterval(() => {
    now = new Date()
    ui_ora.innerText = now.toLocaleTimeString('it-IT', options_ora)
    ui_giorno.innerText = now.toLocaleDateString('it-IT', options_giorno)
    ui_data.innerText = now.toLocaleDateString('it-IT', options_data)
}, 1000);


setInterval(() => {
    current_scroll_sostituzioni += altezza_container_sostituzioni
    if (current_scroll_sostituzioni > altezza_lista_sostituzioni) { current_scroll_sostituzioni = 0 }
    ui_sostituzioni_container.scroll({ top: current_scroll_sostituzioni, behavior: "smooth" })
}, 10000)

setInterval(() => {
    current_scroll_eventi += altezza_container_eventi
    if (current_scroll_eventi > altezza_lista_eventi) { current_scroll_eventi = 0 }
    ui_eventi_container.scroll({ top: current_scroll_eventi, behavior: "smooth" })
}, 10000)

setInterval(() => {
    ui_notizie_lista.style.marginLeft = `-${notizie_marginleft}px`;
    if (notizie_marginleft > ui_notizie_lista.clientWidth) {
        notizie_marginleft = 0;
    }
    notizie_marginleft += notizie_scroll_speed;
}, 20)