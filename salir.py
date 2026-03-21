import streamlit as st

# Inicializar sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = None

# Función de login
def login(correo, password):
    if correo == "demo@correo.com" and password == "1234":
        st.session_state.autenticado = True
        st.session_state.usuario = correo
        return True
    return False

# Interfaz
if not st.session_state.autenticado:
    st.title("Login")
    correo = st.text_input("Correo")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if login(correo, password):
            st.success("Inicio de sesión exitoso")
        else:
            st.error("Credenciales incorrectas")
else:
    st.sidebar.success(f"Usuario: {st.session_state.usuario}")
    st.title("Dashboard")
    st.write("Aquí va tu contenido principal...")

    # Botón salir que reinicia la app
    if st.button("Salir"):
        # Reiniciar variables de sesión
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Forzar refresh
        st.experimental_rerun()
