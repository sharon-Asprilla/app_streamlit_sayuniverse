import streamlit as st

# Estilos personalizados
st.markdown("""
    <style>
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
    .icon {
        font-size: 60px;
        color: white;
        margin-bottom: 10px;
    }
    .input-icon {
        position: absolute;
        margin-left: 10px;
        margin-top: 10px;
        color: #888;
    }
    .input-field {
        padding-left: 30px;
    }
    .login-button {
        background-color: #3498db;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        width: 100%;
        margin-top: 20px;
        font-size: 16px;
    }
    .login-footer {
        margin-top: 20px;
        font-size: 14px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Contenedor de login
st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.markdown("<div class='icon'>🖂</div>", unsafe_allow_html=True)
st.markdown("<div class='login-title'>Sign In</div>", unsafe_allow_html=True)

# Campos de entrada
usuario = st.text_input("Username", placeholder="Enter your email")
password = st.text_input("Password", type="password", placeholder="Enter your password")

# Botón de login
if st.button("LOGIN", use_container_width=True):
    st.success("Inicio de sesión exitoso")

# Footer
st.markdown("<div class='login-footer'>Recordarme | ¿Olvidaste tu contraseña?</div>", unsafe_allow_html=True)

# Botón de registro
if st.button("Registrarse", use_container_width=True):
    st.markdown("""
        <div style='text-align:center; margin-top:20px;'>
            <h4 style='color:white;'>Elige cómo registrarte</h4>
            <button style='padding:10px 20px; margin:10px; background:#DB4437; color:white; border:none; border-radius:6px;'>
                Iniciar con Google
            </button>
            <button style='padding:10px 20px; margin:10px; background:#2c3e50; color:white; border:none; border-radius:6px;'>
                Crear otra cuenta
            </button>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
