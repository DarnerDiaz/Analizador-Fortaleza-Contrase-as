# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-04-01

### Added
- ✨ Análisis individual de contraseñas con puntuación de fortaleza (0-100)
- ✨ Cálculo de entropía (bits) y tiempo estimado de crack
- ✨ Detección de patrones débiles (fechas, palabras comunes, secuencias de teclado)
- ✨ Análisis masivo desde archivo .txt
- ✨ Generación de reportes en PDF (individual y masivo)
- ✨ Gestor seguro con cifrado AES-256-CBC
- ✨ Dashboard interactivo con Streamlit
- ✨ 71 tests unitarios con cobertura >85%
- ✨ Recomendaciones automáticas para fortalecer contraseñas
- ✨ Interfaz intuitiva con alertas visuales (rojo/verde/amarillo)

### Features
- Análisis con librería `zxcvbn` (estimación realista de entropía)
- Derivación de claves con PBKDF2-HMAC (100,000 iteraciones)
- Almacenamiento 100% local (sin internet)
- Soporte para caracteres unicode y especiales
- Exportación de reportes a PDF

### Security
- Cifrado AES-256-CBC de todos los datos
- Master password para proteger contraseñas guardadas
- Sin envío de datos a internet
- Sin tracking ni telemetría

---

## Próximas versiones

### [1.1.0] (planificado)
- Base de datos SQLite para almacenamiento persistente
- Validación contra Have I Been Pwned (HIBP)
- Generador automático de contraseñas seguras
- Autenticación de 2FA

### [1.2.0] (planificado)
- API REST para integración
- Exportación a gestores de contraseñas (Bitwarden, 1Password)
- Análisis de patrones avanzados

---

**Versión actual**: 1.0.0
