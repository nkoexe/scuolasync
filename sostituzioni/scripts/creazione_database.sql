/*
Copyright (c) 2022 Niccolò Ragazzi
Supervisor: Chiara Gandolfi
For: I.I.S.S. "Gandhi" - Merano (BZ)


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

-- DA METTERE ALL'APERTURA DI OGNI SESSIONE
PRAGMA foreign_keys = ON;


------ Creazione Tabelle ------

CREATE TABLE IF NOT EXISTS nota_standard (
    testo VARCHAR PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS ora_predefinita (
    numero INTEGER PRIMARY KEY,
    ora_inizio_default TIME NOT NULL UNIQUE CHECK (length (ora_inizio_default) = 5),
    ora_fine_default TIME NOT NULL UNIQUE CHECK (length (ora_fine_default) = 5)
);

CREATE TABLE IF NOT EXISTS docente (
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    cancellato BOOLEAN NOT NULL,

    PRIMARY KEY (nome, cognome)
);

CREATE TABLE IF NOT EXISTS aula (
    numero VARCHAR(20) PRIMARY KEY,
    piano VARCHAR(20) NOT NULL,
    cancellato BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS classe (
    nome VARCHAR(20) PRIMARY KEY,
    cancellato BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS aula_ospita_classe (
    numero_aula VARCHAR(20) NOT NULL REFERENCES aula(numero) ON UPDATE CASCADE,
    nome_classe VARCHAR(20) NOT NULL REFERENCES classe(nome) ON UPDATE CASCADE,
    predefinito BOOLEAN NOT NULL,

    PRIMARY KEY (numero_aula, nome_classe)
);

CREATE TABLE IF NOT EXISTS visualizzazione (
    nome VARCHAR(50) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS sostituzione (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pubblicato BOOLEAN NOT NULL,
    cancellato BOOLEAN NOT NULL,
    data INTEGER,
    note VARCHAR,
    ora_inizio VARCHAR(5) CHECK (length (ora_inizio) = 5),
    ora_fine VARCHAR(5) CHECK (length (ora_fine) = 5),
    numero_ora_predefinita INTEGER REFERENCES ora_predefinita(numero) ON UPDATE SET NULL,
    numero_aula VARCHAR(20) NOT NULL REFERENCES aula(numero) ON UPDATE CASCADE,
    nome_classe VARCHAR(20) NOT NULL REFERENCES classe(nome) ON UPDATE CASCADE,
    nome_docente VARCHAR(50),
    cognome_docente VARCHAR(50),

    FOREIGN KEY (nome_docente, cognome_docente) REFERENCES docente(nome, cognome) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS visualizzazione_mostra_sostituzione (
    nome_visualizzazione VARCHAR(50) NOT NULL REFERENCES visualizzazione(nome) ON UPDATE CASCADE,
    id_sostituzione INTEGER NOT NULL REFERENCES sostituzione(id) ON UPDATE CASCADE,

    PRIMARY KEY (nome_visualizzazione, id_sostituzione)
);

CREATE TABLE IF NOT EXISTS evento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urgente BOOLEAN NOT NULL,
    cancellato BOOLEAN NOT NULL,
    testo VARCHAR,
    data_ora_inizio INTEGER,
    data_ora_fine INTEGER
);

CREATE TABLE IF NOT EXISTS visualizzazione_mostra_evento (
    nome_visualizzazione VARCHAR(50) NOT NULL REFERENCES visualizzazione(nome) ON UPDATE CASCADE,
    id_evento INTEGER NOT NULL REFERENCES evento(id) ON UPDATE CASCADE,
 
    PRIMARY KEY (nome_visualizzazione, id_evento)
);

CREATE TABLE IF NOT EXISTS notizia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cancellato BOOLEAN NOT NULL,
    testo VARCHAR,
    data_ora_inizio INTEGER,
    data_ora_fine INTEGER
);

CREATE TABLE IF NOT EXISTS visualizzazione_mostra_notizia (
    nome_visualizzazione VARCHAR(50) NOT NULL REFERENCES visualizzazione(nome) ON UPDATE CASCADE,
    id_notizia INTEGER NOT NULL REFERENCES notizia(id) ON UPDATE CASCADE,

    PRIMARY KEY (nome_visualizzazione, id_notizia)
);

------ Creazione Trigger ------

-- -- Inserimento collegamento con ora predefinita se gli orari combaciano
-- CREATE TRIGGER IF NOT EXISTS after_insert_sostituzione AFTER INSERT
-- ON sostituzione
-- WHEN (NEW.ora_inizio, NEW.ora_fine) IN (SELECT ora_inizio_default, ora_fine_default FROM ora_predefinita)
-- BEGIN
--     UPDATE sostituzione SET numero_ora_predefinita = ora_predefinita.numero FROM ora_predefinita WHERE sostituzione.rowid = NEW.rowid AND NEW.ora_inizio = ora_predefinita.ora_inizio_default AND NEW.ora_fine = ora_predefinita.ora_fine_default;
-- END;

-- -- Stesso collegamento con ora predefinita dopo l'aggiornamento
-- CREATE TRIGGER IF NOT EXISTS after_insert_sostituzione AFTER UPDATE
-- ON sostituzione
-- WHEN (NEW.ora_inizio, NEW.ora_fine) IN (SELECT ora_inizio_default, ora_fine_default FROM ora_predefinita)
-- BEGIN
--     UPDATE sostituzione SET numero_ora_predefinita = ora_predefinita.numero FROM ora_predefinita WHERE sostituzione.rowid = NEW.rowid AND NEW.ora_inizio = ora_predefinita.ora_inizio_default AND NEW.ora_fine = ora_predefinita.ora_fine_default;
-- END;

