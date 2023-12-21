class Filtro extends Selezione {
    constructor({ id, ordinamento, filtra_lista, render }) {
        super({ id: id, callback: sostituzioni_applica_filtri, filtra_lista: filtra_lista, render: render })

        this.ordinamento = ordinamento
        this.ordinamento = (typeof this.ordinamento === "undefined") ? true : this.ordinamento
        if (this.ordinamento) {
            this.ui_ordinamento = this.ui_container.getElementsByClassName("sostituzioni-ordinamento")[0]
            this.ui_ordinamento_frecciasu = this.ui_ordinamento.children[0]
            this.ui_ordinamento_frecciagiu = this.ui_ordinamento.children[1]
        }

        this.ordina = false
        this.verso_ordinamento = 1  // 1: crescente, -1: decrescente

        if (this.ordinamento) {
            this.ui_ordinamento.onclick = (event) => {
                this.verso_ordinamento *= -1

                if (this.verso_ordinamento === 1) {
                    this.ui_ordinamento_frecciasu.classList.add("selected")
                    this.ui_ordinamento_frecciagiu.classList.remove("selected")
                } else {
                    this.ui_ordinamento_frecciasu.classList.remove("selected")
                    this.ui_ordinamento_frecciagiu.classList.add("selected")
                }

                this.ordina = true
                sostituzioni_ordina()
                this.ordina = false
            }
        }
    }

    rimuovi_ordinamento() {
        this.ui_ordinamento_frecciasu.classList.remove("selected")
        this.ui_ordinamento_frecciagiu.classList.remove("selected")
    }
}

function sostituzioni_applica_filtri() {
    sostituzioni_visualizzate = sostituzioni
    if (sostituzioni_filtro_ora.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.numero_ora_predefinita === (sostituzioni_filtro_ora.selected))
    }
    if (sostituzioni_filtro_classe.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.nome_classe === sostituzioni_filtro_classe.selected)
    }
    if (sostituzioni_filtro_aula.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.numero_aula === sostituzioni_filtro_aula.selected)
    }
    if (sostituzioni_filtro_docente.selected !== null) {
        sostituzioni_visualizzate = sostituzioni_visualizzate.filter(element => element.nome_docente + " " + element.cognome_docente === sostituzioni_filtro_docente.selected)
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

let sostituzioni_filtro_ora = new Filtro({ id: "sostituzioni-filtro-ora", filtra_lista: prendi_ora, render: element => element.length == 1 ? element + "a ora" : element })
let sostituzioni_filtro_classe = new Filtro({ id: "sostituzioni-filtro-classe", filtra_lista: prendi_nome })
let sostituzioni_filtro_aula = new Filtro({ id: "sostituzioni-filtro-aula", filtra_lista: prendi_numero })
let sostituzioni_filtro_docente = new Filtro({ id: "sostituzioni-filtro-docente", filtra_lista: prendi_nome_cognome })
let sostituzioni_filtro_note = new Filtro({ id: "sostituzioni-filtro-note", ordinamento: false })


// ---------------------


let sostituzioni_filtro_data_attivo = 'future'
const ui_sostituzioni_filtro_data = document.getElementById("sostituzioni-filtro-data")
const ui_sostituzioni_filtro_data_expandible = document.getElementById("sostituzioni-filtro-data-expandible")
const ui_sostituzioni_filtro_data_oggi = document.getElementById("sostituzioni-filtro-data-oggi")
const ui_sostituzioni_filtro_data_domani = document.getElementById("sostituzioni-filtro-data-domani")
const ui_sostituzioni_filtro_data_future = document.getElementById("sostituzioni-filtro-data-future")
const ui_sostituzioni_filtro_data_data = document.getElementById("sostituzioni-filtro-data-data")
const ui_sostituzioni_filtro_data_mese = document.getElementById("sostituzioni-filtro-data-mese")
const ui_sostituzioni_filtro_data_tutte = document.getElementById("sostituzioni-filtro-data-tutte")


function sostituzioni_filtra_data() {
    // funzione per generare i filtri con i quali caricare le sostituzioni

    ui_sostituzioni_filtro_data_rimuovi_selected()

    switch (sostituzioni_filtro_data_attivo) {
        case "oggi":
            data_inizio = new Date()
            data_inizio.setHours(0, 0, 0, 0)
            data_fine = new Date()
            data_fine.setHours(23, 59, 59, 0)

            filtri = {
                data_inizio: data_inizio.getTime() / 1000,
                data_fine: data_fine.getTime() / 1000
            }

            ui_sostituzioni_filtro_data_oggi.classList.add("selected")
            break

        case "domani":
            data_inizio = new Date()
            data_inizio.setDate(data_inizio.getDate() + 1)
            data_inizio.setHours(0, 0, 0, 0)
            data_fine = new Date()
            data_fine.setDate(data_inizio.getDate())
            data_fine.setHours(23, 59, 59, 0)

            filtri = {
                data_inizio: data_inizio.getTime() / 1000,
                data_fine: data_fine.getTime() / 1000
            }

            ui_sostituzioni_filtro_data_domani.classList.add("selected")
            break

        case "future":
            data_inizio = new Date()
            data_inizio.setHours(0, 0, 0, 0)

            filtri = {
                data_inizio: data_inizio.getTime() / 1000,
                data_fine: null
            }

            ui_sostituzioni_filtro_data_future.classList.add("selected")
            break

        case "data":
            data_inizio = ui_sostituzioni_filtro_data_data.valueAsDate

            if (data_inizio == null || data_inizio == undefined) {
                return
            }

            data_inizio.setHours(0, 0, 0, 0)
            data_fine = new Date(data_inizio.getTime())
            data_fine.setHours(23, 59, 59, 0)

            filtri = {
                data_inizio: data_inizio.getTime() / 1000,
                data_fine: data_fine.getTime() / 1000
            }

            ui_sostituzioni_filtro_data_data.classList.add("selected")
            break

        case "mese":
            //todo complete      
            ui_sostituzioni_filtro_data_mese.value

            ui_sostituzioni_filtro_data_mese.classList.add("selected")
            break

        case "tutte":
            filtri = {
                data_inizio: 0
            }

            ui_sostituzioni_filtro_data_tutte.classList.add("selected")
            break

        default:
            data_inizio = new Date()
            data_inizio.setHours(0, 0, 0, 0)

            filtri = {
                data_inizio: data_inizio.getTime() / 1000,
                data_fine: null
            }

            ui_sostituzioni_filtro_data_future.classList.add("selected")
    }

    return filtri
}



ui_sostituzioni_filtro_data.onfocus = (e) => {
    ui_sostituzioni_filtro_data_expandible.classList.add("active")
}

ui_sostituzioni_filtro_data.onblur = (e) => {
    if (e.relatedTarget && e.relatedTarget.closest("#sostituzioni-filtro-data-expandible")) {
        ui_sostituzioni_filtro_data.focus()
        e.preventDefault()
        e.stopPropagation()
        return
    }

    ui_sostituzioni_filtro_data_expandible.classList.remove("active")
}

function ui_sostituzioni_filtra_data() {
    ui_loading_sostituzioni()
    filtri = sostituzioni_filtra_data()
    s_richiedi_sostituzioni(filtri)
}

function ui_sostituzioni_filtro_data_rimuovi_selected() {
    ui_sostituzioni_filtro_data_oggi.classList.remove("selected")
    ui_sostituzioni_filtro_data_domani.classList.remove("selected")
    ui_sostituzioni_filtro_data_future.classList.remove("selected")
    ui_sostituzioni_filtro_data_data.classList.remove("selected")
    ui_sostituzioni_filtro_data_mese.classList.remove("selected")
    ui_sostituzioni_filtro_data_tutte.classList.remove("selected")
}

ui_sostituzioni_filtro_data_oggi.onclick = (e) => {
    sostituzioni_filtro_data_attivo = 'oggi'
    ui_sostituzioni_filtra_data()
}

ui_sostituzioni_filtro_data_domani.onclick = (e) => {
    sostituzioni_filtro_data_attivo = 'domani'
    ui_sostituzioni_filtra_data()
}

ui_sostituzioni_filtro_data_future.onclick = (e) => {
    sostituzioni_filtro_data_attivo = 'future'
    ui_sostituzioni_filtra_data()
}

ui_sostituzioni_filtro_data_data.onchange = (e) => {
    sostituzioni_filtro_data_attivo = 'data'
    ui_sostituzioni_filtra_data()
}

ui_sostituzioni_filtro_data_mese.onchange = (e) => {
    sostituzioni_filtro_data_attivo = 'mese'
    ui_sostituzioni_filtra_data()
}

ui_sostituzioni_filtro_data_tutte.onclick = (e) => {
    sostituzioni_filtro_data_attivo = 'tutte'
    ui_sostituzioni_filtra_data()
}
