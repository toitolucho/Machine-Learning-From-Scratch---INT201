# Proyecto P02: Detección de correos de phishing en el correo institucional

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, en el momento en que un correo llega al servidor, los mensajes de phishing dirigidos al personal de la universidad, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Unidad de Seguridad de la Información (USI) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Unidad de Seguridad de la Información (USI).

## 2. Descripción del caso

La Unidad de Seguridad de la Información (USI) de la universidad administra el correo institucional del personal
docente y administrativo. Durante el último semestre aumentaron los correos fraudulentos que suplantan a bancos,
a la propia universidad o a proveedores, con el fin de robar contraseñas o datos de pago.

La USI recopiló los correos recibidos durante dos meses. Un equipo de analistas revisó cada mensaje y determinó si
era phishing. La USI necesita un modelo que, cuando un correo llega al servidor y antes de entregarlo en la bandeja
de entrada, estime si es phishing. Los correos sospechosos se enviarán a una carpeta de cuarentena.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, en el momento en que un correo llega al servidor, los mensajes que probablemente son phishing?
- **Variable objetivo:** `es_phishing` — 1 si los analistas confirmaron el correo como phishing; 0 en caso contrario.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma cuando el correo llega al servidor, antes de entregarlo al destinatario y antes de que cualquier persona lo lea, lo reporte o lo revise.
- **Costo de los errores:**
  - Un correo de phishing que llega a la bandeja de entrada puede provocar el robo de credenciales o un pago fraudulento.
  - Un correo legítimo enviado a cuarentena retrasa una comunicación (el destinatario puede recuperarlo de la carpeta de cuarentena).
  - La USI prefiere enviar correos a cuarentena en exceso antes que dejar pasar phishing; sin embargo, si más de 4 de cada 10 correos en cuarentena resultan legítimos, el personal dejará de revisar esa carpeta.
- **Usuarios del resultado:** el servidor de correo, de forma automática, y los analistas de la USI, que necesitan comprender por qué un correo fue enviado a cuarentena.
- **Particularidades de los datos:**
  - La USI ejecuta campañas de concienciación: envía correos de **simulacro de phishing** al personal desde la cuenta `avisos@usfx-soporte.com`, un dominio externo que imita al institucional. Estos correos se registran como legítimos (`es_phishing = 0`) porque no son un ataque real.
  - Cuando el servidor de registro se reinicia, vuelve a enviar algunos registros que ya había enviado.
  - El resultado de la verificación SPF (autenticación del remitente) no siempre se registra: algunos servidores de origen no publican esa información.
  - El analizador de correos tuvo errores en algunos mensajes al contar enlaces o calcular el tamaño.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/correos_institucionales.csv` | 4 570 | Un registro por correo recibido (septiembre y octubre de 2026) |

**Diccionario de datos** (según la información proporcionada por la Unidad de Seguridad de la Información (USI)):

| Columna | Descripción |
|---|---|
| `correo_id` | Código del correo en el servidor. |
| `fecha_recepcion` | Fecha y hora en que el correo llegó al servidor. |
| `remitente` | Dirección de correo del remitente. |
| `destinatario_area` | Área de la universidad a la que pertenece el destinatario. |
| `num_enlaces` | Cantidad de enlaces en el cuerpo del correo, según el analizador. |
| `num_enlaces_acortados` | Cantidad de enlaces que usan acortadores (bit.ly, tinyurl, etc.). |
| `palabras_urgentes` | Cantidad de expresiones de urgencia detectadas («urgente», «suspendida», «verifique»…). |
| `tipo_adjunto` | Tipo del archivo adjunto principal; «ninguno» si no tiene. El formato del texto no es uniforme. |
| `tamano_kb` | Tamaño del correo en KB, según el analizador. |
| `spf_resultado` | Resultado de la verificación SPF del remitente (pass, fail, softfail). Puede estar vacío. |
| `cliente_correo_destinatario` | Programa que usa el destinatario para leer su correo. |
| `servidor_entrada` | Servidor que recibió el correo. |
| `reportado_por_usuarios` | Cantidad de usuarios que marcaron el correo como sospechoso con el botón «Reportar». Se actualiza durante los días siguientes a la entrega. |
| `enlace_bloqueado_por_proxy` | 1 si el proxy bloqueó un enlace del correo cuando un usuario intentó abrirlo. |
| `es_phishing` | Variable objetivo: 1 si los analistas confirmaron el correo como phishing. |

## 6. Hipótesis planteadas por el cliente

La Unidad de Seguridad de la Información (USI) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de los correos de phishing llega fuera del horario laboral (antes de las 08:00 o desde las 18:00).
- **H2.** El área de Finanzas recibe proporcionalmente más phishing que las demás áreas.
- **H3.** El número de reportes de usuarios (`reportado_por_usuarios`) permitirá construir un detector casi perfecto.
- **H4.** La mayoría de los correos de phishing contiene un archivo adjunto.

## 7. Actividades a desarrollar

El proyecto no sigue una secuencia de pasos predefinida. El estudiante deberá decidir qué tratamiento aplicar a
los datos y justificar cada decisión en la bitácora. Las preguntas orientadoras de cada fase sirven como guía.

### Fase 1. Comprensión de los datos
El estudiante deberá describir la estructura del conjunto de datos y su calidad.
- ¿Qué representa cada registro? ¿Cómo se distribuye la variable objetivo?
- ¿Existen valores faltantes, repetidos, imposibles o escritos de formas distintas?
- ¿Todos los registros corresponden a la situación real que el cliente desea predecir?

### Fase 2. Preparación de los datos
El estudiante deberá definir y aplicar el tratamiento de los datos.
- ¿Qué columnas aportan información útil, cuáles no aportan y cuáles no deberían usarse según el momento de la
  predicción (sección 4)?
- ¿Qué registros deben excluirse o corregirse, y qué efecto tendría conservarlos?
- ¿Existe información contenida en alguna columna que pueda transformarse en una variable más útil?
- ¿Qué transformaciones requieren las variables para ser utilizadas por los modelos (codificación, escalado,
  tratamiento de faltantes)?

### Fase 3. Modelado
El estudiante deberá entrenar los modelos definidos en la sección 8: regresión logística y Random Forest (obligatorios) y, opcionalmente, k-NN, árbol de decisión o Naive Bayes.
- ¿Por qué la división de datos definida en el protocolo produce una evaluación válida?

### Fase 4. Evaluación
El estudiante deberá seleccionar la métrica principal según las condiciones del caso y justificar el modelo
recomendado.
- ¿Qué métrica refleja mejor el costo de los errores descrito en la sección 4?
- ¿Qué modelo y qué configuración se recomiendan?
- ¿Cada hipótesis se cumple o no se cumple? ¿Con qué evidencia?

### Fase 5. Conclusiones y recomendación
El estudiante deberá presentar la solución en lenguaje del cliente.
- ¿Qué hace la solución, qué tan bien funciona y qué limitaciones tiene?
- ¿Qué datos adicionales permitirían mejorarla?

## 8. Protocolo obligatorio de evaluación

Para que los resultados de todos los estudiantes sean comparables, el notebook deberá respetar las siguientes
condiciones. Las decisiones sobre **qué registros y columnas utilizar** siguen siendo responsabilidad del
estudiante.

| Elemento | Condición obligatoria |
|---|---|
| Momento de la división | Después de eliminar duplicados y excluir los registros que no correspondan a casos reales |
| División de datos | `train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)` |
| Preprocesamiento | Imputación, escalado y codificación dentro de un `Pipeline` / `ColumnTransformer`, ajustados solo con los datos de entrenamiento |
| Modelo obligatorio 1 | `LogisticRegression(max_iter=1000, class_weight="balanced")` |
| Modelo obligatorio 2 | `RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)` |
| Métricas | Exactitud, precisión y recall de la clase positiva (1), sobre el conjunto de prueba |
| Umbral | Resultados con umbral 0.5 y análisis de los umbrales 0.1, 0.2, …, 0.9 para el modelo recomendado |
| Validación cruzada | `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`, métrica recall |

## 9. Estructura obligatoria del notebook

El estudiante deberá utilizar el notebook base `notebook_P02.ipynb`. Se pueden agregar celdas dentro de cada
sección, pero no cambiar su orden ni sus títulos.

| Sección | Contenido esperado |
|---|---|
| 1. Carga de datos | Lectura del archivo y dimensiones |
| 2. Comprensión de los datos | Tipos, faltantes, duplicados, valores imposibles, categorías, registros no reales |
| 3. Preparación de los datos | Cada decisión con el formato **Decisión → Evidencia → Justificación** |
| 4. Contraste de hipótesis | H1 a H4 con evidencia |
| 5. Modelado | División y modelos según el protocolo (sección 8) |
| 6. Evaluación | Métricas, matrices de confusión, análisis de umbral y validación cruzada |
| 7. Conclusiones | Modelo recomendado, justificación y limitaciones |
| 8. Ficha de resultados | Celda final que genera `ficha_resultados.json` (sección 10) |

## 10. Ficha de resultados

La última sección del notebook deberá completar el diccionario `FICHA` (ya definido en el notebook base) con los
valores obtenidos por el estudiante y guardarlo como `ficha_resultados.json`. Cada campo debe calcularse con
código a partir de los datos, no escribirse a mano. La ficha se utiliza para comparar las soluciones y forma
parte de la evaluación.

## 11. Requisitos mínimos

1. El notebook debe ejecutarse completo, de principio a fin, sin errores.
2. Cada decisión sobre los datos debe estar registrada en la bitácora con su evidencia.
3. El protocolo de la sección 8 y la estructura de la sección 9 deben respetarse.
4. La ficha de resultados debe estar completa y generada por el notebook.
5. Todas las hipótesis deben responderse.

## 12. Entregables

| N.º | Entregable | Formato |
|---|---|---|
| 1 | Notebook completo, basado en `notebook_P02.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a la Unidad de Seguridad de la Información (USI) (máximo una página, sin código) | `.pdf` o `.md` |

## 13. Evaluación individual

La evaluación del proyecto incluye tres instancias individuales:

1. **Cuestionario en Moodle** sobre el proyecto: preguntas sobre los datos, las decisiones tomadas, el código
   del protocolo y la interpretación de los resultados. El cuestionario es común para todos los estudiantes que
   desarrollaron el mismo proyecto.
2. **Defensa oral** (10 minutos): presentación (3 min), preguntas sobre la bitácora y los resultados (4 min) y una
   tarea en el notebook que el estudiante deberá realizar y explicar (3 min).
3. **Revisión del trabajo escrito** (notebook, ficha, bitácora y resumen ejecutivo).

El estudiante deberá contar con su notebook abierto y ejecutable durante la defensa.

## 14. Criterios de evaluación

| Criterio | Ponderación |
|---|---|
| Trabajo escrito: preparación de datos justificada en la bitácora | 20 % |
| Trabajo escrito: modelado y evaluación según el protocolo; ficha de resultados | 15 % |
| Trabajo escrito: contraste de hipótesis y resumen ejecutivo | 10 % |
| Cuestionario en Moodle | 30 % |
| Defensa oral (explicación, respuestas y tarea en el notebook) | 25 % |

La calificación del trabajo escrito se ajusta según el cuestionario y la defensa: las decisiones que el
estudiante no pueda explicar no se consideran parte de su trabajo.
