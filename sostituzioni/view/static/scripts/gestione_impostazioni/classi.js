const classe_template = `<div class="classe">
<input class="input-nome-classe" type="text" placeholder="Nome della classe" required minlength="1" maxlength="100" autocomplete="off" value="">
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

  new_numero_aula = new_numero_aula.trim()
  new_piano_aula = new_piano_aula.trim()

  if (new_numero_aula === "") {
    notyf.error("Inserire un valido numero di aula")
    return
  }

  if (new_piano_aula === "") {
    notyf.error("Inserire un valido piano")
    return
  }

  // nessuna modifica
  if (new_numero_aula === numero_aula && new_piano_aula === aule.find(aula => aula[0] === numero_aula)[1]) {
    element.querySelector(".pulsante-elimina-dato").classList.remove("hidden")
    element.querySelector(".pulsante-conferma-modifiche-dato").classList.add("hidden")
    element.querySelector(".input-numero-aula").value = numero_aula
    return
  }

  element.querySelector(".input-numero-aula").disabled = true
  element.querySelector(".input-piano-aula").disabled = true

  socket.emit("modifica aula", { numero_aula: numero_aula, new_numero_aula: new_numero_aula, new_piano_aula: new_piano_aula })
}

function ui_elimina_aula(numero_aula) {
  if (numero_aula == "") {
    const element = document.querySelector(".opzione-aula[data-numero_aula='']")
    element.remove()
    return
  }

  mostra_popup_conferma({ titolo: "Elimina Aula", descrizione: "Sei sicuro di voler eliminare l'aula <strong>" + numero_aula + "</strong>?", numero_aula: numero_aula, callback: () => { elimina_aula(numero_aula) } })
}

function elimina_aula(numero_aula) {
  socket.emit("elimina aula", numero_aula)
}

function nuova_aula() {
  if (document.querySelector('[data-numero_aula=""]')) {
    document.querySelector(".input-numero-aula").focus()
    return
  }

  const empty_element = crea_elemento(["", ""])
  ui_lista_aule.insertAdjacentElement("afterbegin", empty_element)
  empty_element.querySelector(".input-numero-aula").focus()
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
