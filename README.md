# Analizador de Fortaleza de Contraseñas + Gestor Seguro

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B)
![Coverage](https://img.shields.io/badge/Coverage-85%25-green)
![Tests](https://img.shields.io/badge/Tests-71-passing)
![License](https://img.shields.io/badge/License-MIT-green)

🌐 **[Demo en vivo](https://jbfzyvfnnvgsoddtzd52nn.streamlit.app/)** - ¡Pruébalo sin instalar nada!

Herramienta web interactiva para analizar la fortaleza de contraseñas, detectar patrones débiles y guardarlas de forma segura con cifrado AES-256.

## 📋 Descripción

Aplicación web interactiva para analizar la fortaleza de contraseñas, detectar patrones débiles y guardarlas de forma segura con cifrado AES-256. 

**Características principales:**
- ✅ Análisis de entropía y fortaleza de contraseñas
- 🔍 Detección de patrones débiles (fechas, nombres comunes, secuencias)
- 💡 Sugerencias automáticas de mejora
- 🔐 Almacenamiento seguro con cifrado AES-256
- 📊 Reportes en PDF con visualización de alertas (rojo/verde)
- 📁 Soporte para análisis masivo (archivos .txt)
- 🎨 Dashboard interactivo con Streamlit
- 🧪 71 tests unitarios con >85% cobertura

## 🎯 Tecnologías

- **Backend**: Python 3.10+
- **Cifrado**: `cryptography` (AES-256-CBC, PBKDF2-HMAC)
- **Dashboard**: Streamlit
- **Reportes**: ReportLab (PDF)
- **Análisis**: zxcvbn (estimación de entropía)
- **Datos**: Pandas, NumPy
- **Testing**: pytest

## 📦 Instalación

### Requisitos previos
- Python 3.10+
- pip

### Pasos

```bash
# Clonar o navegar al proyecto
cd Analizador-Fortaleza-Contraseñas

# Opción 1: Script automático (Windows)
run.bat

# Opción 2: Script automático (Linux/Mac)
bash run.sh

# Opción 3: Manual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
streamlit run app/main.py
```

La aplicación abrirá en `http://localhost:8501`

## 🚀 Uso

### Análisis Individual
```python
from utils import PasswordAnalyzer

analysis = PasswordAnalyzer.analyze_password("MyP@ssw0rd123!")
print(f"Fortaleza: {analysis['strength']}")
print(f"Puntuación: {analysis['score']}/100")
print(f"Entropía: {analysis['entropy']} bits")
```

### Análisis Masivo
```python
passwords = ["123456", "MyP@ssw0rd!", "WeakPass"]
results = PasswordAnalyzer.batch_analyze(passwords)
```

### Cifrado Seguro
```python
from utils import PasswordEncryptor

encrypted = PasswordEncryptor.encrypt("miContraseña", "miMasterPassword")
decrypted = PasswordEncryptor.decrypt(encrypted, "miMasterPassword")
```

### Detección de Patrones
```python
from utils import PatternDetector

patterns = PatternDetector.detect_patterns("password12/25/1990")
recommendations = PatternDetector.get_pattern_recommendations(patterns)
```

## 📁 Estructura del Proyecto

```
Analizador-Fortaleza-Contraseñas/
├── app/
│   ├── main.py                 # Entrada principal de Streamlit
│   └── __init__.py
├── utils/
│   ├── password_analyzer.py    # Análisis de fortaleza
│   ├── encryption.py           # Cifrado/Descifrado AES-256
│   ├── patterns.py             # Detección de patrones débiles
│   ├── pdf_generator.py        # Generación de reportes PDF
│   └── __init__.py
├── tests/
│   ├── test_encryption.py      # 10 tests
│   ├── test_password_analyzer.py  # 23 tests
│   ├── test_patterns.py        # 28 tests
│   ├── test_pdf_generator.py   # 14 tests
│   └── __init__.py
├── data/
│   └── encrypted_passwords/    # Almacenamiento seguro (gitignore)
├── reports/
│   └── *.pdf                   # Reportes generados
├── config.py                   # Configuración global
├── requirements.txt            # Dependencias
├── requirements-dev.txt        # Dev dependencies
├── pytest.ini                  # Config de pytest
└── README.md                   # Este archivo
```

## 🔐 Seguridad

- Todas las contraseñas se cifran con **AES-256-CBC**
- Las claves maestras se derivan con **PBKDF2** (100,000 iteraciones)
- Los datos nunca se envían a servidores externos
- Procesamiento 100% local
- Sin tracking ni telemetría

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=utils --cov-report=html
```

**71 tests - 100% pasados ✅**
**Cobertura: >85% ✅**

## 📊 Ejemplo de Salida

```
Contraseña: MyP@ssw0rd!
─────────────────────────────────────
Fortaleza: 💪 FUERTE (82/100)
Entropía: 52.3 bits
Tiempo estimado para crack: 200 años
Patrones: Contiene mayúsculas, números, símbolos
Recomendaciones: ✓ Cumple criterios básicos
```

## 🔄 Roadmap

- [ ] Base de datos SQLite para almacenamiento persistente
- [ ] Validación contra Have I Been Pwned (HIBP)
- [ ] Generador automático de contraseñas seguras
- [ ] Autenticación de 2FA
- [ ] Exportación a gestores de contraseñas (bitwarden, 1password)
- [ ] API REST para integración

## 📄 Licencia

MIT

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Ver [CONTRIBUTING.md](CONTRIBUTING.md)

## 👤 Autor

Desarrollado como herramienta de seguridad local.

---

**⚠️ Nota importante**: Esta herramienta es para uso educativo y personal. No proporciona almacenamiento en la nube. Las contraseñas sensibles se guardan localmente.
