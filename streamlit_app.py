"""
Punto de entrada para Streamlit Community Cloud
Ejecuta la aplicación principal directamente
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Agregar ruta padre para importar módulos
sys.path.insert(0, str(Path(__file__).parent))

# Lazy imports - importar solo cuando sea necesario
def load_utils():
    from utils import PasswordAnalyzer, PatternDetector, PDFReportGenerator, PasswordEncryptor
    import config
    return PasswordAnalyzer, PatternDetector, PDFReportGenerator, PasswordEncryptor, config

PasswordAnalyzer = None
PatternDetector = None
PDFReportGenerator = None
PasswordEncryptor = None
config = None

# Configurar página
try:
    _, _, _, _, config = load_utils()
    st.set_page_config(**config.STREAMLIT_CONFIG)
except Exception as e:
    st.set_page_config(page_title="Analizador de Contraseñas", layout="wide")

# Estilos CSS personalizados
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .weak { color: #d32f2f; font-weight: bold; }
    .fair { color: #f57c00; font-weight: bold; }
    .good { color: #388e3c; font-weight: bold; }
    .strong { color: #1b5e20; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar session state
if 'master_password_set' not in st.session_state:
    st.session_state.master_password_set = False

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
    ### Bienvenido a tu herramienta de seguridad
    
    ✅ **Analizar contraseñas** - Puntuación de fortaleza basada en entropía
    ✅ **Detectar patrones débiles** - Identifica fechas, palabras comunes  
    ✅ **Generar reportes PDF** - Informes con recomendaciones
    ✅ **Análisis masivo** - Procesa múltiples contraseñas
    
    **Versión 1.0** | Herramienta completamente local
    """)

def show_single_analysis():
    """Análisis individual de contraseña"""
    st.title("🔍 Analizar Contraseña Individual")
    
    try:
        PasswordAnalyzer_cls, PatternDetector_cls, PDFReportGenerator_cls, _, _ = load_utils()
    except Exception as e:
        st.error(f"Error cargando módulos: {e}")
        return
    
    password = st.text_input("Ingresa una contraseña:", type="password")
    
    if password:
        try:
            analysis = PasswordAnalyzer_cls.analyze_password(password)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Puntuación", f"{analysis['score']}/100")
            with col2:
                st.metric("Entropía", f"{analysis['entropy']} bits")
            with col3:
                st.metric("Longitud", f"{analysis['length']}")
            with col4:
                st.metric("Fortaleza", analysis['strength'])
                
            st.warning(f"⏱️ Tiempo para crack: **{analysis['crack_time']}**")
        except Exception as e:
            st.error(f"Error en análisis: {e}")

def show_batch_analysis():
    """Análisis masivo"""
    st.title("📁 Análisis Masivo")
    st.info("Carga un archivo .txt con contraseñas (una por línea)")

def show_password_manager():
    """Gestor seguro"""
    st.title("💾 Gestor Seguro")
    st.info("Función de demostración en Streamlit Cloud")

def show_statistics():
    """Estadísticas"""
    st.title("📊 Estadísticas")
    st.info("Sección en desarrollo")

# Router
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


