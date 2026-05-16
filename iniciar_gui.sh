#!/bin/bash
# Script para ejecutar el Scanner de Puertos en Linux/macOS

echo "Iniciando Network Port Scanner..."
echo ""

# Detectar qué versión de Python usar
if command -v python3 &> /dev/null; then
    python3 gui.py
elif command -v python &> /dev/null; then
    python gui.py
else
    echo "Error: Python no está instalado o no se encuentra en el PATH"
    exit 1
fi
