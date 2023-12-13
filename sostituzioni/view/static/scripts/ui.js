const pulsante_logout = document.getElementById('pulsante-logout')

function ui_refresh_sostituzioni() {
    ui_sostituzioni_container.innerHTML = ""
    ui_sostituzioni_messaggio_informativo.innerHTML = "<span>Caricamento...</span>"
    ui_sostituzioni_messaggio_informativo.style.display = "flex"

    s_richiedi_sostituzioni()
}

//fun, todo remove
pulsante_logout.onclick = (e) => {
    let fun = document.getElementById('fun')
    fun.style.top = "-70vh"
    fun.style.right = "-70vw"
    fun.style.height = "200vh"
    fun.style.width = "200vw"

    e.preventDefault()

    setTimeout(() => { location.href = pulsante_logout.href }, 170)
}