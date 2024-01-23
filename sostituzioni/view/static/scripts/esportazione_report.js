const ui_pulsante_esporta_report = document.getElementById("pulsante-esporta-sostituzioni")

ui_pulsante_esporta_report.onclick = () => {
    socket.emit("esporta sostituzioni")
}