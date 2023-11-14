let lista_classi
// let lista_aule
// let lista_docenti
// let lista_ore

// const input_ora = document.getElementById('sostituzioni-filtri-input-ora')
// const dropdown_ora = document.getElementById('sostituzioni-filtri-suggerimenti-ora')
const ui_filtro_classe = document.getElementById('sostituzioni-filtro-classe')
const ui_input_classe = ui_filtro_classe.children[0].children[0]
const ui_dropdown_classe = ui_filtro_classe.children[0].children[1]
const ui_lista_classe = ui_dropdown_classe.children[0]
// const input_aula = document.getElementById('sostituzioni-filtri-input-aula')
// const dropdown_aula = document.getElementById('sostituzioni-filtri-suggerimenti-aula')
// const input_docente = document.getElementById('sostituzioni-filtri-input-docente')
// const dropdown_docente = document.getElementById('sostituzioni-filtri-suggerimenti-docente')
// const input_note = document.getElementById('sostituzioni-filtri-input-note')
// const dropdown_note = document.getElementById('sostituzioni-filtri-suggerimenti-note')

function render_lista_filtri(ui_lista, lista, funzione) {
    ui_lista.innerHTML = ''
    lista.forEach((element) => {
        ui_lista.innerHTML += '<li onclick="' + funzione + '(\'' + element + '\')"><span>' + element + '</span></li>'
    })
}

function filtra_classe(classe) {
    console.log('filtro classe ' + classe)
}

function genera_dropdown_classe() {
    search = ui_input_classe.value
    if (search.length == 0) {
        render_lista_filtri(ui_lista_classe, lista_classi.values(), 'filtra_classe')
    } else {
        lista = lista_classi.get(search, [], .1).map(obj => obj[1])
        render_lista_filtri(ui_lista_classe, lista, null)
    }
}
ui_input_classe.onfocus = (event) => {
    ui_dropdown_classe.style.display = 'block'
    genera_dropdown_classe()
}
ui_input_classe.onblur = (event) => {
    console.log(event)
    ui_dropdown_classe.style.display = 'none'
}
ui_input_classe.oninput = (event) => {
    genera_dropdown_classe()
}


// socket.on('lista aule', (data) => {
//     lista_aule = []
//     for (let index = 0; index < data.length; index++) {
//         lista_aule.push(data[index].numero);
//     }
//     cerca_aula = Wade(lista_aule)
// })

socket.on('lista classi', (data) => {
    lista_classi = FuzzySet();
    for (let index = 0; index < data.length; index++) {
        lista_classi.add(data[index].nome);
    }
})

// socket.on('lista docenti', (data) => { })

// socket.on('lista ore predefinite', (data) => { })
