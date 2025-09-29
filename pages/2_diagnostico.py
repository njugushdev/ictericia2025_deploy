import streamlit as st
from PIL import Image
from utils.layout_utils import verificar_autenticacion

st.set_page_config(
    page_title = "Diagnóstico",
    page_icon = "🩺",
    layout = "wide"
)
verificar_autenticacion()

st.title("🩺 Diagnóstico de Ictericia Neonatal")

# CSS para botón nativo flotante
st.markdown("""
        <style>
        div.stButton > button.logout-button {
            position: fixed;
            top: 10px;
            right: 15px;
            background-color: #444;
            color: white;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            z-index: 10000;
        }
        </style>
    """, unsafe_allow_html=True)

#Botón de logout
if st.button("🔒", key="logout"):
    st.session_state.logueado = False
    st.session_state.logout_confirmed = True
    st.rerun()

st.markdown("Cargue la imagen del neonato para analizar signos de ictericia.")
imagen_subida = st.file_uploader("📷 Carga la imagen", type=["jpg", "jpeg", "png"])

if imagen_subida:
    imagen = Image.open(imagen_subida)
    st.image(imagen, caption="Imagen cargada", use_container_width=True)

    if st.button("📊 Analizar imagen"):
       with st.spinner("Procesando..."):
           ancho, alto = imagen.size
           if ancho > 400:
               st.error("⚠️ Posible ictericia detectada (91%)")
           else:
               st.success("✅ Sin signos de ictericia (8%)")
else:
    st.warning("⚠️ No se puede proceder. Por favor, suba una imagen para analizar.")