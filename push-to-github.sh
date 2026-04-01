#!/bin/bash
# Script para subir el proyecto a GitHub
# Reemplaza TU_USUARIO con tu usuario de GitHub
# Luego ejecuta: bash push-to-github.sh

USERNAME="TU_USUARIO"
REPO_NAME="Analizador-Fortaleza-Contraseñas"

echo "=========================================="
echo "Subiendo a GitHub..."
echo "=========================================="
echo ""

# Verificar que se haya especificado el usuario
if [ "$USERNAME" = "TU_USUARIO" ]; then
    echo "❌ ERROR: Reemplaza TU_USUARIO con tu usuario de GitHub"
    echo "Edita este archivo y cambia: USERNAME=\"TU_USUARIO\""
    exit 1
fi

# Añadir remote
echo "1️⃣  Añadiendo remote..."
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

# Hacer push
echo "2️⃣  Haciendo push a main..."
git push -u origin main

echo ""
echo "✅ ¡Listo!"
echo "Accede a: https://github.com/$USERNAME/$REPO_NAME"
