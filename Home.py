import streamlit as st
import time


st.set_page_config(
    page_title="Sistema de Diagnóstico de Ictericia Neonatal",
    page_icon="🩺",
    layout="wide"
)

# Hide the sidebar temporarily using CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Bienvenido al Sistema de Diagnóstico")
st.markdown(
    """
    Este sistema utiliza modelos de IA para apoyar la detección temprana de ictericia neonatal.

    Serás redirigido automáticamente al módulo principal en unos segundos...
    """
)

# Wait 2 seconds before redirect
with st.spinner("Cargando módulo principal..."):
    time.sleep(2)

# Redirect to Diagnóstico page
st.switch_page("pages/2_diagnostico.py")