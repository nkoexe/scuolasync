const docente_template = `<div class="opzione-docente" data-nome="{nome}" data-cognome="{cognome}">
<div class="nome-docente">
<input class="input-cognome-docente" type="text" placeholder="Cognome" required minlength="1" maxlength="80" autocomplete="off" value="{cognome}" oninput="modificato('{nome}', '{cognome}')">
<input class="input-nome-docente" type="text" placeholder="Nome" required minlength="1" maxlength="80" autocomplete="off" value="{nome}" oninput="modificato('{nome}', '{cognome}')">
</div>
<div class="operazioni-dato">
<button class="material-symbols-rounded pulsante-elimina-dato" onclick="ui_elimina_docente('{nome}', '{cognome}')">delete</button>
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato hidden" onclick="ui_conferma_modifiche('{nome}', '{cognome}')">check_circle</button>
</div>
</div>`

const ui_lista_docenti = document.querySelector("#lista-docenti")

docenti.sort((a, b) => {
  if (a[1] == b[1])
    return a[0].localeCompare(b[0])

  return a[1].localeCompare(b[1])
})

docenti.forEach(docenti => {
  ui_lista_docenti.innerHTML += docente_template.replaceAll("{nome}", docenti[0]).replaceAll("{cognome}", docenti[1])
})

function modificato(nome, cognome) {
  let element = document.querySelector(`[data-nome="${nome}"][data-cognome="${cognome}"]`)
  element.querySelector(".pulsante-elimina-dato").classList.add("hidden")
  element.querySelector(".pulsante-conferma-modifiche-dato").classList.remove("hidden")
}

function ui_conferma_modifiche(nome, cognome) {
  let element = document.querySelector(`[data-nome="${nome}"][data-cognome="${cognome}"]`)
  let new_nome = element.querySelector(".input-nome-docente").value
  let new_cognome = element.querySelector(".input-cognome-docente").value

  new_nome = new_nome.replace(/\s/g, "")
  new_cognome = new_cognome.replace(/\s/g, "")

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
    let element = document.querySelector(`[data-nome="${nome}"][data-cognome="${cognome}"]`)
    element.remove()
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

  ui_lista_docenti.innerHTML = docente_template.replaceAll("{nome}", "").replaceAll("{cognome}", "") + ui_lista_docenti.innerHTML;
  document.querySelector(".input-cognome-docente").focus()
}

//----------------------------------


socket.on("modifica docente successo", (data) => {
  let element = document.querySelector(`[data-nome="${data.nome}"][data-cognome="${data.cognome}"]`)
  let new_element = docente_template.replaceAll("{nome}", data.new_nome).replaceAll("{cognome}", data.new_cognome)

  element.outerHTML = new_element

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
  let element = document.querySelector(`[data-nome="${data.nome}"][data-cognome="${data.cognome}"]`)
  element.querySelector(".input-nome-docente").disabled = false
  element.querySelector(".input-cognome-docente").disabled = false

  if (data.nome == "" || data.cognome == "") {
    notyf.error("Errore nell'inserimento del docente: " + data.error)
  } else {
    notyf.error("Errore nella modifica del docente: " + data.error)
  }
})

socket.on("elimina docente successo", (nome, cognome) => {
  let index = docenti.findIndex(docente => docente[0] === nome && docente[1] === cognome)
  if (index == -1) return;
  docenti.splice(index, 1)

  let element = document.querySelector(`[data-nome="${nome}"][data-cognome="${cognome}"]`)
  element.remove()

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
