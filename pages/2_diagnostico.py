import streamlit as st
from PIL import Image
from utils.layout_utils import verificar_autenticacion
from core.processor import predict_image

# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="Diagnóstico - Ictericia Neonatal",
    page_icon="🩺",
    layout="wide"
)

verificar_autenticacion()

st.title("🩺 Diagnóstico de Ictericia Neonatal")
st.markdown("Suba una imagen del recién nacido para analizar signos de ictericia mediante los modelos de IA entrenados.")

# CSS para el botón flotante de cierre de sesión
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

# Botón de cierre de sesión
if st.button("🔒", key="logout"):
    st.session_state.logueado = False
    st.session_state.logout_confirmed = True
    st.rerun()

# ============================================================
# Carga de imagen y predicción del modelo
# ============================================================

uploaded_image = st.file_uploader("📷 Subir imagen del neonato", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Imagen cargada", use_container_width=True)

    if st.button("📊 Analizar imagen"):
        with st.spinner("Ejecutando análisis con IA..."):
            try:
                # Obtener predicciones de los modelos
                pred_label, prob, bilirubin_val = predict_image(image)

                st.markdown("---")
                st.subheader("🧠 Resultados del Análisis con IA")
                st.markdown(f"*Diagnóstico Predicho:* {pred_label.upper()}")
                st.markdown(f"*Confianza del modelo:* {prob * 100:.2f}%")
                st.markdown(f"*Nivel estimado de bilirrubina:* {bilirubin_val} mg/dL")

                # Interpretación visual
                if pred_label == "ictericia":
                    st.error(f"⚠️ Posible ictericia detectada ({prob * 100:.1f}% de confianza).")
                    if bilirubin_val >= 12:
                        st.warning("🚨 Rango severo — se recomienda atención clínica inmediata.")
                    elif bilirubin_val >= 8:
                        st.info("🟠 Rango moderado — se sugiere seguimiento médico.")
                    else:
                        st.success("🟢 Rango leve — monitorear la progresión.")
                else:
                    st.success(f"✅ Sin signos de ictericia detectados ({prob * 100:.1f}% de confianza).")

            except Exception as e:
                st.error(f"Ocurrió un error durante el análisis: {e}")

else:
    st.warning("⚠️ Por favor, suba una imagen para comenzar el análisis.")