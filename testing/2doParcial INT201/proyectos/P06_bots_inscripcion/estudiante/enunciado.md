# Proyecto P06: Detección de bots en el portal de inscripciones

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, durante la sesión, los accesos automatizados (bots) al portal de inscripciones, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Dirección de Registro e Inscripciones (DRI) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Dirección de Registro e Inscripciones (DRI).

## 2. Descripción del caso

Durante la semana de inscripciones, el portal de la Dirección de Registro e Inscripciones (DRI) recibe miles de
sesiones. En la última gestión, algunas personas usaron programas automatizados (bots) para reservar cupos en
materias con pocas plazas y luego revenderlos, dejando sin cupo a estudiantes reales.

La DRI revisó las sesiones de dos semanas de inscripción y determinó cuáles eran bots. La DRI necesita un modelo
que, después de los primeros minutos de cada sesión, estime si se trata de un bot. Las sesiones marcadas se
**bloquearán automáticamente**.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, durante la sesión, los accesos al portal de inscripciones realizados por bots?
- **Variable objetivo:** `es_bot` — 1 si la DRI confirmó que la sesión fue realizada por un bot; 0 si fue una persona.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma durante la sesión, con la actividad de sus primeros minutos, antes de que la sesión termine y antes de cualquier revisión o medida de la DRI.
- **Costo de los errores:**
  - Bloquear a un estudiante real durante la inscripción puede dejarlo sin cupo en sus materias: es el error más grave.
  - Un bot no detectado puede acaparar cupos, pero la DRI puede anular esas inscripciones después.
  - Como el bloqueo es automático, la DRI exige un detector **confiable** (pocas falsas alarmas), siempre que detecte al menos 6 de cada 10 bots.
- **Usuarios del resultado:** el portal, que bloquea automáticamente, y el personal de la DRI, que atiende los reclamos de bloqueo.
- **Particularidades de los datos:**
  - La DTI usa un **monitor de disponibilidad** (`UptimeRobot`) que consulta el portal cada minuto desde la IP `10.0.0.9`. Sus sesiones se registran como `es_bot = 0` porque es un servicio autorizado.
  - Las inscripciones abren a las 08:00 cada día de la semana de inscripción.
  - El CAPTCHA solo se muestra en algunas sesiones, según reglas antiguas del portal; si no se mostró, el campo queda vacío.
  - Cuando el servidor web se reinicia, vuelve a enviar algunos registros.
  - El cálculo del tiempo entre clics presentó errores en algunas sesiones.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/sesiones_inscripcion.csv` | 5 570 | Un registro por sesión del portal (dos semanas de inscripción, 2026) |

**Diccionario de datos** (según la información proporcionada por la Dirección de Registro e Inscripciones (DRI)):

| Columna | Descripción |
|---|---|
| `sesion_id` | Código de la sesión. |
| `ip_origen` | Dirección IP de la sesión. |
| `codigo_estudiante` | Código del estudiante autenticado en la sesión. |
| `inicio_sesion` | Fecha y hora de inicio de la sesión. |
| `user_agent` | Texto que identifica el navegador o programa que accede al portal. |
| `solicitudes_por_minuto` | Promedio de solicitudes al servidor por minuto. |
| `tiempo_medio_entre_clics_s` | Tiempo promedio entre clics, en segundos. |
| `paginas_distintas` | Cantidad de páginas distintas visitadas. |
| `materias_intentadas` | Cantidad de materias en las que se intentó inscribir. |
| `captcha_resultado` | Resultado del CAPTCHA (aprobado o fallido). Vacío si no se mostró. |
| `idioma_navegador` | Idioma configurado en el navegador. |
| `servidor_app` | Servidor que atendió la sesión. |
| `sesion_bloqueada_manual` | 1 si el personal de la DRI bloqueó la sesión manualmente tras revisarla. |
| `inscripciones_anuladas` | Cantidad de inscripciones de la sesión anuladas posteriormente por la DRI. |
| `es_bot` | Variable objetivo: 1 si la DRI confirmó que la sesión fue un bot. |

## 6. Hipótesis planteadas por el cliente

La Dirección de Registro e Inscripciones (DRI) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** La mayoría de los bots actúa en los primeros 10 minutos después de la apertura de inscripciones.
- **H2.** Todos los bots usan herramientas automatizadas evidentes (`python-requests`, `curl`) como agente de usuario.
- **H3.** La columna `sesion_bloqueada_manual` permitirá construir un detector casi perfecto.
- **H4.** Las sesiones en las que no se mostró el CAPTCHA son seguras (casi no contienen bots).

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

El estudiante deberá utilizar el notebook base `notebook_P06.ipynb`. Se pueden agregar celdas dentro de cada
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
| 1 | Notebook completo, basado en `notebook_P06.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a la Dirección de Registro e Inscripciones (DRI) (máximo una página, sin código) | `.pdf` o `.md` |

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
