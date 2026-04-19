#!/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "   GREEN HOUSE INMOBILIARIA - Arranque Automático"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "[1/4] Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo crear el entorno virtual"
        echo "Asegúrate de tener Python 3 instalado"
        exit 1
    fi
else
    echo "[✓] Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "[2/4] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo activar el entorno virtual"
    exit 1
fi

# Instalar dependencias
echo "[3/4] Instalando dependencias..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

# Arrancar servidor
echo "[4/4] Arrancando servidor Flask..."
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "   ✓ Servidor iniciado correctamente"
echo "   "
echo "   Abre tu navegador en:"
echo "   http://localhost:5000       - Web principal"
echo "   http://localhost:5000/admin - Panel administración"
echo "   "
echo "   Presiona Ctrl+C para detener el servidor"
echo "═══════════════════════════════════════════════════════════════"
echo ""

python app.py
