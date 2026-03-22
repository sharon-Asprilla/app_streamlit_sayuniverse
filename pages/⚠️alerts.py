import streamlit as st
from datetime import date

# ===== CONFIGURACIÓN DE SMS CON TWILIO =====
# Instala: pip install twilio
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    st.warning("⚠️ Instala Twilio: pip install twilio")

# Credenciales de Twilio (configurar con tus datos)
TWILIO_ACCOUNT_SID = "your_account_sid"  # Reemplazar con tu Account SID
TWILIO_AUTH_TOKEN = "your_auth_token"    # Reemplazar con tu Auth Token
TWILIO_PHONE = "+1234567890"              # Tu número de Twilio
RECIPIENT_PHONE = "+57XX"                  # Número del estudiante (configurar según usuario)

# Inicializar variables de sesión
if "historial" not in st.session_state:
    st.session_state.historial = []
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "alertas_vistas" not in st.session_state:
    st.session_state.alertas_vistas = 0

# ===== FUNCIÓN PARA ENVIAR SMS =====
def enviar_sms(mensaje):
    """Envía un SMS automático sin necesidad de botón"""
    if not TWILIO_AVAILABLE:
        st.error("❌ Twilio no está instalado. Ejecuta: pip install twilio")
        return False
    
    try:
        # Validar credenciales
        if "your_" in TWILIO_ACCOUNT_SID or "your_" in TWILIO_AUTH_TOKEN:
            st.error("❌ Configura tus credenciales de Twilio en alerts.py")
            return False
        
        # Crear cliente de Twilio
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Enviar SMS
        message = client.messages.create(
            body=mensaje,
            from_=TWILIO_PHONE,
            to=RECIPIENT_PHONE
        )
        
        print(f"✅ SMS enviado exitosamente. ID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar SMS: {str(e)}")
        return False

# Función para crear alerta y guardarla en historial
def crear_alerta(mensaje, tipo="info"):
    if tipo == "success":
        st.success(mensaje)
    elif tipo == "warning":
        st.warning(mensaje)
    elif tipo == "error":
        st.error(mensaje)
    else:
        st.info(mensaje)
    # Guardar en historial
    st.session_state.historial.append(f"ALERTA: {mensaje} ({date.today().strftime('%d/%m/%Y')})")
    st.session_state.alertas.append(mensaje)

# Página de alertas del sistema
st.title("🔔 Alertas del Sistema")

# Mostrar nuevas alertas
nuevas = len(st.session_state.historial) - st.session_state.alertas_vistas
if nuevas > 0:
    st.subheader(f"📢 {nuevas} nuevas alertas desde tu última visita")
    for i in range(st.session_state.alertas_vistas, len(st.session_state.historial)):
        st.info(st.session_state.historial[i])
    st.session_state.alertas_vistas = len(st.session_state.historial)

# Mostrar alertas recientes como mensajes
if st.session_state.alertas:
    st.subheader("📢 Alertas Recientes")
    for alerta in st.session_state.alertas[-5:]:  # Mostrar las últimas 5
        st.info(alerta)

# Mostrar historial
st.markdown("---")
st.subheader("📂 Historial de Procesos")
if st.session_state.historial:
    for proceso in st.session_state.historial:
        st.write(f"- {proceso}")
else:
    st.write("No hay procesos registrados aún.")
