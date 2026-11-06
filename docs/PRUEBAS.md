# Pruebas y validación

## 1. Objetivo

Verificar que el prototipo recibe entradas válidas, rechaza entradas inválidas, genera predicciones y comunica las limitaciones conocidas. Los resultados observados deben registrarse después de ejecutar T03; los resultados esperados no deben presentarse como resultados obtenidos.

## 2. Casos de prueba

| ID | Propósito | Entrada | Condiciones | Resultado esperado | Resultado observado | Conclusión |
|---|---|---|---|---|---|---|
| CP01 | Clasificar un comentario neutral | `You are a wonderful person.` | String en inglés, 3–5.000 caracteres, contiene letras. | Clasificar y mostrar etiqueta, probabilidad tóxica y confianza. Se espera No tóxico. | Completar tras ejecutar | Pendiente |
| CP02 | Clasificar un comentario tóxico | `You are stupid and completely useless.` | String en inglés, 3–5.000 caracteres, contiene letras. | Clasificar y mostrar etiqueta, probabilidad tóxica y confianza. Se espera Tóxico. | Completar tras ejecutar | Pendiente |
| CP03 | Rechazar texto vacío | `""` | Cadena vacía. | Rechazar la solicitud e informar el motivo. No ejecutar el modelo. | Completar tras ejecutar | Pendiente |
| CP04 | Rechazar texto de menos de 3 caracteres | `a` | Longitud inferior a 3 caracteres. | Rechazar e informar la longitud mínima. | Completar tras ejecutar | Pendiente |
| CP05 | Rechazar texto sin letras | `12345%` | No contiene letras. | Rechazar e informar que debe contener al menos una letra. | Completar tras ejecutar | Pendiente |
| CP06 | Advertir limitación de idioma | `Esto es muy malo y no me gusta para nada lo que dices en este comentario.` | Texto en español. El modelo es fiable únicamente en inglés. | Mostrar advertencia de idioma. Si la implementación permite continuar, indicar que el resultado no es fiable. | Completar tras ejecutar | Pendiente |
| CP07 | Rechazar máximo de caracteres | Cadena de 5.001 caracteres. | Supera el límite de 5.000 caracteres. | Rechazar e informar el máximo permitido. No ejecutar el modelo. | Completar tras ejecutar | Pendiente |
| CP08 | Rechazar tipo de entrada distinto de string | `["hello", "world"]` | La entrada es una lista, no una cadena. | Rechazar e informar que se requiere texto (`string`). | Completar tras ejecutar | Pendiente |
| CP09 | Advertir truncamiento de tokens | Comentario en inglés de más de 256 tokens. | La entrada cumple el límite de caracteres, pero supera `MAX_LENGTH=256` tokens. | Ejecutar con truncamiento y mostrar advertencia. | Completar tras ejecutar | Pendiente |

## 3. Criterios de aprobación

- **Casos CP01 y CP02:** comparar la etiqueta real con la expectativa; registrar la probabilidad mostrada. Una diferencia se documenta como error de clasificación, no se modifica el resultado observado.
- **Casos CP03–CP05, CP07 y CP08:** aprobar si la aplicación rechaza la entrada y no ejecuta inferencia.
- **Caso CP06:** aprobar si aparece la advertencia de idioma definida por la aplicación. La advertencia no demuestra que la detección de idioma sea perfecta.
- **Caso CP09:** aprobar si el comentario se procesa con truncamiento y se informa la advertencia correspondiente.

## 4. Registro de resultados

Para cada caso registrar:
- salida exacta o mensaje mostrado;
- etiqueta predicha y probabilidad, cuando corresponda;
- si se ejecutó o no el modelo;
- estado: Aprobado / Fallido;
- observación o explicación si el resultado difiere del esperado.

## 5. Métricas del conjunto de prueba

Copiar los resultados reales de la evaluación final de BERT en T04:

| Métrica | Resultado |
|---|---:|
| Accuracy | Completar |
| Precision macro | Completar |
| Recall macro | Completar |
| F1 macro | Completar |
| F1 clase tóxica | Completar |

Incluir también la matriz de confusión o el `classification_report` generado por T04. No inventar valores ni utilizar las predicciones de los ejemplos manuales como sustituto de las métricas del conjunto de prueba.

## 6. Análisis de errores y límites

Examinar especialmente:
- falsos positivos: comentarios no tóxicos clasificados como tóxicos;
- falsos negativos: comentarios tóxicos clasificados como no tóxicos;
- sarcasmo, ironía, negación y expresiones ambiguas;
- comentarios en español u otros idiomas;
- pérdida de contexto por truncamiento a 256 tokens.

La clasificación de ejemplos aislados es una prueba funcional, no una evaluación estadística del rendimiento del modelo.
