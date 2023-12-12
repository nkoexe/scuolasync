function ui_refresh_sostituzioni() {
    ui_sostituzioni_container.innerHTML = ""
    ui_sostituzioni_messaggio_informativo.innerHTML = "<span>Caricamento...</span>"
    ui_sostituzioni_messaggio_informativo.style.display = "flex"

    s_richiedi_sostituzioni()
}

//fun, todo remove
document.getElementById('header-pulsanti').children[1].onclick = () => {
    let fun = document.getElementById('fun')
    fun.style.top = "-70vh"
    fun.style.right = "-70vw"
    fun.style.height = "200vh"
    fun.style.width = "200vw"

    setTimeout(() => { location.href = "/logout" }, 300)
}