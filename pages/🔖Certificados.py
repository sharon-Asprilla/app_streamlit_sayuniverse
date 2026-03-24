import streamlit as st
from datetime import date
import sqlite3

try:
    from fpdf import FPDF
except ImportError:
    st.error("Librería 'fpdf' no encontrada. Instálala con: pip install fpdf")
    st.stop()

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
    # --- GUARDAR EN BASE DE DATOS ---
    if st.session_state.get("logged_in"):
        try:
            conn = sqlite3.connect("academia.db")
            c = conn.cursor()
            c.execute("INSERT INTO historial (usuario_id, accion, fecha) VALUES (?, ?, ?)",
                      (st.session_state.user_info['id'], mensaje, str(date.today())))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error guardando historial: {e}")

# Función para generar el PDF
def generar_pdf(nombre, curso, nivel, duracion, fecha_inicio, fecha_fin):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Marco decorativo naranja
    pdf.set_line_width(2)
    pdf.set_draw_color(230, 126, 34) # Naranja SayUniverse
    pdf.rect(10, 10, 277, 190)
    
    # Títulos
    pdf.set_font("Arial", 'B', 40)
    pdf.set_text_color(230, 126, 34)
    pdf.set_y(40)
    pdf.cell(0, 15, "CERTIFICADO", 0, 1, 'C')
    
    pdf.set_font("Arial", '', 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 15, "DE FINALIZACIÓN", 0, 1, 'C')
    
    # Cuerpo
    pdf.ln(10)
    pdf.set_font("Arial", '', 14)
    pdf.cell(0, 10, "SayUniverse certifica que:", 0, 1, 'C')
    
    pdf.ln(5)
    pdf.set_font("Arial", 'BI', 30)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 15, nombre, 0, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Ha completado satisfactoriamente el curso:", 0, 1, 'C')
    
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(230, 126, 34)
    pdf.cell(0, 15, curso, 0, 1, 'C')
    
    # Detalles y Fechas
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, f"Nivel: {nivel}  |  Duración: {duracion}", 0, 1, 'C')
    
    # Fechas de inicio y fin
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 10, f"Fecha de Inicio: {fecha_inicio}   -   Fecha de Finalización: {fecha_fin}", 0, 1, 'C')
    
    # Firmas
    pdf.set_y(-50)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    
    y = pdf.get_y()
    pdf.line(60, y, 110, y)
    pdf.line(180, y, 230, y)
    
    pdf.ln(2)
    pdf.set_font("Arial", '', 10)
    pdf.cell(135, 5, "Firma del Instructor", 0, 0, 'C')
    pdf.cell(60, 5, "Director SayUniverse", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# Lista completa de cursos posibles (debe coincidir con cursos.py)
cursos_disponibles = [
    {"nombre": "Inglés Básico 1", "clases": 10, "nivel": "Básico"},
    {"nombre": "Inglés Básico 2", "clases": 12, "nivel": "Básico"},
    {"nombre": "Inglés Básico 3", "clases": 15, "nivel": "Básico"},
    {"nombre": "Inglés Intermedio 1", "clases": 14, "nivel": "Intermedio"},
    {"nombre": "Inglés Intermedio 2", "clases": 16, "nivel": "Intermedio"},
    {"nombre": "Inglés Intermedio 3", "clases": 18, "nivel": "Intermedio"},
    {"nombre": "Inglés Avanzado 1", "clases": 20, "nivel": "Avanzado"},
    {"nombre": "Inglés Avanzado 2", "clases": 22, "nivel": "Avanzado"},
    {"nombre": "Inglés Avanzado 3", "clases": 25, "nivel": "Avanzado"},
]

st.title("🎓 Certificados de Cursos")

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
    body, .stMarkdown, .stButton, .stTextInput, p, h1, h2, h3, h4, h5, h6, span, div, label {
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

# Verificar usuario y pruebas completadas
# --- SINCRONIZAR CON BASE DE DATOS ---
if st.session_state.get('logged_in'):
    try:
        conn = sqlite3.connect("academia.db")
        c = conn.cursor()
        user_id = st.session_state.user_info['id']
        # Buscar cursos completados en la BD
        c.execute("SELECT titulo FROM notas WHERE usuario_id = ? AND tipo = 'Curso' AND nota = '5.0/5.0'", (user_id,))
        db_aprobados = [row[0] for row in c.fetchall()]
        conn.close()
        
        # Actualizar la sesión para que el código de abajo los detecte
        for curso_nombre in db_aprobados:
            st.session_state[f"aprobado_{curso_nombre}"] = True
            st.session_state[f"completado_{curso_nombre}"] = True
    except Exception as e:
        st.error(f"Error sincronizando base de datos: {e}")
# -------------------------------------

if not st.session_state.get('logged_in'):
    st.warning("Debes iniciar sesión para ver tus certificados.")
else:
    certificado_generado = False
    nombre_alumno = st.session_state.get('usuario', 'Estudiante')
    
    for curso in cursos_disponibles:
        key_aprobado = f"aprobado_{curso['nombre']}"
        
        # Verificar si el curso fue aprobado y completado en la sesión
        if st.session_state.get(key_aprobado) and st.session_state.get(f"completado_{curso['nombre']}"):
            # Intentar obtener nivel de la sesión, si no, usar el de la lista
            nivel = st.session_state.get(f"nivel_{curso['nombre']}", curso.get("nivel", "Nivel Completado"))
            duracion = st.session_state.get(f"duracion_{curso['nombre']}", f"{curso['clases']} horas")
            certificado_generado = True
            
            certificado_html = f"""
            <div style='background: white; padding: 40px; border-radius: 10px; color: #333; font-family: "Georgia", serif; max-width: 800px; margin:auto; border: 10px solid #E67E22; text-align: center; box-shadow: 0 0 20px rgba(0,0,0,0.2);'>
                <div style='border-bottom: 2px solid #E67E22; padding-bottom: 20px; margin-bottom: 30px;'>
                    <h1 style='margin:0; font-size: 48px; color: #E67E22; text-transform: uppercase; letter-spacing: 5px;'>Certificado</h1>
                    <p style='font-size: 18px; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-top: 10px;'>De Finalización</p>
                </div>
                
                <div style='padding: 20px 0;'>
                    <p style='font-size: 20px; color: #555;'>Este documento certifica que</p>
                    <h2 style='font-size: 42px; color: #2C3E50; margin: 20px 0; font-style: italic;'>{nombre_alumno}</h2>
                    <p style='font-size: 20px; color: #555;'>Ha completado y aprobado satisfactoriamente el curso de:</p>
                    <h3 style='font-size: 32px; color: #E67E22; margin: 20px 0;'>{curso['nombre']}</h3>
                    <p style='font-size: 18px; color: #777;'>Nivel: <strong>{nivel}</strong> &nbsp;|&nbsp; Intensidad: <strong>{duracion}</strong></p>
                    <p style='font-size: 16px; color: #999; margin-top: 30px;'>Expedido el día: {date.today().strftime('%d de %B de %Y')}</p>
                </div>
                
                <div style='margin-top: 50px; display:flex; justify-content:space-around;'>
                    <div style='text-align:center;'>
                        <div style='border-bottom: 1px solid #333; width: 200px; margin: 0 auto 10px auto;'></div>
                        <p style='font-weight: bold; color: #333;'>Firma del Instructor</p>
                    </div>
                    <div style='text-align:center;'>
                        <div style='border-bottom: 1px solid #333; width: 200px; margin: 0 auto 10px auto;'></div>
                        <p style='font-weight: bold; color: #333;'>Director SayUniverse</p>
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

# Footer Global
st.markdown("""
<div class="footer">
    <p>🦋 SayUniverse | Desarrollada por <b>Sharon Asprilla</b></p>
</div>
""", unsafe_allow_html=True)
