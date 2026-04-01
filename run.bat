@echo off
REM Script para configurar y ejecutar la aplicación

echo.
echo ===============================================
echo  Analizador de Fortaleza de Contraseñas v1.0
echo ===============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Crear environment virtual si no existe
if not exist venv (
    echo.
    echo [1/3] Creando environment virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el environment virtual
        pause
        exit /b 1
    )
)

REM Activar environment virtual
echo.
echo [2/3] Activando environment virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo [3/3] Instalando dependencias...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

REM Ejecutar Streamlit
echo.
echo ===============================================
echo  Iniciando aplicación...
echo ===============================================
echo.
echo La app abrirá en: http://localhost:8501
echo Presiona Ctrl+C para detener la aplicación
echo.

streamlit run app/main.py

pause
