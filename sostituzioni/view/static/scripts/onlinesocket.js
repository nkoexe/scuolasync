const socket = io();


socket.on('lista eventi', (data) => {
    eventi = data
})
socket.on('lista notizie', (data) => {
    notizie = data
})

socket.on('lista sostituzioni', (data) => {
    sostituzioni = data
    sostituzioni_visualizzate = sostituzioni

    refresh_sostituzioni()
})


socket.on('lista ore predefinite', (data) => {
    ore_predefinite = data

    sostituzioni_filtro_ora.aggiorna(ore_predefinite)
})

socket.on('lista classi', (data) => {
    classi = data

    sostituzioni_filtro_classe.aggiorna(classi)
})

socket.on('lista aule', (data) => {
    aule = data

    sostituzioni_filtro_aula.aggiorna(aule)
})

socket.on('lista docenti', (data) => {
    docenti = data

    sostituzioni_filtro_docente.aggiorna(docenti)
})


socket.on('aggiornamento sostituzioni', () => location.reload())


// ----------------

function carica_nuova_sostituzione(pubblicato, data, ora_predefinita, ora_inizio, ora_fine, docente, classe, aula, note) {
    socket.emit('nuova sostituzione', {
        pubblicato: pubblicato,
        data: data,
        ora_predefinita: ora_predefinita,
        ora_inizio: ora_inizio,
        ora_fine: ora_fine,
        docente: docente,
        classe: classe,
        aula: aula,
        note: note,
    })
}