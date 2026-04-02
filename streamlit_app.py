"""
Punto de entrada para Streamlit Community Cloud
Redirige a la aplicación principal en app/main.py
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
sys.path.insert(0, str(Path(__file__).parent))

# Importar y ejecutar la aplicación principal
from app.main import main

if __name__ == "__main__":
    main()
