@echo off
SETLOCAL ENABLEEXTENSIONS

set DIR=%~dp0
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
