const ui_ora = document.getElementById("ora")
const ui_giorno = document.getElementById("giorno")
const ui_data = document.getElementById("data")

let altezza_container_sostituzioni = 0
let altezza_lista_sostituzioni = 0
let current_scroll_sostituzioni = 0


// https://codepen.io/pprakash/pen/oNxNeQE
function Marquee(selector, speed) {
    const parentSelector = document.querySelector(selector);
    const clone = parentSelector.innerHTML;
    const firstElement = parentSelector.children[0];
    let i = 0;
    parentSelector.insertAdjacentHTML('beforeend', clone);

    setInterval(function () {
        firstElement.style.marginLeft = `-${i}px`;
        if (i > firstElement.clientWidth) {
            i = 0;
        }
        i = i + speed;
    }, 20);
}

setTimeout(() => { Marquee('.marquee', 1) }, 2000)

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