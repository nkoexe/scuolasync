const ui_sostituzione_html_template = `
<li>
<div class="sostituzione {oggi}">
  <div class="sostituzione-data sostituzione-docente">
    <span>{cognome_docente} {nome_docente}</span>
  </div>
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
  <div class="sostituzione-data sostituzione-piano">
    <span>{piano_aula}</span>
  </div>
  <div class="sostituzione-data sostituzione-note">
    <span>{note}</span>
  </div>
</div>
</li>`


const ui_sostituzioni_container = document.getElementById("sostituzioni-lista-container")
const ui_sostituzioni_lista = document.getElementById("sostituzioni-lista")
const ui_sostituzioni_messaggio_informativo = document.getElementById("sostituzioni-messaggio-informativo")


function format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	if (numero_ora_predefinita == null) {
		if (ora_inizio == null) { ora = "" }
		else { ora = ora_inizio + " - " + ora_fine }
	}
	else { ora = numero_ora_predefinita.length == 1 ? numero_ora_predefinita + "a ora" : numero_ora_predefinita }
	if (note == null) { note = "" }
	if (nome_docente == null) { nome_docente = "" }
	if (cognome_docente == null) { cognome_docente = "" }
	if (nome_classe == null) { nome_classe = "" }
	if (numero_aula == null) { numero_aula = ""; piano_aula = "" }
	else {
		piano_aula = aule.find(aula => aula.numero === numero_aula).piano
		if (piano_aula == null) { piano_aula = "" }
		else if (piano_aula == "-1") { piano_aula = "Seminterrato" }
		else if (piano_aula == "0") { piano_aula = "Terra" }
		else if (piano_aula == "1") { piano_aula = "Primo" }
		else if (piano_aula == "2") { piano_aula = "Secondo" }
		else if (piano_aula == "3") { piano_aula = "Terzo" }
	}

	// Converte da unix timestamp a dd/mm/yyyy
	data = new Date(data * 1000)
	oggi = data.getDay() === oggi_day
	opzioni_data = { day: '2-digit', month: '2-digit' }
	data = data.toLocaleDateString('it-IT', opzioni_data)

	return ui_sostituzione_html_template.replaceAll("{oggi}", oggi ? "oggi" : "").replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{piano_aula}", piano_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note)
}

function add_sostituzione_to_ui_list(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	// if (cancellato || !pubblicato) { return }

	let sostituzione_html = format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
	ui_sostituzioni_lista.innerHTML += sostituzione_html
}

function refresh_sostituzioni() {
	ordina_sostituzioni()

	ui_sostituzioni_lista.innerHTML = ""
	if (sostituzioni_visualizzate.length === 0) {
		ui_sostituzioni_messaggio_informativo.innerHTML = "<span>" + messaggio_nessuna_sostituzione + "</span>"
		ui_sostituzioni_messaggio_informativo.style.display = "flex"
	} else {
		ui_sostituzioni_messaggio_informativo.style.display = "none"
		oggi_day = new Date().getDay()
		sostituzioni_visualizzate.forEach(element => {
			add_sostituzione_to_ui_list(element.id, element.pubblicato, element.cancellato, element.data, element.ora_inizio, element.ora_fine, element.numero_ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note)
		})
	}
}

function ordina_sostituzioni() {
	sostituzioni_visualizzate.sort((a, b) => {
		res = compara_docente(b, a)
		if (res == 0) { res = compara_data(a, b) }
		if (res == 0) { res = compara_classe(a, b) }
		if (res == 0) { res = compara_aula(a, b) }
		return res
	})
}
