# Arquitectura e integración

## 1. Descripción

El prototipo integra un modelo BERT previamente ajustado en una aplicación de demostración. El notebook T03 carga el modelo y su tokenizador desde un archivo ZIP, valida cada entrada y ejecuta inferencia sin modificar los pesos.

## 2. Componentes

| Componente | Responsabilidad |
|---|---|
| Usuario/moderador | Ingresa o pega un comentario. |
| Interfaz Vigía (Gradio) | Recibe el comentario y presenta el resultado. |
| Validador de entrada | Comprueba tipo, contenido, longitud mínima/máxima y presencia de letras. |
| Detector/advertencias de idioma | Advierte cuando el texto parece estar en español u otro idioma distinto del inglés admitido. |
| Tokenizador BERT | Convierte el texto en tokens y aplica truncamiento a 256 tokens. |
| Modelo BERT fine-tuned | Calcula logits para las clases No tóxico y Tóxico. |
| Postprocesamiento | Aplica softmax y prepara etiqueta, probabilidad y advertencias. |
| Salida | Presenta el resultado para apoyar la revisión humana. |

## 3. Flujo

```text
Moderador
   |
   v
Interfaz Vigía (Gradio)
   |
   v
Validación de entrada
   |--------------------> Error: detener y mostrar mensaje
   |
   v
Advertencias (idioma / truncamiento)
   |
   v
Tokenizador BERT (máx. 256 tokens)
   |
   v
BERT fine-tuned (modo evaluación)
   |
   v
Softmax y postprocesamiento
   |
   v
Etiqueta + probabilidad + advertencias
   |
   v
Revisión humana
```

## 4. Contrato de entrada

| Campo | Tipo | Regla |
|---|---|---|
| `texto` | `string` | Obligatorio; entre 3 y 5.000 caracteres; no vacío ni solo espacios; debe contener al menos una letra. |

El modelo es fiable únicamente para comentarios en inglés. La advertencia de idioma no necesariamente bloquea la inferencia.

## 5. Contrato de salida

| Campo | Tipo | Descripción |
|---|---|---|
| `etiqueta` | `string` | `Tóxico` o `No tóxico`. |
| `prob_toxico` | `float` | Probabilidad asignada a la clase tóxica, entre 0 y 1. |
| `confianza` | `float` | Probabilidad de la clase predicha. |
| `umbral` | `float` | Umbral de decisión documentado: 0.5. |
| `advertencias` | `list[string]` | Avisos que no detienen la inferencia. |
| `limitacion` | `string` | Limitación relevante para interpretar el resultado. |

## 6. Decisiones de integración

- El modelo y el tokenizador se cargan una sola vez.
- El modelo se establece en modo evaluación (`eval()`).
- La inferencia se ejecuta sin gradientes.
- La aplicación separa errores de validación (detienen el proceso) de advertencias (permiten continuar).
- Se conserva `max_length=256`, igual que durante el entrenamiento.
- La interfaz de demostración no requiere una API externa ni un servicio de inferencia independiente.

## 7. Control de integridad

T03 calcula una suma de verificación de los pesos antes y después de realizar predicciones. La igualdad de ambas sumas, junto con el modo `eval()`, sirve como evidencia de que la inferencia no reajusta los pesos del modelo.
