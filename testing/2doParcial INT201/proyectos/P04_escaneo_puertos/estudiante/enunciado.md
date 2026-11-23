# Proyecto P04: Detección de escaneo de puertos en la red del campus

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, al cierre de cada hora, los equipos de la red del campus que están realizando escaneo de puertos, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por el Área de Redes y Comunicaciones (ARC) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para el Área de Redes y Comunicaciones (ARC).

## 2. Descripción del caso

El Área de Redes y Comunicaciones (ARC) administra la red del campus: laboratorios, Wi-Fi de estudiantes, red
administrativa y servidores. Un escaneo de puertos ocurre cuando un equipo intenta conectarse a muchos puertos o
equipos para descubrir servicios vulnerables; suele ser el primer paso de un ataque o la señal de un equipo infectado.

El firewall resume cada hora la actividad de cada equipo (dirección IP). Los analistas revisaron dos meses de
resúmenes e identificaron cuáles correspondían a escaneos. El ARC necesita un modelo que, al cierre de cada hora,
estime si un equipo estuvo escaneando. Los equipos marcados se **aislarán automáticamente** de la red hasta su revisión.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, al cierre de cada hora, los equipos que probablemente están realizando un escaneo de puertos?
- **Variable objetivo:** `es_escaneo` — 1 si los analistas confirmaron que el equipo realizó un escaneo en esa hora; 0 en caso contrario.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma al cierre de cada hora, con el resumen de actividad de esa hora, antes de cualquier acción del sistema de prevención (IPS) o de los analistas.
- **Costo de los errores:**
  - Aislar un equipo legítimo interrumpe clases, servicios o trabajo administrativo, y genera reclamos inmediatos.
  - Un escaneo no detectado permite que el atacante continúe explorando la red.
  - Como el aislamiento es automático, el ARC prefiere un detector **confiable** (pocas falsas alarmas), siempre que detecte al menos 6 de cada 10 escaneos.
- **Usuarios del resultado:** el sistema de aislamiento automático y los analistas del ARC, que revisan cada equipo aislado.
- **Particularidades de los datos:**
  - El ARC ejecuta cada noche un **escáner de vulnerabilidades autorizado** desde la dirección `10.10.5.50`. Su actividad se registra como normal (`es_escaneo = 0`) porque es una tarea aprobada.
  - Cuando el colector de registros se reinicia, vuelve a enviar algunos resúmenes.
  - La columna `protocolo_predominante` proviene de equipos de distintos fabricantes, que no la escriben igual.
  - El sensor que mide la duración de las conexiones tuvo cortes; en esos casos el campo queda vacío.
  - En algunos resúmenes, el porcentaje de conexiones rechazadas se calculó mal.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/flujos_red_campus.csv` | 4 930 | Un registro por equipo y hora (septiembre y octubre de 2026) |

**Diccionario de datos** (según la información proporcionada por el Área de Redes y Comunicaciones (ARC)):

| Columna | Descripción |
|---|---|
| `registro_id` | Código del resumen. |
| `fecha_hora` | Hora del resumen (inicio del intervalo de una hora). |
| `ip_origen` | Dirección IP del equipo. |
| `subred_origen` | Segmento de la red: laboratorios, wifi_estudiantes, administrativa o servidores. |
| `vlan_id` | Número de la red virtual (VLAN) asignada al segmento. |
| `puertos_distintos` | Cantidad de puertos de destino distintos contactados en la hora. |
| `equipos_destino_distintos` | Cantidad de equipos de destino distintos contactados en la hora. |
| `conexiones_por_minuto` | Promedio de conexiones iniciadas por minuto. |
| `pct_conexiones_rechazadas` | Porcentaje de conexiones rechazadas o sin respuesta (0 a 100). |
| `bytes_promedio_por_conexion` | Promedio de bytes transferidos por conexión. |
| `duracion_media_conexion_s` | Duración promedio de las conexiones, en segundos. Puede estar vacía. |
| `protocolo_predominante` | Protocolo más usado en la hora (TCP, UDP o ICMP). |
| `version_firewall` | Versión del firewall que generó el resumen. |
| `bloqueado_por_ips` | 1 si el sistema de prevención de intrusos (IPS) bloqueó el equipo como respuesta a su actividad. |
| `ticket_soc_abierto` | 1 si los analistas abrieron un ticket de incidente para el equipo (al revisar la actividad). |
| `es_escaneo` | Variable objetivo: 1 si los analistas confirmaron un escaneo en esa hora. |

## 6. Hipótesis planteadas por el cliente

El Área de Redes y Comunicaciones (ARC) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de los escaneos proviene de la red Wi-Fi de estudiantes.
- **H2.** Un equipo que contacta más de 100 puertos distintos en una hora siempre está realizando un escaneo.
- **H3.** La columna `bloqueado_por_ips` permitirá construir un detector casi perfecto.
- **H4.** Los escaneos usan principalmente el protocolo ICMP.

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

El estudiante deberá utilizar el notebook base `notebook_P04.ipynb`. Se pueden agregar celdas dentro de cada
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
| 1 | Notebook completo, basado en `notebook_P04.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a el Área de Redes y Comunicaciones (ARC) (máximo una página, sin código) | `.pdf` o `.md` |

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
