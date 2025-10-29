import streamlit as st

st.set_page_config(
    page_title="Sistema de Diagnóstico de Ictericia Neonatal",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Bienvenido al Sistema de Diagnóstico")
st.markdown(
    "Estimado usuario: use el menú lateral para navegar entre los módulos. "
    "Recuerde que debe *iniciar sesión primero* para poder acceder a los demás módulos."
)