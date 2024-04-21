function compara_ora_inizio(a, b) {
    if (a.ora_inizio === null && b.ora_inizio === null) {
        return 0
    } else if (a.ora_inizio === null) {
        return 1
    } else if (b.ora_inizio === null) {
        return -1
    } else {
        return a.ora_inizio.localeCompare(b.ora_inizio)
    }
}

function compara_ora_predefinita(a, b) {
    if (a.ora_predefinita === null && b.ora_predefinita === null) {
        return compara_ora_inizio(a, b)
    } else if (a.ora_predefinita === null) {
        return 1
    } else if (b.ora_predefinita === null) {
        return -1
    } else if (typeof a.ora_predefinita === "string" || typeof b.ora_predefinita === "string") {
        return b.ora_predefinita.localeCompare(a.ora_predefinita)
    } else {
        return b.ora_predefinita - a.ora_predefinita
    }
}

function compara_data(a, b) {
    if (a.data === null && b.data === null) {
        return compara_ora_predefinita(a, b)
    } else if (a.data === null) {
        return 1
    } else if (b.data === null) {
        return -1
    } else {
        return a.data - b.data
    }
}

function compara_classe(a, b) {
    if (a.nome_classe === null && b.nome_classe === null) {
        return 0
    } else if (a.nome_classe === null) {
        return 1
    } else if (b.nome_classe === null) {
        return -1
    } else {
        return b.nome_classe.localeCompare(a.nome_classe)
    }
}

function compara_aula(a, b) {
    if (a.numero_aula === null && b.numero_aula === null) {
        return 0
    } else if (a.numero_aula === null) {
        return 1
    } else if (b.numero_aula === null) {
        return -1
    } else {
        return b.numero_aula.localeCompare(a.numero_aula)
    }
}

function compara_docente(a, b) {
    if (a.cognome_docente === null && b.cognome_docente === null) {
        return 0
    } else if (a.cognome_docente === null) {
        return 1
    } else if (b.cognome_docente === null) {
        return -1
    } else if (a.cognome_docente != b.cognome_docente) {
        return b.cognome_docente.localeCompare(a.cognome_docente)
    } else if (a.nome_docente != b.nome_docente) {
        return b.nome_docente.localeCompare(a.nome_docente)
    } else {
        return 0
    }
}
