# Sistema de diagnóstico no invasivo de ictericia neonatal — **Interfaz Streamlit**

> Proyecto de tesis: *“Sistema de diagnóstico no invasivo de ictericia neonatal en Colombia: un enfoque desde la visión por computador”*.
> Este README se centra en **cómo está organizado el proyecto**, **qué hace cada parte** y **cómo ejecutarlo** end-to-end.


## 🧭 Tabla de contenidos
- [1. Estructura del proyecto (vista rápida)](#1-estructura-del-proyecto-vista-rápida)
- [2. Estructura explicada (para qué sirve cada parte)](#2-estructura-explicada-para-qué-sirve-cada-parte)
- [3. Flujo funcional de la app](#3-flujo-funcional-de-la-app)
- [4. Instalación y ejecución](#4-instalación-y-ejecución)
- [5. Variables de entorno (`.env`) y convenciones](#5-variables-de-entorno-env-y-convenciones)
- [6. Conexión del modelo entrenado](#6-conexión-del-modelo-entrenado)
- [7. Exportación de resultados (CSV) y esquema](#7-exportación-de-resultados-csv-y-esquema)
- [8. Pruebas y validaciones rápidas](#8-pruebas-y-validaciones-rápidas)
- [9. Estilo de código, logs y manejo de errores](#9-estilo-de-código-logs-y-manejo-de-errores)
- [10. Solución de problemas comunes (FAQ)](#10-solución-de-problemas-comunes-faq)

---

## 1. Estructura del proyecto (vista rápida)
```
.
├─ assets/
├─ core/
│  ├─ database.py
│  └─ processor.py
├─ data/
├─ models_ml/
│  └─ preprocessing.py
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
## 2. Estructura explicada (para qué sirve cada parte)

| Ruta / Módulo | ¿Para qué sirve? | Puntos clave / Recomendaciones |
|---|---|---|
| `app.py` | **Punto de entrada** de la interfaz (Streamlit). Crea la barra lateral, maneja el estado global (`st.session_state`) y enruta a las páginas. | Mantén `app.py` delgado: delega lógica en `core/`, `models_ml/` y `utils/`. |
| `pages/1_auth.py` | Página de **inicio de sesión** (si se usa autenticación básica). | Se apoya en `utils/auth_utils.py`. Puedes desactivar auth en `.env` si solo haces pruebas locales. |
| `pages/2_diagnostico.py` | **Núcleo de la app**: carga de imágenes, preprocesamiento, inferencia, visualización de resultado (ictericia sí/no) y alerta de riesgo. | Lee variables (p. ej. `MODEL_PATH`), usa funciones de `core/processor.py` y `models_ml/prepprocessing.py`. |
| `pages/3_dashboard.py` | Tablero de **métricas**: lectura de CSV de `resultados/`, gráficos (p. ej. distribución de probabilidades, conteos por clase). | Evita cálculos pesados a cada render: usa `st.cache_data`. |
| `pages/4_analisis_por_lote.py` | Procesamiento **batch** para carpetas o lotes de imágenes. Permite exportar un CSV por corrida. | Muestra barra de progreso y un resumen al final. |
| `pages/5_about.py` | Información del proyecto, disclaimers, autores, alcance y limitaciones. | Ubicación ideal para notas de ética/privacidad. |
| `core/processor.py` | **Orquesta** el pipeline: lectura de imagen, normalización de iluminación, segmentación de piel/ROI, conversión de color (HSV/Lab), escalado/reshape para el modelo, post-proceso (umbral). | Mantener funciones **puras** (mismo input → mismo output). Facilita pruebas unitarias. |
| `core/database.py` | Capa simple de persistencia para resultados locales (si aplica). | En este proyecto, la **persistencia principal** es el CSV en `resultados/`. |
| `models_ml/prepprocessing.py` | Funciones específicas de **preprocesamiento** y wrappers de modelo (carga, `predict()`). | Separa claramente: `load_model()`, `prepare_input()`, `predict_proba()`. |
| `utils/auth_utils.py` | Helpers para **autenticación** básica (validación de usuario, hash, etc.). | No almacenes contraseñas en texto plano en el repo. Usa `.env`. |
| `utils/layout_utils.py` | Componentes de UI reutilizables (banners, tarjetas, tablas con estilo). | Útil para mantener coherencia visual y limpieza en `pages/*.py`. |
| `assets/` | Logos, íconos, estilos y otros recursos estáticos. | No incluyas material con copyright sin permiso. |
| `data/` | Datos locales de prueba (imágenes ejemplo) y/o datos procesados temporales. | Mantén **anonimización**. No subas datos clínicos reales al repo público. |
| `resultados/` | **Salidas CSV** de cada corrida (lote). También puedes almacenar artefactos (imágenes anotadas). | Nombra los archivos `resultados_YYYYMMDD_HHMMSS.csv` para trazabilidad. |
| `test/TEST.py` | Tests básicos de smoke (import, arranque mínimo de funciones). | Ejecuta con `pytest -q`. |
| `test/dataset_prediccion_simulada.py` | Genera un **dataset simulado** de predicciones para poblar el dashboard sin un modelo real. | Útil en demos y validación de visualizaciones. |
| `test/dataset_viewer_test.py` | Pequeño visor/inspector de dataset para revisar rutas/formatos. | Verifica rápidamente que `pages/2_diagnostico.py` verá archivos válidos. |
| `.gitattributes` | Configuración de atributos de Git (normalización de finales de línea, etc.). | Opcional, pero ayuda a la portabilidad. |

---
## 3. Flujo funcional de la app

```
Usuario → (1) Carga imagen → (2) Preprocesamiento → (3) Modelo predice p(ictericia)
      → (4) Umbral de riesgo → (5) Visualización y alerta → (6) Exportación CSV
```

1) **Carga**: el usuario arrastra/sube JPG/PNG desde `pages/2_diagnostico.py`.  
2) **Preprocesamiento**: `core/processor.py` + `models_ml/prepprocessing.py` (normalización, ROI, HSV/Lab).  
3) **Inferencia**: `predict_proba()` retorna probabilidad `p` (0–1).  
4) **Post-proceso**: se aplica `RISK_THRESHOLD` (ej. 0.75) → `Alto/Medio/Bajo`.  
5) **UI**: banners, tablas y miniaturas (helpers en `utils/layout_utils.py`).  
6) **CSV**: se guarda en `resultados/` con metadatos (modelo, tiempo, parámetros de preproceso).  

---
## ⚙️ Requisitos, instalación y ejecución

### Requisitos (ya preparados)
- Python 3.10+ (recomendado 3.11)
- Dependencias fijadas en `requirements.txt`

### Pasos

### Opción A — Instalación rápida
```bash
# 1) Crear y activar entorno
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 2) Instalar dependencias
pip install --upgrade pip
pip install streamlit==1.37.1 numpy==1.26.4 pandas==2.2.2 opencv-python==4.10.0.84             scikit-image==0.24.0 pillow==10.4.0 scikit-learn==1.5.1             matplotlib==3.9.2 plotly==5.24.1 python-dotenv==1.0.1

# 3) (Opcional) Configurar .env (ver en la siguiente sección)

```
---

### Opción B — Usando `requirements.txt`
Luego de haber completado el paso 1, copia este bloque en `requirements.txt` y luego instala con:
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
tensorflow==2.20.0
```

> Estas versiones son estables al momento de preparar la interfaz y cubren:  
> - UI (Streamlit)  
> - Manejo/visualización de imágenes (Pillow, OpenCV, scikit-image)  
> - Análisis/tablas (NumPy, Pandas)  
> - Gráficos (Matplotlib/Plotly)  
> - Utilidades de entorno (`python-dotenv`)  
> - Modelos clásicos (`scikit-learn`)

---
## 5. Variables de entorno (`.env`) y convenciones

Crea un archivo `.env` en la raíz del proyecto (mismo nivel de `app.py`):

```env
# Modelo (si lo usas)
MODEL_PATH=models/model_ictericia.pt
PREPROCESSOR_PATH=models/preprocessor.joblib

# Directorios
DATA_DIR=data
OUTPUT_DIR=resultados

# Auth (activar/desactivar login básico)
AUTH_MODE=disabled      # disabled | basic
BASIC_USER=admin
BASIC_PASS=admin123

# Umbral de riesgo para alerta (0–1)
RISK_THRESHOLD=0.75
```
## ▶️ Ejecutar
```bash
streamlit run app.
```
La app abrirá en `http://localhost:8501` (por defecto).

---

**Convenciones recomendadas**
- **Nombres de archivos**: sin espacios, usa snake_case.  
- **CSV de resultados**: `resultados_YYYYMMDD_HHMMSS.csv`.  
- **Semillas aleatorias**: fija `numpy.random.seed()` si generas data de prueba.

---
## 6. Conexión del modelo entrenado

1) **Coloca** el archivo del modelo en `models/` (o `models_ml/` si prefieres).  
2) **Apunta** `MODEL_PATH` en `.env` al archivo (ej.: `models/model_ictericia.pt`).  
3) **Implementa** en `models_ml/prepprocessing.py` (o módulo dedicado) estas funciones mínimas:
   - `load_model(model_path) -> model`
   - `prepare_input(image) -> model_input`
   - `predict_proba(model, model_input) -> float`

**Backends opcionales**
```bash
# PyTorch (CPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# TensorFlow (CPU)
pip install tensorflow==2.15.0
```
> Instala **solo uno** según tu tipo de modelo.

---

## 7. Exportación de resultados (CSV) y esquema

Cada corrida genera un CSV con columnas sugeridas:
```csv
image_path,predicted_class,probability,risk_level,preprocess_steps,model_version,run_id,timestamp
data/samples/img_001.jpg,ictericia,0.82,ALTO,"{'color':'HSV','norm':'shades'}",v1.0,20241004-170000,2024-10-04T17:00:00-05:00
```

- `risk_level`: B A J O / M E D I O / A L T O (o equivalente).  
- `preprocess_steps`: json-string con pasos aplicados (útil para auditoría).  
- `model_version`: etiqueta de versión (útil si cambias pesos/modelo).  
- `run_id`: ID único por corrida (timestamp o UUID).  

El tablero (`pages/3_dashboard.py`) puede consumir múltiples CSV y agregarlos.

---

## 8. Pruebas y validaciones rápidas

```bash
# Ejecutar pruebas (si usas pytest)
pytest -q

# Lint y formato (si lo adoptas)
flake8 src
black .
isort .
```
- `test/dataset_prediccion_simulada.py`: genera datos falsos para el dashboard.  
- `test/dataset_viewer_test.py`: verifica rutas y formatos del dataset.  
- `test/TEST.py`: smoke tests de import y funciones básicas.

---

## 9. Estilo de código, logs y manejo de errores

- **Estilo**: PEP8, tipar funciones claves (`-> float`, `-> dict`, etc.).  
- **Logs**: usa `logging` con niveles `INFO/ERROR`. Loggea: ruta de imagen, tamaño, tiempo de inferencia, probabilidad, alerta.  
- **Errores**: captura y muestra mensajes útiles en UI (e.g., “formato no soportado”), pero escribe detalle técnico en logs.  

Ejemplo de setup mínimo:
```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
```

---

## 10. Solución de problemas comunes (FAQ)

- **No carga el modelo**: revisa `MODEL_PATH` en `.env` y permisos de archivo.  
- **ImportError de `prepprocessing`**: el nombre tiene doble “pp”. Renómbralo a `preprocessing.py` y actualiza imports.  
- **No aparecen resultados en el dashboard**: confirma que existen CSV en `resultados/` y que el esquema coincide.  
- **Error de OpenCV/FFmpeg**: reinstala `opencv-python` o cambia a `opencv-python-headless` si corres en servidores sin GUI.  
- **Memoria insuficiente con lotes grandes**: procesa en **batches** o reduce tamaño de entrada.  
- **Poca luz o color extraño en imágenes**: ajusta opciones de normalización/espacio de color en `core/processor.py`.  





