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


function format_sostituzione_to_html(oggi, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	if (numero_ora_predefinita == null) {
		if (ora_inizio == null) { ora = "" }
		else { ora = ora_inizio + " - " + ora_fine }
	}
	else { ora = numero_ora_predefinita.length == 1 ? numero_ora_predefinita + "a ora" : numero_ora_predefinita }
	if (note == null) { note = "" }
	if (nome_docente == null) { nome_docente = "" }
	if (cognome_docente == null) { cognome_docente = "" }
	if (nome_classe == null) { nome_classe = "" }
	let piano_aula = ""
	if (numero_aula == null) { numero_aula = "" }
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
	data = data.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' })

	return ui_sostituzione_html_template.replace("{oggi}", oggi ? "oggi" : "").replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{piano_aula}", piano_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note)
}

function add_sostituzione_to_ui_list(oggi, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	let sostituzione_html = format_sostituzione_to_html(oggi, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
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
		let oggi = false
		let now = new Date()
		let now_timestamp = now.getTime()
		now.setHours(0, 0, 0, 0)
		let max_timestamp = null

		// Tieni solo le sostituzioni entro il range di date impostato
		// Se il numero di giorni futuri è -1 bypassa il filtro
		if (giorni_futuri_da_mostrare >= 0) {
			max_timestamp = (now_timestamp + giorni_futuri_da_mostrare * 24 * 60 * 60 * 1000)
			if (giorni_futuri_da_mostrare_lavorativi) {
				// Interpreta i giorni futuri soltanto come lavorativi, ignorando Sabato e Domenica
				let weekday = now.getDay()
				let day_counter = giorni_futuri_da_mostrare
				while (day_counter >= 0) {
					if (weekday == 0 || weekday == 6) {
						// Sabato o Domenica, quindi aggiungi un loop per controllare il giorno successivo
						day_counter++
						max_timestamp += 24 * 60 * 60 * 1000
					}
					weekday = (weekday + 1) % 7
					day_counter--
				}
			}
		}


		sostituzioni_visualizzate.forEach(element => {
			// Non pubblicata? Cancellata? Non dovrebbe arrivare qui ma meglio un double check
			if (element.cancellato || !element.pubblicato) { return }

			// Conferma che la sostituzione non sia passata
			// La sottrazione è perché le sostituzioni di oggi sono salvate allo timestamp di oggi a mezzanotte
			oggi = false
			if (element.data * 1000 < (now_timestamp - 24 * 60 * 60 * 1000)) {
				return
			}

			// Sostituzioni entro il range di date impostato, vedi sopra
			if (max_timestamp && element.data * 1000 > max_timestamp) {
				return
			}

			// Se la sostituzione è di oggi, filtra solo le sostituzioni che iniziano dopo l'ora attuale
			if (element.data * 1000 < now_timestamp) {
				oggi = true
				if (element.numero_ora_predefinita) {
					const [hour, minute] = (ore_predefinite.find(ora => ora.numero == element.numero_ora_predefinita).ora_fine_default).split(":")
					const timestamp = now.setHours(parseInt(hour), parseInt(minute))
					if (timestamp - 5 * 60 * 1000 <= now_timestamp) { return }

				} else if (element.ora_fine) {
					const [hour, minute] = (element.ora_fine).split(":")
					const timestamp = now.setHours(parseInt(hour), parseInt(minute))
					if (timestamp - 5 * 60 * 1000 <= now_timestamp) { return }
				}
			}

			add_sostituzione_to_ui_list(oggi, element.data, element.ora_inizio, element.ora_fine, element.numero_ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note)
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
