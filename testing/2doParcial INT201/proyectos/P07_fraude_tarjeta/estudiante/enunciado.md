# Proyecto P07: Detección de fraude con la tarjeta universitaria

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, en el momento del pago, las transacciones fraudulentas con la tarjeta universitaria, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Unidad de Servicios Financieros (USF) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Unidad de Servicios Financieros (USF).

## 2. Descripción del caso

La tarjeta universitaria permite pagar en la cafetería, fotocopiadoras, biblioteca y librería, y recargar saldo en
línea. Durante el semestre aumentaron los reclamos de estudiantes y funcionarios por consumos que no realizaron:
tarjetas extraviadas usadas por terceros y recargas con datos robados.

La Unidad de Servicios Financieros (USF) reunió dos meses de transacciones y confirmó cuáles fueron fraudulentas. La
USF necesita un modelo que, en el momento del pago y antes de aprobarlo, estime si la transacción es fraudulenta.
Las transacciones sospechosas se **rechazarán** y se pedirá al titular confirmar su identidad.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, en el momento del pago, las transacciones fraudulentas con la tarjeta universitaria?
- **Variable objetivo:** `es_fraude` — 1 si la USF confirmó la transacción como fraudulenta; 0 en caso contrario.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma en el momento del pago, antes de aprobar la transacción y antes de cualquier reclamo del titular o acción de la USF.
- **Costo de los errores:**
  - Un fraude aprobado significa dinero perdido para el titular y un reclamo que la USF debe reembolsar.
  - Una transacción legítima rechazada obliga al titular a confirmar su identidad (molestia en la fila de la cafetería).
  - La USF prefiere rechazar de más antes que aprobar fraudes; sin embargo, si más de 7 de cada 10 rechazos resultan legítimos, los usuarios dejarán de usar la tarjeta.
- **Usuarios del resultado:** el sistema de pagos, que rechaza automáticamente, y el personal de la USF que atiende los reclamos.
- **Particularidades de los datos:**
  - El proveedor del sistema de pagos realiza **transacciones de prueba** desde la terminal `POS-PRUEBA`. El sistema antifraude anterior las marcó como fraude (`es_fraude = 1`), aunque no son consumos reales.
  - Algunas terminales registran el monto con coma decimal y otras con punto; algunas agregan el prefijo «Bs».
  - Los nombres de los puntos de venta los escribe cada terminal, por lo que no son uniformes.
  - Cuando el servidor de pagos se reinicia, vuelve a enviar algunas transacciones.
  - El saldo previo no se registró en algunas transacciones por una falla del servidor.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/transacciones_tarjeta.csv` | 6 670 | Un registro por transacción (septiembre y octubre de 2026) |

**Diccionario de datos** (según la información proporcionada por la Unidad de Servicios Financieros (USF)):

| Columna | Descripción |
|---|---|
| `transaccion_id` | Código de la transacción. |
| `tarjeta_id` | Código de la tarjeta. |
| `fecha_hora` | Fecha y hora de la transacción. |
| `terminal` | Código de la terminal de pago. |
| `punto_venta` | Tipo de punto de venta (cafetería, fotocopiadora, biblioteca, librería, recarga en línea). |
| `canal` | presencial u online. |
| `tipo_usuario` | estudiante, docente o administrativo. |
| `monto` | Monto de la transacción en bolivianos, tal como lo registra la terminal. |
| `saldo_previo_bs` | Saldo de la tarjeta antes de la transacción. Puede estar vacío. |
| `transacciones_ultima_hora` | Transacciones de la misma tarjeta en la hora anterior. |
| `minutos_desde_transaccion_anterior` | Minutos desde la transacción anterior de la misma tarjeta. |
| `distancia_ubicacion_anterior_m` | Distancia en metros entre el punto de venta actual y el de la transacción anterior. |
| `moneda` | Moneda de la transacción. |
| `diseno_tarjeta` | Diseño visual de la tarjeta (clásica o aniversario). |
| `tarjeta_bloqueada` | 1 si la tarjeta fue bloqueada después de un reporte de robo o extravío. |
| `reclamo_titular` | 1 si el titular presentó un reclamo por esta transacción. |
| `es_fraude` | Variable objetivo: 1 si la USF confirmó la transacción como fraudulenta. |

## 6. Hipótesis planteadas por el cliente

La Unidad de Servicios Financieros (USF) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de los fraudes ocurre en recargas en línea.
- **H2.** Las transacciones fraudulentas tienen montos mayores que las legítimas (comparando medianas).
- **H3.** La columna `tarjeta_bloqueada` permitirá construir un detector casi perfecto.
- **H4.** Las tarjetas con más de 3 transacciones en la última hora son fraudulentas en la mayoría de los casos.

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

El estudiante deberá utilizar el notebook base `notebook_P07.ipynb`. Se pueden agregar celdas dentro de cada
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
| 1 | Notebook completo, basado en `notebook_P07.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a la Unidad de Servicios Financieros (USF) (máximo una página, sin código) | `.pdf` o `.md` |

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
