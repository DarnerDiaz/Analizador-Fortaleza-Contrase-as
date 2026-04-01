#!/bin/bash

# Script para configurar y ejecutar la aplicación

echo "======================================="
echo "Analizador de Fortaleza de Contraseñas"
echo "======================================="
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Descarga desde: https://www.python.org/downloads/"
    exit 1
fi

# Crear environment virtual si no existe
if [ ! -d "venv" ]; then
    echo "[1/3] Creando environment virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo crear el environment virtual"
        exit 1
    fi
fi

# Activar environment virtual
echo "[2/3] Activando environment virtual..."
source venv/bin/activate

# Instalar dependencias
echo "[3/3] Instalando dependencias..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

# Ejecutar Streamlit
echo ""
echo "======================================="
echo "Iniciando aplicación..."
echo "======================================="
echo ""
echo "La app abrirá en: http://localhost:8501"
echo "Presiona Ctrl+C para detener"
echo ""

streamlit run app/main.py
