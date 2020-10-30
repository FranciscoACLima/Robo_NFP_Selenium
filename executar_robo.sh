#!/bin/bash

DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
echo DIR_BASE: $DIR

PYHTON=$DIR/venv/bin/python
echo PYHTON EXEC: $PYHTON

SCRIPT=$DIR/run.py
echo PYHTON SCRIPT: $SCRIPT

$PYHTON $SCRIPT

# set DIR=%~dp0
# set DIR_PAI=%DIR:config_robos\=%
# echo +++ %DIR_PAI%
# echo +++ %DIR%

# set PYHTON=%DIR%venv\Scripts\python

# set SCRIPT="%DIR%run.py"

# :EXECSCRIPT
# echo +++ Executando robo Nota Fiscal Paulista
# %PYHTON% %SCRIPT%
# GOTO FINALLY

# :FINALLY
# ENDLOCAL
# PAUSE
