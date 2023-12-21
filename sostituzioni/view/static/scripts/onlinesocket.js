const socket = io();


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
    sostituzioni_visualizzate = sostituzioni

    refresh_sostituzioni()
})


socket.on("lista ore predefinite", (data) => {
    ore_predefinite = data

    sostituzioni_filtro_ora.aggiorna(ore_predefinite)
})

socket.on("lista classi", (data) => {
    classi = data

    sostituzioni_filtro_classe.aggiorna(classi)
})

socket.on("lista aule", (data) => {
    aule = data

    sostituzioni_filtro_aula.aggiorna(aule)
})

socket.on("lista docenti", (data) => {
    docenti = data

    sostituzioni_filtro_docente.aggiorna(docenti)
})

// todo mostrare messaggio informativo che invita a ricaricare la pagina
socket.on("aggiornamento sostituzioni", () => {
    filtri = sostituzioni_filtra_data()
    s_richiedi_sostituzioni(filtri)
})


// ----------------

function s_richiedi_sostituzioni(filtri) {
    socket.emit("richiesta sostituzioni", filtri)
}

function s_nuova_sostituzione(data) {
    socket.emit("nuova sostituzione", data)
}

function s_elimina_sostituzione(id, mantieni_in_storico) {
    socket.emit("elimina sostituzione", { id: id, mantieni_in_storico: mantieni_in_storico })
}

function s_modifica_sostituzione(id, data) {
    socket.emit("modifica sostituzione", {
        id: id,
        data: data,
    })
}


function s_nuovo_evento(data) {
    socket.emit("nuovo evento", data)
}

function s_elimina_evento(id) {
    socket.emit("elimina evento", { id: id })
}

function s_modifica_evento(id, data) {
    socket.emit("modifica evento", {
        id: id,
        data: data,
    })
}


function s_nuova_notizia(data) {
    socket.emit("nuova notizia", data)
}

function s_elimina_notizia(id) {
    socket.emit("elimina notizia", { id: id })
}

function s_modifica_notizia(id, data) {
    socket.emit("modifica notizia", {
        id: id,
        data: data,
    })
}
