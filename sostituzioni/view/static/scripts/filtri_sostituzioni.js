class Filtro extends Selezione {
    constructor(ui_id, ordinamento) {
        super(ui_id, sostituzioni_applica_filtri)

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

filtro_ore = new Filtro('sostituzioni-filtro-ora')
filtro_classi = new Filtro('sostituzioni-filtro-classe')
filtro_aule = new Filtro('sostituzioni-filtro-aula')
filtro_docenti = new Filtro('sostituzioni-filtro-docente')
filtro_note = new Filtro('sostituzioni-filtro-note', false)
