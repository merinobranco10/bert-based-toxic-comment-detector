# Componente inteligente: BERT

## 1. Modelo utilizado

- **Modelo base:** `google-bert/bert-base-uncased`.
- **Tipo:** modelo Transformer BERT para procesamiento de lenguaje natural.
- **Tarea:** clasificación binaria de comentarios.
- **Clases:** `0 = No tóxico`; `1 = Tóxico`.
- **Dataset de ajuste:** muestra de Civil Comments preparada en el notebook T04.
- **Longitud máxima de entrada:** 256 tokens.
- **Umbral de construcción de etiquetas:** `toxicity >= 0.5` corresponde a la clase tóxica.

El notebook T04 realiza fine-tuning de BERT mediante `AutoModelForSequenceClassification` con dos etiquetas. La selección del mejor checkpoint se basa en `f1_macro` sobre validación y utiliza early stopping.

## 2. Justificación de la elección

BERT es pertinente para clasificación de texto porque genera representaciones contextuales: la representación de una palabra depende de las otras palabras presentes en el comentario. Esto resulta útil en una tarea donde el significado puede variar según el contexto.

Se reutiliza el BERT ajustado en T04 porque fue entrenado para la tarea y las etiquetas definidas por el proyecto. El notebook T03 se concentra en integrar el artefacto ya entrenado; no ejecuta un nuevo entrenamiento.

## 3. Flujo de inferencia

1. Recibir un comentario.
2. Validar que sea una cadena no vacía, con longitud permitida y al menos una letra.
3. Generar advertencias cuando el idioma detectado parezca distinto del inglés o cuando la entrada supere 256 tokens y vaya a truncarse.
4. Tokenizar con el tokenizador guardado junto al modelo.
5. Ejecutar el modelo en modo evaluación y sin cálculo de gradientes.
6. Aplicar softmax a los logits.
7. Obtener la clase predicha y la probabilidad de la clase tóxica.
8. Mostrar etiqueta, probabilidad, confianza, advertencias y limitaciones.

## 4. Criterio de decisión

La salida utiliza dos clases. La probabilidad asociada a la clase tóxica se informa como `prob_toxico`. La etiqueta se determina según la clase de mayor probabilidad (equivalente al umbral 0.5 en una clasificación binaria de dos clases, salvo cambios explícitos en la implementación).

La probabilidad es una salida del modelo y no debe interpretarse como certeza objetiva ni como una medida necesariamente calibrada.

## 5. Evidencia de desempeño

Completar con las salidas reales de T04, evaluadas sobre el conjunto de prueba. No copiar métricas de entrenamiento o validación como si fueran resultados de prueba.

| Métrica | BERT |
|---|---:|
| Accuracy | Completar |
| Precision macro | Completar |
| Recall macro | Completar |
| F1 macro | Completar |
| F1 de la clase tóxica | Completar |

T04 también implementa Regresión Logística + TF-IDF y un `DummyClassifier` mayoritario como referencias. Si se incluyen comparaciones, utilizar las métricas generadas por la misma ejecución y el mismo conjunto de prueba.

## 6. Artefactos

El modelo se guarda desde T04 en `modelo_bert_toxicidad/`, junto con el tokenizador. El ZIP generado por el notebook contiene esa carpeta y, además, el modelo TF-IDF + Regresión Logística.

Para cargar BERT, la carpeta debe incluir `config.json`, los pesos del modelo (`model.safetensors` o `pytorch_model.bin`, según el guardado) y los archivos del tokenizador.

## 7. Límites

- El modelo fue ajustado con comentarios principalmente en inglés; la aplicación advierte sobre texto en español u otros idiomas.
- El modelo puede confundir crítica, insulto, ironía, sarcasmo y lenguaje contextual.
- Puede generar falsos positivos y falsos negativos.
- Los comentarios superiores a 256 tokens se truncan durante la tokenización.
- No debe utilizarse como único criterio para sancionar usuarios o eliminar contenido.
