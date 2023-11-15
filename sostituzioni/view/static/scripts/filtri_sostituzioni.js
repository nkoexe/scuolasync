let lista_current_index

let lista_classi
let lista_classi_visualizzate
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

function render_lista_filtri(ui_lista, elementi, funzione) {
    ui_lista.innerHTML = ''
    for (let index = 0; index < elementi.length; index++) {
        ui_lista.innerHTML += '<li id="lista_classe_' + index + '" onclick="' + funzione + '(' + index + ')"><span>' + elementi[index]; + '</span></li>'
    }
}

function filtra_classe(index_classe) {
    console.log('filtro classe ' + index_classe + ' ' + lista_classi_visualizzate[index_classe])
}

function genera_dropdown_classe() {
    search = ui_input_classe.value
    if (search.length == 0) {
        lista_classi_visualizzate = lista_classi.values()
    } else {
        lista_classi_visualizzate = lista_classi.get(search, [], .1).map(obj => obj[1])
    }
    render_lista_filtri(ui_lista_classe, lista_classi_visualizzate, 'filtra_classe')
}
ui_input_classe.onfocus = (event) => {
    lista_current_index = -1
    ui_dropdown_classe.style.display = 'block'
    genera_dropdown_classe()
}
ui_input_classe.onblur = (event) => {
    ui_dropdown_classe.style.display = 'none'
}
ui_input_classe.oninput = (event) => {
    genera_dropdown_classe()
}
ui_input_classe.onkeydown = (event) => {
    switch (event.keyCode) {
        case 38: // up arrow
            if (lista_classi_visualizzate.length == 0) break
            event.preventDefault()
            if (lista_current_index !== -1) {
                prev_ui_element = document.getElementById('lista_classe_' + lista_current_index)
                prev_ui_element.classList.remove('lista_current')
            } else lista_current_index = 0
            lista_current_index = (lista_current_index + lista_classi_visualizzate.length - 1) % lista_classi_visualizzate.length
            ui_element = document.getElementById('lista_classe_' + lista_current_index)
            ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
            ui_element.classList.add('lista_current')
            break
        case 40: // down arrow
            if (lista_classi_visualizzate.length == 0) break
            event.preventDefault()
            if (lista_current_index !== -1) {
                prev_ui_element = document.getElementById('lista_classe_' + lista_current_index)
                prev_ui_element.classList.remove('lista_current')
            }
            lista_current_index = (lista_current_index + 1) % lista_classi_visualizzate.length
            ui_element = document.getElementById('lista_classe_' + lista_current_index)
            ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
            ui_element.classList.add('lista_current')
            break
        case 13: // enter
            event.preventDefault()
            ui_input_classe.blur()
            filtra_classe(lista_current_index)
            break
    }
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
