import streamlit as st

st.set_page_config(
    page_title="Salir",
    page_icon="ð🚪",
    layout="centered"
)

st.title("Cerrar Sesión")

st.write("¿Estás seguro de que quieres salir?")

if st.button("Sí, cerrar sesión", type="primary"):
    # Clear all session state variables
    for key in st.session_state.keys():
        del st.session_state[key]
    
    # Rerun to reflect the cleared state and show the redirection message
    st.rerun()

# This part will be shown after the rerun
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.success("Has cerrado sesión exitosamente.")
    st.write("Serás redirigido a la página de inicio de sesión.")
    st.page_link("app.py", label="Ir a la página de inicio de sesión")
    st.markdown('<meta http-equiv="refresh" content="3;url=app.py">', unsafe_allow_html=True)

st.page_link("pages/cursos.py", label="Volver a los cursos")
