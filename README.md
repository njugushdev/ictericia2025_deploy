# README — Interfaz Streamlit (Tesis Ictericia)

## 📂 Estructura del proyecto
```
.
├─ assets/
├─ core/
│  ├─ database.py
│  └─ processor.py
├─ data/
├─ models_ml/
│  └─ prepprocessing.py
├─ pages/
│  ├─ 1_auth.py
│  ├─ 2_diagnostico.py
│  ├─ 3_dashboard.py
│  ├─ 4_analisis_por_lote.py
│  └─ 5_about.py
├─ resultados/
├─ test/
│  ├─ dataset_prediccion_simulada.py
│  ├─ dataset_viewer_test.py
│  └─ TEST.py
├─ utils/
│  ├─ auth_utils.py
│  └─ layout_utils.py
├─ .gitattributes
└─ app.py
```

> Nota: `app.py` es el punto de entrada de la app.  
> Las páginas multipágina de Streamlit viven en `pages/`.  
> Los módulos de apoyo están en `core/` y `utils/`.  
> Los resultados exportados se guardan en `resultados/`.

---

## ⚙️ Requisitos e instalación

### Opción A — Instalación rápida
```bash
python -m venv .venv
# Windows
. .venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install --upgrade pip
pip install streamlit==1.37.1 numpy==1.26.4 pandas==2.2.2 opencv-python==4.10.0.84             scikit-image==0.24.0 pillow==10.4.0 scikit-learn==1.5.1             matplotlib==3.9.2 plotly==5.24.1 python-dotenv==1.0.1
```

### Opción B — Usando `requirements.txt`
Copia este bloque en `requirements.txt` y luego instala con:
```bash
pip install -r requirements.txt
```

```txt
streamlit==1.37.1
numpy==1.26.4
pandas==2.2.2
opencv-python==4.10.0.84
scikit-image==0.24.0
pillow==10.4.0
scikit-learn==1.5.1
matplotlib==3.9.2
plotly==5.24.1
python-dotenv==1.0.1
```

> Estas versiones son estables al momento de preparar la interfaz y cubren:  
> - UI (Streamlit)  
> - Manejo/visualización de imágenes (Pillow, OpenCV, scikit-image)  
> - Análisis/tablas (NumPy, Pandas)  
> - Gráficos (Matplotlib/Plotly)  
> - Utilidades de entorno (`python-dotenv`)  
> - Modelos clásicos (`scikit-learn`)

---

## ▶️ Ejecutar
```bash
streamlit run app.py
```

---

## (Opcional) Soporte para modelos de Deep Learning
Si luego conectas un modelo entrenado, instala **uno** de estos backends según el formato del modelo:

```bash
# PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# TensorFlow (CPU)
pip install tensorflow==2.15.0
```

> ⚠️ No instales ambos a la vez si no los necesitas.





