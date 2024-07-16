const aula_template = `<div class="aula">
<input class="input-numero-aula" type="text" placeholder="Numero Aula" required minlength="1" maxlength="100" autocomplete="off" value="">
<div class="selezione-piano">
  <div class="selezione">
    <input type="text" class="input-piano selezione-input" placeholder="Piano" />
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

const ui_lista_aule = document.querySelector("#lista-aule")
let lista_selezioni_piano = []
let lista_tag_piani = new Set()

function crea_elemento(aula) {
  const element = document.createElement("div")
  element.classList.add("opzione-aula")
  element.dataset.numero_aula = aula[0]
  element.innerHTML = aula_template

  const input_numero_aula = element.querySelector(".input-numero-aula")
  input_numero_aula.value = aula[0]
  input_numero_aula.oninput = () => modificato(aula[0])
  const input_piano_aula = element.querySelector(".input-piano")
  // input_piano_aula.value = aula[1]
  input_piano_aula.oninput = () => modificato(aula[0])

  element.querySelector(".pulsante-elimina-dato").onclick = () => ui_elimina_aula(aula[0])
  element.querySelector(".pulsante-conferma-modifiche-dato").onclick = () => ui_conferma_modifiche(aula[0])

  return element
}

aule.sort((a, b) => {
  return a[0].localeCompare(b[0])
})

aule.forEach(aula => {
  ui_lista_aule.appendChild(crea_elemento(aula))
  lista_tag_piani.add(aula[1])
})
aule.forEach(aula => {
  const selezione_piano = new Selezione({ query: ".opzione-aula[data-numero_aula='" + aula[0] + "'] .selezione-piano", lista: [...lista_tag_piani] })
  selezione_piano.valore = aula[1]
  selezione_piano.callback = (valore) => {
    if (valore == aula[1]) return;
    modificato(aula[0])
  }
  lista_selezioni_piano.push(selezione_piano)
})

function modificato(numero_aula) {
  const element = Array.from(document.querySelectorAll(".opzione-aula"))
    .find(element => element.dataset.numero_aula === numero_aula)
  element.querySelector(".pulsante-elimina-dato").classList.add("hidden")
  element.querySelector(".pulsante-conferma-modifiche-dato").classList.remove("hidden")
}

function ui_conferma_modifiche(numero_aula) {
  const element = Array.from(document.querySelectorAll(".opzione-aula"))
    .find(element => element.dataset.numero_aula === numero_aula)
  let new_numero_aula = element.querySelector(".input-numero-aula").value
  let new_piano_aula = element.querySelector(".input-piano").value

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

  const aula = aule.find(aula => aula[0] === numero_aula)
  if (!aula) {
    aula
  }

  // nessuna modifica
  if (new_numero_aula === numero_aula && new_piano_aula === aule.find(aula => aula[0] === numero_aula)[1]) {
    element.querySelector(".pulsante-elimina-dato").classList.remove("hidden")
    element.querySelector(".pulsante-conferma-modifiche-dato").classList.add("hidden")
    element.querySelector(".input-numero-aula").value = numero_aula
    return
  }

  element.querySelector(".input-numero-aula").disabled = true
  element.querySelector(".input-piano").disabled = true

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

  const selezione_piano = new Selezione({ query: ".opzione-aula[data-numero_aula=''] .selezione-piano", lista: [...lista_tag_piani] })
  selezione_piano.callback = (valore) => {
    if (!valore) return;
    modificato("")
  }
  lista_selezioni_piano.push(selezione_piano)

  empty_element.querySelector(".input-numero-aula").focus()
}


//----------------------------------


socket.on("modifica aula successo", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-aula"))
    .find(element => element.dataset.numero_aula === data.numero_aula)
  element.querySelector(".input-numero-aula").disabled = false
  element.querySelector(".input-piano").disabled = false

  const aula = [data.new_numero_aula, data.new_piano_aula]
  const old_lista_tag_piani = new Set(lista_tag_piani)
  lista_tag_piani.add(data.new_piano_aula)
  if (lista_tag_piani.size > old_lista_tag_piani.size) {
    lista_selezioni_piano.forEach(selezione_piano => {
      selezione_piano.aggiorna([...lista_tag_piani])
    })
  }

  element.replaceWith(crea_elemento(aula))
  const selezione_piano = new Selezione({ query: ".opzione-aula[data-numero_aula='" + data.new_numero_aula + "'] .selezione-piano", lista: [...lista_tag_piani] })
  selezione_piano.valore = data.new_piano_aula
  selezione_piano.callback = (valore) => {
    if (valore == data.new_piano_aula) return;
    modificato(data.new_numero_aula)
  }

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
  element.querySelector(".input-piano").disabled = false

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
