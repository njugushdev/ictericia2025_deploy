import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.layout_utils import verificar_autenticacion

# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="Panel de Control - Ictericia Neonatal",
    page_icon="📊",
    layout="wide"
)

verificar_autenticacion()
st.title("📊 Panel de Diagnóstico - Ictericia Neonatal")

# ============================================================
# Cargar resultados
# ============================================================
csv_path = "resultados/todos_lotes.csv"
if not os.path.exists(csv_path):
    st.warning("No se encontraron resultados acumulados. Por favor, ejecute al menos un análisis por lote antes de acceder al panel.")
    st.stop()

with st.spinner("🔄 Cargando resultados..."):
    df = pd.read_csv(csv_path)

required_columns = {"imagen", "etiqueta_real", "prediccion", "probabilidad", "bilirrubina_predicha", "acierto"}
if not required_columns.issubset(df.columns):
    st.error("El archivo de resultados no contiene las columnas requeridas.")
    st.stop()

# ============================================================
# Mostrar tabla completa
# ============================================================
with st.expander("🔍 Ver tabla completa de resultados"):
    st.dataframe(df)

# ============================================================
# Métricas globales
# ============================================================
total = len(df)
ictericia = df.loc[df["prediccion"] == "ictericia"].shape[0]
no_ictericia = df.loc[df["prediccion"] == "no_ictericia"].shape[0]
aciertos = df.loc[df["acierto"] == "✔️"].shape[0]
errores = df.loc[df["acierto"] == "❌"].shape[0]
exactitud = (aciertos / total) * 100 if total else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total analizado", total)
col2.metric("Predicciones: Ictericia", ictericia)
col3.metric("Predicciones: No Ictericia", no_ictericia)
col4.metric("Exactitud global", f"{exactitud:.2f}%")

# ============================================================
# Gráficos
# ============================================================
st.markdown("---")
st.subheader("📊 Distribución por clase")
st.bar_chart(pd.DataFrame({
    "Clase": ["ictericia", "no_ictericia"],
    "Cantidad": [ictericia, no_ictericia]
}).set_index("Clase"))

st.subheader("✅ Aciertos vs ❌ Errores")
st.bar_chart(pd.DataFrame({
    "Resultado": ["Aciertos", "Errores"],
    "Cantidad": [aciertos, errores]
}).set_index("Resultado"))

# ============================================================
# Fecha y hora de actualización
# ============================================================
st.markdown("---")
st.caption(f"🕒 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")