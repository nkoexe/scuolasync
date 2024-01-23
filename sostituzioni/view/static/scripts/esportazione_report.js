const ui_pulsante_esporta_report = document.getElementById("pulsante-esporta-sostituzioni")
const ui_popup_esporta_report = document.getElementById("popup-esporta-sostituzioni")
const ui_radio_mese_esporta_report = document.getElementById("radio-filtro-mese-esporta-sostituzioni")
const ui_radio_data_esporta_report = document.getElementById("radio-filtro-data-esporta-sostituzioni")
const ui_filtro_mese_esporta_report = document.getElementById("filtro-mese-esporta-sostituzioni")
const ui_filtro_data_inizio_esporta_report = document.getElementById("filtro-data-inizio-esporta-sostituzioni")
const ui_filtro_data_fine_esporta_report = document.getElementById("filtro-data-fine-esporta-sostituzioni")
const ui_filtro_pubblicati_esporta_report = document.getElementById("filtro-pubblicati-esporta-sostituzioni")
const ui_filtro_cancellati_esporta_report = document.getElementById("filtro-cancellati-esporta-sostituzioni")
const ui_select_formato_report = document.getElementById("select-sostituzione-formato")
const ui_pulsante_scarica_report = document.getElementById("pulsante-scarica-esporta-sostituzioni")


ui_pulsante_esporta_report.onclick = () => {
    ui_popup_esporta_report.style.display = "flex"
    setTimeout(() => {
        ui_popup_esporta_report.style.opacity = "1"
        ui_popup_esporta_report.style.top = "100%"
    }, 1)
    ui_popup_esporta_report.focus()
}


ui_popup_esporta_report.onblur = (e) => {
    if (e.relatedTarget && e.relatedTarget.closest("#popup-esporta-sostituzioni")) {
        return
    }

    ui_popup_esporta_report.style.opacity = "0"
    ui_popup_esporta_report.style.top = "80%"
    setTimeout(() => {
        ui_popup_esporta_report.style.display = "none"
    }, 200)
}

ui_filtro_mese_esporta_report.onclick = () => {
    ui_radio_mese_esporta_report.checked = true
    ui_radio_data_esporta_report.checked = false
}

let focus_data_esporta_report = () => {
    ui_radio_mese_esporta_report.checked = false
    ui_radio_data_esporta_report.checked = true
}
ui_filtro_data_inizio_esporta_report.onclick = focus_data_esporta_report
ui_filtro_data_inizio_esporta_report.onchange = focus_data_esporta_report
ui_filtro_data_fine_esporta_report.onclick = focus_data_esporta_report
ui_filtro_data_fine_esporta_report.onchange = focus_data_esporta_report


ui_pulsante_scarica_report.onclick = () => {
    let data_inizio
    let data_fine

    if (ui_radio_mese_esporta_report.checked) {
        const mese = parseInt(ui_filtro_mese_esporta_report.value)
        const now = new Date()
        const mese_corrente = now.getMonth() + 1
        let anno = now.getFullYear()
        if (mese > 7 && mese_corrente <= 7) {
            // Anno scolastico precedente
            anno -= 1
        } else if (mese <= 7 && mese_corrente > 7) {
            // Anno scolastico successivo
            anno += 1
        }

        data_inizio = new Date(anno, mese, 1).getTime() / 1000
        data_fine = new Date(anno, mese + 1, 0, 23, 59, 59).getTime() / 1000
    } else {
        data_inizio = fix_date_from_input(ui_filtro_data_inizio_esporta_report.valueAsNumber) / 1000
        data_fine = fix_date_from_input(ui_filtro_data_fine_esporta_report.valueAsNumber) / 1000
    }

    const pubblicati = ui_filtro_pubblicati_esporta_report.checked
    const cancellati = ui_filtro_cancellati_esporta_report.checked
    const formato = ui_select_formato_report.value


    socket.emit("esporta sostituzioni", {
        data_inizio,
        data_fine,
        pubblicati,
        cancellati,
        formato,
    })
}