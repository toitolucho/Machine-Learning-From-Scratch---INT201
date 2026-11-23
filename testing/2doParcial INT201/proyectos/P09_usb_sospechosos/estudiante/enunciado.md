# Proyecto P09: Detección de dispositivos USB maliciosos en los laboratorios

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, en el momento en que se conecta un dispositivo USB a una computadora de laboratorio, los dispositivos maliciosos, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Jefatura de Laboratorios de Computación (JLC) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Jefatura de Laboratorios de Computación (JLC).

## 2. Descripción del caso

La Jefatura de Laboratorios de Computación (JLC) detectó infecciones que comenzaron al conectar memorias USB:
algunas contenían programas que se ejecutaban solos (autorun) y otras eran dispositivos que se hacían pasar por
teclados para escribir comandos automáticamente (ataques «BadUSB»).

El agente instalado en las computadoras registró durante dos meses cada conexión de un dispositivo USB. Los técnicos
analizaron los dispositivos y determinaron cuáles eran maliciosos. La JLC necesita un modelo que, en el momento de la
conexión y antes de montar el dispositivo, estime si es malicioso. Los dispositivos sospechosos se **bloquearán** y
el técnico del laboratorio deberá revisarlos. La JLC pide que los técnicos puedan **entender las reglas** del modelo.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, en el momento de la conexión, los dispositivos USB que probablemente son maliciosos?
- **Variable objetivo:** `es_malicioso` — 1 si los técnicos confirmaron que el dispositivo era malicioso; 0 en caso contrario.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma en el momento en que se conecta el dispositivo, antes de montarlo y antes de que se ejecute cualquier archivo o de que intervenga un técnico.
- **Costo de los errores:**
  - Un dispositivo malicioso no bloqueado puede infectar la computadora y, desde ella, la red del laboratorio.
  - Un dispositivo seguro bloqueado obliga al estudiante a esperar la revisión del técnico.
  - La JLC prefiere bloquear de más antes que permitir una infección; sin embargo, si más de la mitad de los bloqueos resultan innecesarios, los técnicos no podrán atenderlos.
- **Usuarios del resultado:** el agente de cada computadora, que bloquea automáticamente, y los técnicos, que necesitan reglas comprensibles.
- **Particularidades de los datos:**
  - El Departamento de TI usa **dispositivos de prueba** (número de serie que comienza con `TI-PRUEBA`) para verificar las políticas de bloqueo. Contienen autorun y emulan teclado a propósito, pero se registran como `es_malicioso = 0`.
  - El fabricante lo informa el propio dispositivo, por lo que aparece escrito de muchas formas; algunos dispositivos no informan fabricante.
  - Cuando el servidor del agente se reinicia, vuelve a enviar algunos registros.
  - Algunos dispositivos informaron una capacidad imposible (0 GB o valores enormes).

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/conexiones_usb.csv` | 3 990 | Un registro por conexión de un dispositivo USB (septiembre y octubre de 2026) |

**Diccionario de datos** (según la información proporcionada por la Jefatura de Laboratorios de Computación (JLC)):

| Columna | Descripción |
|---|---|
| `evento_id` | Código de la conexión. |
| `fecha_hora` | Fecha y hora de la conexión. |
| `equipo_id` | Código de la computadora. |
| `laboratorio` | Laboratorio donde está la computadora. |
| `numero_serie` | Número de serie informado por el dispositivo. |
| `fabricante` | Fabricante informado por el dispositivo. Puede estar vacío. |
| `clase_dispositivo` | Tipo informado: almacenamiento, teclado o compuesto (varias funciones). |
| `capacidad_gb` | Capacidad de almacenamiento informada, en GB. |
| `archivos_autorun` | Cantidad de archivos de ejecución automática en el dispositivo. |
| `archivos_ocultos` | Cantidad de archivos ocultos. |
| `archivos_ejecutables` | Cantidad de archivos ejecutables. |
| `emula_teclado` | 1 si el dispositivo se presenta como teclado (puede escribir comandos). |
| `politica_usb` | Versión de la política de USB aplicada. |
| `alerta_edr_posterior` | 1 si el antivirus avanzado (EDR) generó una alerta en el equipo después de la conexión. |
| `equipo_reinstalado` | 1 si la computadora tuvo que reinstalarse después de la conexión. |
| `es_malicioso` | Variable objetivo: 1 si los técnicos confirmaron que el dispositivo era malicioso. |

## 6. Hipótesis planteadas por el cliente

La Jefatura de Laboratorios de Computación (JLC) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de los dispositivos maliciosos son de fabricante genérico o desconocido.
- **H2.** Todos los dispositivos que emulan teclado son maliciosos.
- **H3.** La columna `alerta_edr_posterior` permitirá construir un detector casi perfecto.
- **H4.** Los dispositivos de mayor capacidad (más de 64 GB) son más peligrosos que los de menor capacidad.

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

El estudiante deberá utilizar el notebook base `notebook_P09.ipynb`. Se pueden agregar celdas dentro de cada
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
| 1 | Notebook completo, basado en `notebook_P09.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a la Jefatura de Laboratorios de Computación (JLC) (máximo una página, sin código) | `.pdf` o `.md` |

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
