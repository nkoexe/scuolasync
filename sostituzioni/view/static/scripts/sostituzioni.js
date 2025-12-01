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


const ui_sostituzioni_lista_container = document.querySelector("#sostituzioni-lista-container");
const ui_sostituzioni_lista = document.querySelector("#sostituzioni-lista")
const ui_sostituzioni_messaggio_informativo = document.querySelector("#sostituzioni-messaggio-informativo")
const ui_sostituzioni_batch_sentinel = document.querySelector("#sostituzioni-batch-sentinel");

const ui_sostituzioni_ordinamento_data = document.querySelector("#sostituzioni-ordinamento-data")
const ui_sostituzioni_ordinamento_data_up = ui_sostituzioni_ordinamento_data.children[0]
const ui_sostituzioni_ordinamento_data_down = ui_sostituzioni_ordinamento_data.children[1]

let sostituzioni_ordinamento = "data"
let sostituzioni_verso_ordinamento = 1


const sostituzioneDateFormatter = new Intl.DateTimeFormat(userLocale, {
	year: "numeric",
	month: "2-digit",
	day: "2-digit"
});

const SOSTITUZIONI_BATCH_SIZE = 200;
let renderedSostituzioni = 0;

const sostituzioniBatchObserver = new IntersectionObserver(entries => {
	if (entries.some(entry => entry.boundingClientRect.top < entry.rootBounds.bottom)) {
		renderNextBatch();
	}
}, {
	root: ui_sostituzioni_lista_container,
	// render 1000px in advance
	// has to be less than batchsize * 2.5rem * 16 = 8000px
	rootMargin: "1000px 0px",
});

sostituzioniBatchObserver.observe(ui_sostituzioni_batch_sentinel);

// fix for jump in scrolls
ui_sostituzioni_lista_container.addEventListener("scrollend", () => {
	if (ui_sostituzioni_batch_sentinel.offsetTop - ui_sostituzioni_lista_container.scrollTop < ui_sostituzioni_lista_container.clientHeight) {
		requestAnimationFrame(renderNextBatch);
	}
});

async function renderNextBatch(amount = SOSTITUZIONI_BATCH_SIZE, initial = false) {
	if (renderedSostituzioni >= sostituzioni_visualizzate.length) return;

	const nextChunk = await Promise.all(
		sostituzioni_visualizzate
			.slice(renderedSostituzioni, renderedSostituzioni + amount)
			.map(element => {
				return format_sostituzione_to_html(element.id, element.pubblicato, element.cancellato, element.data, element.ora_inizio, element.ora_fine, element.ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note, element.incompleta, element.sovrapposizioni, element.descrizione_sovrapposizione);
			})
	);

	const fragment = document.createDocumentFragment();

	// Combine all HTML into a single string and parse once
	const template = document.createElement("template");
	template.innerHTML = nextChunk.join("");
	fragment.appendChild(template.content);

	if (sostituzioni_write) {
		for (const sostituzione of fragment.querySelectorAll(".sostituzione")) {
			sostituzione.oncontextmenu = (e) => { mostra_context_menu_sostituzione(e, sostituzione) }
		}
	}

	attach_tooltips({ root: fragment })

	ui_sostituzioni_lista.appendChild(fragment);

	renderedSostituzioni += nextChunk.length;

	const remaining_height_estimate = (sostituzioni_visualizzate.length - renderedSostituzioni) * 2.5; // 2.5rem minimo per sostituzione
	ui_sostituzioni_batch_sentinel.style.height = remaining_height_estimate + "rem";

	// if initial render, not checking .offsetTop means not halting to calculate the style
	// this saves like a couple ms
	// next batch will be rendered in 100 ms anyway
	if (!initial) {
		if (ui_sostituzioni_batch_sentinel.offsetTop - ui_sostituzioni_lista_container.scrollTop < ui_sostituzioni_lista_container.clientHeight) {
			requestAnimationFrame(renderNextBatch);
			return;
		}
	}
}

async function render_singola_sostituzione(sostituzione) {
	const html = await format_sostituzione_to_html(sostituzione.id, sostituzione.pubblicato, sostituzione.cancellato, sostituzione.data, sostituzione.ora_inizio, sostituzione.ora_fine, sostituzione.ora_predefinita, sostituzione.numero_aula, sostituzione.nome_classe, sostituzione.nome_docente, sostituzione.cognome_docente, sostituzione.note, sostituzione.incompleta, sostituzione.sovrapposizioni, sostituzione.descrizione_sovrapposizione)
	const template = document.createElement("template");
	template.innerHTML = html;

	if (sostituzioni_write) {
		template.content.firstChild.oncontextmenu = (e) => { mostra_context_menu_sostituzione(e, e.currentTarget) }
	}

	attach_tooltips({ root: template.content })

	return template.content.firstChild;
}

function render_ora_predefinita(ora_predefinita) {
	if (ora_predefinita.match(/^[0-9]+$/) !== null) {
		return ora_predefinita + "a ora"
	} else {
		return ora_predefinita
	}
}

async function format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note, incompleta, sovrapposizioni, descrizione_sovrapposizione) {
	if (ora_predefinita == null) {
		if (ora_inizio == null) { ora = "" }
		else {
			ora = ora_inizio + " - " + ora_fine
		}
	}
	else { ora = render_ora_predefinita(ora_predefinita) }
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
	const dateObject = new Date(data * 1000);
	data = sostituzioneDateFormatter.format(dateObject);

	return ui_sostituzione_html_template.replace("{id}", id).replace('{pubblicato}', pubblicato).replace("{incompleta}", incompleta).replace("{sovrapposizioni}", sovrapposizioni).replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note).replace("{icona_pubblicato}", icona_pubblicato).replace("{icona_incompleta}", icona_incompleta).replace("{icona_sovrapposizioni}", icona_sovrapposizioni)
}

async function refresh_sostituzioni() {
	// Ordina e filtra
	sostituzioni_applica_filtri()
	ordina_sostituzioni()

	// Rimuovi completamente ogni dato e rigenera la lista. Necessario al caricamento iniziale.
	renderedSostituzioni = 0;
	ui_sostituzioni_lista_container.scrollTo(0, 0);
	ui_sostituzioni_lista.innerHTML = "";

	// smaller first batch for faster initial render
	renderNextBatch(20, true);
	setTimeout(() => {
		renderNextBatch(200);
	}, 100);

	ui_sostituzioni_messaggio_informativo.classList.add("hidden")
	if (sostituzioni_visualizzate.length === 0) {
		ui_sostituzioni_batch_sentinel.style.height = "0rem";
		ui_sostituzioni_messaggio_informativo.innerHTML = "<span>" + messaggio_nessuna_sostituzione + "</span>"
		ui_sostituzioni_messaggio_informativo.classList.remove("hidden")
	}

	aggiorna_info_sostituzioni()
}

function ordina_sostituzioni() {
	// rimuovi ordinamento dei vari filtri
	ui_sostituzioni_ordinamento_data_up.classList.remove("selected")
	ui_sostituzioni_ordinamento_data_down.classList.remove("selected")
	sostituzioni_filtro_ora.ui_rimuovi_ordinamento()
	sostituzioni_filtro_classe.ui_rimuovi_ordinamento()
	sostituzioni_filtro_aula.ui_rimuovi_ordinamento()
	sostituzioni_filtro_docente.ui_rimuovi_ordinamento()

	// ordina i dati secondo l'ordinamento impostato
	switch (sostituzioni_ordinamento) {
		case "data":
			sostituzioni_visualizzate.sort((a, b) => {
				res = compara_data(a, b) * sostituzioni_verso_ordinamento
				if (res == 0) { res = compara_ora_predefinita(b, a) }
				if (res == 0) { res = compara_docente(b, a) }
				return res
			})

			if (sostituzioni_verso_ordinamento === 1) {
				ui_sostituzioni_ordinamento_data_up.classList.remove("selected")
				ui_sostituzioni_ordinamento_data_down.classList.add("selected")
			} else {
				ui_sostituzioni_ordinamento_data_down.classList.remove("selected")
				ui_sostituzioni_ordinamento_data_up.classList.add("selected")
			}

			break;

		case "#sostituzioni-filtro-ora":
			sostituzioni_visualizzate.sort((a, b) => {
				res = compara_ora_predefinita(a, b) * sostituzioni_verso_ordinamento
				if (res == 0) { res = compara_data(a, b) }
				if (res == 0) { res = compara_docente(a, b) }
				return res
			})

			sostituzioni_filtro_ora.ui_mostra_ordinamento()
			break;

		case "#sostituzioni-filtro-classe":
			sostituzioni_visualizzate.sort((a, b) => {
				res = compara_classe(a, b) * sostituzioni_verso_ordinamento
				if (res == 0) { res = compara_data(a, b) }
				if (res == 0) { res = compara_ora_predefinita(a, b) }
				return res
			})

			sostituzioni_filtro_classe.ui_mostra_ordinamento()
			break;

		case "#sostituzioni-filtro-aula":
			sostituzioni_visualizzate.sort((a, b) => {
				res = compara_aula(a, b) * sostituzioni_verso_ordinamento
				if (res == 0) { res = compara_data(a, b) }
				if (res == 0) { res = compara_ora_predefinita(a, b) }
				return res
			})

			sostituzioni_filtro_aula.ui_mostra_ordinamento()
			break;

		case "#sostituzioni-filtro-docente":
			sostituzioni_visualizzate.sort((a, b) => {
				res = compara_docente(a, b) * sostituzioni_verso_ordinamento
				if (res == 0) { res = compara_data(a, b) }
				if (res == 0) { res = compara_ora_predefinita(a, b) }
				return res
			})

			sostituzioni_filtro_docente.ui_mostra_ordinamento()
			break;
	}
}

ui_sostituzioni_ordinamento_data.onclick = (e) => {
	if (sostituzioni_ordinamento !== "data") {
		sostituzioni_ordinamento = "data"
		sostituzioni_verso_ordinamento = 1
	} else {
		sostituzioni_verso_ordinamento = sostituzioni_verso_ordinamento * -1
	}

	refresh_sostituzioni()
}

function aggiorna_info_sostituzioni() {
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


async function aggiungi_sostituzione(data) {
	sostituzioni.push(data)

	sostituzioni_applica_filtri()
	ordina_sostituzioni()
	aggiorna_info_sostituzioni()

	const new_sostituzione_index = sostituzioni_visualizzate.findIndex(element => element.id === data.id)
	if (new_sostituzione_index === -1) {
		// filtered out
		return;
	}
	if (new_sostituzione_index >= renderedSostituzioni) {
		// not rendered yet
		return;
	}

	const new_sostituzione_element = await render_singola_sostituzione(data)

	const referenceNode = ui_sostituzioni_lista.querySelector(`.sostituzione[data-id='${sostituzioni_visualizzate[new_sostituzione_index + 1]?.id}']`);
	if (referenceNode) {
		referenceNode.before(new_sostituzione_element);
	} else {
		ui_sostituzioni_lista.appendChild(new_sostituzione_element);
	}
	renderedSostituzioni++;
}

async function modifica_sostituzione_visualizzata(data) {
	let sostituzione = sostituzioni.find(element => element.id === data.id)
	let sostituzione_element = ui_sostituzioni_lista.querySelector(`.sostituzione[data-id='${data.id}']`)

	if (sostituzione) {
		for (const key in data) {
			sostituzione[key] = data[key]
		}
	} else {
		aggiungi_sostituzione(data);
		return;
	}

	const previous_index = sostituzioni_visualizzate.findIndex(element => element.id === data.id)

	sostituzioni_applica_filtri()
	ordina_sostituzioni()
	aggiorna_info_sostituzioni()

	const sostituzione_index = sostituzioni_visualizzate.findIndex(element => element.id === data.id)

	if (sostituzione_index === -1) {
		// filtered out
		if (sostituzione_element) {
			sostituzione_element.remove();
			renderedSostituzioni--;
		}
		return;
	}

	if (sostituzione_index === previous_index && sostituzione_element) {
		const new_sostituzione_element = await render_singola_sostituzione(sostituzione)
		sostituzione_element.replaceWith(new_sostituzione_element);

		return;
	}

	if (sostituzione_element) {
		sostituzione_element.remove();
		renderedSostituzioni--;
	}

	if (sostituzione_index >= renderedSostituzioni) {
		// not rendered yet
		return;
	}

	const new_sostituzione_element = await render_singola_sostituzione(data)

	const referenceNode = ui_sostituzioni_lista.querySelector(`.sostituzione[data-id='${sostituzioni_visualizzate[sostituzione_index + 1]?.id}']`);
	if (referenceNode) {
		referenceNode.before(new_sostituzione_element);
	} else {
		ui_sostituzioni_lista.appendChild(new_sostituzione_element);
	}
	renderedSostituzioni++;
}

async function elimina_sostituzione_visualizzata(id) {
	sostituzioni.splice(sostituzioni.findIndex(element => element.id === id), 1)
	const sostituzione_list_index = sostituzioni_visualizzate.findIndex(element => element.id === id)

	if (sostituzione_list_index !== -1) {
		sostituzioni_visualizzate.splice(sostituzione_list_index, 1)
	}

	aggiorna_info_sostituzioni()

	if (sostituzione_list_index >= renderedSostituzioni) {
		// not rendered yet
		return;
	}

	let sostituzione_element = ui_sostituzioni_lista.querySelector(`.sostituzione[data-id='${id}']`)

	if (sostituzione_element) {
		sostituzione_element.remove();
		renderedSostituzioni--;
	}
}
