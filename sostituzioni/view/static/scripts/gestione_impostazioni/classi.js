const classe_template = `<div class="classe">
<input class="input-nome-classe" type="text" placeholder="Classe" required minlength="1" maxlength="100" autocomplete="off" value="">
<div class="selezione-aula">
  <div class="selezione">
    <input type="text" class="input-aula selezione-input" placeholder="Aula" />
    <div class="selezione-dropdown">
      <ul></ul>
    </div>
  </div>
</div>
</div>
<div class="operazioni-dato">
<button class="material-symbols-rounded pulsante-elimina-dato">delete</button>
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato">save</button>
</div>`

const ui_cerca_classe = document.querySelector("#cerca-classe-input")
const ui_lista_classi = document.querySelector("#lista-classi")

function crea_elemento(classe) {
  const element = document.createElement("div")
  element.classList.add("opzione-classe")
  element.dataset.nome_classe = classe[0]
  element.innerHTML = classe_template

  const input_nome_classe = element.querySelector(".input-nome-classe")
  input_nome_classe.value = classe[0]
  input_nome_classe.oninput = () => modificato(classe[0])

  // const input_aula = element.querySelector(".input-aula")
  // input_aula.value = classe[1].length == 0 ? "" : classe[1][0]
  // input_aula.oninput = () => modificato(classe[0])

  element.querySelector(".pulsante-elimina-dato").onclick = () => ui_elimina_classe(classe[0])
  element.querySelector(".pulsante-conferma-modifiche-dato").onclick = () => ui_conferma_modifiche(classe[0])

  return element
}

classi.sort((a, b) => {
  return a[0].localeCompare(b[0])
})

classi.forEach(classe => {
  ui_lista_classi.appendChild(crea_elemento(classe))
})
classi.forEach(classe => {
  let q = `.opzione-classe[data-nome_classe='${classe[0]}'] .selezione-aula`
  const selezione_aula = new Selezione({ query: q, lista: aule })
  selezione_aula.valore = classe[1][0]
  selezione_aula.callback = (valore) => {
    if (valore == classe[1][0]) return;
    modificato(classe[0])
  }
})

function cerca_classe() {
  const query = document.querySelector("#cerca-classe-input").value.toLowerCase()

  if (query == "") {
    ui_lista_classi.querySelectorAll(".opzione-classe").forEach(element => {
      element.classList.remove("hidden")
    })
    return
  }

  ui_lista_classi.querySelectorAll(".opzione-classe").forEach(element => {
    const nome_classe = element.querySelector(".input-nome-classe").value.toLowerCase()
    const nome_classe_nowhitespace = nome_classe.replace(/\s/g, "")
    const aula = element.querySelector(".input-aula").value.toLowerCase()
    if (nome_classe_nowhitespace.includes(query) || nome_classe.includes(query) || aula.startsWith(query)) {
      element.classList.remove("hidden")
    } else {
      element.classList.add("hidden")
    }
  })
}


function modificato(nome_classe) {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === nome_classe)

  element.classList.add("modificato")
}

function ui_conferma_modifiche(nome_classe) {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === nome_classe)
  let new_nome_classe = element.querySelector(".input-nome-classe").value
  let new_aula = element.querySelector(".input-aula").value

  let classe
  if (nome_classe == "") {
    classe = ["", []]
  } else {
    classe = classi.find(classe => classe[0] === nome_classe)
  }
  new_nome_classe = new_nome_classe.trim()
  new_aula = new_aula.trim()

  if (new_nome_classe === "") {
    notyf.error("Inserire una classe valida")
    return
  }

  // nessuna modifica
  if (new_nome_classe === classe[0] && new_aula === classe[1][0]) {
    element.classList.remove("modificato")
    element.querySelector(".input-nome-classe").value = classe[0]
    return
  }

  element.querySelector(".input-nome-classe").disabled = true
  element.querySelector(".input-aula").disabled = true

  socket.emit("modifica classe", { nome: classe[0], new_nome: new_nome_classe, new_aule: [new_aula] })
}

function ui_elimina_classe(nome_classe) {
  if (nome_classe == "") {
    const element = document.querySelector(".opzione-classe[data-nome_classe='']")
    element.remove()
    return
  }

  mostra_popup_conferma({ titolo: "Elimina Classe", descrizione: "Sei sicuro di voler eliminare la classe <strong>" + nome_classe + "</strong>?", callback: () => { elimina_classe(nome_classe) } })
}

function elimina_classe(nome_classe) {
  socket.emit("elimina classe", nome_classe)
}

function nuova_classe() {
  if (document.querySelector('[data-nome_classe=""]')) {
    document.querySelector(".input-nome-classe").focus()
    return
  }

  const empty_element = crea_elemento(["", ""])
  ui_lista_classi.insertAdjacentElement("afterbegin", empty_element)

  const selezione_aula = new Selezione({ query: ".opzione-classe[data-nome_classe=''] .selezione-aula", lista: aule })
  selezione_aula.callback = (valore) => {
    if (!valore) return;
    modificato("")
  }
  empty_element.querySelector(".input-nome-classe").focus()
}


//----------------------------------


socket.on("modifica classe successo", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === data.nome)

  element.querySelector(".input-nome-classe").disabled = false
  element.querySelector(".input-aula").disabled = false

  const classe = [data.new_nome, data.new_aule]

  element.replaceWith(crea_elemento(classe))
  const selezione_aula = new Selezione({ query: ".opzione-classe[data-nome_classe='" + data.new_nome + "'] .selezione-aula", lista: aule })
  selezione_aula.callback = (valore) => {
    if (valore == classe[1][0]) return;
    modificato(classe[0])
  }
  selezione_aula.valore = classe[1][0]

  if (data.nome == "") {
    // nuova classe
    classi.push(classe)
  } else {
    // modifica classe esistente
    let index = classi.findIndex(classe => classe[0] === data.nome)
    classi[index] = classe
  }

  if (data.nome == "") {
    notyf.success("Classe inserita con successo")
  } else {
    notyf.success("Classe modificata con successo")
  }
})

socket.on("modifica classe errore", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === data.nome)
  element.querySelector(".input-nome-classe").disabled = false
  element.querySelector(".input-aula").disabled = false

  if (data.nome_classe == "") {
    notyf.error("Errore nell'inserimento della classe: " + data.error)
  } else {
    notyf.error("Errore nella modifica della classe: " + data.error)
  }
})

socket.on("elimina classe successo", (nome_classe) => {
  let index = classi.findIndex(classe => classe[0] === nome_classe)
  if (index == -1) return;
  classi.splice(index, 1)

  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === nome_classe)
  element.remove()

  notyf.success("Classe eliminata con successo")
})

socket.on("elimina classe errore", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === data.nome_classe)
  element.querySelector(".input-nome-classe").disabled = false
  element.querySelector(".input-aula").disabled = false

  if (data.nome_classe == "") {
    notyf.error("Errore nell'eliminazione della classe: " + data.error)
  } else {
    notyf.error("Errore nella eliminazione della classe: " + data.error)
  }
})