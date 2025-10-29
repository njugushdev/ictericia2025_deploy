import streamlit as st

def iniciar_sesion(usuario, contrasena):
    """Ejemplo básico de inicio de sesión estático (reemplazar por autenticación con base de datos más adelante)."""
    if usuario == "admin" and contrasena == "1234":
        st.session_state["logueado"] = True
        return True
    return False


def cerrar_sesion():
    """Cierra la sesión del usuario."""
    st.session_state["logueado"] = False
    st.success("✅ Sesión cerrada exitosamente.")
    st.switch_page("pages/1_auth.py")


def esta_logueado():
    """Devuelve True si el usuario está autenticado."""
    return st.session_state.get("logueado", False)