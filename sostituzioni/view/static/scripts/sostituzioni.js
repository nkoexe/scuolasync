const sostituzione_template = `
<li>
<div>
  <h4 class="title">{titolo}</h4>
  <button>Elimina</button>
</div>
</li>`

const sostituzioni_container = document.getElementById('sostituzioni-lista')

function add_sostituzione(title) {
  let sostituzione_html = sostituzione_template
  sostituzione_html = sostituzione_html.replace('{titolo}', title)
  sostituzioni_container.innerHTML += sostituzione_html
}


socket.on('lista sostituzioni', (data) => {
  console.log('ok')
  console.log(data)
  data.forEach(element => {
    add_sostituzione(element.numero)
  })
})