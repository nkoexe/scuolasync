const socket = io();


socket.on('lista eventi', (data) => {

})

socket.on('lista sostituzioni', (data) => {
    lista_sostituzioni = data
    lista_sostituzioni_visualizzate = data
    refresh_sostituzioni()
})

socket.on('lista notizie', (data) => {

})


socket.on('lista ore predefinite', (data) => {
    ore.lista_completa = FuzzySet();
    for (let index = 0; index < data.length; index++) {
        ore.lista_completa.add(data[index].numero.toString());
    }
})

socket.on('lista aule', (data) => {
    aule.lista_completa = FuzzySet();
    for (let index = 0; index < data.length; index++) {
        aule.lista_completa.add(data[index].numero);
    }
})

socket.on('lista classi', (data) => {
    classi.lista_completa = FuzzySet();
    for (let index = 0; index < data.length; index++) {
        classi.lista_completa.add(data[index].nome);
    }
})

socket.on('lista docenti', (data) => {
    docenti.lista_completa = FuzzySet();
    for (let index = 0; index < data.length; index++) {
        docenti.lista_completa.add(data[index].nome + ' ' + data[index].cognome);
    }
})

