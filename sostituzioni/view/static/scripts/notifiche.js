const ui_errore_notifiche = document.querySelector("#errore-notifiche")
const ui_pulsante_notifiche = document.querySelector("#pulsante-notifiche")
const ui_pulsante_impostazioni_notifiche = document.querySelector("#pulsante-impostazioni-notifiche")
const ui_pulsante_gestione_notifiche = document.querySelector("#pulsante-gestione-notifiche")

const ui_container_notifiche = new Popup({ query: "#container-notifiche" })
const ui_impostazioni_notifiche = new Popup({ query: "#impostazioni-notifiche" })


ui_pulsante_notifiche.onclick = (e) => {
  ui_container_notifiche.toggle()
}

ui_pulsante_impostazioni_notifiche.onclick = (e) => {
  e.stopPropagation();
  ui_impostazioni_notifiche.toggle()
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
    socket.emit('get vapid public key', {}, (vapidPublicKey) => {
      if (!vapidPublicKey) {
        ui_errore_notifiche.innerHTML = "Notifiche non supportate.";
        return;
      }

      console.log("Vapid public key: ", vapidPublicKey);

      const subscribeOptions = {
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
      };

      registration.pushManager.subscribe(subscribeOptions).then((pushSubscription) => {
        socket.emit('iscrizione notifiche', pushSubscription)
      });

    });
  });

  ui_errore_notifiche.innerHTML = "Notifiche abilitate.";
  ui_pulsante_gestione_notifiche.innerHTML = "Disattiva notifiche";
}

ui_pulsante_gestione_notifiche.onclick = () => {
  setup_notifications()
}

