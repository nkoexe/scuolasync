socket = io("/impostazioni");


function ui_loading(title, description) {
    document.querySelector('#title').innerHTML = title
    document.querySelector('#description').innerHTML = description
    document.querySelector('#button').classList.remove('active')
    document.querySelector('#button').onclick = () => { }
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
        document.querySelector('#button').classList.add('active')
        document.querySelector('#button-text-container').style.opacity = '1'
        if (button_callback) {
            document.querySelector('#button').onclick = button_callback
        }
        if (href) {
            document.querySelector('#success-link').href = href
        }
    }, 500)
}

function update() {
    ui_loading("Aggiornamento in corso...", "Durata stimata: 10 secondi")
    socket.emit("update")
}

function reboot() {
    ui_loading("Riavvio in corso...", "")
    socket.emit("reboot")
}


// ----------------


socket.on("check update successo", (data) => {
    if (data.value) {
        ui_prompt("Aggiornamento disponibile!", "", "Aggiorna", update, null)
    } else {
        ui_prompt("Nessun aggiornamento disponibile.", "Questa è la versione del software più recente!", "Torna al sito", null, "/")
    }
})


socket.io.on("reconnect", () => {
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
    socket.emit("check update")
    ui_loading("Controllo aggiornamenti...", "")
}


// function checkserver() {
//     fetch('/version')
//         .then((response) => {
//             if (response.ok) {
//                 return response.text()
//             }
//         })
//         .then((new_version) => {
//             if (version != new_version) {
//                 document.querySelector('#success-link').href = '/'
//                 document.querySelector('#title').innerHTML = '{{operazione}} completato.'
//                 document.querySelector('#loading-container').style.opacity = '0'
//                 setTimeout(() => {
//                     document.querySelector('#button').classList.add('active')
//                     document.querySelector('#button-text-container').style.opacity = '1'
//                 }, 500)

//             } else {
//                 setTimeout(checkserver, 1000)
//             }
//         })
//         .catch(() => {
//             setTimeout(checkserver, 1000)
//         })
// }
// checkserver()