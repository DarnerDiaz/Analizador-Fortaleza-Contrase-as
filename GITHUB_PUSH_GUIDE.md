# 📤 INSTRUCCIONES PARA SUBIR A GITHUB

## ✅ Ya Completado

El repositorio git ya ha sido inicializado con:
- ✅ Rama `main` creada y configurada  
- ✅ 30 archivos agregados al staging
- ✅ Commit inicial completado: `dff0f8b`

## 🚀 Pasos Finales (Manual)

### Opción 1: Script automático (Recomendado)

#### Windows
```bash
# 1. Edita push-to-github.bat
# 2. Cambia: set USERNAME=TU_USUARIO
#    por tu usuario de GitHub
# 3. Ejecuta:
push-to-github.bat
```

#### Linux/Mac
```bash
# 1. Edita push-to-github.sh
# 2. Cambia: USERNAME="TU_USUARIO"
#    por tu usuario de GitHub
# 3. Ejecuta:
bash push-to-github.sh
```

### Opción 2: Manual (Paso a paso)

#### 1. Crear repositorio en GitHub
- Ve a https://github.com/new
- Nombre: `Analizador-Fortaleza-Contraseñas`
- Descripción: `Análisis de fortaleza de contraseñas + Gestor seguro con AES-256`
- Selecciona "Public" (opcional)
- **NO** inicialices con README, .gitignore ni LICENSE
- Click en "Create repository"

#### 2. Configurar credenciales de GitHub (primera vez)

```bash
# Opción A: Personal Access Token (Recomendado)
git config --global credential.helper store

# O para solo este repositorio:
git config credential.helper store

# Luego haz el push y usa:
# Usuario: tu_usuario_github
# Contraseña: tu_token_generado_en_github
```

#### 3. Agregar remote y hacer push

```bash
cd d:\ProyectosProgra\Analizador-Fortaleza-Contraseñas

# Reemplaza TU_USUARIO con tu usuario real
git remote add origin https://github.com/TU_USUARIO/Analizador-Fortaleza-Contraseñas.git

# Verificar remote
git remote -v

# Hacer push
git push -u origin main
```

#### 4. Si todo va bien, verás:
```
Enumerating objects: 35, done.
Counting objects: 100% (35/35), done.
Delta compression using up to X threads
Compressing objects: 100% (28/28), done.
Writing objects: 100% (35/35), X KiB | X KiB/s, done.
Total 35 (delta 12), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (12/12), done.
To https://github.com/TU_USUARIO/Analizador-Fortaleza-Contraseñas.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🔑 Generar Personal Access Token

Si no tienes un token:

1. Ve a https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Nombre: `Git Password Manager`
4. Permisos: `repo` (acceso total a repositorios)
5. Expira: Selecciona una duración (ej: 90 días o sin expiración)
6. Click "Generate token"
7. **Copia el token** (solo lo verás una vez)
8. Usa el token como contraseña en git

---

## ✨ Después del Push

Una vez subido, tu repositorio estará en:
```
https://github.com/TU_USUARIO/Analizador-Fortaleza-Contraseñas
```

### Opcional: Crear Release v1.0.0

```bash
git tag -a v1.0.0 -m "First release - Password Strength Analyzer"
git push origin v1.0.0
```

### Opcional: Configurar GitHub Pages

Si quieres documentación online:
- Ve a Settings → Pages
- Selecciona "main" branch
- Click Save
- Espera a que GitHub construya el sitio

---

## 🆘 Solución de Problemas

### Error: "Username for... not provided"
→ Seguro que has configurado `credential.helper store`
→ O usa SSH en lugar de HTTPS

### Error: "remote: permission denied"
→ Verifica que el Personal Access Token tiene permisos `repo`
→ Token expirado → Genera uno nuevo

### Error: "Authentication failed"
→ Contraseña incorrecta o usuario mal escrito
→ Revisa que hayas usado tu token, no tu contraseña real

### "fatal: remote origin already exists"
→ El remote ya está configurado
→ Usa: `git remote set-url origin https://github.com/TU_USUARIO/repo.git`

---

## 📋 Checklist

- ✅ Repositorio git inicializado localmente
- ✅ Commit inicial completado
- ✅ Rama `main` configurada
- ⭕ Repositorio creado en GitHub (manual)
- ⭕ Credenciales de GitHub configuradas (manual)
- ⭕ Remote añadido (manual o script)
- ⭕ Push completado (manual o script)
- ⭕ Verificar en GitHub (manual)

---

**Commit hash**: `dff0f8b`  
**Archivos**: 30 archivos, 3071 líneas  
**Status**: Listo para push 🚀
