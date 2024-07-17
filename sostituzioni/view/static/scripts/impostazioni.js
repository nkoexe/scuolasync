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


// const docenti_filepicker = document.getElementById("import-docenti-filepicker")
// const docenti_selected_file_label = document.getElementById("import-docenti-selected-file-label")

// docenti_filepicker.onchange = () => {
//     if (docenti_filepicker.value == "") {
//         docenti_selected_file_label.innerHTML = ""
//     } else {
//         docenti_selected_file_label.innerHTML = docenti_filepicker.files[0].name
//     }
// }

// function importa_docenti() {
//     if (docenti_filepicker.files.length == 0) {
//         alert("Seleziona un file");
//     }

//     let file = docenti_filepicker.files[0]
//     let reader = new FileReader();
//     reader.readAsArrayBuffer(file);
//     reader.onload = () => {
//         socket.emit("importa docenti", reader.result);
//     }
// }


//////////////////////////////


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

window.addEventListener('pageswap', async (e) => {
  if (e.viewTransition) {
    const targetUrl = new URL(e.activation.entry.url);

    if (targetUrl.pathname.startsWith('/impostazioni')) {
      const element = document.querySelector('.link-gestione:focus');
      const elementicon = element.querySelector('.icon');
      const elementtext = element.querySelector('h2');

      element.style.viewTransitionName = 'gestione-dati';
      elementicon.style.viewTransitionName = 'gestione-dati-icon';
      elementtext.style.viewTransitionName = 'gestione-dati-text';

      // await e.viewTransition.finished;

      // element.style.viewTransitionName = '';
    }
  }
});
