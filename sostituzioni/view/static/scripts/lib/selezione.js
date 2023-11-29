class Selezione {
    constructor(ui_id, lista, callback) {
        this.id = ui_id

        this.ui_container = document.getElementById(ui_id)
        this.ui_input = this.ui_container.getElementsByClassName('selezione-input')[0]
        this.ui_dropdown = this.ui_container.getElementsByClassName('selezione-dropdown')[0]
        this.ui_lista = this.ui_dropdown.children[0]

        this.lista_completa = lista
        this.lista_visualizzati = lista
        this.current_index = 0

        this.selected = null

        this.callback = callback

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
                        this.ui_input.value = this.lista_visualizzati[this.current_index]
                    }
                    this.seleziona(this.ui_input.value)
                    break
                case 27: // escape
                    this.ui_input.blur()
                    this.seleziona()
            }
        }
    }

    seleziona(data) {
        if ((typeof data === 'string' || data instanceof String) && data.length !== 0) {
            this.ui_input.value = data
            this.selected = data
        } else {
            this.ui_input.value = ''
            this.selected = null
        }

        this.callback()
    }

    aggiorna(lista) {
        this.lista_completa = FuzzySet();
        for (let index = 0; index < lista.length; index++) {
            this.lista_completa.add(lista[index].numero.toString());
        }
    }

    render_lista() {
        this.ui_lista.innerHTML = ''
        for (let index = 0; index < this.lista_visualizzati.length; index++) {
            this.ui_lista.innerHTML += '<li id="lista_' + this.id + index + '" onmousedown="filtro_' + this.id + '.seleziona(\'' + this.lista_visualizzati[index] + '\')"><span>' + this.lista_visualizzati[index]; + '</span></li>'
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