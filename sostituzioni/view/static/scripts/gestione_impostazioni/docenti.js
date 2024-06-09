const docente_template = `<div class="nome-docente">
<input class="input-cognome-docente" type="text" placeholder="Cognome" required minlength="1" maxlength="80" autocomplete="off" value="">
<input class="input-nome-docente" type="text" placeholder="Nome" required minlength="1" maxlength="80" autocomplete="off" value="">
</div>
<div class="operazioni-dato">
<button class="material-symbols-rounded pulsante-elimina-dato">delete</button> 
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato hidden">check_circle</button>
</div>`

const ui_cerca_docente = document.querySelector("#cerca-docente-input")
const ui_lista_docenti = document.querySelector("#lista-docenti")

let lista_elementi = []

function crea_elemento(nome, cognome) {
  const element = document.createElement("div")
  element.classList.add("opzione-docente")
  element.dataset.nome = nome
  element.dataset.cognome = cognome
  element.innerHTML = docente_template.replaceAll("{nome}", nome).replaceAll("{cognome}", cognome)

  const input_nome = element.querySelector(".input-nome-docente")
  input_nome.value = nome
  input_nome.oninput = () => modificato(nome, cognome)

  const input_cognome = element.querySelector(".input-cognome-docente")
  input_cognome.value = cognome
  input_cognome.oninput = () => modificato(nome, cognome)

  element.querySelector(".pulsante-elimina-dato").onclick = () => ui_elimina_docente(nome, cognome)
  element.querySelector(".pulsante-conferma-modifiche-dato").onclick = () => ui_conferma_modifiche(nome, cognome)

  return element
}

docenti.sort((a, b) => {
  if (a[1] == b[1])
    return a[0].localeCompare(b[0])

  return a[1].localeCompare(b[1])
})

// function genera_lista_docenti(docenti) {
docenti.forEach(docenti => {
  const element = crea_elemento(docenti[0], docenti[1])
  ui_lista_docenti.appendChild(element)
})
// }

lista_elementi = Array.from(document.querySelectorAll(".opzione-docente"))

function cerca_docente() {
  const query = document.querySelector("#cerca-docente-input").value.toLowerCase()

  if (query == "") {
    lista_elementi.forEach(element => {
      element.classList.remove("hidden")
    })
    return
  }

  lista_elementi.forEach(element => {
    const nome = element.dataset.nome.toLowerCase()
    const cognome = element.dataset.cognome.toLowerCase()
    if ((nome + " " + cognome).includes(query) || (cognome + " " + nome).includes(query)) {
      element.classList.remove("hidden")
    } else {
      element.classList.add("hidden")
    }
  })
}

function modificato(nome, cognome) {
  const element = lista_elementi.find(element => element.dataset.nome === nome && element.dataset.cognome === cognome)

  element.querySelector(".pulsante-elimina-dato").classList.add("hidden")
  element.querySelector(".pulsante-conferma-modifiche-dato").classList.remove("hidden")
}

function ui_conferma_modifiche(nome, cognome) {
  const element = lista_elementi.find(element => element.dataset.nome === nome && element.dataset.cognome === cognome)

  let new_nome = element.querySelector(".input-nome-docente").value
  let new_cognome = element.querySelector(".input-cognome-docente").value

  new_nome = new_nome.trim()
  new_cognome = new_cognome.trim()

  if (new_nome === "") {
    notyf.error("Inserire un nome valido")
    return
  }

  if (new_cognome === "") {
    notyf.error("Inserire un cognome valido")
    return
  }

  // nessuna modifica
  if (new_nome === nome && new_cognome === cognome) {
    element.querySelector(".pulsante-elimina-dato").classList.remove("hidden")
    element.querySelector(".pulsante-conferma-modifiche-dato").classList.add("hidden")
    return
  }

  element.querySelector(".input-nome-docente").disabled = true
  element.querySelector(".input-cognome-docente").disabled = true

  socket.emit("modifica docente", { nome: nome, cognome: cognome, new_nome: new_nome, new_cognome: new_cognome })
}

function ui_elimina_docente(nome, cognome) {
  if (nome == "" || cognome == "") {
    const element = lista_elementi.find(element => element.dataset.nome === nome && element.dataset.cognome === cognome)
    element.remove()
    lista_elementi.splice(lista_elementi.indexOf(element), 1)
    return
  }
  mostra_popup_conferma({ titolo: "Elimina Docente", descrizione: "Sei sicuro di voler eliminare il docente <strong>" + nome + " " + cognome + "</strong>?", testo_pulsante_secondario: "Annulla", testo_pulsante_primario: "Elimina", callback: () => { elimina_docente(nome, cognome) } })
}

function elimina_docente(nome, cognome) {
  socket.emit("elimina docente", nome, cognome)
}

function ui_elimina_tutti_docenti() {
  mostra_popup_conferma({ titolo: "Elimina tutti i docenti", descrizione: "Sei sicuro di voler eliminare <strong>tutti</strong> i docenti del sistema?", testo_pulsante_secondario: "Annulla", testo_pulsante_primario: "Elimina", callback: () => { socket.emit("elimina tutti docenti") } })
}

function nuovo_docente() {
  if (document.querySelector('[data-nome=""][data-cognome=""]')) {
    document.querySelector(".input-cognome-docente").focus()
    return
  }

  const empty_element = crea_elemento("", "")
  lista_elementi.push(empty_element)
  ui_lista_docenti.insertAdjacentElement("afterbegin", empty_element)
  empty_element.querySelector(".input-cognome-docente").focus()
}

//----------------------------------


socket.on("modifica docente successo", (data) => {
  const element = lista_elementi.find(element => element.dataset.nome === data.nome && element.dataset.cognome === data.cognome)
  const new_element = crea_elemento(data.new_nome, data.new_cognome)

  element.replaceWith(new_element)
  lista_elementi.splice(lista_elementi.indexOf(element), 1)
  lista_elementi.push(new_element)

  if (data.nome == "" || data.cognome == "") {
    // nuovo docente
    docenti.push([data.new_nome, data.new_cognome])
  } else {
    // modifica docente esistente
    let index = docenti.findIndex(docente => docente[0] === data.nome && docente[1] === data.cognome)
    docenti[index][0] = data.new_nome
    docenti[index][1] = data.new_cognome
  }

  if (data.nome == "" || data.cognome == "") {
    notyf.success("Docente inserito con successo")
  } else {
    notyf.success("Docente modificato con successo")
  }
})

socket.on("modifica docente errore", (data) => {
  const element = lista_elementi.find(element => element.dataset.nome === data.nome && element.dataset.cognome === data.cognome)
  element.querySelector(".input-nome-docente").disabled = false
  element.querySelector(".input-cognome-docente").disabled = false

  if (data.nome == "" && data.cognome == "") {
    notyf.error("Errore nell'inserimento del docente: " + data.error)
  } else {
    notyf.error("Errore nella modifica del docente: " + data.error)
  }
})

socket.on("elimina docente successo", (data) => {
  let index = docenti.findIndex(docente => docente[0] === data.nome && docente[1] === data.cognome)
  if (index == -1) return;
  docenti.splice(index, 1)

  const element = lista_elementi.find(element => element.dataset.nome === data.nome && element.dataset.cognome === data.cognome)
  element.remove()
  lista_elementi.splice(lista_elementi.indexOf(element), 1)

  notyf.success("Docente eliminato con successo")
})

socket.on("elimina docente errore", (data) => {
  notyf.error("Errore nell'eliminazione del docente: " + data.error)
})

socket.on("elimina tutti docenti in corso", (data) => {
  let should_reload = true
  setTimeout(() => {
    if (should_reload) {
      location.reload()
    }
  },
    data * 1000 + 1000)
  notyf
    .open({
      type: 'info',
      message: "Eliminazione di tutti i docenti in corso. Premere il pulsante X per annullare l'operazione.",
      dismissible: true,
      duration: data * 1000
    })
    .on('dismiss', ({ target, event }) => {
      should_reload = false
      socket.emit("elimina tutti docenti annulla")
    });
})

socket.on("elimina tutti docenti annulla successo", () => {
  notyf.success("Eliminazione annullata.")
})
