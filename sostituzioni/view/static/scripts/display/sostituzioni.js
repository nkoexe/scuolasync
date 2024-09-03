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


const ui_sostituzioni_container = document.querySelector("#sostituzioni-lista-container")
const ui_sostituzioni_lista = document.querySelector("#sostituzioni-lista")
const ui_sostituzioni_messaggio_informativo = document.querySelector("#sostituzioni-messaggio-informativo")
const ui_sostituzioni_pagine = document.querySelector("#sostituzioni-pagine")

let sostituzioni_elemento_scroll = 0
let sostituzioni_indici_scroll = []


function format_sostituzione_to_html(oggi, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	if (ora_predefinita == null) {
		if (ora_inizio == null) { ora = "" }
		else { ora = ora_inizio + " - " + ora_fine }
	}
	else { ora = ora_predefinita.length == 1 ? ora_predefinita + "a ora" : ora_predefinita }
	if (note == null) { note = "" }
	if (nome_docente == null) { nome_docente = "" }
	if (cognome_docente == null) { cognome_docente = "" }
	if (nome_classe == null) { nome_classe = "" }
	let piano_aula = ""
	if (numero_aula == null) { numero_aula = "" }
	else {
		const aula = aule.find(aula => aula.numero === numero_aula)
		if (aula) {
			if (aula.piano == "-1") { piano_aula = "Seminterrato" }
			else if (aula.piano == "0") { piano_aula = "Terra" }
			else if (aula.piano == "1") { piano_aula = "Primo" }
			else if (aula.piano == "2") { piano_aula = "Secondo" }
			else if (aula.piano == "3") { piano_aula = "Terzo" }
			else if (aula.piano == "4") { piano_aula = "Quarto" }
			else if (aula.piano == "5") { piano_aula = "Quinto" }
		}
	}

	// Converte da unix timestamp a dd/mm/yyyy
	data = new Date(data * 1000)
	data = data.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' })

	return ui_sostituzione_html_template.replace("{oggi}", oggi ? "oggi" : "").replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{piano_aula}", piano_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note)
}

function add_sostituzione_to_ui_list(oggi, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
	let sostituzione_html = format_sostituzione_to_html(oggi, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
	ui_sostituzioni_lista.innerHTML += sostituzione_html
}

function refresh_sostituzioni() {
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

	sostituzioni_visualizzate = sostituzioni_visualizzate.filter(sostituzione => {
		// Non pubblicata? Cancellata? Non dovrebbe arrivare qui ma meglio un double check
		if (sostituzione.cancellato || !sostituzione.pubblicato) { return False }

		// Conferma che la sostituzione non sia passata
		// La sottrazione è perché le sostituzioni di oggi sono salvate allo timestamp di oggi a mezzanotte
		if (sostituzione.data * 1000 < (now_timestamp - 24 * 60 * 60 * 1000)) {
			return false
		}

		// Sostituzioni entro il range di date impostato, vedi sopra
		if (max_timestamp && sostituzione.data * 1000 > max_timestamp) {
			return false
		}

		// Se la sostituzione è di oggi, filtra solo le sostituzioni che iniziano dopo l'ora attuale
		if (sostituzione.data * 1000 < now_timestamp) {
			if (sostituzione.ora_predefinita) {
				const ora_predefinita = ore_predefinite.find(ora => ora.numero == sostituzione.ora_predefinita)
				if (ora_predefinita) {
					const [hour, minute] = (ora_predefinita.ora_fine_default).split(":")
					const timestamp = now.setHours(parseInt(hour), parseInt(minute))
					if (timestamp - 5 * 60 * 1000 <= now_timestamp) { return false }
				} else {
					return false
				}
			} else if (sostituzione.ora_fine) {
				const [hour, minute] = (sostituzione.ora_fine).split(":")
				const timestamp = now.setHours(parseInt(hour), parseInt(minute))
				if (timestamp - 5 * 60 * 1000 <= now_timestamp) { return false }
			}
		}

		return true
	})

	ordina_sostituzioni()

	ui_sostituzioni_lista.innerHTML = ""
	if (sostituzioni_visualizzate.length === 0) {
		ui_sostituzioni_messaggio_informativo.innerHTML = "<span>" + messaggio_nessuna_sostituzione + "</span>"
		ui_sostituzioni_messaggio_informativo.style.display = "flex"
	} else {
		ui_sostituzioni_messaggio_informativo.style.display = "none"

		sostituzioni_visualizzate.forEach(element => {
			let oggi = false

			if (element.data * 1000 < now_timestamp) {
				oggi = true
			}

			add_sostituzione_to_ui_list(oggi, element.data, element.ora_inizio, element.ora_fine, element.ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note)
		})
	}

	genera_indici_scroll_sostituzioni()
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

function genera_indici_scroll_sostituzioni() {
	// Genera indici delle sostituzioni alle quali scrollare

	// Scrolla sempre al primo elemento
	sostituzioni_indici_scroll = [0]

	// Altezza del container, nello schermo ci stanno soltanto un determinato numero di elementi
	let container_height = ui_sostituzioni_container.offsetHeight
	// L'elemento precedente che verrà utilizzato per calcolare esattamente la posizione y del prossimo scroll
	// Per la seconda sostituzione alla quale scrollare, l'elemento precedente sarà il primo elemento della lista, quindi inizializza ora
	let prev_scroll_element = ui_sostituzioni_lista.children[0]

	// Per ogni altra sostituzione (dalla seconda in poi)
	for (let index = 1; index < ui_sostituzioni_lista.children.length; index++) {
		const element = ui_sostituzioni_lista.children[index]

		// Per ottenere il prossimo elemento al quale scrollare, controlla che la sua posizione y + la sua altezza sia maggiore dello schermo,
		// ovvero controlla che la sostituzione sia fuori dal bordo del container oppure tagliata a metà
		if ((element.offsetTop + element.offsetHeight) > (container_height + prev_scroll_element.offsetTop)) {
			// Aggiungi l'indice della sostituzione alla lista
			sostituzioni_indici_scroll.push(index)
			// Aggiorna l'elemento precedente in modo da poter calcolare il delta verticale
			prev_scroll_element = element
			// element.style.fontWeight = "bold" // test
		}
	}

	// Aggiorna gli indici di paginazione
	ui_sostituzioni_pagine.innerHTML = ""
	for (let i = 0; i < sostituzioni_indici_scroll.length; i++) {
		const element = document.createElement("div")
		element.classList.add("sostituzioni-pagina")
		if (i == sostituzioni_elemento_scroll) {
			element.classList.add("current")
		}
		ui_sostituzioni_pagine.appendChild(element)
	}
}

new ResizeObserver(genera_indici_scroll_sostituzioni).observe(ui_sostituzioni_container)


// Loop che scrolla la lista di sostituzioni
setInterval(() => {
	// Rimuovi la classe "current" dall'indice della pagina attuale, se presente
	if (ui_sostituzioni_pagine.children[sostituzioni_elemento_scroll]) {
		ui_sostituzioni_pagine.children[sostituzioni_elemento_scroll].classList.remove("current")
	}
	// Prossimo elemento della lista di indici
	sostituzioni_elemento_scroll = (sostituzioni_elemento_scroll + 1) % sostituzioni_indici_scroll.length
	// Trova la sostituzione tra gli elementi del DOM tramite l'indice fornito dalla lista
	const element = ui_sostituzioni_lista.children[sostituzioni_indici_scroll[sostituzioni_elemento_scroll]]
	// Scrolla l'elemento in posizione
	element.scrollIntoView({ behavior: "smooth" })
	// Aggiunge la classe "current" all'indice della pagina attuale
	ui_sostituzioni_pagine.children[sostituzioni_elemento_scroll].classList.add("current")
}, 10000)