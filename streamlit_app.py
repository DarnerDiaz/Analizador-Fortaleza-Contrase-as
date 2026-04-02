"""
Punto de entrada para Streamlit Community Cloud
Ejecuta la aplicación principal directamente
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar ruta padre para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

from utils import PasswordAnalyzer, PatternDetector, PDFReportGenerator, PasswordEncryptor
import config
from datetime import datetime

# Configurar página
st.set_page_config(**config.STREAMLIT_CONFIG)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .weak { color: #d32f2f; font-weight: bold; }
    .fair { color: #f57c00; font-weight: bold; }
    .good { color: #388e3c; font-weight: bold; }
    .strong { color: #1b5e20; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar session state
if 'master_password_set' not in st.session_state:
    st.session_state.master_password_set = False
if 'credentials' not in st.session_state:
    st.session_state.credentials = {}

# Sidebar
st.sidebar.title("🔐 Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["🏠 Inicio", "🔍 Analizar Contraseña", "📁 Análisis Masivo", "💾 Gestor Seguro", "📊 Estadísticas"]
)

def show_home():
    """Página de inicio"""
    st.title("🔐 Analizador de Fortaleza de Contraseñas")
    st.markdown("""
    ### Bienvenido a tu herramienta de seguridad local
    
    Esta aplicación te ayuda a:
    
    ✅ **Analizar contraseñas** - Obtén una puntuación de fortaleza basada en entropía y patrones
    
    ✅ **Detectar patrones débiles** - Identifica fechas, palabras comunes, secuencias inseguras
    
    ✅ **Generar reportes** - Crea informes PDF con recomendaciones de mejora
    
    ✅ **Almacenaje seguro** - Guarda contraseñas cifradas con AES-256-CBC localmente
    
    ✅ **Análisis masivo** - Procesa múltiples contraseñas desde un archivo .txt
    
    ---
    
    ### 🔒 Características de Seguridad
    
    - **Cifrado AES-256-CBC**: Todas las contraseñas almacenadas se cifran con los más altos estándares
    - **Almacenamiento Local**: Nada se envía a internet, todo se procesa en tu máquina
    - **Derivación PBKDF2**: Claves derivadas con 100,000 iteraciones para máxima seguridad
    - **Sin conexión**: Funciona completamente offline
    
    ---
    
    ### 📖 Cómo empezar
    
    1. **Vía a "Analizar Contraseña"** para probar una única contraseña
    2. **Carga un archivo .txt** en "Análisis Masivo" para múltiples contraseñas
    3. **Guarda contraseñas** en el "Gestor Seguro" para acceso posterior
    
    ---
    
    **Versión 1.0** | Herramienta completamente local y privada
    """)

def show_single_analysis():
    """Análisis individual de contraseña"""
    st.title("🔍 Analizar Contraseña Individual")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        password = st.text_input(
            "Ingresa una contraseña:",
            type="password",
            help="Tu contraseña se analiza localmente, no se almacena ni envía a internet"
        )
    
    with col2:
        password_visible = st.checkbox("👁️ Mostrar contraseña")
    
    if password_visible and password:
        st.info(f"Contraseña: `{password}`")
    
    if password:
        # Analizar
        analysis = PasswordAnalyzer.analyze_password(password)
        patterns = PatternDetector.detect_patterns(password)
        recommendations = PasswordAnalyzer.get_recommendations(analysis)
        
        # Mostrar resultados
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Puntuación", f"{analysis['score']}/100", delta=None)
        
        with col2:
            st.metric("Entropía", f"{analysis['entropy']} bits", delta=None)
        
        with col3:
            st.metric("Longitud", f"{analysis['length']} caracteres", delta=None)
        
        with col4:
            st.metric("Fortaleza", analysis['strength'], delta=None)
        
        st.markdown("---")
        
        # Tiempo de crack
        st.subheader("⏱️ Tiempo estimado para crack")
        st.warning(f"**{analysis['crack_time']}** (asumiendo 1 millón de intentos/segundo)")
        
        # Tipos de caracteres
        st.subheader("🔤 Tipos de caracteres")
        chars = analysis['character_types']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status = "✅" if chars['lowercase'] else "❌"
            st.write(f"{status} Minúsculas (a-z)")
        with col2:
            status = "✅" if chars['uppercase'] else "❌"
            st.write(f"{status} Mayúsculas (A-Z)")
        with col3:
            status = "✅" if chars['digits'] else "❌"
            st.write(f"{status} Números (0-9)")
        with col4:
            status = "✅" if chars['special'] else "❌"
            st.write(f"{status} Símbolos (!@#$%^&*)")
        
        # Patrones detectados
        if patterns:
            st.subheader("⚠️ Patrones débiles detectados")
            for pattern_type, pattern_data in patterns.items():
                st.error(f"**{pattern_type.capitalize()}**: {pattern_data}")
        else:
            st.success("✅ No se detectaron patrones débiles")
        
        # Recomendaciones
        st.subheader("💡 Recomendaciones")
        for rec in recommendations:
            st.info(rec)
        
        # Generar PDF
        st.subheader("📥 Descargar reporte")
        pdf_bytes = PDFReportGenerator.generate_single_password_report(analysis, recommendations, patterns)
        st.download_button(
            label="📄 Descargar reporte PDF",
            data=pdf_bytes,
            file_name=f"analisis_contraseña_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

def show_batch_analysis():
    """Análisis masivo de contraseñas"""
    st.title("📁 Análisis Masivo de Contraseñas")
    st.markdown("Carga un archivo `.txt` con contraseñas (una por línea)")
    
    uploaded_file = st.file_uploader("Carga un archivo .txt", type="txt")
    
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        passwords = [line.strip() for line in content.split('\n') if line.strip()]
        st.info(f"Se encontraron {len(passwords)} contraseñas")
        
        if st.button("🔍 Analizar todas"):
            analyses = PasswordAnalyzer.batch_analyze(passwords)
            total = len(analyses)
            strong = sum(1 for a in analyses if a['score'] >= 80)
            average_score = round(sum(a['score'] for a in analyses) / total, 2) if total > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", total)
            with col2:
                st.metric("Promedio", f"{average_score}/100")
            with col3:
                st.metric("Fuertes", strong)

def show_password_manager():
    """Gestor seguro de contraseñas"""
    st.title("💾 Gestor Seguro de Contraseñas")
    st.info("Función de demostración en Streamlit Cloud")

def show_statistics():
    """Estadísticas"""
    st.title("📊 Estadísticas")
    st.info("Sección de estadísticas - En desarrollo")

# Router de páginas
if page == "🏠 Inicio":
    show_home()
elif page == "🔍 Analizar Contraseña":
    show_single_analysis()
elif page == "📁 Análisis Masivo":
    show_batch_analysis()
elif page == "💾 Gestor Seguro":
    show_password_manager()
elif page == "📊 Estadísticas":
    show_statistics()

