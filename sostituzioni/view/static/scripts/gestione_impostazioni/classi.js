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
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato hidden">check_circle</button>
</div>`

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

function modificato(nome_classe) {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === nome_classe)

  element.querySelector(".pulsante-elimina-dato").classList.add("hidden")
  element.querySelector(".pulsante-conferma-modifiche-dato").classList.remove("hidden")
}

function ui_conferma_modifiche(nome_classe) {
  const element = Array.from(document.querySelectorAll(".opzione-classe"))
    .find(element => element.dataset.nome_classe === nome_classe)
  let new_nome_classe = element.querySelector(".input-nome-classe").value
  let new_aula = element.querySelector(".input-aula").value

  new_nome_classe = new_nome_classe.trim()
  new_aula = new_aula.trim()

  if (new_nome_classe === "") {
    notyf.error("Inserire una classe valida")
    return
  }

  if (new_aula === "") {
    notyf.error("Inserire un'aula valida")
    return
  }

  // nessuna modifica
  if (new_nome_classe === classe[0] && new_aula === classe[1][0]) {
    element.querySelector(".pulsante-elimina-dato").classList.remove("hidden")
    element.querySelector(".pulsante-conferma-modifiche-dato").classList.add("hidden")
    element.querySelector(".input-nome-classe").value = classe[0]
    return
  }

  element.querySelector(".input-nome-classe").disabled = true
  element.querySelector(".input-aula").disabled = true

  socket.emit("modifica classe", { nome_classe: classe[0], new_nome_classe: new_nome_classe, new_aula: new_aula })
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


socket.on("modifica aula successo", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-aula"))
    .find(element => element.dataset.numero_aula === data.numero_aula)
  element.querySelector(".input-numero-aula").disabled = false
  element.querySelector(".input-piano-aula").disabled = false

  const aula = [data.new_numero_aula, data.new_piano_aula]

  element.replaceWith(crea_elemento(aula))

  if (data.numero_aula == "") {
    // nuova aula
    aule.push(aula)
  } else {
    // modifica aula esistente
    let index = aule.findIndex(aula => aula[0] === data.numero_aula)
    aule[index] = aula
  }

  if (data.numero_aula == "") {
    notyf.success("Aula inserita con successo")
  } else {
    notyf.success("Aula modificata con successo")
  }
})

socket.on("modifica aula errore", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-aula"))
    .find(element => element.dataset.numero_aula === data.numero_aula)
  element.querySelector(".input-numero-aula").disabled = false
  element.querySelector(".input-piano-aula").disabled = false

  if (data.numero_aula == "") {
    notyf.error("Errore nell'inserimento dell'aula: " + data.error)
  } else {
    notyf.error("Errore nella modifica dell'aula: " + data.error)
  }
})

socket.on("elimina aula successo", (numero_aula) => {
  let index = aule.findIndex(aula => aula[0] === numero_aula)
  if (index == -1) return;
  aule.splice(index, 1)

  const element = Array.from(document.querySelectorAll(".opzione-aula"))
    .find(element => element.dataset.numero_aula === numero_aula)
  element.remove()

  notyf.success("Aula eliminata con successo")
})
