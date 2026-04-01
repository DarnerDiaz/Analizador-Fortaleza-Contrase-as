@echo off
REM Script para subir el proyecto a GitHub
REM Reemplaza TU_USUARIO con tu usuario de GitHub
REM Luego ejecuta: push-to-github.bat

setlocal enabledelayedexpansion

set USERNAME=TU_USUARIO
set REPO_NAME=Analizador-Fortaleza-Contraseñas

echo.
echo ==========================================
echo  Subiendo a GitHub...
echo ==========================================
echo.

REM Verificar que se haya especificado el usuario
if "%USERNAME%"=="TU_USUARIO" (
    echo ❌ ERROR: Reemplaza TU_USUARIO con tu usuario de GitHub
    echo Edita este archivo y cambia: set USERNAME=TU_USUARIO
    pause
    exit /b 1
)

REM Añadir remote
echo 1️⃣  Añadiendo remote...
git remote add origin https://github.com/!USERNAME!/!REPO_NAME!.git
if errorlevel 1 (
    echo ❌ Error al añadir remote
    pause
    exit /b 1
)

REM Hacer push
echo 2️⃣  Haciendo push a main...
git push -u origin main
if errorlevel 1 (
    echo ❌ Error al hacer push
    echo Verifica tus credenciales de GitHub
    pause
    exit /b 1
)

echo.
echo ✅ ¡Listo!
echo Accede a: https://github.com/!USERNAME!/!REPO_NAME!
echo.
pause
