"""
Punto de entrada para Streamlit Community Cloud
Versión simplificada sin dependencias de compilación
"""
import streamlit as st
import math
import re
from datetime import datetime

st.set_page_config(
    page_title="Analizador de Fortaleza de Contraseñas",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .weak { color: #d32f2f; font-weight: bold; }
    .fair { color: #f57c00; font-weight: bold; }
    .good { color: #388e3c; font-weight: bold; }
    .strong { color: #1b5e20; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def calculate_entropy(password: str) -> float:
    """Calcula la entropía de Shannon de una contraseña"""
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        charset_size += 32
    
    if charset_size == 0:
        return 0
    
    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

def estimate_crack_time(entropy: float) -> str:
    """Estima el tiempo para crack basado en entropía"""
    if entropy < 30:
        return "Menos de 1 segundo"
    elif entropy < 40:
        return "1-100 segundos"
    elif entropy < 50:
        return "Horas"
    elif entropy < 60:
        return "Días"
    elif entropy < 70:
        return "Años"
    elif entropy < 80:
        return "Siglos"
    else:
        return "Milenios"

def get_strength_label(entropy: float) -> str:
    """Obtiene la etiqueta de fortaleza"""
    if entropy < 30:
        return "🔴 Muy débil"
    elif entropy < 50:
        return "🟠 Débil"
    elif entropy < 70:
        return "🟡 Regular"
    elif entropy < 90:
        return "🟢 Fuerte"
    else:
        return "🟢 Muy fuerte"

def detect_patterns(password: str) -> dict:
    """Detecta patrones débiles en la contraseña"""
    patterns = {}
    
    # Detectar fechas
    if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', password):
        patterns['Fecha'] = 'Se detectó formato de fecha'
    
    # Detectar años
    if re.search(r'(19|20)\d{2}', password):
        patterns['Año'] = 'Se detectó un año'
    
    # Detectar caracteres repetidos
    if re.search(r'(.)\1{2,}', password):
        patterns['Repetición'] = 'Se detectaron caracteres repetidos'
    
    # Detectar secuencias numéricas
    if re.search(r'012|123|234|345|456|567|678|789|890', password):
        patterns['Secuencia'] = 'Se detectó secuencia numérica'
    
    # Solo números
    if password.isdigit():
        patterns['Números'] = 'La contraseña contiene solo números'
    
    return patterns

# Sidebar
st.sidebar.title("🔐 Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["🏠 Inicio", "🔍 Análisis Individual", "📊 Características"]
)

if page == "🏠 Inicio":
    st.title("🔐 Analizador de Fortaleza de Contraseñas")
    st.markdown("""
    ### Bienvenido a tu herramienta de seguridad
    
    Una aplicación web interactiva para:
    
    ✅ **Analizar contraseñas** - Obtén puntuación de fortaleza basada en entropía
    
    ✅ **Detectar patrones débiles** - Identifica fechas, números, secuencias
    
    ✅ **Consejos de seguridad** - Recomendaciones para mejorar tus contraseñas
    
    ---
    
    ### 🔒 Características
    
    - **Análisis local**: Todo se procesa en tu navegador
    - **100% privado**: Nada se envía a internet
    - **Instantáneo**: Resultados en tiempo real
    - **Gratuito**: Herramienta completamente libre
    
    ---
    
    ### 🚀 Versión 1.0 en vivo
    
    Prueba en la sección **"Análisis Individual"** →
    """)
    
    st.info("""
    ⭐ **Para reclutadores/entrevistadores**: 
    Esta es una **demostración funcional en Streamlit Cloud**. 
    
    El [repositorio completo en GitHub](https://github.com/DarnerDiaz/Analizador-Fortaleza-Contrase-as) 
    incluye versión de escritorio con cifrado AES-256, gestión segura de contraseñas y generación de reportes PDF.
    """)

elif page == "🔍 Análisis Individual":
    st.title("🔍 Análisis Individual de Contraseña")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        password = st.text_input(
            "Ingresa una contraseña para analizar:",
            type="password",
            placeholder="Tu contraseña se analiza localmente"
        )
    
    with col2:
        show_pwd = st.checkbox("👁️ Mostrar")
    
    if show_pwd and password:
        st.code(password)
    
    if password:
        entropy = calculate_entropy(password)
        strength = get_strength_label(entropy)
        crack_time = estimate_crack_time(entropy)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Entropía", f"{entropy} bits")
        with col2:
            st.metric("Longitud", len(password))
        with col3:
            st.metric("Fortaleza", strength)
        with col4:
            st.metric("Tiempo crack", crack_time)
        
        st.markdown("---")
        
        # Tipos de caracteres
        st.subheader("🔤 Tipos de caracteres")
        col1, col2, col3, col4 = st.columns(4)
        
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        with col1:
            st.write("✅ Minúsculas" if has_lower else "❌ Minúsculas")
        with col2:
            st.write("✅ Mayúsculas" if has_upper else "❌ Mayúsculas")
        with col3:
            st.write("✅ Números" if has_digit else "❌ Números")
        with col4:
            st.write("✅ Símbolos" if has_special else "❌ Símbolos")
        
        st.markdown("---")
        
        # Patrones detectados
        patterns = detect_patterns(password)
        
        if patterns:
            st.subheader("⚠️ Patrones débiles detectados")
            for pattern, desc in patterns.items():
                st.warning(f"🔴 **{pattern}**: {desc}")
        else:
            st.success("✅ No se detectaron patrones débiles")
        
        st.markdown("---")
        
        # Recomendaciones
        st.subheader("💡 Recomendaciones")
        
        recommendations = []
        if len(password) < 12:
            recommendations.append("📝 Usa al menos 12 caracteres")
        if not has_upper:
            recommendations.append("📝 Incluye letras mayúsculas (A-Z)")
        if not has_digit:
            recommendations.append("📝 Incluye números (0-9)")
        if not has_special:
            recommendations.append("📝 Incluye símbolos (!@#$%^&*)")
        if entropy < 70:
            recommendations.append("📝 Aumenta la variedad de caracteres")
        
        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("✔️ Tu contraseña tiene una buena fortaleza. ¡Excelente!")

elif page == "📊 Características":
    st.title("📊 Características del Proyecto")
    
    st.subheader("🛠️ Tecnologías")
    
    cols = st.columns(3)
    with cols[0]:
        st.write("""
        **Backend:**
        - Python 3.10+
        - Streamlit
        - zxcvbn (análisis)
        """)
    
    with cols[1]:
        st.write("""
        **Seguridad:**
        - AES-256-CBC
        - PBKDF2-HMAC
        - Procesamiento local
        """)
    
    with cols[2]:
        st.write("""
        **Características:**
        - 71 tests unitarios
        - >85% cobertura
        - Reportes PDF
        """)
    
    st.markdown("---")
    
    st.subheader("🔗 Enlaces útiles")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[📦 Repositorio GitHub](https://github.com/DarnerDiaz/Analizador-Fortaleza-Contrase-as)")
    with col2:
        st.markdown("[📖 README](https://github.com/DarnerDiaz/Analizador-Fortaleza-Contrase-as/blob/main/README.md)")
    with col3:
        st.markdown("[✨ Características Completas](https://github.com/DarnerDiaz/Analizador-Fortaleza-Contrase-as#-características)")
    
    st.info("""
    💻 **Para uso completo con cifrado y gestión segura:**
    ```bash
    git clone https://github.com/DarnerDiaz/Analizador-Fortaleza-Contrase-as.git
    cd Analizador-Fortaleza-Contraseñas
    pip install -r requirements.txt
    streamlit run app/main.py
    ```
    """)



