import streamlit as st
import pandas as pd


st.markdown("<h1 style='text-align: center;'>🦋sayuniverse🦋</h1>", unsafe_allow_html=True)


pg = st.navigation([st.Page("👤login.py"),st.Page("📖Cursos.py"), st.Page("🔖Certificados.py"),st.Page("📝history.py"),st.Page("⚠️alerts.py"),st.Page("📚dashboard.py"),st.Page("salir.py")])
pg.run()

















