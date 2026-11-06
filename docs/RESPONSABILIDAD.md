# Responsabilidad, privacidad, seguridad y licencias

## 1. Uso previsto

Vigía es un prototipo académico de apoyo a la moderación de comentarios. Su resultado debe orientar una revisión humana y no utilizarse como veredicto definitivo, sanción automática o única base para eliminar contenido o restringir cuentas.

## 2. Riesgos y sesgos

- **Falsos positivos:** un comentario legítimo puede clasificarse como tóxico.
- **Falsos negativos:** un comentario ofensivo puede clasificarse como no tóxico.
- **Sesgo lingüístico y cultural:** el dataset está principalmente en inglés y puede no representar expresiones, modismos o contextos propios del español de Chile.
- **Ambigüedad contextual:** sarcasmo, ironía, humor, citas y negaciones pueden dificultar la clasificación.
- **Simplificación de etiquetas:** convertir una puntuación continua en dos clases mediante el umbral 0.5 pierde matices.
- **Truncamiento:** el límite de 256 tokens puede eliminar contexto relevante del final del comentario.

## 3. Privacidad

Los comentarios pueden contener nombres, datos personales u otra información sensible. Para las pruebas se deben preferir ejemplos públicos o sintéticos y evitar ingresar datos personales reales.

El prototipo no debe almacenar ni compartir comentarios sin una finalidad definida, información al usuario y medidas de protección apropiadas. Antes de desplegarlo en un entorno real, se debe revisar dónde se procesan las entradas, qué registros conserva la plataforma y quién puede acceder a ellos.

## 4. Seguridad

- No publicar el archivo del modelo ni la interfaz con permisos abiertos si no es necesario.
- No incluir claves, credenciales ni datos personales en el notebook o repositorio.
- Mantener dependencias actualizadas y revisar su procedencia.
- Validar las entradas antes de procesarlas.
- Limitar el acceso a la interfaz y a los archivos del modelo en cualquier despliegue.
- La interfaz de demostración no equivale a una solución de producción con autenticación, control de acceso, auditoría y protección de datos.

## 5. Licencias y procedencia

Recursos identificados en los notebooks:

- **Dataset:** Civil Comments — https://huggingface.co/datasets/google/civil_comments
- **Modelo base:** `google-bert/bert-base-uncased` — https://huggingface.co/google-bert/bert-base-uncased
- **Modelo ajustado:** artefacto generado por el equipo durante T04 a partir del modelo base y los datos indicados.

Antes de redistribuir el dataset, los pesos o el prototipo, consultar las fichas oficiales de cada recurso y registrar aquí la licencia exacta, atribución requerida y restricciones aplicables. No asumir que el dataset y el modelo comparten licencia.

## 6. Uso de IA generativa

El notebook T03 declara el uso de Claude (Anthropic) como apoyo para estructurar y redactar funciones del código. El equipo indica que revisó y ejecutó el notebook y verificó los casos de demostración.

La clasificación de comentarios la realiza el modelo BERT ajustado; no la realiza la herramienta de IA generativa utilizada como apoyo al desarrollo.

## 7. Condiciones para un uso responsable

1. Presentar la salida como una predicción, no como una verdad.
2. Mantener revisión humana antes de tomar medidas.
3. Informar que el modelo es fiable únicamente para inglés.
4. No utilizarlo para evaluar personas, trabajadores o estudiantes.
5. No procesar información sensible sin autorización y medidas adecuadas.
6. Evaluar periódicamente errores y sesgos antes de cualquier uso real.
