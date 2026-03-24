import streamlit as st
from datetime import date

# --- Authentication Check ---
if not st.session_state.get("logged_in", False):
    st.error("Por favor, inicia sesión para acceder a esta página.")
    st.page_link("app.py", label="Ir a la página de inicio de sesión")
    st.stop()

# Inicializar certificados en la sesión
if "certificados" not in st.session_state:
    st.session_state.certificados = {}

# Inicializar historial en sesión
if "historial" not in st.session_state:
    st.session_state.historial = []

# Función para registrar procesos en historial
def registrar_proceso(mensaje):
    st.session_state.historial.append(f"{mensaje} ({date.today().strftime('%d/%m/%Y')})")

# Lista completa de cursos posibles (debe coincidir con cursos.py)
cursos_disponibles = [
    {"nombre": "Inglés Básico 1", "clases": 10},
    {"nombre": "Inglés Básico 2", "clases": 12},
    {"nombre": "Inglés Básico 3", "clases": 15},
    {"nombre": "Inglés Intermedio 1", "clases": 14},
    {"nombre": "Inglés Intermedio 2", "clases": 16},
    {"nombre": "Inglés Intermedio 3", "clases": 18},
    {"nombre": "Inglés Avanzado 1", "clases": 20},
    {"nombre": "Inglés Avanzado 2", "clases": 22},
    {"nombre": "Inglés Avanzado 3", "clases": 25},
]

st.title("🎓 Certificados de Cursos")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #E67E22;
    }
    </style>
""", unsafe_allow_html=True)

# Verificar usuario y pruebas completadas
if not st.session_state.get('logged_in'):
    st.warning("Debes iniciar sesión para ver tus certificados.")
else:
    certificado_generado = False
    nombre_alumno = st.session_state.get('usuario', 'Estudiante')
    
    for curso in cursos_disponibles:
        key_aprobado = f"aprobado_{curso['nombre']}"
        
        # Verificar si el curso fue aprobado y completado en la sesión
        if st.session_state.get(key_aprobado) and st.session_state.get(f"completado_{curso['nombre']}"):
            nivel = st.session_state.get(f"nivel_{curso['nombre']}", "Desconocido")
            duracion = st.session_state.get(f"duracion_{curso['nombre']}", f"{curso['clases']} horas")
            certificado_generado = True
            
            certificado_html = f"""
            <div style='background: radial-gradient(circle, #000000 0%, #0d0d0d 60%, #000000 100%); padding: 30px; border-radius: 20px; color: white; font-family: Arial, sans-serif; max-width: 850px; margin:auto; border: 2px solid gold;'>
                <div style='text-align:center; padding: 15px; color: #f3d86b;'>
                    <h1 style='margin:0; font-size: 56px; font-weight: 900;'>CERTIFICADO</h1>
                    <p style='font-size: 20px; margin-top: 5px;'>DE RECONOCIMIENTO</p>
                </div>
                <div style='margin-top: 20px;'>
                    <p style='color:#cccccc; font-size: 18px;'>SayUniverse certifica que</p>
                    <h2 style='margin: 0; font-size: 44px; color: #ffffff;'>{nombre_alumno}</h2>
                    <p style='color:#f3d86b; font-size: 18px;'>ha completado satisfactoriamente el curso</p>
                    <h3 style='margin: 5px 0 15px 0; font-size: 30px; color:#ffffff;'>{curso['nombre']}</h3>
                    <p style='color:#ffffff; font-size: 16px;'>Nivel de certificación: <strong>{nivel}</strong></p>
                    <p style='color:#ffffff; font-size: 16px;'>Duración de la formación: <strong>{duracion}</strong></p>
                    <p style='color:#ffffff; font-size: 16px;'>Fecha: <strong>{date.today().strftime('%d/%m/%Y')}</strong></p>
                </div>
                <div style='margin-top: 30px; display:flex; justify-content:space-between;'>
                    <div style='text-align:center;'>
                        <p style='color:#ffffff; margin-bottom:60px;'>______________________</p>
                        <p style='color:#ffffff;'>Firma</p>
                    </div>
                    <div style='text-align:center;'>
                        <p style='color:#ffffff; margin-bottom:60px;'>______________________</p>
                        <p style='color:#ffffff;'>Director SayUniverse</p>
                    </div>
                </div>
            </div>
            """
            st.markdown(certificado_html, unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Descargar certificado estilizado",
                data=certificado_html,
                file_name=f"certificado_{curso['nombre'].replace(' ','_')}_{nombre_alumno.replace(' ','_')}.html",
                mime="text/html"
            )

    if not certificado_generado:
        st.info("No tienes certificados disponibles aún. Completa y aprueba un curso (5/5 respuestas correctas) para obtener tu certificado.")

# Mostrar certificados guardados en sesión
st.markdown("---")
st.subheader("📂 Certificados guardados en tu sesión")
for nombre, contenido in st.session_state.certificados.items():
    st.text(f"- {nombre}")
