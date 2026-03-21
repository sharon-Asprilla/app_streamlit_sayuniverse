import streamlit as st
from datetime import date

# Inicializar variables de sesión
if "historial" not in st.session_state:
    st.session_state.historial = []
if "alertas" not in st.session_state:
    st.session_state.alertas = []

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

# Ejemplo de acciones que generan alertas
st.title("🔔 Sistema de Alertas")

if st.button("Iniciar sesión"):
    crear_alerta("Inicio de sesión exitoso", "success")

if st.button("Cambiar contraseña"):
    crear_alerta("Contraseña actualizada correctamente", "info")

if st.button("Inscribirse en curso"):
    crear_alerta("Te inscribiste en Inglés Intermedio 1", "success")

if st.button("Generar certificado"):
    crear_alerta("Certificado de Inglés Básico 1 generado", "success")

if st.button("Evaluación pendiente"):
    crear_alerta("Tienes una evaluación pendiente en Inglés Intermedio 2", "warning")

if st.button("Nuevo curso disponible"):
    crear_alerta("Nuevo curso complementario: Inglés Conversacional", "info")

if st.button("Advertencia de sistema"):
    crear_alerta("⚠️ El sistema tuvo una caída temporal", "error")

# Mostrar historial
st.markdown("---")
st.subheader("📂 Historial de procesos")
if st.session_state.historial:
    for proceso in st.session_state.historial:
        st.write(f"- {proceso}")
