const sostituzione_template = `
<li>
<div class="sostituzione">
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
  <div class="sostituzione-pulsanti">
    <button onclick=modifica_sostituzione({id})>Modifica</button>
    <button onclick=duplica_sostituzione({id})>Duplica</button>
    <button onclick=elimina_sostituzione({id})>Elimina</button>
  </div>
</div>
</li>`

let lista_sostituzioni = []
let lista_sostituzioni_visualizzate = []


const sostituzioni_container = document.getElementById('sostituzioni-lista')

function format_sostituzione(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
  if (numero_ora_predefinita == null) { ora = ora_inizio + ' - ' + ora_fine }
  else { ora = numero_ora_predefinita + 'a ora' }
  if (note == null) { note = '' }

  let sostituzione_html = sostituzione_template.replaceAll('{id}', id).replace('{data}', data).replace('{ora}', ora).replace('{numero_aula}', numero_aula).replace('{nome_classe}', nome_classe).replace('{nome_docente}', nome_docente).replace('{cognome_docente}', cognome_docente).replace('{note}', note)
  return sostituzione_html
}

function add_sostituzione(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note) {
  let sostituzione_html = format_sostituzione(id, pubblicato, cancellato, data, ora_inizio, ora_fine, numero_ora_predefinita, numero_aula, nome_classe, nome_docente, cognome_docente, note)
  sostituzioni_container.innerHTML += sostituzione_html
}

function modifica_sostituzione(id) {
  let sostituzione = lista_sostituzioni.find(element => element.id === id)
  console.log('modifica sostituzione ' + sostituzione.id)
}
function duplica_sostituzione(id) {
  console.log('duplica sostituzione ' + id)
}
function elimina_sostituzione(id) {
  console.log('elimina sostituzione ' + id)
}

function refresh_sostituzioni() {
  sostituzioni_container.innerHTML = ''
  lista_sostituzioni_visualizzate.forEach(element => {
    add_sostituzione(element.id, element.pubblicato, element.cancellato, element.data, element.ora_inizio, element.ora_fine, element.numero_ora_predefinita, element.numero_aula, element.nome_classe, element.nome_docente, element.cognome_docente, element.note)
  })

  // add_sostituzione(0, 0, 0, 'data', 1, 1, 4, 'aula', 'classe', 'ciccio', 'bombo', 'questa è una nota. che palle. persona del futuro, ciao. è il 12 novembre e sono ancora sano di mente.')
  // for (let index = 0; index < 50; index++) {
  //   add_sostituzione()
  // }
}