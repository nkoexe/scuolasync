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
