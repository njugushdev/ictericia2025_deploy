import streamlit as st

def verificar_autenticacion():
    if not st.session_state.get("logueado", False):
        st.warning("Debe iniciar sesión para acceder a esta sección.")
        st.stop()

def redireccionar_si_logueado():
    if st.session_state.get("logueado", False):
        st.switch_page("pages/2_diagnostico.py")

def boton_logout():
    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.success("Sesión cerrada exitosamente.")
        st.switch_page("pages/1_auth.py")