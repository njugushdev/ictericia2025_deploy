import streamlit as st
from utils.layout_utils import redireccionar_si_logueado


st.set_page_config(page_title="Inicio de Sesión", page_icon="🔐", layout="centered")
# Autenticación (puedes conectarlo con una base de datos luego)
USUARIOS = {
    "admin": "1234",
    "medico1": "ictericia2025"
}

# Página de inicio de sesión

redireccionar_si_logueado() #Evita mostrar esta pantalla si ya está logueado

st.title("🔐 Iniciar Sesión")
st.markdown("Por favor, ingrese sus credenciales para continuar.")

usuario = st.text_input("Usuario")
contrasena = st.text_input("Contrasena", type="password")

col1, col2 = st.columns([1, 1,])
with col1:
    login = st.button("Ingresar")

if login:
    if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
        st.session_state.logueado = True
        st.success("Inicio de sesión exitoso.")
        st.rerun()
    else:
        st.error("❌ Usuario o contraseña incorrectos")

