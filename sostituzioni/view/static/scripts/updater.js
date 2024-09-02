socket = io("/impostazioni");

let has_rebooted = false


function ui_loading(title, description) {
    let button = document.querySelector('#button')
    button.classList.remove('active')
    button.onclick = () => { }
    button.onkeydown = () => { }
    document.querySelector('#button-text').innerHTML = ''
    document.querySelector('#title').innerHTML = title
    document.querySelector('#description').innerHTML = description
    document.querySelector('#button-text-container').style.opacity = '0'
    setTimeout(() => {
        document.querySelector('#loading-container').style.opacity = '1'
    }, 500);
}


function ui_prompt(title, description, button_text, button_callback, href) {
    document.querySelector('#title').innerHTML = title
    document.querySelector('#description').innerHTML = description
    document.querySelector('#loading-container').style.opacity = '0'
    document.querySelector('#button-text').innerHTML = button_text
    setTimeout(() => {
        let button = document.querySelector('#button')
        button.classList.add('active')
        document.querySelector('#button-text-container').style.opacity = '1'
        if (button_callback) {
            button.onclick = button_callback
            button.onkeydown = (e) => {
                if (e.key === 'Enter') {
                    button_callback()
                }
            }
        }
        if (href) {
            button.href = href
        }
    }, 500)
}

function update() {
    ui_loading("Aggiornamento in corso...", "Durata stimata: <10 secondi")
    socket.emit("update")
    setTimeout(() => {
        if (!has_rebooted) {
            ui_loading("Ancora ad aspettare?", "È possibile che ci sia stato un problema, ed il sistema non si sia aggiornato correttamente. Prego contattare il supporto.")
        }
    }, 15000)
}

function reboot() {
    ui_loading("Riavvio in corso...", "")
    socket.emit("reboot")
    setTimeout(() => {
        if (!has_rebooted) {
            ui_loading("Ancora ad aspettare?", "È possibile che ci sia stato un problema, ed il sistema non si sia riavviato. Prego contattare il supporto.")
        }
    }, 15000)
}


// ----------------


socket.on("check update successo", (data) => {
    if (data.value) {
        ui_prompt("Aggiornamento disponibile!", "", "Aggiorna", update, null)
    } else {
        ui_prompt("Nessun aggiornamento disponibile.", "Questa è la versione del software più recente!", "Torna al sito", null, "/")
    }
})

socket.on("check update errore", (data) => {
    ui_prompt("Errore durante il controllo dell'aggiornamento.", "Si prega di riprovare più tardi.<br>Errore: " + data, "Torna al sito", null, "/")
})



socket.io.on("reconnect", () => {
    has_rebooted = true
    if (should_reboot) {
        ui_prompt("Riavvio completato.", "", "Vai al sito", null, "/")
    } else {
        ui_prompt("Aggiornamento completato.", "Il sistema è ora aggiornato alla versione più recente.", "Vai al sito", null, "/")
    }
})

socket.on("unauthorized", () => {
    location.reload()
})


// ----------------


if (should_reboot) {
    ui_prompt("Riavviare il sistema?", "", "Riavvia", reboot, null)
} else {
    ui_loading("Controllo aggiornamenti...", "")
    socket.emit("check update")
}
