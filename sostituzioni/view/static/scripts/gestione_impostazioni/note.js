const nota_template = `<div class="opzione-nota" data-testo="{testo}">
<input class="input-testo-nota" type="text" placeholder="Testo della nota" required minlength="1" maxlength="100" autocomplete="off" value="{testo}" oninput="modificato('{testo}')">
<div class="operazioni-dato">
<button class="material-symbols-rounded pulsante-elimina-dato" onclick="ui_elimina_nota('{testo}')">delete</button>
<button class="material-symbols-rounded pulsante-conferma-modifiche-dato hidden" onclick="ui_conferma_modifiche('{testo}')">check_circle</button>
</div>
</div>`

const ui_lista_note = document.querySelector("#lista-note")

note.sort((a, b) => {
  return a.localeCompare(b)
})

note.forEach(nota => {
  ui_lista_note.innerHTML += nota_template.replaceAll("{testo}", nota)
})

function modificato(testo) {
  let element = document.querySelector(`[data-testo="${testo}"]`)
  element.querySelector(".pulsante-elimina-dato").classList.add("hidden")
  element.querySelector(".pulsante-conferma-modifiche-dato").classList.remove("hidden")
}

function ui_conferma_modifiche(testo) {
  let element = document.querySelector(`[data-testo="${testo}"]`)
  let new_testo = element.querySelector(".input-testo-nota").value

  new_testo = new_testo.replace(/\s/g, "")

  if (new_testo === "") {
    notyf.error("Inserire un testo valido")
    return
  }

  // nessuna modifica
  if (new_testo === testo) {
    element.querySelector(".pulsante-elimina-dato").classList.remove("hidden")
    element.querySelector(".pulsante-conferma-modifiche-dato").classList.add("hidden")
    element.querySelector(".input-testo-nota").value = testo
    return
  }

  element.querySelector(".input-testo-nota").disabled = true

  socket.emit("modifica nota", { testo: testo, new_testo: new_testo })
}

function ui_elimina_nota(testo) {
  if (testo == "") {
    let element = document.querySelector(`[data-testo="${testo}"]`)
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

  ui_lista_note.innerHTML = nota_template.replaceAll("{testo}", "") + ui_lista_note.innerHTML;

  document.querySelector(".input-testo-nota").focus()
}


//----------------------------------


socket.on("modifica nota successo", (data) => {
  let element = document.querySelector(`[data-testo="${data.testo}"]`)
  let new_element = nota_template.replaceAll("{testo}", data.new_testo)

  element.outerHTML = new_element

  if (data.testo == "") {
    // nuovo nota
    note.push([data.new_testo])
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
  let element = document.querySelector(`[data-testo="${data.testo}"]`)
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

  let element = document.querySelector(`[data-testo="${testo}"]`)
  element.remove()

  notyf.success("Nota eliminata con successo")
})

socket.on("elimina nota errore", (data) => {
  notyf.error("Errore nell'eliminazione della nota: " + data.error)
})
