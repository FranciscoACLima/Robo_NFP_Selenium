@echo off
SETLOCAL ENABLEEXTENSIONS

set DIR=%~dp0
set DIR_PAI=%DIR:config_robos\=%
echo +++ %DIR_PAI%
echo +++ %DIR%

set PYHTON=%DIR%venv\Scripts\python

set SCRIPT="%DIR%run.py"

:EXECSCRIPT
echo +++ Executando robo Nota Fiscal Paulista
%PYHTON% %SCRIPT%
GOTO FINALLY

:FINALLY
ENDLOCAL
PAUSE
