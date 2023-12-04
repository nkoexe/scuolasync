#!/bin/bash


# cursed script lo so, non pensavo di essere in grado di creare atrocità simili
# script per ricaricare il sistema, sia su windows sia su linux
# eseguire con cmd /c file.bat (pid) su windows, sh file.bat (pid) su linux

#|| goto :batch_part
kill -9 $1
python -m sostituzioni &

#exiting the bash part
exit

:batch_part
@echo off

kill -9 %1
python -m sostituzioni &