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
    data DATE,
    note VARCHAR,
    ora_inizio TIME CHECK (length (ora_inizio) = 5),
    ora_fine TIME CHECK (length (ora_fine) = 5),
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
    data_ora_inizio DATETIME,
    data_ora_fine DATETIME
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
    data_ora_inizio DATETIME,
    data_ora_fine DATETIME
);

CREATE TABLE IF NOT EXISTS visualizzazione_mostra_notizia (
    nome_visualizzazione VARCHAR(50) NOT NULL REFERENCES visualizzazione(nome) ON UPDATE CASCADE,
    id_notizia INTEGER NOT NULL REFERENCES notizia(id) ON UPDATE CASCADE,

    PRIMARY KEY (nome_visualizzazione, id_notizia)
);

CREATE TABLE IF NOT EXISTS permesso (
    nome VARCHAR(50) PRIMARY KEY,
    descrizione VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS ruolo (
    nome VARCHAR(50) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS permesso_per_ruolo (
    nome_ruolo VARCHAR(50) NOT NULL REFERENCES ruolo(nome) ON UPDATE CASCADE,
    permesso_ruolo VARCHAR(50) NOT NULL REFERENCES permesso(nome) ON UPDATE CASCADE,

    PRIMARY KEY (nome_ruolo, permesso_ruolo)
);

CREATE TABLE IF NOT EXISTS utente (
    nome VARCHAR PRIMARY KEY,
    pwd VARCHAR NOT NULL,
    ruolo VARCHAR(50) NOT NULL REFERENCES ruolo(nome) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS accounting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_ora DATETIME NOT NULL,
    nome_utente VARCHAR NOT NULL,
    ruolo_utente VARCHAR(50) NOT NULL,
    descrizione VARCHAR NOT NULL,
    legame_utente VARCHAR(50) REFERENCES utente(nome) ON DELETE SET NULL
);


------ Creazione Trigger ------

-- -- Copia dati nome e ruolo dall'utente che ha eseguito l'azione
-- CREATE TRIGGER IF NOT EXISTS after_insert_accounting AFTER INSERT
-- ON accounting
-- BEGIN
--     UPDATE accounting SET nome_utente = utente.nome, ruolo_utente = utente.ruolo FROM utente WHERE accounting.rowid = NEW.rowid AND utente.nome = NEW.legame_utente;
-- END;

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


------ Inserimento Dati di Test ------

INSERT OR IGNORE INTO ora_predefinita
VALUES
    ('1', '07:50', '08:40'),
    ('2', '08:40', '09:30');
 
INSERT OR IGNORE INTO docente
VALUES
    ('Mario', 'Rossi', FALSE),
    ('Giulia', 'Bianchi', FALSE);

INSERT OR IGNORE INTO aula
VALUES
    ('100', '1', FALSE),
    ('200', '1', FALSE);

INSERT OR IGNORE INTO classe
VALUES
    ('linguistico', FALSE),
    ('classico', FALSE);

INSERT OR IGNORE INTO sostituzione (pubblicato, cancellato, data, ora_inizio, ora_fine, numero_aula, nome_classe, nome_docente, cognome_docente)
VALUES
    (TRUE, FALSE, '10-10-2010', '07:50', '09:30', '200', 'linguistico', 'Mario', 'Rossi'),
    (TRUE, FALSE, '10-10-2010', '07:34', '08:25', '100', 'classico', 'Mario', 'Rossi'),
    (TRUE, FALSE, '10-10-2010', '07:50', '08:40', '200', 'linguistico', 'Mario', 'Rossi'),
    (TRUE, FALSE, '10-10-2010', '08:40', '09:30', '100', 'classico', 'Giulia', 'Bianchi');

INSERT OR IGNORE INTO ruolo (nome)
VALUES
    ('admin'),
    ('editor');

INSERT OR IGNORE INTO utente (nome, pwd, ruolo)
VALUES
    ('u1', 'pwd1', 'admin'),
    ('u2', 'pwd2', 'editor');

INSERT OR IGNORE INTO accounting (data_ora, nome_utente, ruolo_utente, descrizione, legame_utente)
VALUES
    ('10:00:00', '', '', 'descrizione azione', 'u1'),
    ('10:00:01', '', '', 'descrizione azione', 'u2');


SELECT * FROM sostituzione;
