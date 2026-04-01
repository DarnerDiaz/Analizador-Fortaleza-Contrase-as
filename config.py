"""
Configuración global del proyecto
"""

import os
from pathlib import Path

# Directorios
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
ENCRYPTED_DIR = DATA_DIR / "encrypted_passwords"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Crear directorios si no existen
ENCRYPTED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Analizador de Fortaleza de Contraseñas",
    "page_icon": "🔐",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Configuración de seguridad
ENCRYPTION_CONFIG = {
    "algorithm": "AES-256-CBC",
    "salt_length": 32,  # bytes
    "iterations": 100000,  # PBKDF2 iterations
    "key_derivation": "PBKDF2",
}

# Configuración de análisis
PASSWORD_CONFIG = {
    "min_length": 8,
    "min_strength": 50,  # Mínimo recomendado en escala 0-100
}

# Thresholds de color
COLOR_THRESHOLDS = {
    "weak": (0, 40),        # Rojo
    "fair": (40, 60),       # Amarillo
    "good": (60, 80),       # Verde claro
    "strong": (80, 100),    # Verde oscuro
}

# Patrones débiles comunes
WEAK_PATTERNS = {
    "dates": [
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'\d{4}-\d{1,2}-\d{1,2}',
        r'\d{1,2}-\d{1,2}-\d{4}',
    ],
    "common_words": [
        "password", "pass", "admin", "user", "login", 
        "test", "demo", "root", "welcome", "qwerty",
        "123456", "password123", "admin123",
    ],
    "sequences": [
        r'123', r'456', r'789', r'abc', r'xyz',
        r'qwerty', r'asdf', r'zxcv',
    ],
}

# Configuración de reportes
PDF_CONFIG = {
    "page_size": "A4",
    "margin": 15,
    "title_size": 20,
    "heading_size": 14,
    "text_size": 10,
}

# Colores para reportes
COLORS = {
    "red": (0.8, 0.1, 0.1),
    "yellow": (0.9, 0.7, 0.1),
    "green": (0.1, 0.7, 0.1),
    "dark_green": (0.0, 0.5, 0.0),
    "black": (0, 0, 0),
    "gray": (0.5, 0.5, 0.5),
}
