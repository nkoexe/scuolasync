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

    refresh_sostituzioni()
})


socket.on("lista ore predefinite", (data) => {
    ore_predefinite = data
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
    s_richiedi_notizie()
})
