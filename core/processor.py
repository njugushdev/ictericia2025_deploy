import random
from PIL import Image
import os

def predecir_con_modelo_falso(imagen):
    pred = random.choice(["ictericia", "no_ictericia"])
    prob = round(random.uniform(0.7, 1.0), 2)
    return pred, prob


def mostrar_imagen_con_prediccion(fila, pred, prob, st):
    """
    Muestra visualmente una imagen con su predicción ya calculada.
    """
    imagen = Image.open(fila["ruta"])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(imagen, caption=os.path.basename(fila["ruta"]), use_container_width=True)
    with col2:
        st.markdown(f"**Etiqueta real:** `{fila['etiqueta']}`")
        st.markdown(f"**Predicción simulada:** `{pred}` ({prob * 100:.1f}%)")

        if pred == fila['etiqueta']:
            st.success("✅ ¡Coincide con la etiqueta!")
        else:
            st.error("❌ No coincide con la etiqueta.")

