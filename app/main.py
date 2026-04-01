"""
Aplicación principal de Streamlit - Analizador de Fortaleza de Contraseñas
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Agregar ruta padre para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

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


def main():
    """Función principal de la aplicación"""

    # Sidebar
    st.sidebar.title("🔐 Navegación")
    page = st.sidebar.radio(
        "Selecciona una sección:",
        ["🏠 Inicio", "🔍 Analizar Contraseña", "📁 Análisis Masivo", "💾 Gestor Seguro", "📊 Estadísticas"]
    )

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

    ### ⚡ Consejos para contraseñas seguras

    - Usa **al menos 12 caracteres**
    - Combina **mayúsculas, minúsculas, números y símbolos**
    - Evita **fechas, nombres o palabras predecibles**
    - Usa **frases aleatorias** o **generadores de contraseñas**
    - Mantén contraseñas **únicas por servicio**

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

        # Guardar en gestor seguro
        st.subheader("💾 Guardar en Gestor Seguro")
        col1, col2 = st.columns([2, 1])
        with col1:
            nickname = st.text_input("Dale un nombre/alias a esta contraseña", placeholder="ej: email_gmail")
        with col2:
            if st.button("💾 Guardar", use_container_width=True):
                if nickname:
                    if 'saved_passwords' not in st.session_state:
                        st.session_state.saved_passwords = {}
                    st.session_state.saved_passwords[nickname] = {
                        'password': password,
                        'analysis': analysis,
                        'timestamp': datetime.now().isoformat()
                    }
                    st.success(f"✅ Contraseña guardada como '{nickname}'")
                else:
                    st.warning("⚠️ Ingresa un alias para la contraseña")


def show_batch_analysis():
    """Análisis masivo de contraseñas"""
    st.title("📁 Análisis Masivo de Contraseñas")

    st.markdown("""
    Carga un archivo `.txt` con contraseñas (una por línea) para obtener un análisis masivo y reporte PDF.
    """)

    uploaded_file = st.file_uploader("Carga un archivo .txt", type="txt")

    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        passwords = [line.strip() for line in content.split('\n') if line.strip()]

        st.info(f"Se encontraron {len(passwords)} contraseñas para analizar")

        if st.button("🔍 Analizar todas", use_container_width=True):
            with st.spinner("Analizando contraseñas..."):
                analyses = PasswordAnalyzer.batch_analyze(passwords)

            # Mostrar resumen
            st.subheader("📊 Resumen")
            total = len(analyses)
            strong = sum(1 for a in analyses if a['score'] >= 80)
            weak = sum(1 for a in analyses if a['score'] < 40)
            average_score = round(sum(a['score'] for a in analyses) / total, 2) if total > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total", total)
            with col2:
                st.metric("Promedio", f"{average_score}/100")
            with col3:
                st.metric("Fuertes", strong)
            with col4:
                st.metric("Débiles", weak)

            # Tabla de resultados
            st.subheader("📋 Resultados detallados")

            df_data = []
            for i, analysis in enumerate(analyses, 1):
                df_data.append({
                    '#': i,
                    'Puntuación': analysis['score'],
                    'Fortaleza': analysis['strength'],
                    'Entropía': analysis['entropy'],
                    'Longitud': analysis['length'],
                    'Tiempo de crack': analysis['crack_time'],
                })

            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Descargar reporte PDF
            st.subheader("📥 Descargar reporte")
            pdf_bytes = PDFReportGenerator.generate_batch_report(analyses)
            st.download_button(
                label="📄 Descargar reporte PDF",
                data=pdf_bytes,
                file_name=f"analisis_masivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )


def show_password_manager():
    """Gestor seguro de contraseñas"""
    st.title("💾 Gestor Seguro de Contraseñas")

    st.markdown("""
    Guarda y gestiona contraseñas cifradas con AES-256-CBC. 
    Las contraseñas se protegen con una contraseña maestra.
    """)

    if not st.session_state.master_password_set:
        st.subheader("🔑 Configura tu contraseña maestra")
        master_password = st.text_input(
            "Crea una contraseña maestra:",
            type="password",
            help="Esta contraseña protege todas tus contraseñas guardadas. No la olvides."
        )
        master_password_confirm = st.text_input(
            "Confirma tu contraseña maestra:",
            type="password"
        )

        if st.button("Configurar contraseña maestra", use_container_width=True):
            if master_password and master_password == master_password_confirm:
                st.session_state.master_password = master_password
                st.session_state.master_password_set = True
                st.success("✅ Contraseña maestra configurada")
                st.rerun()
            else:
                st.error("❌ Las contraseñas no coinciden o están vacías")
    else:
        st.success("✅ Contraseña maestra activada")

        # Opciones
        option = st.radio("Selecciona una opción:", ["Guardar contraseña", "Ver contraseñas guardadas", "Eliminar contraseña"])

        if option == "Guardar contraseña":
            st.subheader("➕ Guardar nueva contraseña")
            col1, col2 = st.columns(2)
            with col1:
                service = st.text_input("Nombre del servicio", placeholder="ej: Gmail, Facebook")
            with col2:
                password = st.text_input("Contraseña", type="password")

            if st.button("💾 Guardar", use_container_width=True):
                if service and password:
                    if 'stored_passwords' not in st.session_state:
                        st.session_state.stored_passwords = {}

                    try:
                        encrypted = PasswordEncryptor.encrypt(password, st.session_state.master_password)
                        st.session_state.stored_passwords[service] = encrypted
                        st.success(f"✅ Contraseña para '{service}' guardada de forma segura")
                    except Exception as e:
                        st.error(f"❌ Error al guardar: {e}")
                else:
                    st.warning("⚠️ Completa todos los campos")

        elif option == "Ver contraseñas guardadas":
            st.subheader("📁 Contraseñas guardadas")
            if 'stored_passwords' not in st.session_state or not st.session_state.stored_passwords:
                st.info("No hay contraseñas guardadas aún")
            else:
                for service, encrypted_password in st.session_state.stored_passwords.items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"🔐 **{service}**")
                    with col2:
                        if st.button("👁️ Ver", key=f"view_{service}"):
                            try:
                                decrypted = PasswordEncryptor.decrypt(encrypted_password, st.session_state.master_password)
                                st.info(f"Contraseña: `{decrypted}`")
                            except Exception as e:
                                st.error(f"Error: {e}")
                    with col3:
                        if st.button("🗑️", key=f"delete_{service}"):
                            del st.session_state.stored_passwords[service]
                            st.success("✅ Contraseña eliminada")
                            st.rerun()

        elif option == "Eliminar contraseña":
            st.subheader("🗑️ Eliminar contraseña guardada")
            if 'stored_passwords' not in st.session_state or not st.session_state.stored_passwords:
                st.info("No hay contraseñas guardadas para eliminar")
            else:
                service_to_delete = st.selectbox(
                    "Selecciona una contraseña para eliminar:",
                    list(st.session_state.stored_passwords.keys())
                )
                if st.button("🗑️ Eliminar", use_container_width=True):
                    del st.session_state.stored_passwords[service_to_delete]
                    st.success(f"✅ Contraseña '{service_to_delete}' eliminada")
                    st.rerun()


def show_statistics():
    """Página de estadísticas"""
    st.title("📊 Estadísticas")
    st.info("Sección en desarrollo. Aquí verás gráficos de tendencias de análisis.")


if __name__ == "__main__":
    main()
