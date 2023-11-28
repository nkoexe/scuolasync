const socket = io();

let eventi = []
let notizie = []
let sostituzioni = []
let sostituzioni_visualizzate = []

let ore_predefinite = []
let aule = []
let classi = []
let docenti = []



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

    filtro_ore.lista_completa = FuzzySet();
    for (let index = 0; index < ore_predefinite.length; index++) {
        filtro_ore.lista_completa.add(ore_predefinite[index].numero.toString());
    }
})

socket.on('lista aule', (data) => {
    aule = data

    filtro_aule.lista_completa = FuzzySet();
    for (let index = 0; index < aule.length; index++) {
        filtro_aule.lista_completa.add(aule[index].numero);
    }
})

socket.on('lista classi', (data) => {
    classi = data

    filtro_classi.lista_completa = FuzzySet();
    for (let index = 0; index < classi.length; index++) {
        filtro_classi.lista_completa.add(classi[index].nome);
    }
})

socket.on('lista docenti', (data) => {
    docenti = data

    filtro_docenti.lista_completa = FuzzySet();
    for (let index = 0; index < docenti.length; index++) {
        filtro_docenti.lista_completa.add(docenti[index].nome + ' ' + docenti[index].cognome);
    }
})


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