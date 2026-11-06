# Datos y preparación

## 1. Fuente

- **Dataset:** Civil Comments.
- **Repositorio:** https://huggingface.co/datasets/google/civil_comments
- **Identificador de carga:** `google/civil_comments`.
- **Split de origen utilizado:** `train`.
- **Muestra:** hasta 50.000 filas, seleccionadas mediante `shuffle(seed=42)` y `select`.
- **Semilla:** `42`.
- **Fecha de acceso:** el notebook T04 la registra dinámicamente al ejecutarse.

El notebook utiliza el split `train` del dataset publicado y genera particiones internas. No debe confundirse esta partición interna con los splits oficiales `validation` y `test` del repositorio.

## 2. Variables

| Variable | Uso | Descripción |
|---|---|---|
| `text` | Entrada (`X`) | Texto del comentario que procesa el clasificador. |
| `toxicity` | Fuente de etiqueta | Puntuación continua de toxicidad, en el rango `[0, 1]`. |
| `toxico` | Objetivo (`y`) | Etiqueta binaria derivada de `toxicity`. |

La etiqueta se construye con el umbral `0.5`:

- `0` — No tóxico: `toxicity < 0.5`.
- `1` — Tóxico: `toxicity >= 0.5`.

Este umbral es una decisión del proyecto y no una etiqueta binaria original del dataset.

## 3. Preparación y transformaciones

El notebook T04 realiza las siguientes operaciones:

1. Convierte el texto a tipo string y elimina espacios al inicio y al final.
2. Elimina registros cuyo texto es nulo o queda vacío.
3. Convierte `toxicity` a valor numérico y elimina puntuaciones nulas, no numéricas o fuera de `[0, 1]`.
4. Elimina textos duplicados exactos, conservando la primera aparición.
5. Crea `toxico` con el umbral `0.5`.
6. Conserva `text` como única variable de entrada y `toxico` como objetivo.

La puntuación `toxicity` se conserva para trazabilidad, pero no se utiliza como entrada del clasificador.

## 4. Partición

El código ejecutable del notebook realiza una partición estratificada:

- **70 % entrenamiento**
- **15 % validación**
- **15 % prueba**

Se utiliza `random_state=42` y `stratify` para mantener aproximadamente la proporción de clases en cada subconjunto. El conjunto de validación se utiliza durante la selección/ajuste del modelo y el conjunto de prueba se reserva para la evaluación final.

**Nota de consistencia:** si una celda Markdown del notebook indica 80/20, debe corregirse para que coincida con el código, que implementa 70/15/15.

El notebook verifica que no existan textos idénticos compartidos entre los subconjuntos.

## 5. Representación del texto

- Para el modelo clásico se utiliza TF-IDF con hasta 10.000 características y unigramas/bigramas. El vectorizador se ajusta únicamente con entrenamiento.
- Para BERT se utiliza el tokenizador de `google-bert/bert-base-uncased`, con truncamiento y longitud máxima de 256 tokens.

## 6. Cantidades que deben registrarse desde la ejecución

Completar después de ejecutar T04:

| Indicador | Resultado |
|---|---:|
| Filas cargadas inicialmente | 50.000 (máximo solicitado por el notebook) |
| Filas finales después de limpieza y deduplicación | Completar desde la salida |
| Filas de entrenamiento | Completar desde la salida |
| Filas de validación | Completar desde la salida |
| Filas de prueba | Completar desde la salida |
| Registros de clase 0 y clase 1 | Completar desde la salida |
| Textos vacíos eliminados | Completar desde la salida |
| Puntuaciones inválidas eliminadas | Completar desde la salida |
| Textos duplicados eliminados | Completar desde la salida |

## 7. Limitaciones de los datos

- Civil Comments está compuesto principalmente por comentarios en inglés. El modelo no debe presentarse como detector fiable de toxicidad en español.
- La puntuación continua se reduce a dos clases mediante un umbral. Los comentarios cercanos a `0.5` pueden ser ambiguos.
- Deduplicar por texto conserva la primera aparición y puede descartar anotaciones diferentes asociadas a un mismo texto.
- Una partición aleatoria no garantiza generalización a usuarios, conversaciones o periodos futuros.
- El truncamiento a 256 tokens puede eliminar información relevante situada al final de un comentario.
- La muestra de hasta 50.000 filas no equivale necesariamente al dataset completo.

## 8. Reproducibilidad de la fuente

El notebook registra fecha de acceso, semilla y split. Para reproducibilidad estricta a largo plazo, se recomienda fijar también una revisión/commit concreto del dataset y conservar el identificador de esa revisión.
