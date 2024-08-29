const nota_template = `<input class="input-testo-nota" type="text" placeholder="Testo della nota" required minlength="1" maxlength="100" autocomplete="off" value="">
<div class="operazioni-dato">
<button class="material-symbols-rounded pulsante-elimina-dato">delete</button>
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato">save</button>
</div>`

const ui_lista_note = document.querySelector("#lista-note")

function crea_elemento(testo) {
  const element = document.createElement("div")
  element.classList.add("opzione-nota")
  element.dataset.testo = testo
  element.innerHTML = nota_template.replaceAll("{testo}", testo)

  const input_testo = element.querySelector(".input-testo-nota")
  input_testo.value = testo
  input_testo.oninput = () => modificato(testo)

  element.querySelector(".pulsante-elimina-dato").onclick = () => ui_elimina_nota(testo)
  element.querySelector(".pulsante-conferma-modifiche-dato").onclick = () => ui_conferma_modifiche(testo)

  return element
}

note.sort((a, b) => {
  return a.localeCompare(b)
})

note.forEach(nota => {
  ui_lista_note.appendChild(crea_elemento(nota))
})

function modificato(testo) {
  const element = Array.from(document.querySelectorAll(".opzione-nota"))
    .find(element => element.dataset.testo === testo)
  element.classList.add("modificato")
}

function ui_conferma_modifiche(testo) {
  const element = Array.from(document.querySelectorAll(".opzione-nota"))
    .find(element => element.dataset.testo === testo)
  let new_testo = element.querySelector(".input-testo-nota").value

  new_testo = new_testo.trim()

  if (new_testo === "") {
    notyf.error("Inserire un testo valido")
    return
  }

  // nessuna modifica
  if (new_testo === testo) {
    element.classList.remove("modificato")
    element.querySelector(".input-testo-nota").value = testo
    return
  }

  element.querySelector(".input-testo-nota").disabled = true

  socket.emit("modifica nota", { testo: testo, new_testo: new_testo })
}

function ui_elimina_nota(testo) {
  if (testo == "") {
    const element = Array.from(document.querySelectorAll(".opzione-nota"))
      .find(element => element.dataset.testo === testo)
    element.remove()
    return
  }
  mostra_popup_conferma({ titolo: "Elimina Nota", descrizione: "Sei sicuro di voler eliminare la nota <strong>" + testo + "</strong>?", testo_pulsante_secondario: "Annulla", testo_pulsante_primario: "Elimina", callback: () => { elimina_nota(testo) } })
}

function elimina_nota(testo) {
  socket.emit("elimina nota", testo)
}

function nuova_nota() {
  if (document.querySelector('[data-testo=""]')) {
    document.querySelector(".input-testo-nota").focus()
    return
  }

  const empty_element = crea_elemento("")
  ui_lista_note.insertAdjacentElement("afterbegin", empty_element)
  empty_element.querySelector(".input-testo-nota").focus()
}


//----------------------------------


socket.on("modifica nota successo", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-nota"))
    .find(element => element.dataset.testo === data.testo)

  element.replaceWith(crea_elemento(data.new_testo))

  if (data.testo == "") {
    // nuovo nota
    note.push(data.new_testo)
  } else {
    // modifica nota esistente
    let index = note.findIndex(nota => nota === data.testo)
    note[index] = data.new_testo
  }

  if (data.testo == "") {
    notyf.success("Nota inserita con successo")
  } else {
    notyf.success("Nota modificata con successo")
  }
})

socket.on("modifica nota errore", (data) => {
  const element = Array.from(document.querySelectorAll(".opzione-nota"))
    .find(element => element.dataset.testo === data.testo)
  element.querySelector(".input-testo-nota").disabled = false

  if (data.testo == "") {
    notyf.error("Errore nell'inserimento della nota: " + data.error)
  } else {
    notyf.error("Errore nella modifica della nota: " + data.error)
  }
})

socket.on("elimina nota successo", (testo) => {
  let index = note.findIndex(nota => nota === testo)
  if (index == -1) return;
  note.splice(index, 1)

  const element = Array.from(document.querySelectorAll(".opzione-nota"))
    .find(element => element.dataset.testo === testo)
  element.remove()

  notyf.success("Nota eliminata con successo")
})

socket.on("elimina nota errore", (data) => {
  notyf.error("Errore nell'eliminazione della nota: " + data.error)
})
