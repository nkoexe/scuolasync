const ui_sostituzione_html_template = `
<li>
<div class="sostituzione" data-id={id} tabindex="0">
  <div class="sostituzione-data">
    <span>{data}</span>
  </div>
  <div class="sostituzione-data sostituzione-ora">
    <span>{ora}</span>
  </div>
  <div class="sostituzione-data sostituzione-classe">
    <span>{nome_classe}</span>
  </div>
  <div class="sostituzione-data sostituzione-aula">
    <span>{numero_aula}</span>
  </div>
  <div class="sostituzione-data sostituzione-docente">
    <span>{cognome_docente} {nome_docente}</span>
  </div>
  <div class="sostituzione-data sostituzione-note">
    <span>{note}</span>
  </div>
</div>
</li>`


const ui_sostituzioni_container = document.getElementById("sostituzioni-lista")
const ui_sostituzioni_messaggio_informativo = document.getElementById("sostituzioni-messaggio-informativo")

let sostituzioni_data_verso_ordinamento = 1


function format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	if (numero_ora_predefinita == null) {
		if (ora_inizio == null) { ora = "" }
		else {
			ora = ora_inizio + " - " + ora_fine
		}
	}
	else { ora = numero_ora_predefinita.length == 1 ? numero_ora_predefinita + "a ora" : numero_ora_predefinita }
	if (note == null) { note = "" }
	if (nome_docente == null) { nome_docente = "" }
	if (cognome_docente == null) { cognome_docente = "" }
	if (nome_classe == null) { nome_classe = "" }
	if (numero_aula == null) { numero_aula = "" }

	// Converte da unix timestamp a dd/mm/yyyy
	data = new Date(data * 1000).toLocaleDateString()

	return ui_sostituzione_html_template.replaceAll("{id}", id).replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note)
}

function add_sostituzione_to_ui_list(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	let sostituzione_html = format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
	ui_sostituzioni_container.innerHTML += sostituzione_html
}

function refresh_sostituzioni() {
	ordina_sostituzioni()

	ui_sostituzioni_container.innerHTML = ""
	if (sostituzioni_visualizzate.length === 0) {
		ui_sostituzioni_messaggio_informativo.innerHTML = "<span>" + messaggio_nessuna_sostituzione + "</span>"
		ui_sostituzioni_messaggio_informativo.style.display = "flex"
	} else {
		ui_sostituzioni_messaggio_informativo.style.display = "none"
		sostituzioni_visualizzate.forEach(element => {
			add_sostituzione_to_ui_list(element.id, element.pubblicato, element.cancellato, element.data, element.ora_inizio, element.ora_fine, element.numero_ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note)
		})
	}

	if (sostituzioni_write) {
		for (const sostituzione of document.getElementsByClassName("sostituzione")) {
			sostituzione.oncontextmenu = (e) => { mostra_context_menu_sostituzione(e, sostituzione) }
		}
	}
}

function ordina_sostituzioni() {
	if (sostituzioni_data_verso_ordinamento === 1) {
		sostituzioni_visualizzate.sort((a, b) => {
			return a.data - b.data
		})
	} else {
		sostituzioni_visualizzate.sort((a, b) => {
			return b.data - a.data
		})
	}

	if (!sostituzioni_filtro_ora.ordina) {
		sostituzioni_filtro_ora.ui_rimuovi_ordinamento()
		sostituzioni_filtro_ora.verso_ordinamento = 1
	}
	if (!sostituzioni_filtro_classe.ordina) {
		sostituzioni_filtro_classe.ui_rimuovi_ordinamento()
		sostituzioni_filtro_classe.verso_ordinamento = 1
	}
	if (!sostituzioni_filtro_aula.ordina) {
		sostituzioni_filtro_aula.ui_rimuovi_ordinamento()
		sostituzioni_filtro_aula.verso_ordinamento = 1
	}
	if (!sostituzioni_filtro_docente.ordina) {
		sostituzioni_filtro_docente.ui_rimuovi_ordinamento()
		sostituzioni_filtro_docente.verso_ordinamento = 1
	}

	if (sostituzioni_filtro_ora.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			return compara_ora_predefinita(a, b) * sostituzioni_filtro_ora.verso_ordinamento
		})
	}
	if (sostituzioni_filtro_classe.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			return compara_classe(a, b) * sostituzioni_filtro_classe.verso_ordinamento
		})
	}
	if (sostituzioni_filtro_aula.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			return compara_aula(a, b) * sostituzioni_filtro_aula.verso_ordinamento
		})
	}
	if (sostituzioni_filtro_docente.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			return compara_docente(a, b) * sostituzioni_filtro_docente.verso_ordinamento
		})
	}
}
