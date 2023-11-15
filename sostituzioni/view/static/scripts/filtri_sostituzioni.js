class Filtro {
    constructor(nome, ui_id) {
        this.nome = nome
        this.ui_filtro = document.getElementById(ui_id)
        this.ui_input = this.ui_filtro.children[0].children[0]
        this.ui_dropdown = this.ui_filtro.children[0].children[1]
        this.ui_lista = this.ui_dropdown.children[0]

        this.lista_completa
        this.lista_visualizzati
        this.current_index = 0
        this.selected = null

        this.callback = (data) => {
            if ((typeof data === 'string' || data instanceof String) && data.length !== 0) {
                this.ui_input.value = data
                this.selected = data
            } else {
                this.ui_input.value = ''
                this.selected = null
            }

            sostituzioni_applica_filtri()
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
                        let prev_ui_element = document.getElementById('lista_' + this.nome + this.current_index)
                        prev_ui_element.classList.remove('lista_current')
                    } else this.current_index = 0
                    this.current_index = (this.current_index + this.lista_visualizzati.length - 1) % this.lista_visualizzati.length
                    ui_element = document.getElementById('lista_' + this.nome + this.current_index)
                    ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
                    ui_element.classList.add('lista_current')
                    break
                case 40: // down arrow
                    if (this.lista_visualizzati.length == 0) break
                    event.preventDefault()
                    if (this.current_index !== -1) {
                        let prev_ui_element = document.getElementById('lista_' + this.nome + this.current_index)
                        prev_ui_element.classList.remove('lista_current')
                    }
                    this.current_index = (this.current_index + 1) % this.lista_visualizzati.length
                    ui_element = document.getElementById('lista_' + this.nome + this.current_index)
                    ui_element.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "nearest" })
                    ui_element.classList.add('lista_current')
                    break
                case 13: // enter
                    event.preventDefault()
                    this.ui_input.blur()
                    if (this.current_index !== -1) {
                        this.ui_input.value = this.lista_visualizzati[this.current_index]
                    }
                    this.callback(this.ui_input.value)
                    break
                case 27: // escape
                    this.ui_input.blur()
                    this.callback()
            }
        }
    }

    render_lista() {
        this.ui_lista.innerHTML = ''
        for (let index = 0; index < this.lista_visualizzati.length; index++) {
            this.ui_lista.innerHTML += '<li id="lista_' + this.nome + index + '" onmousedown="' + this.nome + '.callback(\'' + this.lista_visualizzati[index] + '\')"><span>' + this.lista_visualizzati[index]; + '</span></li>'
        }
    }

    genera_dropdown() {
        if (this.lista_completa == undefined) {
            this.ui_dropdown.style.display = 'none'
            return
        }
        let search = this.ui_input.value
        if (search.length == 0) {
            this.lista_visualizzati = this.lista_completa.values()
        } else {
            this.lista_visualizzati = this.lista_completa.get(search, [], .1).map(obj => obj[1])
        }
        this.render_lista()
    }
}

function sostituzioni_applica_filtri() {
    lista_sostituzioni_visualizzate = lista_sostituzioni
    if (ore.selected !== null) {
        lista_sostituzioni_visualizzate = lista_sostituzioni_visualizzate.filter(element => element.ora_predefinita === ore.selected)
    }
    if (classi.selected !== null) {
        lista_sostituzioni_visualizzate = lista_sostituzioni_visualizzate.filter(element => element.nome_classe === classi.selected)
    }
    if (aule.selected !== null) {
        lista_sostituzioni_visualizzate = lista_sostituzioni_visualizzate.filter(element => element.numero_aula === aule.selected)
    }
    if (docenti.selected !== null) {
        lista_sostituzioni_visualizzate = lista_sostituzioni_visualizzate.filter(element => element.nome_docente + ' ' + element.cognome_docente === docenti.selected)
    }
    if (note.selected !== null) {
        // todo: implement fuzzy search
        lista_sostituzioni_visualizzate = lista_sostituzioni_visualizzate.filter(element => element.note === note.selected)
    }

    refresh_sostituzioni()
}

ore = new Filtro('ore', 'sostituzioni-filtro-ora')
classi = new Filtro('classi', 'sostituzioni-filtro-classe')
aule = new Filtro('aule', 'sostituzioni-filtro-aula')
docenti = new Filtro('docenti', 'sostituzioni-filtro-docente')
note = new Filtro('note', 'sostituzioni-filtro-note')
