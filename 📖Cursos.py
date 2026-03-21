import streamlit as st

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
                st.info(f"📘 {curso['nombre']} tiene {curso['clases']} clases en total.")
