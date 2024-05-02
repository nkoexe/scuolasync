const ui_ora = document.getElementById("ora")
const ui_giorno = document.getElementById("giorno")
const ui_data = document.getElementById("data")


// Cose da fare in un determinato momento
// struttura: { unixtimestamp: func }
let tasks = {}

const options_ora = { 'hour': '2-digit', 'minute': '2-digit', 'second': '2-digit' }
const options_giorno = { 'day': '2-digit' }
const options_data = { 'month': 'long', 'year': 'numeric' }

function update_ui() {
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
}

update_ui()
setInterval(update_ui, 1000);
