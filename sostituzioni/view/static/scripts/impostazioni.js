const pulsante_applica = document.getElementById("applica");

function mostra_pulsante_applica() {
    pulsante_applica.disabled = false;
}

function applica() {

    // Trova tutti gli le opzioni cercando per classe
    let opzioni = document.getElementsByClassName("opzione");
    // Da mandare al server, {id_opzione: valore, "id2": ["12", "px"]} 
    let dati = {};

    for (let i = 0; i < opzioni.length; i++) {
        if (opzioni[i].classList.contains("opzione_selezione")) {
            // Se l'opzione è un dropdown

            let select = opzioni[i].getElementsByTagName("select")[0];
            dati[opzioni[i].id] = select.selectedIndex;

        } else if (opzioni[i].classList.contains("opzione_colore")) {
            // Se l'opzione è un colorpicker

        } else {
            // Se l'opzione è un input

            // Trova tutti gli elementi input
            let input = opzioni[i].getElementsByTagName("input");

            // Se ce n'è solo uno, non c'è bisogno di creare una lista
            if (input.length == 1) {
                dati[opzioni[i].id] = getValue(input[0]);

            } else {
                // Altrimenti, aggiungi ogni input
                let valori = []
                for (let j = 0; j < input.length; i++) {
                    valori.push(getValue(input[j]));
                }

                dati[opzioni[i].id] = valori;
            }

        }
    }

    socket.emit("applica", dati);
}


function getValue(input) {
    if (input.type == "number") {
        return input.valueAsNumber;

    } else if (input.type == "checkbox") {
        return input.checked;

    } else if (input.type == "text") {
        return input.value;

    }
}

socket.on("applica", (data) => {
    if (data == "ok") {
        location.reload();
    };
})