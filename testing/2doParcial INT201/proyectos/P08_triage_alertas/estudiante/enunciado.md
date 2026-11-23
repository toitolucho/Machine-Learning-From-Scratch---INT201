# Proyecto P08: Clasificación de alertas de seguridad del SIEM

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que estime, en el momento en que se genera una alerta del SIEM, si corresponde a un incidente real, para priorizar la atención de los analistas, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por el Centro de Operaciones de Seguridad (SOC) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para el Centro de Operaciones de Seguridad (SOC).

## 2. Descripción del caso

El Centro de Operaciones de Seguridad (SOC) de la universidad recibe cientos de alertas diarias del SIEM (sistema que
centraliza los registros de seguridad). La mayoría son falsas alarmas, y los analistas no alcanzan a revisarlas todas
a tiempo: algunos incidentes reales se atendieron con horas de retraso.

El SOC reunió dos meses de alertas, cada una con la conclusión final de los analistas. El SOC necesita un modelo que,
en el momento en que se genera la alerta, estime si corresponde a un incidente real, para atender primero las alertas
con mayor probabilidad.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible estimar, en el momento en que se genera una alerta, si corresponde a un incidente real?
- **Variable objetivo:** `incidente_real` — 1 si los analistas concluyeron que la alerta correspondía a un incidente real; 0 si fue una falsa alarma.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma en el momento en que el SIEM genera la alerta, antes de que cualquier analista la revise, la escale o la cierre.
- **Costo de los errores:**
  - Un incidente real clasificado como falsa alarma queda al final de la cola y se atiende tarde.
  - Una falsa alarma clasificada como incidente consume tiempo de un analista.
  - El SOC prioriza no dejar incidentes reales al final de la cola; sin embargo, si más de la mitad de las alertas priorizadas son falsas alarmas, la priorización pierde su utilidad.
- **Usuarios del resultado:** los analistas del SOC, que revisan las alertas en el orden propuesto por el modelo.
- **Particularidades de los datos:**
  - Durante octubre, una empresa externa realizó un **ejercicio autorizado de ataque (red team)** desde la red `10.99.x.x`. Sus alertas se cerraron con `incidente_real = 0` porque fueron parte del ejercicio.
  - La severidad la asignan reglas escritas por distintos equipos: algunas usan texto en español, otras en inglés y otras un número (1 = baja, 2 = media, 3 = alta).
  - Cuando el SIEM se reinicia, vuelve a enviar algunas alertas.
  - Algunos conectores registraron mal los bytes salientes.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/alertas_siem.csv` | 5 540 | Un registro por alerta del SIEM (septiembre y octubre de 2026) |

**Diccionario de datos** (según la información proporcionada por el Centro de Operaciones de Seguridad (SOC)):

| Columna | Descripción |
|---|---|
| `alerta_id` | Código de la alerta. |
| `fecha_hora` | Fecha y hora de la alerta. |
| `regla_disparada` | Regla del SIEM que generó la alerta. |
| `severidad` | Severidad asignada por la regla. |
| `ip_origen` | Dirección IP de origen del evento. |
| `sensor_id` | Número del sensor que registró el evento. |
| `activo_afectado` | Tipo de equipo afectado: servidor_critico, estacion, impresora o iot. |
| `ip_en_lista_negra` | 1 si la IP de origen figura en listas públicas de direcciones maliciosas. |
| `alertas_relacionadas_24h` | Alertas del mismo origen o destino en las 24 horas anteriores. |
| `usuario_privilegiado` | 1 si el evento involucra una cuenta con privilegios de administrador. |
| `bytes_salientes` | Bytes enviados desde el equipo afectado hacia el exterior durante el evento. |
| `version_siem` | Versión del SIEM. |
| `tiempo_resolucion_min` | Minutos que tomó resolver la alerta, desde su apertura hasta su cierre. |
| `estado_final` | Estado con el que se cerró la alerta: escalado o cerrado. |
| `incidente_real` | Variable objetivo: 1 si los analistas concluyeron que fue un incidente real. |

## 6. Hipótesis planteadas por el cliente

El Centro de Operaciones de Seguridad (SOC) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de las alertas de severidad alta corresponde a incidentes reales.
- **H2.** Las alertas con IP de origen en lista negra tienen una tasa de incidentes reales al menos 3 veces mayor que el resto.
- **H3.** La columna `tiempo_resolucion_min` permitirá construir un clasificador casi perfecto.
- **H4.** La regla `R-POLITICA` casi nunca corresponde a un incidente real (menos del 2 %).

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

El estudiante deberá utilizar el notebook base `notebook_P08.ipynb`. Se pueden agregar celdas dentro de cada
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
| 1 | Notebook completo, basado en `notebook_P08.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a el Centro de Operaciones de Seguridad (SOC) (máximo una página, sin código) | `.pdf` o `.md` |

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
