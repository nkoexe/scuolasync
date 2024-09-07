const socket = io("/impostazioni");

const ui_main_frame = document.querySelector("#main-frame")
const pulsante_applica = document.querySelector('#pulsante-applica');

let modifiche = []

let sezioni = document.getElementsByClassName('sezione-header');

for (let index = 0; index < sezioni.length; index++) {
  sezioni[index].addEventListener('click', () => {
    sezioni[index].classList.toggle('expanded');

    let listaopzioni = sezioni[index].nextElementSibling;
    if (listaopzioni.style.maxHeight) {
      listaopzioni.style.maxHeight = null;
    } else {
      listaopzioni.style.maxHeight = listaopzioni.scrollHeight + 'px';
    }
  });
}


//////////////////////////////


function elimina_file(id) {
  let file_container = document.getElementById(id);
  file_container.querySelector(".img-container").classList.add("hidden");
  file_container.querySelector(".opzione-file-dropzone").classList.remove("hidden");

  let file_input = file_container.querySelector("#" + id + "-filepicker");
  file_input.value = "";

  file_input.onchange = () => {
    file_container.classList.add("loading");

    let reader = new FileReader();
    reader.readAsArrayBuffer(file_input.files[0]);
    reader.onload = () => {
      socket.emit("carica file", { "id": id, "name": file_input.files[0].name, "mime": file_input.files[0].type, "data": reader.result });
    };
  }
}

for (element of document.querySelectorAll(".opzione-file-dropzone")) {
  element.ondrop = (e) => {
    e.preventDefault();
    element.classList.remove("filehover")

    let input = element.querySelector("input")
    input.files = e.dataTransfer.files
    input.onchange()
  }

  element.ondragover = (e) => {
    e.preventDefault();
  }

  element.ondragenter = (e) => {
    e.preventDefault();
    element.classList.add("filehover")
  }

  element.ondragleave = (e) => {
    element.classList.remove("filehover")
  }
}


function modificato(id) {
  if (!modifiche.includes(id)) {
    modifiche.push(id);
    mostra_pulsante_applica();
  }
}

function mostra_pulsante_applica() {
  pulsante_applica.disabled = false;
}

function applica() {
  // Da mandare al server, {id_opzione: valore, "id2": ["12", "px"]} 
  let dati = {};

  modifiche.forEach(element => {

    if (element.classList.contains("opzione-testo")) {
      // Se l'opzione è un testo

      let testo = element.getElementsByTagName("input")[0];
      dati[element.id] = testo.value;

    } else if (element.classList.contains("opzione-numero")) {
      // Se l'opzione è un numero

      let numero = element.getElementsByTagName("input")[0];
      dati[element.id] = numero.valueAsNumber;

    } else if (element.classList.contains("opzione-numero-unita")) {
      // Se l'opzione è un numero con unità

      let valore = element.getElementsByTagName("input")[0];
      let unita = element.getElementsByTagName("select")[0];
      dati[element.id] = [valore.valueAsNumber, unita.selectedIndex]

    } else if (element.classList.contains("opzione-booleano")) {
      // Se l'opzione è un checkbox

      let checkbox = element.getElementsByTagName("input")[0];
      dati[element.id] = checkbox.checked;

    }
    else if (element.classList.contains("opzione-selezione")) {
      // Se l'opzione è un dropdown

      let select = element.getElementsByTagName("select")[0];
      dati[element.id] = select.selectedIndex;

    } else if (element.classList.contains("opzione-colore")) {
      // Se l'opzione è un colorpicker

    } else if (element.classList.contains("opzione-percorso")) {
      // Se l'opzione è un percorso

      let radice = element.getElementsByTagName("select")[0];
      let percorso = element.getElementsByTagName("input")[0];
      dati[element.id] = [radice.selectedIndex, percorso.value]

    } else if (element.classList.contains("opzione-file")) {
      // Se l'opzione è un file

      let file = element.getElementsByTagName("input")[0];
      dati[element.id] = file.files[0];
    }
  })

  socket.emit("applica impostazioni", dati);
}

socket.on("applica impostazioni errore", (errore) => {
  alert(errore);
})

socket.on("applica impostazioni successo", (data) => {
  location.reload();
})

socket.on("carica file successo", (data) => {
  let file_container = document.getElementById(data.id);
  file_container.classList.remove("loading");
  file_container.querySelector(".opzione-file-dropzone").classList.add("hidden");
  file_container.querySelector(".img-container").classList.remove("hidden");
  file_container.querySelector(".img-container").querySelector("img").src = data.path;

  if (data.id == "schoolmainlogo") {
    notyf.success("Logo aggiornato con successo");
  }
})

socket.on("carica file errore", (errore) => {
  alert(errore);
})