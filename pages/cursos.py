import streamlit as st
from datetime import date

# --- Authentication Check ---
# This must be at the top of every page in the `pages` directory
if not st.session_state.get("logged_in", False):
    st.error("Por favor, inicia sesión para acceder a esta página.")
    st.page_link("app.py", label="Ir a la página de inicio de sesión")
    st.stop()




st.markdown("<h1 style='text-align: center;'>🦋sayuniverse🦋</h1>", unsafe_allow_html=True)




st.title("Cursos")



    




# Inicializar historial en sesión
if "historial" not in st.session_state:
    st.session_state.historial = []

# Función para registrar procesos en historial
def registrar_proceso(mensaje):
    st.session_state.historial.append(f"{mensaje} ({date.today().strftime('%d/%m/%Y')})")

# Función para mostrar lección
def mostrar_leccion(curso, nivel):
    # Definir lecciones por nivel
    lecciones = {
        "Básico": {
            "tema": "Greetings and Introductions",
            "explicacion": """
            **Greetings and Introductions**  
            In English, greetings are important for polite communication.  
            - **Hello**: Used anytime.  
            - **Hi**: Informal.  
            - **Good morning/afternoon/evening**: Time-specific.  
            - Introductions: "My name is...", "Nice to meet you."  
            **Reading**: Read aloud to practice pronunciation.  
            **Writing**: Write a short introduction.  
            **Speaking**: Practice saying greetings.
            """,
            "preguntas": [
                {
                    "pregunta": "What do you say when you meet someone for the first time?",
                    "opciones": ["Goodbye", "Nice to meet you", "See you later"],
                    "correcta": "Nice to meet you",
                    "explicacion": "Correct: 'Nice to meet you' is used for introductions. Incorrect options are for leaving."
                },
                {
                    "pregunta": "How do you greet someone in the morning?",
                    "opciones": ["Good night", "Good morning", "Good evening"],
                    "correcta": "Good morning",
                    "explicacion": "Correct: 'Good morning' is for mornings. 'Good night' is for bedtime, 'Good evening' for evenings."
                },
                {
                    "pregunta": "What is the informal way to say hello?",
                    "opciones": ["Hello", "Hi", "Good day"],
                    "correcta": "Hi",
                    "explicacion": "Correct: 'Hi' is informal. 'Hello' is more formal, 'Good day' is less common."
                },
                {
                    "pregunta": "How do you introduce yourself?",
                    "opciones": ["My name is John", "I am John", "Hello, John"],
                    "correcta": "My name is John",
                    "explicacion": "Correct: 'My name is...' is standard. Others are incomplete."
                },
                {
                    "pregunta": "What do you say when leaving?",
                    "opciones": ["Hello", "Goodbye", "Nice to meet you"],
                    "correcta": "Goodbye",
                    "explicacion": "Correct: 'Goodbye' for leaving. 'Hello' for arriving, 'Nice to meet you' for introductions."
                }
            ]
        },
        "Intermedio": {
            "tema": "Past Simple Tense",
            "explicacion": """
            **Past Simple Tense**  
            Used for completed actions in the past.  
            - Regular: add -ed (walked, played).  
            - Irregular: go -> went, eat -> ate.  
            **Reading**: Read past tense stories.  
            **Writing**: Write about yesterday.  
            **Speaking**: Describe past events.
            """,
            "preguntas": [
                {
                    "pregunta": "What is the past of 'go'?",
                    "opciones": ["went", "gone", "going"],
                    "correcta": "went",
                    "explicacion": "Correct: 'went' is irregular past. 'Gone' is past participle, 'going' is present continuous."
                },
                {
                    "pregunta": "How do you form past simple for regular verbs?",
                    "opciones": ["Add -ing", "Add -ed", "No change"],
                    "correcta": "Add -ed",
                    "explicacion": "Correct: Add -ed for regular verbs. -ing is for continuous, no change for base form."
                },
                {
                    "pregunta": "Yesterday, I _____ to the store.",
                    "opciones": ["go", "went", "gone"],
                    "correcta": "went",
                    "explicacion": "Correct: 'went' for past action. 'Go' is present, 'gone' is participle."
                },
                {
                    "pregunta": "She _____ her homework last night.",
                    "opciones": ["do", "did", "done"],
                    "correcta": "did",
                    "explicacion": "Correct: 'did' is past of 'do'. 'Do' present, 'done' participle."
                },
                {
                    "pregunta": "They _____ the movie last week.",
                    "opciones": ["watch", "watched", "watching"],
                    "correcta": "watched",
                    "explicacion": "Correct: 'watched' regular past. 'Watch' present, 'watching' continuous."
                }
            ]
        },
        "Avanzado": {
            "tema": "English Idioms",
            "explicacion": """
            **English Idioms**  
            Idioms are expressions with figurative meaning.  
            - Break a leg: Good luck.  
            - Hit the books: Study.  
            **Reading**: Read texts with idioms.  
            **Writing**: Use idioms in sentences.  
            **Speaking**: Explain idiom meanings.
            """,
            "preguntas": [
                {
                    "pregunta": "What does 'break a leg' mean?",
                    "opciones": ["Be careful", "Good luck", "Have fun"],
                    "correcta": "Good luck",
                    "explicacion": "Correct: Means good luck, especially in performances. Not literal."
                },
                {
                    "pregunta": "What does 'hit the books' mean?",
                    "opciones": ["Read a book", "Study hard", "Buy books"],
                    "correcta": "Study hard",
                    "explicacion": "Correct: Means to study. 'Hit' implies striking, like hitting the books to study."
                },
                {
                    "pregunta": "What does 'piece of cake' mean?",
                    "opciones": ["Difficult", "Easy", "Boring"],
                    "correcta": "Easy",
                    "explicacion": "Correct: Means very easy. Like eating cake."
                },
                {
                    "pregunta": "What does 'kick the bucket' mean?",
                    "opciones": ["Die", "Dance", "Sleep"],
                    "correcta": "Die",
                    "explicacion": "Correct: Euphemism for die. Not literal."
                },
                {
                    "pregunta": "What does 'spill the beans' mean?",
                    "opciones": ["Cook beans", "Tell a secret", "Drop food"],
                    "correcta": "Tell a secret",
                    "explicacion": "Correct: Means to reveal a secret. 'Spill' like spilling beans."
                }
            ]
        }
    }
    
    if nivel not in lecciones:
        st.error("Lección no disponible para este nivel.")
        return
    
    leccion = lecciones[nivel]
    
    with st.expander(f"📖 Lección: {leccion['tema']} - {curso['nombre']}", expanded=True):
        st.markdown(leccion['explicacion'])
        
        # Inicializar respuestas en session_state si no existe
        key_respuestas = f"respuestas_{curso['nombre']}"
        if key_respuestas not in st.session_state:
            st.session_state[key_respuestas] = [None] * len(leccion['preguntas'])
        
        # Mostrar preguntas
        for i, p in enumerate(leccion['preguntas']):
            st.markdown(f"**Pregunta {i+1}:** {p['pregunta']}")
            st.session_state[key_respuestas][i] = st.radio(
                f"Opción para pregunta {i+1}", 
                p['opciones'], 
                index=p['opciones'].index(st.session_state[key_respuestas][i]) if st.session_state[key_respuestas][i] in p['opciones'] else 0,
                key=f"q_{i}_{curso['nombre']}"
            )
        
        # Botón Verificar
        if st.button("Verificar Respuestas", key=f"verificar_{curso['nombre']}"):
            st.session_state[f"submitted_{curso['nombre']}"] = True
            st.session_state[f"presentado_{curso['nombre']}"] = True
        
        # Mostrar resultados si submitted
        if st.session_state.get(f"submitted_{curso['nombre']}", False):
            st.markdown("### Resultados:")
            correctas = 0
            for i, p in enumerate(leccion['preguntas']):
                if st.session_state[key_respuestas][i] == p['correcta']:
                    st.success(f"✅ Pregunta {i+1}: Correcta - Verdadera")
                    correctas += 1
                else:
                    st.error(f"❌ Pregunta {i+1}: Incorrecta - Falsa. Elegiste '{st.session_state[key_respuestas][i]}'. La correcta es '{p['correcta']}'")
                st.info(f"Explicación: {p['explicacion']}")
            st.markdown(f"**Puntuación: {correctas}/5**")
            
            if correctas == 5:
                st.progress(1.0)
                st.success("🎉 ¡Curso aprobado! Puedes finalizar.")
                st.session_state[f"aprobado_{curso['nombre']}"] = True
                st.session_state[f"nivel_{curso['nombre']}"] = nivel
                st.session_state[f"duracion_{curso['nombre']}"] = f"{curso['clases']} horas"
                if st.button("Terminar Intento", key=f"terminar_{curso['nombre']}"):
                    st.session_state[f"completado_{curso['nombre']}"] = True
                    st.rerun()
            else:
                # Retroalimentación general
                if correctas >= 4:
                    st.warning("¡Muy bien! Casi perfecto. Estudia un poco más para reforzar.")
                elif correctas >= 3:
                    st.info("Bien, pero necesitas estudiar más. Revisa las explicaciones.")
                else:
                    st.error("Necesitas estudiar mucho más. Relee la explicación del tema.")
                
                if st.button("Intentar de Nuevo", key=f"reintentar_{curso['nombre']}"):
                    st.session_state[key_respuestas] = [None] * len(leccion['preguntas'])
                    st.session_state[f"submitted_{curso['nombre']}"] = False
                    st.rerun()

# Estilos personalizados
st.markdown("""
    <style>
    .titulo {
        text-align: center;
        font-size: 36px;
        color: #E67E22;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .subtitulo {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 40px;
    }
    .card {
        background-color: #FDEBD0; /* naranja muy pálido */
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .card h3 {
        color: #D35400;
        margin-bottom: 10px;
    }
    .card p {
        color: #333;
        font-size: 15px;
    }
    .fecha {
        font-size: 14px;
        color: #555;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<div class='titulo'>Cursos de Inglés por Niveles</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Selecciona tu nivel y comienza tu aprendizaje</div>", unsafe_allow_html=True)

# Cursos por niveles con fecha y número de clases
cursos = {
    "Básico": [
        {"nombre": "Inglés Básico 1", "descripcion": "Saludos y vocabulario esencial.", "fecha": "Inicio: 5 Abril 2026", "clases": 10},
        {"nombre": "Inglés Básico 2", "descripcion": "Frases comunes y diálogos simples.", "fecha": "Inicio: 12 Abril 2026", "clases": 12},
        {"nombre": "Inglés Básico 3", "descripcion": "Gramática inicial y conversación.", "fecha": "Inicio: 20 Abril 2026", "clases": 15}
    ],
    "Intermedio": [
        {"nombre": "Inglés Intermedio 1", "descripcion": "Gramática avanzada y tiempos verbales.", "fecha": "Inicio: 10 Abril 2026", "clases": 14},
        {"nombre": "Inglés Intermedio 2", "descripcion": "Comprensión de textos y conversaciones.", "fecha": "Inicio: 18 Abril 2026", "clases": 16},
        {"nombre": "Inglés Intermedio 3", "descripcion": "Escritura básica y práctica oral.", "fecha": "Inicio: 25 Abril 2026", "clases": 18}
    ],
    "Avanzado": [
        {"nombre": "Inglés Avanzado 1", "descripcion": "Conversaciones complejas y vocabulario académico.", "fecha": "Inicio: 15 Abril 2026", "clases": 20},
        {"nombre": "Inglés Avanzado 2", "descripcion": "Redacción de ensayos y artículos.", "fecha": "Inicio: 22 Abril 2026", "clases": 22},
        {"nombre": "Inglés Avanzado 3", "descripcion": "Inglés profesional y presentaciones.", "fecha": "Inicio: 30 Abril 2026", "clases": 25}
    ]
}

# Mostrar cursos por nivel
for nivel, lista in cursos.items():
    st.markdown(f"## {nivel}")
    for curso in lista:
        with st.container():
            st.markdown(f"<div class='card'><h3>{curso['nombre']}</h3><p>{curso['descripcion']}</p><div class='fecha'>{curso['fecha']}</div></div>", unsafe_allow_html=True)
            if st.button(f"Empezar {curso['nombre']}", key=curso['nombre']):
                registrar_proceso(f"Empezó el curso: {curso['nombre']}")
                mostrar_leccion(curso, nivel)


