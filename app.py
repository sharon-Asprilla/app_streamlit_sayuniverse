import streamlit as st
import sqlite3
import pandas as pd
from datetime import date


# --- Database Functions ---
def init_db():
    conn = sqlite3.connect("academia.db")
    c = conn.cursor()
    # Crear tabla de notas si no existe
    c.execute("""CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tipo TEXT,
        titulo TEXT,
        nota TEXT,
        fecha TEXT
    )""")
    # Crear tabla de historial si no existe
    c.execute("""CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        accion TEXT,
        fecha TEXT
    )""")
    conn.commit()
    return conn

def check_user(conn, email):
    df = pd.read_sql(f"SELECT * FROM usuarios WHERE correo='{email}'", conn)
    return not df.empty

def get_user(conn, email):
    df = pd.read_sql(f"SELECT * FROM usuarios WHERE correo='{email}'", conn)
    return df.iloc[0]

def update_password(conn, email, new_password):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE usuarios SET password = '{new_password}' WHERE correo = '{email}'")
    conn.commit()

def register_user(conn, nombre, email, password):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, correo, password, fecha_registro) VALUES (?, ?, ?, ?)", (nombre, email, password, str(date.today())))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None

# --- Page Configuration ---
st.set_page_config(
    page_title="SayUniverse",
    page_icon="ð🌠",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- Main App Logic ---

# If logged in, show a welcome message and redirect.
if st.session_state.logged_in:
    st.switch_page("pages/cursos.py")


# --- Login UI ---
st.markdown("""
    <style>
    /* Add your custom CSS from login.py here */
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Arial', sans-serif !important;
    }
    /* Forzar Arial en todos los componentes */
    .stMarkdown, .stButton, .stTextInput, p, h1, h2, h3 {
        font-family: 'Arial', sans-serif !important;
    }
    .login-box {
        width: 100%;
        max-width: 420px;
        margin: auto;
        margin-top: 30px;
        text-align: center;
    }
    .login-title {
        font-size: 22px;
        color: white;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .logo-container {
        font-size: 60px;
        font-weight: bold;
        background: -webkit-linear-gradient(#F39C12, #E67E22);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    /* Estilos para los tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }
    /* Hide sidebar for login page */
    [data-testid="stSidebar"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0f2027;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 100;
        border-top: 1px solid #E67E22;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.markdown("<div class='logo-container'>🦋 SayUniverse</div>", unsafe_allow_html=True)
st.markdown("<div class='login-title'>Plataforma Académica</div>", unsafe_allow_html=True)

conn = init_db()

tab_login, tab_register = st.tabs(["Iniciar Sesión", "Registrarse"])

with tab_login:
    with st.form("login_form"):
        email = st.text_input("Correo Electrónico", placeholder="Ingresa tu correo")
        password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        if check_user(conn, email):
            user_data = get_user(conn, email)
            if user_data['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user_info = user_data
                st.switch_page("pages/cursos.py")
            else:
                st.error("Contraseña incorrecta.")
        else:
            st.error("Usuario no encontrado.")

    with st.expander("¿Olvidaste tu contraseña?"):
        with st.form("change_pass_form"):
            email_change = st.text_input("Confirma tu correo")
            new_pass = st.text_input("Nueva contraseña", type="password")
            if st.form_submit_button("Actualizar"):
                if check_user(conn, email_change):
                    update_password(conn, email_change, new_pass)
                    st.success("Contraseña actualizada.")
                else:
                    st.error("El correo no existe.")

with tab_register:
    with st.form("register_form"):
        reg_name = st.text_input("Nombre Completo")
        reg_email = st.text_input("Correo Electrónico")
        reg_password = st.text_input("Contraseña", type="password")
        submitted_reg = st.form_submit_button("Crear Cuenta")
    
    if submitted_reg:
        if reg_name and reg_email and reg_password:
            if register_user(conn, reg_name, reg_email, reg_password):
                st.success("¡Cuenta creada! Ingresando...")
                st.session_state.logged_in = True
                st.session_state.user_info = get_user(conn, reg_email)
                st.switch_page("pages/cursos.py")
            else:
                st.error("El correo ya está registrado.")
        else:
            st.warning("Completa todos los campos.")

# Close the login box div
st.markdown("</div>", unsafe_allow_html=True)

conn.close()

# Footer Global
st.markdown("""
<div class="footer">
    <p>🦋 SayUniverse | Desarrollada por <b>Sharon Asprilla</b></p>
</div>
""", unsafe_allow_html=True)
