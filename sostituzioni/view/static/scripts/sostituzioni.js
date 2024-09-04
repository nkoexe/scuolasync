const ui_sostituzione_html_template = `<div class="sostituzione ${sostituzioni_write ? "{pubblicato} {incompleta} {sovrapposizioni}" : ""}" data-id={id} tabindex="0">
  <div class="dato-sostituzione sostituzione-data">
    <span>{data}</span>
  </div>
  <div class="dato-sostituzione sostituzione-ora">
    <span>{ora}</span>
  </div>
  <div class="dato-sostituzione sostituzione-classe">
    <span>{nome_classe}</span>
  </div>
  <div class="dato-sostituzione sostituzione-aula">
    <span>{numero_aula}</span>
  </div>
  <div class="dato-sostituzione sostituzione-docente">
    <span>{cognome_docente} {nome_docente}</span>
  </div>
  <div class="dato-sostituzione sostituzione-note">
    <span>{note}</span>
  </div>${sostituzioni_write ?
		`<div class="dato-sostituzione sostituzione-icon">
  {icona_pubblicato}
  {icona_incompleta}
  {icona_sovrapposizioni}
</div>` : ''}
</div>`


const ui_sostituzioni_lista = document.querySelector("#sostituzioni-lista")
const ui_sostituzioni_messaggio_informativo = document.querySelector("#sostituzioni-messaggio-informativo")

const ui_sostituzioni_ordinamento_data = document.querySelector("#sostituzioni-ordinamento-data")
const ui_sostituzioni_ordinamento_data_up = ui_sostituzioni_ordinamento_data.children[0]
const ui_sostituzioni_ordinamento_data_down = ui_sostituzioni_ordinamento_data.children[1]
let sostituzioni_data_verso_ordinamento = 1


async function format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note, incompleta, sovrapposizioni, descrizione_sovrapposizione) {
	if (ora_predefinita == null) {
		if (ora_inizio == null) { ora = "" }
		else {
			ora = ora_inizio + " - " + ora_fine
		}
	}
	else { ora = ora_predefinita.length == 1 ? ora_predefinita + "a ora" : ora_predefinita }
	if (note == null) { note = "" }
	if (cognome_docente == null) { cognome_docente = ""; nome_docente = "" }
	if (nome_classe == null) { nome_classe = "" }
	if (numero_aula == null) { numero_aula = "" }
	if (pubblicato) {
		pubblicato = ""
		icona_pubblicato = ""
	} else {
		pubblicato = "non-pubblicato"
		icona_pubblicato = '<span class="material-symbols-rounded icon" data-tooltip="Questa sostituzione non è pubblicata. È invisibile agli utenti e non verrà mostrata sul display.">visibility_off</span>'
	}
	if (incompleta) {
		incompleta = "incompleta"
		icona_incompleta = '<span class="material-symbols-rounded icon" data-tooltip="Questa sostituzione è incompleta.">error</span>'
	} else {
		incompleta = ""
		icona_incompleta = ""
	}
	if (sovrapposizioni) {
		sovrapposizioni = "sovrapposizioni"
		icona_sovrapposizioni = '<span class="material-symbols-rounded icon" data-tooltip="' + descrizione_sovrapposizione + '">warning</span>'
	} else {
		sovrapposizioni = ""
		icona_sovrapposizioni = ""
	}

	// Converte da unix timestamp a dd/mm/yyyy
	data = new Date(data * 1000).toLocaleDateString(userLocale, {
		year: "numeric",
		month: "2-digit",
		day: "2-digit"
	})

	return ui_sostituzione_html_template.replace("{id}", id).replace('{pubblicato}', pubblicato).replace("{incompleta}", incompleta).replace("{sovrapposizioni}", sovrapposizioni).replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note).replace("{icona_pubblicato}", icona_pubblicato).replace("{icona_incompleta}", icona_incompleta).replace("{icona_sovrapposizioni}", icona_sovrapposizioni)
}

// async function add_sostituzione_to_ui_list(id, pubblicato, cancellato, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
// 	let sostituzione_html = format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
// 	ui_sostituzioni_lista.innerHTML += sostituzione_html
// }

async function refresh_sostituzioni(hard_refresh) {
	hard_refresh = typeof hard_refresh === 'boolean' ? hard_refresh : false

	// Ordina e filtra
	sostituzioni_applica_filtri()
	ordina_sostituzioni()

	if (hard_refresh) {
		// Rimuovi completamente ogni dato e rigenera la lista. Per liste di grandi dimensioni, diventa un processo sostanzioso. Necessario al caricamento iniziale.

		ui_sostituzioni_lista.innerHTML = ""

		const promises = sostituzioni_visualizzate.map(element => {
			return format_sostituzione_to_html(element.id, element.pubblicato, element.cancellato, element.data, element.ora_inizio, element.ora_fine, element.ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note, element.incompleta, element.sovrapposizioni, element.descrizione_sovrapposizione);
		});

		const htmlStrings = await Promise.all(promises);

		if (sostituzioni_visualizzate.length > 100) {
			ui_sostituzioni_lista.innerHTML = htmlStrings.slice(0, 30).join('');
			await new Promise(resolve => setTimeout(resolve, 1))
			ui_sostituzioni_lista.innerHTML += htmlStrings.slice(30).join('');
		} else {
			ui_sostituzioni_lista.innerHTML = htmlStrings.join('');
		}

		if (sostituzioni_write) {
			for (const sostituzione of document.querySelectorAll(".sostituzione")) {
				sostituzione.oncontextmenu = (e) => { mostra_context_menu_sostituzione(e, sostituzione) }
			}
		}

		attach_tooltips()
	}


	// Non rigenerare la lista ma mostra soltanto le sostituzioni filtrate, le altre vengono nascoste

	const elementsMap = new Map();
	const elementsToShow = []
	const elementsToHide = []
	let index = 0;

	const ids = sostituzioni_visualizzate.map(element => element.id);

	for (const sostituzione of document.querySelectorAll(".sostituzione")) {
		const id = parseInt(sostituzione.dataset.id);
		if (ids.includes(id)) {
			elementsToShow.push(sostituzione);
			elementsMap.set(id, { sostituzione, index });
			index++;
		} else {
			elementsToHide.push(sostituzione);
		}
	}

	// Move elements up and down based on the new order
	for (let newIndex = 0; newIndex < ids.length; newIndex++) {
		const id = ids[newIndex];
		const { sostituzione } = elementsMap.get(id);

		// Move the element only if the new position is different from the current position
		if (newIndex !== sostituzione.index) {
			const referenceNode = newIndex > index ? ui_sostituzioni_lista.children[newIndex + 1] : ui_sostituzioni_lista.children[newIndex];
			ui_sostituzioni_lista.insertBefore(sostituzione, referenceNode);
		}
	};

	elementsToHide.forEach(element => element.classList.add("hidden"));
	elementsToShow.forEach(element => element.classList.remove("hidden"));


	ui_sostituzioni_messaggio_informativo.classList.add("hidden")
	if (sostituzioni_visualizzate.length === 0) {
		ui_sostituzioni_messaggio_informativo.innerHTML = "<span>" + messaggio_nessuna_sostituzione + "</span>"
		ui_sostituzioni_messaggio_informativo.classList.remove("hidden")
	}

	// Aggiorna info sostituzioni
	let now = new Date()
	now.setHours(0, 0, 0, 0)
	now = now.getTime() / 1000

	let sostituzioni_oggi = 0
	let sostituzioni_nascoste = 0
	let sostituzioni_incomplete = 0
	let sostituzioni_errori = 0

	for (const sostituzione of sostituzioni_visualizzate) {
		if (sostituzione.data >= now && sostituzione.data < now + 24 * 60 * 60) {
			sostituzioni_oggi++
		}
		if (!sostituzione.pubblicato) {
			sostituzioni_nascoste++
		}
		if (sostituzione.incompleta) {
			sostituzioni_incomplete++
		}
		if (sostituzione.sovrapposizioni) {
			sostituzioni_errori++
		}
	}

	document.querySelector("#sostituzioni-info-numero-totale").innerHTML = sostituzioni_visualizzate.length
	document.querySelector("#sostituzioni-info-numero-oggi").innerHTML = sostituzioni_oggi
	if (sostituzioni_write) {
		document.querySelector("#sostituzioni-info-numero-nascoste").innerHTML = sostituzioni_nascoste == 0 ? '' : sostituzioni_nascoste
		document.querySelector("#sostituzioni-info-numero-incomplete").innerHTML = sostituzioni_incomplete == 0 ? '' : sostituzioni_incomplete
		document.querySelector("#sostituzioni-info-numero-errori").innerHTML = sostituzioni_errori == 0 ? '' : sostituzioni_errori
	}
}

function ordina_sostituzioni() {
	// rimuovi ordinamento dei vari filtri	
	ui_sostituzioni_ordinamento_data_up.classList.remove("selected")
	ui_sostituzioni_ordinamento_data_down.classList.remove("selected")

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

	// ordina i dati secondo l'ordinamento impostato
	if (sostituzioni_filtro_ora.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			res = compara_ora_predefinita(a, b) * sostituzioni_filtro_ora.verso_ordinamento
			if (res == 0) { res = compara_data(a, b) }
			if (res == 0) { res = compara_docente(a, b) }
			return res
		})
		sostituzioni_data_verso_ordinamento = -1
	} else if (sostituzioni_filtro_classe.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			res = compara_classe(a, b) * sostituzioni_filtro_classe.verso_ordinamento
			if (res == 0) { res = compara_data(a, b) }
			if (res == 0) { res = compara_ora_predefinita(a, b) }
			return res
		})
		sostituzioni_data_verso_ordinamento = -1
	} else if (sostituzioni_filtro_aula.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			res = compara_aula(a, b) * sostituzioni_filtro_aula.verso_ordinamento
			if (res == 0) { res = compara_data(a, b) }
			if (res == 0) { res = compara_ora_predefinita(a, b) }
			return res
		})
		sostituzioni_data_verso_ordinamento = -1
	} else if (sostituzioni_filtro_docente.ordina) {
		sostituzioni_visualizzate.sort((a, b) => {
			res = compara_docente(a, b) * sostituzioni_filtro_docente.verso_ordinamento
			if (res == 0) { res = compara_data(a, b) }
			if (res == 0) { res = compara_ora_predefinita(a, b) }
			return res
		})
		sostituzioni_data_verso_ordinamento = -1
	} else {

		if (sostituzioni_data_verso_ordinamento === 1) {
			ui_sostituzioni_ordinamento_data_down.classList.add("selected")
		} else {
			ui_sostituzioni_ordinamento_data_up.classList.add("selected")
		}

		sostituzioni_visualizzate.sort((a, b) => {
			res = compara_data(a, b) * sostituzioni_data_verso_ordinamento
			if (res == 0) { res = compara_ora_predefinita(b, a) }
			if (res == 0) { res = compara_docente(b, a) }
			return res
		})
	}
}

ui_sostituzioni_ordinamento_data.onclick = (e) => {
	sostituzioni_data_verso_ordinamento *= -1
	refresh_sostituzioni()
}
