const sostituzione_template = `
<li>
  <h4 class="title">{titolo}</h4>
  <button>Elimina</button>
</li>`

const sostituzioni_container = document.getElementById('sostituzioni')

function add_sostituzione(title) {
    let sostituzione_html = sostituzione_template
    sostituzione_html = sostituzione_html.replace('{titolo}', title)
    sostituzioni_container.innerHTML += sostituzione_html
}