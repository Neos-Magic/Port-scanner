@echo off
REM Script para ejecutar el Scanner de Puertos en Windows
REM Requiere Python 3.6 o superior

title Network Port Scanner - GUI

echo Iniciando Network Port Scanner...
echo.

python gui.py

if %ERRORLEVEL% neq 0 (
    echo Error: No se pudo ejecutar la aplicacion
    echo Asegurate de tener Python instalado y agregado al PATH
    pause
)
