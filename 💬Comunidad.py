import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- Authentication Check ---
if not st.session_state.get("logged_in", False):
    st.error("Por favor, inicia sesión para acceder a esta página.")
    st.page_link("app.py", label="Ir a la página de inicio de sesión")
    st.stop()

st.set_page_config(page_title="Comunidad SayUniverse", page_icon="💬")

# Estilos
st.markdown("""
    <style>
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #FFFFFF, #FFEDD5, #E67E22, #FFF7E6);
        background-size: 400% 400%;
        animation: gradient-animation 15s ease infinite;
    }
    /* Texto negro global */
    body, .stMarkdown, .stButton, .stTextInput, .stTextArea, p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: black !important;
    }
    [data-testid="stSidebar"] {
        background-color: #E67E22;
    }
    /* Botón de navegación (Sidebar toggle) ROJO Y GRANDE */
    [data-testid="collapsedControl"] {
        transform: scale(1.5) !important;
        background-color: #FF0000 !important;
        color: white !important;
        border-radius: 50%;
        border: 2px solid white;
        margin-left: 10px;
        margin-top: 5px;
    }
    /* Fuente Arial Global */
    * {
        font-family: 'Arial', sans-serif !important;
    }
    .chat-card {
        background: #FFFFFF;
        border-left: 5px solid #E67E22;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .chat-card:hover {
        transform: scale(1.02);
    }
    .chat-user {
        font-weight: bold;
        color: #D35400;
        font-size: 14px;
    }
    .chat-date {
        font-size: 11px;
        color: #888;
        float: right;
    }
    .chat-msg {
        margin-top: 5px;
        font-size: 15px;
        color: black;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: #FFFFFF;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 100;
        border-top: 2px solid #E67E22;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Comunidad y Apuntes")
st.write("Comparte tus aprendizajes o guarda tus notas personales aquí.")

# --- LÓGICA DE BASE DE DATOS ---
def guardar_mensaje(usuario_id, nombre, mensaje):
    conn = sqlite3.connect("academia.db")
    c = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO comunidad (usuario_id, usuario_nombre, mensaje, fecha) VALUES (?, ?, ?, ?)",
              (usuario_id, nombre, mensaje, fecha_actual))
    conn.commit()
    conn.close()

def leer_mensajes():
    conn = sqlite3.connect("academia.db")
    df = pd.read_sql("SELECT usuario_nombre, mensaje, fecha FROM comunidad ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    return df

# --- INPUT DE MENSAJE ---
with st.form("chat_form", clear_on_submit=True):
    nuevo_mensaje = st.text_area("Escribe tu apunte o comentario:", placeholder="Ej: Hoy aprendí sobre el verbo To Be...")
    enviado = st.form_submit_button("Enviar Comentario 🚀")
    
    if enviado and nuevo_mensaje:
        user_id = st.session_state.user_info['id']
        user_name = st.session_state.user_info['nombre']
        guardar_mensaje(user_id, user_name, nuevo_mensaje)
        st.success("¡Mensaje publicado!")
        st.rerun()

# --- MOSTRAR MENSAJES ---
st.subheader("Muro de la Comunidad")
df_msgs = leer_mensajes()

if not df_msgs.empty:
    for index, row in df_msgs.iterrows():
        st.markdown(f"""
        <div class="chat-card">
            <span class="chat-user">👤 {row['usuario_nombre']}</span>
            <span class="chat-date">{row['fecha']}</span>
            <div class="chat-msg">{row['mensaje']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Aún no hay comentarios. ¡Sé el primero en escribir!")

if st.button("🔄 Actualizar muro"):
    st.rerun()

# Footer Global
st.markdown("""
<div class="footer">
    <p>🦋 SayUniverse | Desarrollada por <b>Sharon Asprilla</b></p>
</div>
""", unsafe_allow_html=True)