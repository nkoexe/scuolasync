#!/bin/bash

utenti_db="sostituzioni/database/utenti.db"
main_db="sostituzioni/database/database.db"

sqlite3 $utenti_db ".dump" | sqlite3 $main_db
