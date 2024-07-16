let objectID = 0

class Selezione {
    constructor({ query, lista, callback, filtra_lista, render, select_on_exit, select_on_keydown, autocomplete }) {
        objectID += 1
        this.id = objectID

        this.ui_container = document.querySelector(query)
        this.ui_input = this.ui_container.querySelector('.selezione-input')
        this.ui_dropdown = this.ui_container.querySelector('.selezione-dropdown')
        this.ui_lista = this.ui_dropdown.children[0]
        this.select_on_exit = select_on_exit == undefined ? true : select_on_exit
        this.select_on_keydown = select_on_keydown == undefined ? false : select_on_keydown
        this.autocomplete = autocomplete == undefined ? false : autocomplete

        this.lista_elementi  // fuzzyset obj
        this.lista_visualizzati

        this.current_index = 0
        this.selected = null  // actual value - set to null while editing
        this.already_selected = false  // inner signal to prevent callback repeating

        this.callback = callback

        this.filtra_lista = l => l
        this.render = s => s

        if (filtra_lista) {
            this.filtra_lista = filtra_lista
        }

        if (render) {
            this.render = render
        }

        if (lista instanceof Array) {
            this.aggiorna(lista)
        }

        this.ui_input.onfocus = (event) => {
            this.already_selected = false
            this.selected = null
            this.current_index = -1
            this.ui_input.select()
            this.ui_dropdown.style.display = 'block'
            this.genera_dropdown()
        }

        this.ui_input.onblur = (event) => {
            if (this.autocomplete) {
                if (this.ui_input.value == '' || this.lista_visualizzati.length == 0 || this.lista_visualizzati == this.lista_elementi.values()) {
                    this.seleziona(null)
                } else {
                    if (this.selected == null) {
                        this.seleziona(this.lista_visualizzati[0])
                    } else {
                        this.seleziona(this.selected)
                    }
                }
            } else if (this.select_on_exit) {
                if (!this.already_selected) {
                    this.seleziona(this.ui_input.value)
                }
            }
            this.ui_dropdown.style.display = 'none'
        }

        this.ui_input.oninput = (event) => {
            this.already_selected = false
            this.selected = null
            if (this.select_on_keydown) {
                this.seleziona(this.ui_input.value)
            } else {
                this.current_index = -1
                this.genera_dropdown()
                this.ui_lista.scrollTop = 0
            }
        }

        let ui_element
        this.ui_input.onkeydown = (event) => {
            switch (event.keyCode) {
                case 38: // up arrow
                    if (this.lista_visualizzati.length == 0) break
                    event.preventDefault()
                    if (this.current_index !== -1) {
                        let prev_ui_element = document.getElementById('ls_' + this.id + "_" + this.current_index)
                        prev_ui_element.classList.remove('lista_current')
                    } else this.current_index = 0
                    this.current_index = (this.current_index + this.lista_visualizzati.length - 1) % this.lista_visualizzati.length
                    ui_element = document.getElementById('ls_' + this.id + "_" + this.current_index)
                    ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
                    ui_element.classList.add('lista_current')
                    break
                case 40: // down arrow
                    if (this.lista_visualizzati.length == 0) break
                    event.preventDefault()
                    if (this.current_index !== -1) {
                        let prev_ui_element = document.getElementById('ls_' + this.id + "_" + this.current_index)
                        prev_ui_element.classList.remove('lista_current')
                    }
                    this.current_index = (this.current_index + 1) % this.lista_visualizzati.length
                    ui_element = document.getElementById('ls_' + this.id + "_" + this.current_index)
                    ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
                    ui_element.classList.add('lista_current')
                    break
                case 13: // enter
                    event.preventDefault()
                    if (this.current_index !== -1) {
                        this.seleziona(this.lista_visualizzati[this.current_index])
                    } else {
                        this.ui_input.onblur()
                    }
                    this.ui_input.blur()
                    break
                case 27: // escape
                    this.seleziona(null)
                    this.ui_input.blur()
                    break
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
        this.already_selected = true
        if ((typeof data === 'string' || data instanceof String) && data.length !== 0) {
            this.ui_input.value = this.render(data)
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
            let elem = document.createElement("li");
            elem.id = 'ls_' + this.id + "_" + index
            elem.innerHTML = `<span>${this.render(this.lista_visualizzati[index])}</span>`
            elem.onmousedown = () => { this.seleziona(this.lista_visualizzati[index]) }
            this.ui_lista.appendChild(elem)

            // Benvenuto. Questo abominio di codice riposerà in pace qui, in memoria della Grande battaglia combattuta nel nome di D'Incà.
            // this.ui_lista.innerHTML += '<li id="lista_' + this.id + index + '" onmousedown="' + this.id + '.seleziona(\'' + this.lista_visualizzati[index] + '\')"><span>' + this.render(this.lista_visualizzati[index]) + '</span></li>'
        }
    }

    genera_dropdown() {
        if (this.lista_elementi == undefined) {
            this.ui_dropdown.style.display = 'none'
            return
        }
        let search = this.ui_input.value.toLowerCase()
        if (search.length == 0) {
            this.lista_visualizzati = this.lista_elementi.values()
        } else {
            // firstly, check if string is contained in any of the values
            this.lista_visualizzati = this.lista_elementi.values().filter(value => value.toLowerCase().includes(search))

            if (this.lista_visualizzati.length > 0) {
                // if there are values found, order them by their distance to the search string
                this.lista_visualizzati = this.lista_visualizzati.sort((a, b) => {
                    return a.toLowerCase().indexOf(search) - b.toLowerCase().indexOf(search)
                })

            } else {
                // if there aren't any values, do a fuzzy search
                this.lista_visualizzati = this.lista_elementi.get(search, [], .15).map(obj => obj[1])
            }
        }
        this.render_lista()
    }
}

function prendi_ora(ore_predefinite) { return Array.from(ore_predefinite, (ora) => ora.numero) }
function prendi_testo(note_standard) { return Array.from(note_standard, (nota) => nota.testo) }
function prendi_nome(classi) { return Array.from(classi, (classe) => classe.nome) }
function prendi_numero(aule) { return Array.from(aule, (aula) => aula.numero) }
function prendi_cognome_nome(docenti) { return Array.from(docenti, (docente) => docente.cognome + ' ' + docente.nome) }
