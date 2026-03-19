# 🎵 Análisis de Clasificación No Supervisada de Composiciones Musicales
### Basado en la Elicitación de Emociones de Estudiantes de la UAM Cuajimalpa

**Proyecto Terminal — Licenciatura en Tecnologías y Sistemas de Información**  
**Universidad Autónoma Metropolitana, Unidad Cuajimalpa**  
**Autor:** Daniel Arellano Morales | **Matrícula:** 2203065732 | **Diciembre 2025**  
**Asesores:** Dr. Carlos Joel Rivero Moreno · Ing. Carmen Lucia Bustillo Hernández

---

## 📌 Descripción

Este proyecto aplica técnicas de **aprendizaje no supervisado** (K-Means + PCA) para clasificar composiciones musicales de distintos géneros a partir de las **emociones que evocan** en estudiantes universitarios, usando la escala **GEMS-25** (Geneva Emotion Music Scale).

El resultado es un **mapa emocional 2D interactivo** desarrollado con Dash y Plotly, donde cada canción está posicionada según su perfil emocional y se puede escuchar su fragmento representativo al pasar el cursor.

---

## 🎯 Objetivo General

Desarrollar un análisis de clasificación no supervisada con K-Means y PCA de composiciones musicales, a partir de la elicitación de emociones en estudiantes de LTSI de la UAM Cuajimalpa, y visualizarlo mediante una interfaz gráfica interactiva con dendrogramas, heatmaps y un mapa emocional 2D.

---

## 🧠 Metodología

```
Encuesta de géneros → Selección de 280 canciones → Elicitación emocional (GEMS-25)
        ↓
Construcción del dataset → Limpieza y Pivot → Normalización (Z-score)
        ↓
Medidas de similitud (Euclidiana, Minkowski, City Block, Chebyshev, Correlación)
        ↓
K-Means (k=3, método del codo) + PCA (2 componentes)
        ↓
Dendrogramas · Heatmaps · Mapa Emocional 2D Interactivo
```

---

## 📊 Resultados — 3 Clústeres Emocionales

| Clúster | Nombre | Emociones dominantes |
|---------|--------|----------------------|
| **E** | Energía Positiva | Alegre, Animado, Enérgico, Sereno |
| **C** | Calma Afectiva | Suave, Calma, Ensueño, Tranquilo, Cariñoso |
| **I** | Intensidad Emocional | Fuerte, Eufórico, Abrumado, Agitado |

---

## 🗂️ Estructura del Repositorio

```
📦 music-emotion-clustering/
├── 📄 music_emotion_map.py           # App principal — Mapa 2D Interactivo (Dash + Plotly)
├── 📄 recortar_frecuencias.py        # Extracción del segmento de mayor energía (librosa)
├── 📊 matriz_pivot_con_genero.xlsx   # Dataset procesado (emociones GEMS-25 por canción)
├── 📁 assets/                        # Fragmentos de audio de 30 segundos (~75 MB)
│   ├── E1_clip.mp3
│   ├── E2_clip.mp3
│   ├── H1_clip.mp3
│   └── ...                           # Nombrados por ID_Cancion del dataset
├── 📄 requirements.txt
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🔊 Nota sobre los fragmentos de audio

La carpeta `assets/` contiene fragmentos de **30 segundos** por canción, extraídos automáticamente del segmento de mayor energía espectral (200–8000 Hz) usando `librosa`. Los archivos siguen la nomenclatura `ID_Cancion_clip.mp3` (ej: `E1_clip.mp3`, `H3_clip.mp3`).

> ⚠️ **Limitación conocida:** Algunos puntos del mapa interactivo no reproducen audio al hacer hover. Esto ocurre porque durante el proceso de recorte, algunos archivos no pudieron convertirse correctamente al formato MP3 por limitaciones de tiempo en la etapa de desarrollo. Son casos aislados y no afectan el análisis ni la clasificación emocional.

---

## ⚙️ Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/music-emotion-clustering.git
cd music-emotion-clustering
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python music_emotion_map.py
```
Abre tu navegador en: `http://127.0.0.1:8050`

---

### (Opcional) Generar tus propios fragmentos de audio

Edita la variable `input_folder` en `recortar_frecuencias.py` con la ruta de tu carpeta de MP3 y ejecuta:

```bash
python recortar_frecuencias.py
```

Los archivos `_clip.mp3` generados deben colocarse en la carpeta `assets/`.

---

## 🖥️ Demo de la App

- **Mapa emocional animado** con los 280 fragmentos musicales clasificados
- **Filtro por clúster** en panel lateral (Energía Positiva / Calma Afectiva / Intensidad Emocional)
- **Hover interactivo:** muestra ID de canción, género musical y clúster emocional, y reproduce el fragmento de audio

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Librerías |
|-----------|-----------|
| App interactiva | `Dash`, `Plotly` |
| Machine Learning | `scikit-learn` (KMeans, PCA, StandardScaler) |
| Procesamiento de datos | `pandas`, `numpy` |
| Procesamiento de audio | `librosa`, `pydub` |
| Dataset | Excel (`.xlsx`) vía `openpyxl` |

---

## 📁 Dataset

El archivo `matriz_pivot_con_genero.xlsx` contiene:
- **Filas:** una por cada combinación participante–canción (30 participantes × 280 canciones)
- **Columnas:** `ID_Participante`, `ID_Cancion`, `Genero` + 25 emociones GEMS-25
- **Valores:** intensidad emocional (0–5), donde 0 = emoción no seleccionada

### Corpus musical
| Idioma | Géneros | Canciones/género | Total |
|--------|---------|-----------------|-------|
| Inglés | 26 | 5 | 130 |
| Español | 15 | 10 | 150 |
| **Total** | **41** | — | **280** |

---

## 📐 Detalles Técnicos

**Preprocesamiento:**
- Emociones no seleccionadas → codificadas como `0`
- Transformación pivot: filas = canciones, columnas = emociones
- Normalización Z-score con `StandardScaler` (excluyendo columnas categóricas)

**Determinación de k:**
- Método del codo sobre inercia intra-cluster (k=1 a 10)
- k=3 seleccionado por equilibrio entre cohesión y simplicidad

**PCA:**
- 25 dimensiones → 2 componentes principales
- PC1: gradiente de activación emocional (intenso ↔ calmado)
- PC2: valencia emocional (positivo ↔ sombrío)

**Extracción de audio (`recortar_frecuencias.py`):**
- Espectrograma STFT con `librosa` (n_fft=2048, hop_length=512)
- Rango de frecuencias: 200–8000 Hz
- Segmento de 30s con mayor energía promedio exportado como MP3 vía `pydub`

---

## 📚 Referencia académica

> Arellano Morales, D. (2025). *Análisis de Clasificación No Supervisada de Composiciones Musicales Basado En la Elicitación de Emociones de Estudiantes de la UAM Cuajimalpa*. Proyecto Terminal, Licenciatura en Tecnologías y Sistemas de Información, UAM Cuajimalpa.

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos. El código es de uso libre para investigación y educación.

---

*Casa abierta al tiempo — Universidad Autónoma Metropolitana*
