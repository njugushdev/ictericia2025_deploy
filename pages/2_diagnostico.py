import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from PIL import Image
from core.processor import predict_image

# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="Diagnóstico - Ictericia Neonatal",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Diagnóstico de Ictericia Neonatal")
st.markdown("Suba una imagen del recién nacido para analizar signos de ictericia mediante los modelos de IA.")

# ============================================================
# Carga de imagen y predicción del modelo
# ============================================================
uploaded_image = st.file_uploader("📷 Subir imagen del neonato", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Imagen cargada", use_column_width=True)

    if st.button("📊 Analizar imagen"):
        with st.spinner("Ejecutando análisis con IA..."):
            try:
                pred_label, prob, bilirubin_val = predict_image(image)

                st.markdown("---")
                st.subheader("🧠 Resultados del Análisis con IA")
                st.markdown(f"Diagnóstico Predicho: *{pred_label.upper()}*")
                st.markdown(f"Confianza del modelo: *{prob * 100:.2f}%*")
                st.markdown(f"Nivel estimado de bilirrubina: *{bilirubin_val} mg/dL*")

                # Interpretación
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