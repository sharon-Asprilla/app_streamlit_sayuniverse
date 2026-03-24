import streamlit as st
from datetime import date
import sqlite3
import pandas as pd

# --- Authentication Check ---
if not st.session_state.get("logged_in", False):
    st.error("Por favor, inicia sesión para acceder a esta página.")
    st.page_link("app.py", label="Ir a la página de inicio de sesión")
    st.stop()

# Importar función de SMS desde alerts.py
try:
    from alerts import enviar_sms
    SMS_DISPONIBLE = True
except:
    SMS_DISPONIBLE = False

# Protección contra copias y capturas de pantalla
st.markdown("""
<style>
    body {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
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
    body, .stMarkdown, .stButton, .stTextInput, p, h1, h2, h3, h4, h5, h6, span, div, label, .stRadio div {
        color: black !important;
    }
    [data-testid="stSidebar"] {
        background-color: #E67E22;
    }
    .stMarkdown, .stRadio, .stExpander {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
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
<script>
    // Bloquear click derecho
    document.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        alert('⚠️ No se permite copiar o capturar pantalla durante el examen.');
        return false;
    });
    
    // Bloquear atajos de teclado
    document.addEventListener('keydown', function(event) {
        // Ctrl+C, Ctrl+X, Ctrl+S
        if ((event.ctrlKey || event.metaKey) && (event.key === 'c' || event.key === 'x' || event.key === 's')) {
            event.preventDefault();
            alert('⚠️ No se permite copiar contenido durante el examen.');
            return false;
        }
        // F12 (Developer Tools)
        if (event.key === 'F12') {
            event.preventDefault();
            alert('⚠️ Las herramientas de desarrollo están deshabilitadas.');
            return false;
        }
        // Ctrl+Shift+C (Inspect Element)
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'C') {
            event.preventDefault();
            return false;
        }
        // PrintScreen
        if (event.key === 'PrintScreen') {
            event.preventDefault();
            alert('⚠️ Captura de pantalla bloqueada. No puedes presentar el examen.');
            return false;
        }
    });
    
    // Bloquear selección de texto
    document.addEventListener('selectstart', function(event) {
        event.preventDefault();
        return false;
    });
</script>
""", unsafe_allow_html=True)

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

# Definir preguntas para cada nivel
preguntas_basico = [
    {"pregunta": "What is the result of 2 + 2?", "opciones": ["3", "4", "5", "6"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the color of the sky on a clear day?", "opciones": ["Red", "Blue", "Green", "Yellow"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "How many days does a week have?", "opciones": ["5", "6", "7", "8"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "What is the plural of 'cat'?", "opciones": ["Cats", "Gates", "Cat", "Cats"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "What animal is known as the 'king of the jungle'?", "opciones": ["Elephant", "Lion", "Tiger", "Bear"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the next number after 9?", "opciones": ["8", "10", "11", "12"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What fruit is yellow and curved?", "opciones": ["Apple", "Banana", "Orange", "Pear"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "How many hours does a day have?", "opciones": ["12", "24", "36", "48"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the opposite of 'hot'?", "opciones": ["Cold", "Warm", "Mild", "Cool"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "What do you use to write?", "opciones": ["Pencil", "Knife", "Fork", "Plate"], "puntuaciones": [4, 1, 2, 3]}
]

preguntas_intermedio = [
    {"pregunta": "What is the capital of France?", "opciones": ["London", "Paris", "Rome", "Madrid"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What gas do we breathe mainly?", "opciones": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "How many planets are there in the solar system?", "opciones": ["7", "8", "9", "10"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the longest river in the world?", "opciones": ["Amazon", "Nile", "Yangtze", "Mississippi"], "puntuaciones": [2, 4, 1, 3]},
    {"pregunta": "What does 'www' mean in a web address?", "opciones": ["World Wide Web", "Web World Wide", "Wide World Web", "Web Wide World"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "What is the chemical symbol of water?", "opciones": ["H2O", "CO2", "O2", "NaCl"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "In what year did man land on the moon?", "opciones": ["1965", "1969", "1972", "1975"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the official language of Brazil?", "opciones": ["Spanish", "Portuguese", "English", "French"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What part of the body pumps blood?", "opciones": ["Lung", "Liver", "Heart", "Kidney"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "What is the largest continent?", "opciones": ["Africa", "Asia", "America", "Europe"], "puntuaciones": [1, 4, 2, 3]}
]

preguntas_avanzado = [
    {"pregunta": "What is the speed of light in a vacuum?", "opciones": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "Who wrote 'Don Quixote'?", "opciones": ["Cervantes", "Shakespeare", "Dante", "Goethe"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "What is the Pythagorean theorem?", "opciones": ["a² + b² = c²", "a + b = c", "a² - b² = c²", "a × b = c²"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "What element has atomic number 1?", "opciones": ["Helium", "Hydrogen", "Lithium", "Beryllium"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the chemical formula of methane?", "opciones": ["CH4", "CO2", "H2O", "NH3"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "In what year did World War I begin?", "opciones": ["1912", "1914", "1916", "1918"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "What is the square root of 144?", "opciones": ["10", "12", "14", "16"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "Which philosopher said 'I think, therefore I am'?", "opciones": ["Plato", "Aristotle", "Descartes", "Kant"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "What is the largest ocean?", "opciones": ["Atlantic", "Indian", "Arctic", "Pacific"], "puntuaciones": [1, 2, 3, 4]},
    {"pregunta": "What subatomic particle has a positive charge?", "opciones": ["Electron", "Neutron", "Proton", "Photon"], "puntuaciones": [1, 2, 4, 3]}
]

# Preguntas de Inglés - Nivel Básico (Presente - To Be)
english_basico = [
    {"pregunta": "Complete: I _____ a student.", "opciones": ["are", "am", "is", "be"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "Complete: She _____ a teacher.", "opciones": ["am", "are", "is", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: They _____ happy.", "opciones": ["is", "am", "are", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: You _____ a good friend.", "opciones": ["is", "am", "are", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: He _____ my brother.", "opciones": ["are", "am", "is", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: We _____ engineers.", "opciones": ["is", "am", "are", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: It _____ a nice day.", "opciones": ["are", "am", "is", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: The cat _____ black.", "opciones": ["are", "am", "is", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: I _____ from London.", "opciones": ["is", "are", "am", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: Mary and John _____ cousins.", "opciones": ["is", "am", "are", "be"], "puntuaciones": [1, 2, 4, 3]}
]

# Preguntas de Inglés - Nivel Intermedio (Pasado y preguntas)
english_intermedio = [
    {"pregunta": "Complete: She _____ a doctor last year. (pasado)", "opciones": ["be", "are", "were", "was"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: They _____ not at home yesterday.", "opciones": ["was", "were", "am", "is"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "Complete: _____ you at the party last night?", "opciones": ["Are", "Was", "Were", "Is"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "Complete: I _____ not happy about that decision.", "opciones": ["is", "was", "were", "am"], "puntuaciones": [1, 2, 3, 4]},
    {"pregunta": "Complete: The students _____ very excited about the trip.", "opciones": ["was", "is", "are", "be"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: _____ she ready for the exam?", "opciones": ["Are", "Am", "Was", "Is"], "puntuaciones": [1, 2, 3, 4]},
    {"pregunta": "Complete: We _____ not in the office last Monday.", "opciones": ["was", "are", "were", "is"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: The weather _____ terrible yesterday.", "opciones": ["are", "were", "was", "is"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: _____ they happy with the results?", "opciones": ["Are", "Is", "Was", "Were"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "Complete: It _____ a beautiful morning when we arrived.", "opciones": ["are", "is", "were", "was"], "puntuaciones": [1, 2, 3, 4]}
]

# Preguntas de Inglés - Nivel Avanzado (Expresiones complejas)
english_avanzado = [
    {"pregunta": "Complete: If I _____ you, I would accept the job offer.", "opciones": ["am", "was", "were", "is"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: I wish the weather _____ better today.", "opciones": ["is", "am", "was", "were"], "puntuaciones": [1, 2, 3, 4]},
    {"pregunta": "Complete: By next year, she will _____ the CEO of the company.", "opciones": ["be", "been", "being", "am"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "Complete: It seems as if there _____ a problem with the system.", "opciones": ["is not", "are not", "was not", "were not"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "Complete: Whether the project succeeds or not, it _____ a learning experience.", "opciones": ["was", "is", "were", "am"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "Complete: I'd rather _____ patient and wait for the right moment.", "opciones": ["am", "be", "is", "are"], "puntuaciones": [1, 4, 2, 3]},
    {"pregunta": "Complete: The issue is that there _____ not enough resources available.", "opciones": ["am", "is", "are", "were"], "puntuaciones": [1, 2, 4, 3]},
    {"pregunta": "Complete: Should life _____ so complicated?", "opciones": ["be", "am", "is", "are"], "puntuaciones": [4, 1, 2, 3]},
    {"pregunta": "Complete: All things considered, this _____ the best solution.", "opciones": ["are", "am", "were", "is"], "puntuaciones": [1, 2, 3, 4]},
    {"pregunta": "Complete: It's important that he _____ present at the meeting tomorrow.", "opciones": ["am", "are", "is", "be"], "puntuaciones": [1, 2, 3, 4]}
]



# Sección de pruebas
st.subheader("📝 Presentar Prueba")
col1, col2 = st.columns(2)
with col1:
    materia = st.selectbox("Selecciona la materia:", ["Español", "Inglés"])
with col2:
    nivel = st.selectbox("Selecciona el nivel de la prueba:", ["Básico", "Intermedio", "Avanzado"])

if st.button("Presentar Prueba"):
    st.session_state.presentar_prueba = True
    st.session_state.materia_seleccionada = materia
    st.session_state.nivel_seleccionado = nivel
    registrar_proceso(f"Prueba presentada en {materia} nivel {nivel}")
    st.rerun()

if "presentar_prueba" in st.session_state and st.session_state.presentar_prueba:
    if st.session_state.materia_seleccionada == "Español":
        if st.session_state.nivel_seleccionado == "Básico":
            preguntas = preguntas_basico
        elif st.session_state.nivel_seleccionado == "Intermedio":
            preguntas = preguntas_intermedio
        else:
            preguntas = preguntas_avanzado
    else:  # Inglés
        if st.session_state.nivel_seleccionado == "Básico":
            preguntas = english_basico
        elif st.session_state.nivel_seleccionado == "Intermedio":
            preguntas = english_intermedio
        else:
            preguntas = english_avanzado
    
    with st.form("prueba_form"):
        st.subheader(f"Prueba de {st.session_state.materia_seleccionada} - Nivel {st.session_state.nivel_seleccionado}")
        respuestas = []
        for i, q in enumerate(preguntas, 1):
            with st.expander(f"{i}. {q['pregunta']}"):
                respuesta = st.radio(f"Selecciona tu respuesta", q['opciones'], key=f"q{i}_{st.session_state.materia_seleccionada}_{st.session_state.nivel_seleccionado}")
                idx = q['opciones'].index(respuesta)
                respuestas.append(q['puntuaciones'][idx])
        
        submitted = st.form_submit_button("Enviar Prueba")
        if submitted:
            promedio = sum(respuestas) / len(respuestas)
            st.success(f"Prueba completada. Tu promedio es: {promedio:.2f}/4")
            mensaje_registro = f"Prueba de {st.session_state.materia_seleccionada} nivel {st.session_state.nivel_seleccionado} completada con promedio {promedio:.2f}"
            
            # 1. Guardar en Historial de Movimientos
            registrar_proceso(mensaje_registro)
            
            # 2. Guardar en Notas (Base de Datos)
            try:
                conn = sqlite3.connect("academia.db")
                c = conn.cursor()
                user_id = st.session_state.user_info['id']
                c.execute("INSERT INTO notas (usuario_id, tipo, titulo, nota, fecha) VALUES (?, ?, ?, ?, ?)",
                          (user_id, "Prueba", f"{st.session_state.materia_seleccionada} - {st.session_state.nivel_seleccionado}", f"{promedio:.2f}/4", str(date.today())))
                conn.commit()
                conn.close()
                st.toast("✅ Calificación guardada en tu panel de Notas.")
            except Exception as e:
                st.error(f"Error al guardar nota: {e}")
            # --------------------------------
            
            # 📱 ENVÍO AUTOMÁTICO DE SMS (sin botón)
            if SMS_DISPONIBLE:
                sms_mensaje = f"📊 Completaste una prueba de {st.session_state.materia_seleccionada} ({st.session_state.nivel_seleccionado}) con promedio {promedio:.2f}/4."
                enviar_sms(sms_mensaje)
            
            st.session_state.presentar_prueba = False
            st.rerun()



# Sección de entrega de actividades
st.subheader("📂 Submit Activities")
archivo = st.file_uploader("Upload your activity in PDF or Word", type=["pdf", "docx"])
if archivo is not None:
    if st.button("Submit activity"):
        st.success(f"Activity '{archivo.name}' submitted successfully")
        mensaje_registro = f"Activity submitted: {archivo.name}"
        registrar_proceso(mensaje_registro)
        
        # --- GUARDAR EN BASE DE DATOS ---
        try:
            conn = sqlite3.connect("academia.db")
            c = conn.cursor()
            user_id = st.session_state.user_info['id']
            c.execute("INSERT INTO notas (usuario_id, tipo, titulo, nota, fecha) VALUES (?, ?, ?, ?, ?)",
                      (user_id, "Actividad", archivo.name, "Entregado", str(date.today())))
            conn.commit()
            conn.close()
            st.toast("✅ Entrega registrada en tu panel de Notas.")
        except Exception as e:
            st.error(f"Error al guardar actividad: {e}")
        # --------------------------------
        
        # 📱 ENVÍO AUTOMÁTICO DE SMS (sin botón)
        if SMS_DISPONIBLE:
            sms_mensaje = f"📄 Entregaste una actividad: {archivo.name}"
            enviar_sms(sms_mensaje)

# --- PROGRESO GENERAL DEL ESTUDIANTE ---
st.markdown("---")
st.subheader("📊 Tu Progreso Global")

try:
    conn = sqlite3.connect("academia.db")
    c = conn.cursor()
    
    # 1. Calcular Total de Cursos
    # Intentamos contar desde la tabla 'cursos'. Si no existe o está vacía, asumimos 9 (3 niveles x 3 cursos)
    try:
        c.execute("SELECT COUNT(*) FROM cursos")
        total_db = c.fetchone()[0]
        total_cursos = total_db if total_db > 0 else 9
    except sqlite3.OperationalError:
        total_cursos = 9 # Fallback si la tabla cursos no está creada aún
    
    # 2. Calcular Cursos Aprobados (Nota 5.0/5.0)
    user_id = st.session_state.user_info['id']
    c.execute("SELECT COUNT(DISTINCT titulo) FROM notas WHERE usuario_id=? AND tipo='Curso' AND nota='5.0/5.0'", (user_id,))
    aprobados = c.fetchone()[0]
    
    conn.close()
    
    # 3. Mostrar Barra
    progreso = min(aprobados / total_cursos, 1.0) # Asegurar que no pase de 100%
    st.progress(progreso)
    st.write(f"Has completado **{aprobados}** de **{total_cursos}** cursos disponibles ({int(progreso * 100)}%).")
    
    if progreso == 1.0:
        st.balloons()
        st.success("¡Felicidades! Has completado todo el plan de estudios.")

except Exception as e:
    st.error(f"Error calculando progreso: {e}")

# Historial de procesos
st.markdown("---")
st.subheader("📂 Historial de Movimientos")

# Cargar historial desde la base de datos
try:
    conn = sqlite3.connect("academia.db")
    user_id = st.session_state.user_info['id']
    df_hist = pd.read_sql(f"SELECT fecha, accion FROM historial WHERE usuario_id={user_id} ORDER BY id DESC LIMIT 20", conn)
    conn.close()
    
    if not df_hist.empty:
        for index, row in df_hist.iterrows():
            st.text(f"📅 {row['fecha']} - {row['accion']}")
    else:
        st.info("No hay movimientos registrados aún.")
except Exception as e:
    st.error(f"Error cargando historial: {e}")

# Footer Global
st.markdown("""
<div class="footer">
    <p>🦋 SayUniverse | Desarrollada por <b>Sharon Asprilla</b></p>
</div>
""", unsafe_allow_html=True)
    