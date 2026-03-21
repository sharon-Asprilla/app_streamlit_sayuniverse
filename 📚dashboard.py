import streamlit as st
import pandas as pd 


st.title("panel ")

import streamlit as st
from datetime import date

# Inicializar historial en sesión
if "historial" not in st.session_state:
    st.session_state.historial = []

# Función para registrar procesos en historial
def registrar_proceso(mensaje):
    st.session_state.historial.append(f"{mensaje} ({date.today().strftime('%d/%m/%Y')})")

# Dashboard
st.title("📊 Dashboard Académico")

# Sección de cuestionarios
st.subheader("📝 Cuestionarios")
pregunta1 = st.radio("¿Cuál es el plural de 'mouse'?", ["mouses", "mice", "mousees"])
if st.button("Enviar cuestionario"):
    st.success("Cuestionario enviado correctamente")
    registrar_proceso("Cuestionario respondido")

# Sección de evaluaciones
st.subheader("📚 Evaluaciones")
evaluacion = st.selectbox("Selecciona evaluación pendiente:", ["Evaluación 1 - Básico", "Evaluación 2 - Intermedio", "Evaluación 3 - Avanzado"])
if st.button("Enviar evaluación"):
    st.success(f"{evaluacion} enviada correctamente")
    registrar_proceso(f"Evaluación enviada: {evaluacion}")

# Sección de entrega de actividades
st.subheader("📂 Entrega de actividades")
archivo = st.file_uploader("Sube tu actividad en PDF o Word", type=["pdf", "docx"])
if archivo is not None:
    if st.button("Enviar actividad"):
        st.success(f"Actividad '{archivo.name}' enviada correctamente")
        registrar_proceso(f"Actividad entregada: {archivo.name}")

# Historial de procesos
st.markdown("---")
st.subheader("📂 Historial de procesos")
if st.session_state.historial:
    for proceso in st.session_state.historial:
        st.write(f"- {proceso}")
else:
    st.info("Historial sin procesos")



    