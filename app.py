import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- Database Functions ---
def init_db():
    conn = sqlite3.connect("academia.db")
    return conn

def check_user(conn, email):
    df = pd.read_sql(f"SELECT * FROM usuarios WHERE correo='{email}'", conn)
    return not df.empty

def get_user(conn, email):
    df = pd.read_sql(f"SELECT * FROM usuarios WHERE correo='{email}'", conn)
    return df.iloc[0]

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
    st.success(f"Bienvenido de nuevo, {st.session_state.user_info['nombre']}!")
    st.write("Serás redirigido a la página de cursos en un momento.")
    # Use a meta refresh tag for redirection as st.switch_page can be buggy in the main script
    st.markdown('<meta http-equiv="refresh" content="3;url=Cursos">', unsafe_allow_html=True)
    st.page_link("pages/cursos.py", label="O haz clic aquí si no eres redirigido")
    st.stop()


# --- Login UI ---
st.markdown("""
    <style>
    /* Add your custom CSS from login.py here */
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 20px;
        width: 400px;
        margin: auto;
        margin-top: 50px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        text-align: center;
    }
    .login-title {
        font-size: 28px;
        color: white;
        margin-bottom: 20px;
    }
    /* Hide sidebar for login page */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.markdown("<div class='login-title'>Iniciar Sesión</div>", unsafe_allow_html=True)

conn = init_db()

with st.form("login_form"):
    email = st.text_input("Correo Electrónico", placeholder="Ingresa tu correo")
    password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
    submitted = st.form_submit_button("Entrar")

    if submitted:
        if check_user(conn, email):
            user_data = get_user(conn, email)
            # NOTE: Storing passwords in plain text is highly insecure.
            # This should be replaced with hashed password verification.
            if user_data['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user_info = user_data
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
        else:
            st.error("Usuario no encontrado. Por favor, regístrese.")

# --- Registration Section ---
st.markdown("<div style='margin-top: 20px;'>¿No tienes una cuenta?</div>", unsafe_allow_html=True)

if st.button("Registrarse con Google", use_container_width=True):
    # This part will be implemented later with an OAuth library
    st.info("La funcionalidad de registro con Google se implementará pronto.")

# Close the login box div
st.markdown("</div>", unsafe_allow_html=True)

conn.close()
