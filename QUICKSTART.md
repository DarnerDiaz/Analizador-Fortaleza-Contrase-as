# GUÍA DE INICIO RÁPIDO

## ⚡ Instalación (Windows)

### Opción 1: Script automático (recomendado)
```bash
run.bat
```

### Opción 2: Manual
```bash
# Crear environment virtual
python -m venv venv

# Activar environment virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app/main.py
```

---

## ⚡ Instalación (Linux/Mac)

### Opción 1: Script automático (recomendado)
```bash
bash run.sh
```

### Opción 2: Manual
```bash
# Crear environment virtual
python3 -m venv venv

# Activar environment virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app/main.py
```

---

## 🚀 Funcionalidades disponibles

### 1. Analizar contraseña individual
- Ingresa una contraseña
- Obtén puntuación de fortaleza (0-100)
- Ve entropía, tiempo de crack estimado
- Identifica patrones débiles
- Descarga reporte PDF

### 2. Análisis masivo
- Carga archivo .txt (una contraseña por línea)
- Análisis de todas a la vez
- Reporte comparativo PDF
- Identificación de contraseñas débiles

### 3. Gestor seguro
- Configura contraseña maestra
- Guarda contraseñas cifradas AES-256
- Visualiza/edita contraseñas guardadas
- Almacenamiento totalmente local

---

## 🔐 Normas de seguridad

**IMPORTANTE**: Esta aplicación:
- ✅ Procesa todo localmente
- ✅ No envía datos a internet
- ✅ Cifra con AES-256-CBC
- ✅ Usa derivación de claves PBKDF2 (100,000 iteraciones)
- ❌ No requiere conexión a internet

---

## 📦 Dependencias principales

| Dependencia | Versión | Propósito |
|------------|---------|----------|
| streamlit | 1.28.1+ | Dashboard interactivo |
| cryptography | 41.0.7+ | Cifrado AES-256 |
| reportlab | 4.0.9+ | Generación de PDFs |
| zxcvbn | 4.4.28+ | Análisis de entropía |
| pandas | 2.1.3+ | Manejo de datos |

---

## 🤔 Preguntas frecuentes

### ¿Dónde se guardan las contraseñas?
En la carpeta `data/encrypted_passwords/`. Están encriptadas con AES-256-CBC, tu master password es la única clave para desencriptarlas.

### ¿Puedo compartir este proyecto?
Sí, es código abierto bajo MIT. Puedes modificarlo y distribuirlo libremente.

### ¿Es seguro para contraseñas reales?
Es una herramienta educativa. Para gestión de contraseñas en producción, considera usar:
- Bitwarden
- 1Password
- LastPass
- KeePass

Pero esta tool es perfecta para análisis local y aprendizaje.

### ¿Qué pasa si olvido la contraseña maestra?
Se pierden todas las contraseñas guardadas. No hay recuperación. Usa una contraseña que recuerdes o anótala en un lugar seguro.

---

## 🐛 Solución de problemas

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Asegúrate que el environment virtual está activado
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstala las dependencias
pip install -r requirements.txt
```

### "Port 8501 already in use"
```bash
# Usa otro puerto
streamlit run app/main.py --server.port 8502
```

### Errores de permisos en Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

---

## 📞 Soporte

Para reportar bugs o sugerir mejoras, abre un issue en el repositorio.

---

**¡Disfruta analizando contraseñas de forma segura! 🔐**
