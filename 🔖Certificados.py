import streamlit as st
from datetime import date

# Inicializar certificados en la sesión
if "certificados" not in st.session_state:
    st.session_state.certificados = {}

# Simulación de cursos terminados
cursos_terminados = [
    {"nombre": "Inglés Básico 1", "clases": 10},
    {"nombre": "Inglés Intermedio 2", "clases": 16},
]

st.title("🎓 Certificados de Cursos")

# Mostrar cursos terminados
for curso in cursos_terminados:
    st.subheader(curso["nombre"])
    st.write(f"Este curso tiene {curso['clases']} clases. ¡Ya lo completaste!")

    if st.button(f"Generar certificado de {curso['nombre']}", key=curso['nombre']):
        # Crear contenido del certificado
        certificado_texto = f"""
        CERTIFICADO DE FINALIZACIÓN

        Se otorga a: {st.session_state.get('usuario','Estudiante')}
        Por haber completado satisfactoriamente el curso:
        {curso['nombre']}
        Número de clases: {curso['clases']}
        Fecha: {date.today().strftime('%d/%m/%Y')}
        """

        # Guardar en sesión
        st.session_state.certificados[curso["nombre"]] = certificado_texto

        # Mostrar certificado
        st.success("🎉 ¡Certificado generado!")
        st.text(certificado_texto)

        # Botón de descarga
        st.download_button(
            label="⬇️ Descargar certificado",
            data=certificado_texto,
            file_name=f"certificado_{curso['nombre'].replace(' ','_')}.txt",
            mime="text/plain"
        )

# Mostrar certificados guardados en sesión
st.markdown("---")
st.subheader("📂 Certificados guardados en tu sesión")
for nombre, contenido in st.session_state.certificados.items():
    st.text(f"- {nombre}")
