const popup_conferma = document.getElementById("popup-conferma-container");
const popup_conferma_titolo = document.getElementById("popup-conferma-titolo");
const popup_conferma_descrizione = document.getElementById("popup-conferma-descrizione");
const popup_conferma_pulsante_secondario = document.getElementById("popup-conferma-pulsante-secondario");
const popup_conferma_pulsante_primario = document.getElementById("popup-conferma-pulsante-primario");

function mostra_popup_conferma({ titolo = "", descrizione = "", testo_pulsante_secondario = "Annulla", testo_pulsante_primario = "Conferma", callback = () => { } }) {
  popup_conferma_titolo.innerText = titolo;
  popup_conferma_descrizione.innerHTML = descrizione;
  popup_conferma_pulsante_secondario.innerText = testo_pulsante_secondario;
  popup_conferma_pulsante_primario.innerText = testo_pulsante_primario;
  popup_conferma_pulsante_primario.onclick = () => {
    callback();
    nascondi_popup_conferma();
  };
  popup_conferma_pulsante_secondario.onclick = nascondi_popup_conferma;
  popup_conferma.classList.remove("hidden");
}

function nascondi_popup_conferma() {
  popup_conferma.classList.add("hidden");
}