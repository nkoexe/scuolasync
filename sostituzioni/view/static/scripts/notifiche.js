const ui_errore_notifiche = document.querySelector("#errore-notifiche")
const ui_pulsante_notifiche = document.querySelector("#pulsante-notifiche")
const ui_pulsante_gestione_notifiche = document.querySelector("#pulsante-gestione-notifiche")

const ui_container_notifiche = new Popup({ query: "#container-notifiche" })
const ui_selezione_docente_notifiche = new Selezione({ query: "#selezione-docente-notifiche", filtra_lista: prendi_cognome_nome, autocomplete: true })


ui_pulsante_notifiche.onclick = (e) => {
  e.stopPropagation();
  ui_container_notifiche.toggle()
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function setup_notifications() {
  if (!("Notification" in window)) {
    ui_errore_notifiche.innerHTML = "Il tuo browser non supporta le notifiche.";
    return;
  }

  Notification.requestPermission().then((result) => {
    if (result !== 'granted') {
      ui_errore_notifiche.innerHTML = "Permesso per le notifiche mancante.";
      return;
    }
  });

  navigator.serviceWorker.ready.then((registration) => {
    const subscribeOptions = {
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(
        'BKBRjX_4TBOtWNrNKK2PgFF9X5rwQtis3NQC1eMn4xkaUVAjPk_O0QTq4YMKyMlf2WC740BO2KuEvx3gPU2IfEQ'
      )
    };

    registration.pushManager.subscribe(subscribeOptions).then((pushSubscription) => {
      socket.emit('iscrizione notifiche', pushSubscription)
    });
  });

  ui_errore_notifiche.innerHTML = "Notifiche abilitate.";
  ui_pulsante_gestione_notifiche.innerHTML = "Disattiva notifiche";
}

ui_pulsante_gestione_notifiche.onclick = () => {
  setup_notifications()
}

