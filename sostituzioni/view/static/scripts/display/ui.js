const ui_ora = document.getElementById("ora")
const ui_giorno = document.getElementById("giorno")
const ui_data = document.getElementById("data")

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


setInterval(() => {
    now = dayjs()
    ui_ora.innerText = now.format('HH:mm:ss')
    ui_giorno.innerText = now.format('DD')
    ui_data.innerText = now.format('MMMM YYYY')

}, 1000);