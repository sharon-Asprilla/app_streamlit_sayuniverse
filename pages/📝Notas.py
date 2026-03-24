import streamlit as st
import sqlite3
import pandas as pd
import time

# --- Authentication Check ---
if not st.session_state.get("logged_in", False):
    st.error("Por favor, inicia sesión para acceder a esta página.")
    st.page_link("app.py", label="Ir a la página de inicio de sesión")
    st.stop()

st.set_page_config(page_title="Mis Notas", page_icon="📝")

# Estilos (Mismo sidebar naranja)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #E67E22;
    }
    .stDataFrame {
        width: 100%;
    }
    /* Fuente Arial Global */
    * {
        font-family: 'Arial', sans-serif !important;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 100;
        border-top: 2px solid #E67E22;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📝 Mis Calificaciones y Entregas")
st.write(f"Estudiante: **{st.session_state.user_info['nombre']}**")

def get_mis_notas(user_id):
    conn = sqlite3.connect("academia.db")
    # Consultar notas filtrando por el ID del usuario actual
    query = f"SELECT fecha, tipo, titulo, nota FROM notas WHERE usuario_id = {user_id} ORDER BY id DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Obtener ID del usuario desde la sesión
user_id = st.session_state.user_info['id']

# --- EFECTO DE CARGA DE 5 SEGUNDOS ---
with st.spinner("Espera un momento porfavor..."):
    time.sleep(5)

# Cargar datos
df_notas = get_mis_notas(user_id)

if not df_notas.empty:
    # Métricas rápidas
    col1, col2 = st.columns(2)
    with col1:
        pruebas_realizadas = df_notas[df_notas['tipo'] == 'Prueba'].shape[0]
        st.metric("Pruebas Realizadas", pruebas_realizadas)
    with col2:
        actividades_entregadas = df_notas[df_notas['tipo'] == 'Actividad'].shape[0]
        st.metric("Actividades Entregadas", actividades_entregadas)

    st.markdown("### Historial Detallado")
    
    # Renombrar columnas para mejor visualización
    df_notas.columns = ["Fecha", "Origen (De dónde salió)", "Título de la Actividad", "Nota / Estado"]
    
    # Mostrar tabla interactiva
    st.dataframe(
        df_notas,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Aún no tienes notas registradas. Ve al Dashboard para presentar pruebas o subir actividades.")

if st.button("🔄 Actualizar Tabla"):
    st.rerun()

# Footer Global
st.markdown("""
<div class="footer">
    <p>🦋 SayUniverse | Desarrollada por <b>Sharon Asprilla</b></p>
</div>
""", unsafe_allow_html=True)