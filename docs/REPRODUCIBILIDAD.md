# Reproducibilidad y ejecución

## 1. Entorno

La ejecución de referencia se realiza en Google Colab. Se puede utilizar CPU; GPU es opcional y puede reducir el tiempo de ejecución.

Se necesita:
- acceso a Google Colab o un entorno Python compatible;
- conexión a Internet para instalar dependencias y obtener el dataset/modelo cuando corresponda;
- el archivo `modelos_toxicidad.zip` para ejecutar T03;
- memoria suficiente para cargar BERT.

## 2. Notebooks y orden de trabajo

### T04 — Preparación y entrenamiento

1. Abrir el notebook T04 en Google Colab.
2. Ejecutar las celdas en orden.
3. El notebook carga `google/civil_comments`, selecciona hasta 50.000 filas con semilla 42 y prepara la etiqueta binaria.
4. Ejecutar las etapas de partición, TF-IDF, entrenamiento/evaluación de Regresión Logística y BERT.
5. Guardar el modelo BERT y el tokenizador en `modelo_bert_toxicidad/`.
6. Generar y descargar `modelos_toxicidad.zip`.

T04 contiene el pipeline y entrenamiento original. Si solo se desea ejecutar la demostración ya preparada, no es necesario volver a entrenar siempre que se disponga del ZIP generado previamente.

### T03 — Demostrador Vigía

1. Abrir T03 en Google Colab.
2. Ejecutar las celdas en orden.
3. Cuando se solicite, cargar `modelos_toxicidad.zip`.
4. El notebook descomprime el archivo, localiza la carpeta del modelo y carga modelo y tokenizador.
5. Ejecutar los casos de prueba y la interfaz Gradio.

T03 no entrena el modelo: ejecuta inferencia con los pesos guardados.

## 3. Contenido esperado del ZIP

```text
modelos_toxicidad.zip
└── modelos_toxicidad/
    ├── modelo_bert_toxicidad/
    │   ├── config.json
    │   ├── model.safetensors  (o pytorch_model.bin)
    │   └── archivos del tokenizador
    └── modelo_tfidf_toxicidad/
        ├── modelo_lr.joblib
        └── vectorizador_tfidf.joblib
```

La estructura exacta puede variar según la versión de Transformers y el procedimiento de compresión. Lo imprescindible para T03 es que el directorio de BERT contenga configuración, pesos y tokenizador.

## 4. Dependencias

T03 instala `transformers` y utiliza PyTorch, NumPy y Gradio, además de las dependencias de visualización que se importen en el notebook. T04 instala `datasets`, `pandas`, `scikit-learn` y `matplotlib`, y utiliza `transformers`, `accelerate` y `torch` para BERT.

**Versiones:** registrar las versiones reales del entorno ejecutando:

```python
import sys
import torch
import transformers
import numpy
import gradio

print("Python:", sys.version)
print("PyTorch:", torch.__version__)
print("Transformers:", transformers.__version__)
print("NumPy:", numpy.__version__)
print("Gradio:", gradio.__version__)
```

Para T04, registrar también:

```python
import datasets
import pandas
import sklearn

print("Datasets:", datasets.__version__)
print("Pandas:", pandas.__version__)
print("Scikit-learn:", sklearn.__version__)
```

No fijar versiones en este documento hasta verificar las que se utilizaron realmente.

## 5. Semillas y parámetros relevantes

| Parámetro | Valor |
|---|---|
| Semilla de preparación | 42 |
| Muestra máxima T04 | 50.000 filas |
| Umbral de etiqueta | 0.5 |
| Partición real del código T04 | 70 % / 15 % / 15 % |
| Modelo base | `google-bert/bert-base-uncased` |
| Número de clases | 2 |
| Longitud máxima BERT | 256 tokens |
| Longitud máxima de entrada en T03 | 5.000 caracteres |
| Longitud mínima de entrada en T03 | 3 caracteres |

## 6. Solución de problemas

- **No se encuentra el ZIP:** comprobar que se cargó el archivo correcto y que su nombre coincide con el solicitado por el notebook.
- **No se encuentra `config.json` o los pesos:** revisar la estructura interna del ZIP y confirmar que se comprimió la carpeta completa del modelo.
- **Falta memoria:** reiniciar el entorno, cerrar sesiones innecesarias o utilizar una GPU disponible.
- **Instalación de librerías:** volver a ejecutar la celda de instalación y reiniciar el entorno si Colab lo solicita.
- **Diferencias de resultados:** comprobar que se está utilizando el mismo ZIP, la misma versión de librerías y los mismos parámetros.

## 7. Evidencia de ejecución

Conservar capturas o salidas de:
- carga exitosa del modelo y tokenizador;
- versiones de dependencias;
- ejecución de los casos de prueba;
- métricas y matriz de confusión de T04;
- interfaz Vigía funcionando;
- control de pesos antes y después de inferencia.
