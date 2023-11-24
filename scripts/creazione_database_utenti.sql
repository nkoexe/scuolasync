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

-- 

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
    email VARCHAR PRIMARY KEY,
    ruolo VARCHAR(50) NOT NULL REFERENCES ruolo(nome) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS accounting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_ora DATETIME NOT NULL,
    nome_utente VARCHAR NOT NULL,
    ruolo_utente VARCHAR(50) NOT NULL,
    descrizione VARCHAR NOT NULL,
    legame_utente VARCHAR(50) REFERENCES utente(email) ON DELETE SET NULL
);


------ Creazione Trigger ------

-- -- Copia dati nome e ruolo dall'utente che ha eseguito l'azione
-- CREATE TRIGGER IF NOT EXISTS after_insert_accounting AFTER INSERT
-- ON accounting
-- BEGIN
--     UPDATE accounting SET nome_utente = utente.email, ruolo_utente = utente.ruolo FROM utente WHERE accounting.rowid = NEW.rowid AND utente.email = NEW.legame_utente;
-- END;
