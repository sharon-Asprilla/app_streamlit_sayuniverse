import streamlit as st
from datetime import date

# Inicializar certificados en la sesión
if "certificados" not in st.session_state:
    st.session_state.certificados = {}

# Inicializar historial en sesión
if "historial" not in st.session_state:
    st.session_state.historial = []

# Función para registrar procesos en historial
def registrar_proceso(mensaje):
    st.session_state.historial.append(f"{mensaje} ({date.today().strftime('%d/%m/%Y')})")

# Simulación de cursos terminados
cursos_terminados = [
    {"nombre": "Inglés Básico 1", "clases": 10},
    {"nombre": "Inglés Intermedio 2", "clases": 16},
]

st.title("🎓 Certificados de Cursos")

# Verificar usuario y pruebas completadas
if not st.session_state.get('usuario'):
    st.warning("Debes iniciar sesión para obtener el certificado.")
else:
    certificado_generado = False
    for curso in cursos_terminados:
        key_aprobado = f"aprobado_{curso['nombre']}"
        if st.session_state.get(key_aprobado) and st.session_state.get(f"completado_{curso['nombre']}"):
            nivel = st.session_state.get(f"nivel_{curso['nombre']}", "Desconocido")
            duracion = st.session_state.get(f"duracion_{curso['nombre']}", f"{curso['clases']} horas")
            nombre_alumno = st.session_state.get('usuario')
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
        st.error("No has completado el curso requerido para recibir certificado. Presenta y completa la prueba primero.")
        
        # Crear contenido del certificado
        certificado_texto = f"""
        CERTIFICADO DE FINALIZACIÓN

        SayUniverse

        Se otorga a

        {st.session_state.get('usuario','Estudiante')}
        Por haber completado satisfactoriamente el curso
        {curso['nombre']}
        nivel de certificación
        {st.session_state.get(f"nivel_{curso['nombre']}", 'Desconocido')}
        Número de clases: {curso['clases']}
        Duración estimada: {curso['clases']} horas
        Fecha: {date.today().strftime('%d/%m/%Y')}"""

        # Guardar en sesión
        st.session_state.certificados[curso["nombre"]] = certificado_texto

        # Mostrar certificado con colores
        st.success("¡Certificado generado!")
        registrar_proceso(f"Certificado generado para: {curso['nombre']}")
        st.markdown(f"<div style='background-color:black; color:white; padding:30px; border-radius:10px; font-family:monospace;'>{certificado_texto}</div>", unsafe_allow_html=True)


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
