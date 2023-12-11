const ui_sostituzione_html_template = `
<li>
<div class="sostituzione" data-id={id}>
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
    <span>{nome_docente} {cognome_docente}</span>
  </div>
  <div class="sostituzione-data sostituzione-note">
    <span>{note}</span>
  </div>
</div>
</li>`


const ui_sostituzioni_container = document.getElementById("sostituzioni-lista")
const ui_sostituzioni_messaggio_informativo = document.getElementById("sostituzioni-messaggio-informativo")
const ui_context_menu = document.getElementById("context-menu")

function format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
  if (numero_ora_predefinita == null) { ora = ora_inizio + " - " + ora_fine }
  else { ora = numero_ora_predefinita + "a ora" }
  if (note == null) { note = "" }
  if (nome_docente == null) { nome_docente = "" }
  if (cognome_docente == null) { cognome_docente = "" }

  // Converte da unix timestamp a dd/mm/yyyy
  data = new Date(data * 1000).toLocaleDateString()

  return ui_sostituzione_html_template.replaceAll("{id}", id).replace("{data}", data).replace("{ora}", ora).replace("{numero_aula}", numero_aula).replace("{nome_classe}", nome_classe).replace("{nome_docente}", nome_docente).replace("{cognome_docente}", cognome_docente).replace("{note}", note)
}

function add_sostituzione_to_ui_list(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
  let sostituzione_html = format_sostituzione_to_html(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
  ui_sostituzioni_container.innerHTML += sostituzione_html
}

function modifica_sostituzione(id) {
  mostra_modifica_sostituzione(id)
}
function duplica_sostituzione(id) {
  console.log("duplica sostituzione " + id)
}
function elimina_sostituzione(id) {
  s_elimina_sostituzione(id, true)
}

function refresh_sostituzioni() {
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

  for (const sostituzione of document.getElementsByClassName("sostituzione")) {
    sostituzione.oncontextmenu = (e) => { mostra_context_menu(e, sostituzione) }
  }
}

function mostra_context_menu(event, sostituzione) {
  event.preventDefault()
  let id = sostituzione.dataset.id

  ui_context_menu.classList.remove("hidden");
  ui_context_menu.style.left = event.clientX + "px";
  ui_context_menu.style.top = event.clientY + "px";
  ui_context_menu.focus()
  ui_context_menu.onblur = () => { ui_context_menu.classList.add("hidden") }
}