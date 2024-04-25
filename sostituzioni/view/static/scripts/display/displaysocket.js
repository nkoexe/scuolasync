const socket = io('/display');


socket.on("lista eventi", (data) => {
    eventi = data

    refresh_eventi()
})

socket.on("lista notizie", (data) => {
    notizie = data

    refresh_notizie()
})

socket.on("lista sostituzioni", (data) => {
    sostituzioni = data

    for (const sostituzione of sostituzioni) {
        if (sostituzione.cognome_docente)
            sostituzione.cognome_docente = sostituzione.cognome_docente.toUpperCase();
    }

    sostituzioni_visualizzate = sostituzioni

    // ugly ass fix perché vado a prendere il piano dell'aula dalla lista di aule che non ha ancora finito di caricare
    setTimeout(refresh_sostituzioni, 100);
})


socket.on("lista ore predefinite", (data) => {
    ore_predefinite = data

    let now = new Date()
    now.setHours(0, 0, 0, 0)

    for (const ora_predefinita of ore_predefinite) {
        const [hour, minute] = ora_predefinita.ora_fine_default.split(':')
        let timestamp = now.setHours(parseInt(hour), parseInt(minute))

        // reload sostituzioni tot minuti prima della fine dell'ora
        timestamp -= 5 * 60 * 1000
        tasks[timestamp] = refresh_sostituzioni
    }
})

socket.on("lista classi", (data) => {
    classi = data
})

socket.on("lista aule", (data) => {
    aule = data
})

socket.on("lista docenti", (data) => {
    docenti = data

    for (const docente of docenti) {
        if (docente.cognome)
            docente.cognome = docente.cognome.toUpperCase();
    }

    docenti.sort((a, b) => a.cognome.localeCompare(b.cognome) || a.nome.localeCompare(b.nome));
})

socket.on("aggiornamento sostituzioni", () => {
    socket.emit("richiesta sostituzioni")
})

socket.on("aggiornamento eventi", () => {
    socket.emit("richiesta eventi")
})

socket.on("aggiornamento notizie", () => {
    socket.emit("richiesta notizie")
})


// ----------------

// vedi view/__init__.py
// socket.on('shutdown', () => {
//     console.log('Shutting down')
//     socket.disconnect()
// })


// socket.on('connect_error', reconnect)
socket.on('connect_failed', reconnect)
socket.on('disconnect', reconnect)

function reconnect() {
    fetch('/')
        .then((response) => {
            if (response.ok) {
                location.reload()
            }
        })
        .catch(() => { })
        .finally(() => {
            setTimeout(reconnect, 10000)
        })
}