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


ATTACH DATABASE 'database.db' AS generale;
ATTACH DATABASE 'utenti.db' AS users;

BEGIN TRANSACTION;

-- nota_standard
INSERT OR IGNORE INTO main.nota_standard 
SELECT * FROM generale.nota_standard;

-- ora_predefinita
INSERT OR IGNORE INTO main.ora_predefinita 
SELECT * FROM generale.ora_predefinita;

-- docente
INSERT OR IGNORE INTO main.docente 
SELECT * FROM generale.docente;

-- aula
INSERT OR IGNORE INTO main.aula 
SELECT * FROM generale.aula;

-- classe
INSERT OR IGNORE INTO main.classe 
SELECT * FROM generale.classe;

-- aula_ospita_classe
INSERT OR IGNORE INTO main.aula_ospita_classe 
SELECT * FROM generale.aula_ospita_classe;

-- sostituzione
INSERT OR IGNORE INTO main.sostituzione 
SELECT * FROM generale.sostituzione;

-- archivio_sostituzioni
INSERT OR IGNORE INTO main.archivio_sostituzioni 
SELECT * FROM generale.archivio_sostituzioni;

-- evento
INSERT OR IGNORE INTO main.evento 
SELECT * FROM generale.evento;

-- notizia
INSERT OR IGNORE INTO main.notizia 
SELECT * FROM generale.notizia;

-- permesso
INSERT OR IGNORE INTO main.permesso 
SELECT * FROM users.permesso;

INSERT OR IGNORE INTO main.ruolo 
SELECT * FROM users.ruolo;

-- permesso_per_ruolo 
INSERT OR IGNORE INTO main.permesso_per_ruolo 
SELECT * FROM users.permesso_per_ruolo;

-- utente
INSERT OR IGNORE INTO main.utente 
SELECT * FROM users.utente;

COMMIT;

DETACH DATABASE generale;
DETACH DATABASE users;

-- Verify data
SELECT 'nota_standard count:', COUNT(*) FROM nota_standard;
SELECT 'ora_predefinita count:', COUNT(*) FROM ora_predefinita;
SELECT 'docente count:', COUNT(*) FROM docente;
SELECT 'aula count:', COUNT(*) FROM aula;
SELECT 'classe count:', COUNT(*) FROM classe;
SELECT 'aula_ospita_classe count:', COUNT(*) FROM aula_ospita_classe;
SELECT 'sostituzione count:', COUNT(*) FROM sostituzione;
SELECT 'archivio_sostituzioni count:', COUNT(*) FROM archivio_sostituzioni;
SELECT 'evento count:', COUNT(*) FROM evento;
SELECT 'notizia count:', COUNT(*) FROM notizia;
SELECT 'permesso count:', COUNT(*) FROM permesso;
SELECT 'ruolo count:', COUNT(*) FROM ruolo;
SELECT 'permesso_per_ruolo count:', COUNT(*) FROM permesso_per_ruolo;
SELECT 'utente count:', COUNT(*) FROM utente;
