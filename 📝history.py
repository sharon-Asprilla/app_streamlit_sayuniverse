import streamlit as st
from datetime import date

# Inicializar variables de sesión
if "historial" not in st.session_state:
    st.session_state.historial = []
if "certificados" not in st.session_state:
    st.session_state.certificados = {}

# Cursos por niveles
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
        {"nombre": "Inglés Avanzado 2", "descripcion": "Redacción de ensayos y artículos.", "fecha": "Inicio: 22 Abril 2026", "clases": 22}
    ]
}