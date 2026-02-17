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
    document.querySelector('#release-notes-container').classList.remove('visible')
}


function ui_prompt(title, description, release_notes, button_text, button_callback, href) {
    document.querySelector('#title').innerHTML = title
    document.querySelector('#description').innerHTML = description
    document.querySelector('#button-text').innerHTML = button_text

    if (release_notes) {
        document.querySelector('#release-notes-container').classList.add('visible')
        document.querySelector('#release-notes').innerHTML = release_notes
    } else {
        document.querySelector('#release-notes-container').classList.remove('visible')
    }

    setTimeout(() => {
        let button = document.querySelector('#button')
        button.classList.add('active')
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
        ui_prompt("Aggiornamento disponibile!", "", data.release_notes, "Aggiorna", update, null)
        // Show short commit hash (first 8 characters) in UI
        if (data.new_version && data.new_version.length > 8) {
            document.querySelector("#new-version").innerHTML = " >>> " + data.new_version.substring(0, 8)
        }
        let old_href = document.querySelector("#version a").href
        // Link to compare view between current demo and new commit
        document.querySelector("#version a").href = old_href.replace("/commits/", "/compare/") + "..." + data.new_version
    } else {
        ui_prompt("Nessun aggiornamento disponibile.", "Questa è la versione del software più recente!", "", "Torna al sito", null, "/")
    }
})

socket.on("check update errore", (data) => {
    ui_prompt("Errore durante il controllo dell'aggiornamento.", "Si prega di riprovare più tardi.<br>Errore: " + data, "", "Torna al sito", null, "/")
})



socket.io.on("reconnect", () => {
    has_rebooted = true
    if (should_reboot) {
        ui_prompt("Riavvio completato.", "", "", "Vai al sito", null, "/")
    } else {
        ui_prompt("Aggiornamento completato.", "Il sistema è ora aggiornato alla versione più recente.", "", "Vai al sito", null, "/")
    }
})

socket.on("unauthorized", () => {
    location.reload()
})


// ----------------


if (should_reboot) {
    ui_prompt("Riavviare il sistema?", "", "", "Riavvia", reboot, null)
} else {
    ui_loading("Controllo aggiornamenti...", "")
    socket.emit("check update")
}
