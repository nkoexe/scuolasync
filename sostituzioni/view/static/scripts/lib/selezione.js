class Selezione {
    constructor({ id, lista, callback, filtra_lista, render }) {
        this.id = id.replaceAll('-', '_')

        this.ui_container = document.getElementById(id)
        this.ui_input = this.ui_container.getElementsByClassName('selezione-input')[0]
        this.ui_dropdown = this.ui_container.getElementsByClassName('selezione-dropdown')[0]
        this.ui_lista = this.ui_dropdown.children[0]

        this.lista_elementi  // fuzzyset obj
        this.lista_visualizzati

        if (lista instanceof Array) {
            this.aggiorna(lista)
        }

        this.current_index = 0
        this.selected = null

        this.callback = callback

        this.filtra_lista = l => l
        this.render = s => s

        if (filtra_lista) {
            this.filtra_lista = filtra_lista
        }

        if (render) {
            this.render = render
        }

        this.ui_input.onfocus = (event) => {
            this.current_index = -1
            this.ui_dropdown.style.display = 'block'
            this.genera_dropdown()
        }

        this.ui_input.onblur = (event) => {
            this.ui_dropdown.style.display = 'none'
        }

        this.ui_input.oninput = (event) => {
            this.current_index = -1
            this.genera_dropdown()
        }

        let ui_element
        this.ui_input.onkeydown = (event) => {
            switch (event.keyCode) {
                case 38: // up arrow
                    if (this.lista_visualizzati.length == 0) break
                    event.preventDefault()
                    if (this.current_index !== -1) {
                        let prev_ui_element = document.getElementById('lista_' + this.id + this.current_index)
                        prev_ui_element.classList.remove('lista_current')
                    } else this.current_index = 0
                    this.current_index = (this.current_index + this.lista_visualizzati.length - 1) % this.lista_visualizzati.length
                    ui_element = document.getElementById('lista_' + this.id + this.current_index)
                    ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
                    ui_element.classList.add('lista_current')
                    break
                case 40: // down arrow
                    if (this.lista_visualizzati.length == 0) break
                    event.preventDefault()
                    if (this.current_index !== -1) {
                        let prev_ui_element = document.getElementById('lista_' + this.id + this.current_index)
                        prev_ui_element.classList.remove('lista_current')
                    }
                    this.current_index = (this.current_index + 1) % this.lista_visualizzati.length
                    ui_element = document.getElementById('lista_' + this.id + this.current_index)
                    ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
                    ui_element.classList.add('lista_current')
                    break
                case 13: // enter
                    event.preventDefault()
                    this.ui_input.blur()
                    if (this.current_index !== -1) {
                        this.seleziona(this.render(this.lista_visualizzati[this.current_index]))
                    } else {
                        this.seleziona(this.ui_input.value)
                    }
                    break
                case 27: // escape
                    this.ui_input.blur()
                    this.seleziona()
            }
        }
    }

    get valore() {
        return this.ui_input.value
    }

    set valore(data) {
        this.seleziona(data)
    }

    seleziona(data) {
        if ((typeof data === 'string' || data instanceof String) && data.length !== 0) {
            this.ui_input.value = data
            this.selected = data
        } else {
            this.ui_input.value = ''
            this.selected = null
        }

        if (this.callback) { this.callback(this.selected) }
    }

    aggiorna(lista) {
        lista = this.filtra_lista(lista)
        this.lista_elementi = FuzzySet()

        for (let index = 0; index < lista.length; index++) {
            this.lista_elementi.add(lista[index]);
        }
    }

    render_lista() {
        this.ui_lista.innerHTML = ''
        for (let index = 0; index < this.lista_visualizzati.length; index++) {
            this.ui_lista.innerHTML += '<li id="lista_' + this.id + index + '" onmousedown="' + this.id + '.seleziona(\'' + this.render(this.lista_visualizzati[index]) + '\')"><span>' + this.render(this.lista_visualizzati[index]) + '</span></li>'
        }
    }

    genera_dropdown() {
        if (this.lista_elementi == undefined) {
            this.ui_dropdown.style.display = 'none'
            return
        }
        let search = this.ui_input.value
        if (search.length == 0) {
            this.lista_visualizzati = this.lista_elementi.values()
        } else {
            this.lista_visualizzati = this.lista_elementi.get(search, [], .15).map(obj => obj[1])
        }
        this.render_lista()
    }
}

function prendi_ora(ore_predefinite) { return Array.from(ore_predefinite, (ora) => ora.numero.toString()) }
function prendi_nome(classi) { return Array.from(classi, (classe) => classe.nome) }
function prendi_numero(aule) { return Array.from(aule, (aula) => aula.numero) }
function prendi_nome_cognome(docenti) { return Array.from(docenti, (docente) => docente.nome + ' ' + docente.cognome) }
