class Filtro {
    constructor(nome, ui_id, ordinamento) {
        this.nome = nome
        this.ui_filtro = document.getElementById(ui_id)
        this.ui_input = this.ui_filtro.getElementsByClassName('sostituzioni-filtri-input')[0]
        this.ordinamento = ordinamento
        this.ordinamento = (typeof this.ordinamento === 'undefined') ? true : this.ordinamento
        if (this.ordinamento) {
            this.ui_ordinamento = this.ui_filtro.getElementsByClassName('sostituzioni-ordinamento')[0]
            this.ui_ordinamento_frecciasu = this.ui_ordinamento.children[0]
            this.ui_ordinamento_frecciagiu = this.ui_ordinamento.children[1]
        }
        this.ui_dropdown = this.ui_filtro.getElementsByClassName('sostituzioni-filtri-dropdown')[0]
        this.ui_lista = this.ui_dropdown.children[0]

        this.lista_completa
        this.lista_visualizzati
        this.current_index = 0

        this.selected = null
        this.ordina = false
        this.verso_ordinamento = 1  // 1: crescente, -1: decrescente

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

        if (this.ordinamento) {
            this.ui_ordinamento.onclick = (event) => {
                this.verso_ordinamento *= -1

                if (this.verso_ordinamento === 1) {
                    this.ui_ordinamento_frecciasu.classList.add('selected')
                    this.ui_ordinamento_frecciagiu.classList.remove('selected')
                } else {
                    this.ui_ordinamento_frecciasu.classList.remove('selected')
                    this.ui_ordinamento_frecciagiu.classList.add('selected')
                }

                this.ordina = true
                sostituzioni_ordina()
                this.ordina = false
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

    rimuovi_ordinamento() {
        this.ui_ordinamento_frecciasu.classList.remove('selected')
        this.ui_ordinamento_frecciagiu.classList.remove('selected')
    }
}

function sostituzioni_applica_filtri() {
    lista_sostituzioni_visualizzate = lista_sostituzioni
    if (filtro_ore.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.ora_predefinita === filtro_ore.selected)
    }
    if (filtro_classi.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.nome_classe === filtro_classi.selected)
    }
    if (filtro_aule.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.numero_aula === filtro_aule.selected)
    }
    if (filtro_docenti.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.nome_docente + ' ' + element.cognome_docente === filtro_docenti.selected)
    }
    if (filtro_note.selected !== null) {
        // todo: implement fuzzy search
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.note === filtro_note.selected)
    }

    sostituzioni_ordina()
}

function sostituzioni_ordina() {
    if (!filtro_ore.ordina) filtro_ore.rimuovi_ordinamento()
    if (!filtro_classi.ordina) filtro_classi.rimuovi_ordinamento()
    if (!filtro_aule.ordina) filtro_aule.rimuovi_ordinamento()
    if (!filtro_docenti.ordina) filtro_docenti.rimuovi_ordinamento()

    if (filtro_ore.ordina) {
        if (filtro_ore.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.ora_predefinita - a.ora_predefinita)
        else
            sostituzioni_visualizzate.sort((a, b) => a.ora_predefinita - b.ora_predefinita)
    }
    if (filtro_classi.ordina) {
        if (filtro_classi.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.nome_classe.localeCompare(a.nome_classe))
        else
            sostituzioni_visualizzate.sort((a, b) => a.nome_classe.localeCompare(b.nome_classe))
    }
    if (filtro_aule.ordina) {
        if (filtro_aule.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.numero_aula.localeCompare(a.numero_aula))
        else
            sostituzioni_visualizzate.sort((a, b) => a.numero_aula.localeCompare(b.numero_aula))
    }
    if (filtro_docenti.ordina) {
        if (filtro_docenti.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.nome_docente.localeCompare(a.nome_docente) || b.cognome_docente.localeCompare(a.cognome_docente))
        else
            sostituzioni_visualizzate.sort((a, b) => a.nome_docente.localeCompare(b.nome_docente) || a.cognome_docente.localeCompare(b.cognome_docente))
    }

    refresh_sostituzioni()
}

filtro_ore = new Filtro('ore', 'sostituzioni-filtro-ora')
filtro_classi = new Filtro('classi', 'sostituzioni-filtro-classe')
filtro_aule = new Filtro('aule', 'sostituzioni-filtro-aula')
filtro_docenti = new Filtro('docenti', 'sostituzioni-filtro-docente')
filtro_note = new Filtro('note', 'sostituzioni-filtro-note', false)
