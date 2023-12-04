class Filtro extends Selezione {
    constructor({ id, ordinamento, filtra_lista, render }) {
        super({ id: id, callback: sostituzioni_applica_filtri, filtra_lista: filtra_lista, render: render })

        this.ordinamento = ordinamento
        this.ordinamento = (typeof this.ordinamento === 'undefined') ? true : this.ordinamento
        if (this.ordinamento) {
            this.ui_ordinamento = this.ui_container.getElementsByClassName('sostituzioni-ordinamento')[0]
            this.ui_ordinamento_frecciasu = this.ui_ordinamento.children[0]
            this.ui_ordinamento_frecciagiu = this.ui_ordinamento.children[1]
        }

        this.ordina = false
        this.verso_ordinamento = 1  // 1: crescente, -1: decrescente

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

    rimuovi_ordinamento() {
        this.ui_ordinamento_frecciasu.classList.remove('selected')
        this.ui_ordinamento_frecciagiu.classList.remove('selected')
    }
}

function sostituzioni_applica_filtri() {
    sostituzioni_visualizzate = sostituzioni
    if (sostituzioni_filtro_ora.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.numero_ora_predefinita === sostituzioni_filtro_ora.selected)
    }
    if (sostituzioni_filtro_classe.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.nome_classe === sostituzioni_filtro_classe.selected)
    }
    if (sostituzioni_filtro_aula.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.numero_aula === sostituzioni_filtro_aula.selected)
    }
    if (sostituzioni_filtro_docente.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.nome_docente + ' ' + element.cognome_docente === sostituzioni_filtro_docente.selected)
    }
    if (sostituzioni_filtro_note.selected !== null) {
        // todo: implement fuzzy search
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.note === sostituzioni_filtro_note.selected)
    }

    sostituzioni_ordina()
}

function sostituzioni_ordina() {
    if (!sostituzioni_filtro_ora.ordina) {
        sostituzioni_filtro_ora.rimuovi_ordinamento()
        sostituzioni_filtro_ora.verso_ordinamento = 1
    }
    if (!sostituzioni_filtro_classe.ordina) {
        sostituzioni_filtro_classe.rimuovi_ordinamento()
        sostituzioni_filtro_classe.verso_ordinamento = 1
    }
    if (!sostituzioni_filtro_aula.ordina) {
        sostituzioni_filtro_aula.rimuovi_ordinamento()
        sostituzioni_filtro_aula.verso_ordinamento = 1
    }
    if (!sostituzioni_filtro_docente.ordina) {
        sostituzioni_filtro_docente.rimuovi_ordinamento()
        sostituzioni_filtro_docente.verso_ordinamento = 1
    }

    if (sostituzioni_filtro_ora.ordina) {
        if (sostituzioni_filtro_ora.verso_ordinamento === 1) {
            sostituzioni_visualizzate.sort((a, b) => {
                if (a.numero_ora_predefinita === null && b.numero_ora_predefinita === null) {
                    console.log('wow')
                    return b.ora_inizio.localeCompare(a.ora_inizio)
                } else if (a.numero_ora_predefinita === null) {
                    return 1
                } else if (b.numero_ora_predefinita === null) {
                    return -1
                } else {
                    return b.numero_ora_predefinita - a.numero_ora_predefinita
                }
            })
        } else {
            sostituzioni_visualizzate.sort((a, b) => {
                if (a.numero_ora_predefinita === null && b.numero_ora_predefinita === null) {
                    return a.ora_inizio.localeCompare(b.ora_inizio)
                } else if (a.numero_ora_predefinita === null) {
                    return 1
                } else if (b.numero_ora_predefinita === null) {
                    return -1
                } else {
                    return a.numero_ora_predefinita - b.numero_ora_predefinita
                }
            })
        }
    }
    if (sostituzioni_filtro_classe.ordina) {
        if (sostituzioni_filtro_classe.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.nome_classe.localeCompare(a.nome_classe))
        else
            sostituzioni_visualizzate.sort((a, b) => a.nome_classe.localeCompare(b.nome_classe))
    }
    if (sostituzioni_filtro_aula.ordina) {
        if (sostituzioni_filtro_aula.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.numero_aula.localeCompare(a.numero_aula))
        else
            sostituzioni_visualizzate.sort((a, b) => a.numero_aula.localeCompare(b.numero_aula))
    }
    if (sostituzioni_filtro_docente.ordina) {
        if (sostituzioni_filtro_docente.verso_ordinamento === 1)
            sostituzioni_visualizzate.sort((a, b) => b.nome_docente.localeCompare(a.nome_docente) || b.cognome_docente.localeCompare(a.cognome_docente))
        else
            sostituzioni_visualizzate.sort((a, b) => a.nome_docente.localeCompare(b.nome_docente) || a.cognome_docente.localeCompare(b.cognome_docente))
    }

    refresh_sostituzioni()
}

let sostituzioni_filtro_ora = new Filtro({ id: 'sostituzioni-filtro-ora', filtra_lista: prendi_ora, render: element => element + 'a ora' })
let sostituzioni_filtro_classe = new Filtro({ id: 'sostituzioni-filtro-classe', filtra_lista: prendi_nome })
let sostituzioni_filtro_aula = new Filtro({ id: 'sostituzioni-filtro-aula', filtra_lista: prendi_numero })
let sostituzioni_filtro_docente = new Filtro({ id: 'sostituzioni-filtro-docente', filtra_lista: prendi_nome_cognome })
let sostituzioni_filtro_note = new Filtro({ id: 'sostituzioni-filtro-note', ordinamento: false })
