const ora_template = `<input class="input-numero-ora" type="text" placeholder="Numero dell'ora predefinita" required minlength="1" maxlength="100" autocomplete="off" value="">
<div class="orario">
<input class="input-ora-inizio" type="time" required minlength="1" maxlength="100" autocomplete="off" value="">
<span class="separator"><span>-</span></span>
<input class="input-ora-fine" type="time" required minlength="1" maxlength="100" autocomplete="off" value="">
</div>
<div class="operazioni-dato">
<button class="material-symbols-rounded pulsante-elimina-dato">delete</button>
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato hidden">check_circle</button>
</div>`

const ui_lista_ore = document.querySelector("#lista-ore")

function crea_elemento(ora) {
  const element = document.createElement("div")
  element.classList.add("opzione-ora")
  element.dataset.numero = ora[0.]
  element.innerHTML = ora_template

  const input_ora = element.querySelector(".input-numero-ora")
  input_ora.value = ora[0]
  input_ora.oninput = () => modificato(ora)

  const input_ora_inizio = element.querySelector(".input-ora-inizio")
  input_ora_inizio.value = ora[1][0]
  input_ora_inizio.oninput = () => modificato(ora)

  const input_ora_fine = element.querySelector(".input-ora-fine")
  input_ora_fine.value = ora[1][1]
  input_ora_fine.oninput = () => modificato(ora)

  element.querySelector(".pulsante-elimina-dato").onclick = () => ui_elimina_ora(ora)
  element.querySelector(".pulsante-conferma-modifiche-dato").onclick = () => ui_conferma_modifiche(ora)

  return element
}

ore.sort((a, b) => {
  return a[0].localeCompare(b[0])
})

ore.forEach(nota => {
  ui_lista_ore.appendChild(crea_elemento(nota))
})

function modificato(ora) {
  const element = Array.from(document.querySelectorAll(".opzione-ora"))
    .find(element => element.dataset.numero === ora[0])
  element.querySelector(".pulsante-elimina-dato").classList.add("hidden")
  element.querySelector(".pulsante-conferma-modifiche-dato").classList.remove("hidden")
}

function ui_conferma_modifiche(ora) {
  const element = Array.from(document.querySelectorAll(".opzione-ora"))
    .find(element => element.dataset.numero === ora[0])
  let new_ora = element.querySelector(".input-numero-ora").value
  let new_ora_inizio = element.querySelector(".input-ora-inizio").value
  let new_ora_fine = element.querySelector(".input-ora-fine").value

  new_ora = new_ora.trim()

  if (new_ora === "") {
    notyf.error("Inserire un numero o testo per l'ora.")
    return
  }

  // nessuna modifica
  if (new_ora === ora[0] && new_ora_inizio === ora[1][0] && new_ora_fine === ora[1][1]) {
    element.querySelector(".pulsante-elimina-dato").classList.remove("hidden")
    element.querySelector(".pulsante-conferma-modifiche-dato").classList.add("hidden")
    element.querySelector(".input-numero-ora").value = ora[0]
    return
  }

  element.querySelector(".input-numero-ora").disabled = true
  element.querySelector(".input-ora-inizio").disabled = true
  element.querySelector(".input-ora-fine").disabled = true

  socket.emit("modifica ora", { numero: ora[0], new_numero: new_ora, new_ora_inizio: new_ora_inizio, new_ora_fine: new_ora_fine })
}

function ui_elimina_ora(ora) {
  if (ora[0] == "") {
    const element = Array.from(document.querySelectorAll(".opzione-ora"))
      .find(element => element.dataset.numero === ora[0])
    element.remove()
    return
  }
  mostra_popup_conferma({ titolo: "Elimina Ora Predefinita", descrizione: "Sei sicuro di voler eliminare l'ora predefinita <strong>" + ora[0] + "</strong>?", testo_pulsante_secondario: "Annulla", testo_pulsante_primario: "Elimina", callback: () => { elimina_ora(ora) } })
}

function elimina_ora(ora) {
  socket.emit("elimina ora", ora[0])
}

function nuova_ora() {
  if (document.querySelector('[data-numero=""]')) {
    document.querySelector(".input-numero-ora").focus()
    return
  }

  const empty_element = crea_elemento(["", ["", ""]])
  ui_lista_ore.insertAdjacentElement("afterbegin", empty_element)
  empty_element.querySelector(".input-numero-ora").focus()
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
