/*
    This file is part of ScuolaSync.

    Copyright (C) 2022-present Niccolò Ragazzi <hi@njco.dev>
    Supervisor: Chiara Gandolfi
    For: I.I.S.S. "Gandhi" - Merano (BZ)

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
*/

-- DA METTERE ALL'APERTURA DI OGNI SESSIONE
PRAGMA foreign_keys = ON;


------ Creazione Tabelle ------

CREATE TABLE IF NOT EXISTS nota_standard (
    testo VARCHAR PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS ora_predefinita (
    numero VARCHAR(20) PRIMARY KEY,
    ora_inizio_default TIME NOT NULL CHECK (length (ora_inizio_default) = 5),
    ora_fine_default TIME NOT NULL CHECK (length (ora_fine_default) = 5)
);

CREATE TABLE IF NOT EXISTS docente (
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    cancellato BOOLEAN NOT NULL DEFAULT 0,

    PRIMARY KEY (nome, cognome)
);

CREATE TABLE IF NOT EXISTS aula (
    numero VARCHAR(30) PRIMARY KEY,
    piano VARCHAR(15) NOT NULL,
    cancellato BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS classe (
    nome VARCHAR(30) PRIMARY KEY,
    cancellato BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS aula_ospita_classe (
    numero_aula VARCHAR(30) NOT NULL REFERENCES aula(numero) ON UPDATE CASCADE,
    nome_classe VARCHAR(30) NOT NULL REFERENCES classe(nome) ON UPDATE CASCADE,
    predefinito BOOLEAN NOT NULL DEFAULT 0,

    PRIMARY KEY (numero_aula, nome_classe)
);

CREATE TABLE IF NOT EXISTS sostituzione (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pubblicato BOOLEAN NOT NULL DEFAULT 0,
    cancellato BOOLEAN NOT NULL DEFAULT 0,
    data INTEGER,
    note VARCHAR,
    ora_inizio VARCHAR(5),
    ora_fine VARCHAR(5),
    numero_ora_predefinita VARCHAR(20) REFERENCES ora_predefinita(numero) ON UPDATE SET NULL,
    numero_aula VARCHAR(30) REFERENCES aula(numero) ON UPDATE CASCADE,
    nome_classe VARCHAR(30) REFERENCES classe(nome) ON UPDATE CASCADE,
    nome_docente VARCHAR(50),
    cognome_docente VARCHAR(50),

    FOREIGN KEY (nome_docente, cognome_docente) REFERENCES docente(nome, cognome) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS archivio_sostituzioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pubblicato BOOLEAN NOT NULL DEFAULT 0,
    cancellato BOOLEAN NOT NULL DEFAULT 0,
    data INTEGER,
    note VARCHAR,
    ora_inizio VARCHAR(5),
    ora_fine VARCHAR(5),
    numero_ora_predefinita VARCHAR(20),
    numero_aula VARCHAR(30),
    nome_classe VARCHAR(30),
    nome_docente VARCHAR(50),
    cognome_docente VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS evento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urgente BOOLEAN NOT NULL DEFAULT 0,
    cancellato BOOLEAN NOT NULL DEFAULT 0,
    testo VARCHAR,
    data_ora_inizio INTEGER,
    data_ora_fine INTEGER
);

CREATE TABLE IF NOT EXISTS notizia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cancellato BOOLEAN NOT NULL DEFAULT 0,
    testo VARCHAR,
    data_inizio INTEGER,
    data_fine INTEGER
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
    email VARCHAR PRIMARY KEY,
    ruolo VARCHAR(50) NOT NULL REFERENCES ruolo(nome) ON UPDATE CASCADE
);

INSERT OR IGNORE INTO permesso VALUES 
    ('notizie.read', ''),
    ('notizie.write', ''),
    ('eventi.read', ''),
    ('eventi.write', ''),
    ('sostituzioni.read', ''),
    ('sostituzioni.write', ''),
    ('impostazioni.write', '');

INSERT OR IGNORE INTO ruolo VALUES 
    ('amministratore'),
    ('editor'),
    ('visualizzatore');

INSERT OR IGNORE INTO permesso_per_ruolo VALUES 
    ('amministratore', 'notizie.read'),
    ('amministratore', 'notizie.write'),
    ('amministratore', 'eventi.read'),
    ('amministratore', 'eventi.write'),
    ('amministratore', 'sostituzioni.read'),
    ('amministratore', 'sostituzioni.write'),
    ('amministratore', 'impostazioni.write'),
    ('editor', 'notizie.read'),
    ('editor', 'notizie.write'),
    ('editor', 'eventi.read'),
    ('editor', 'eventi.write'),
    ('editor', 'sostituzioni.read'),
    ('editor', 'sostituzioni.write'),
    ('visualizzatore', 'notizie.read'),
    ('visualizzatore', 'eventi.read'),
    ('visualizzatore', 'sostituzioni.read');


------ Creazione Trigger ------

-- -- Copia dati nome e ruolo dall'utente che ha eseguito l'azione
-- CREATE TRIGGER IF NOT EXISTS after_insert_accounting AFTER INSERT
-- ON accounting
-- BEGIN
--     UPDATE accounting SET nome_utente = utente.email, ruolo_utente = utente.ruolo FROM utente WHERE accounting.rowid = NEW.rowid AND utente.email = NEW.legame_utente;
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
