# Proyecto P10: Estimación del tiempo de recuperación de servidores tras un incidente

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de regresión que estime, al inicio de un incidente, cuántas horas tomará recuperar los servicios afectados, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Unidad de Infraestructura Tecnológica (UIT) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Unidad de Infraestructura Tecnológica (UIT).

## 2. Descripción del caso

La Unidad de Infraestructura Tecnológica (UIT) administra los servidores de la universidad: sistema académico, correo,
biblioteca digital y plataformas virtuales. Cuando ocurre un incidente (ransomware, falla de hardware, error de
configuración, ataque de denegación de servicio), la UIT debe informar a las autoridades cuánto tiempo estarán
interrumpidos los servicios.

La UIT reunió los registros de los incidentes de los últimos dos años. La UIT necesita un modelo que, **al inicio**
de un incidente, estime cuántas horas tomará la recuperación, para comunicar un tiempo realista y organizar al
personal.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible estimar, al inicio de un incidente, cuántas horas tomará recuperar los servicios?
- **Variable objetivo:** `horas_recuperacion` — horas transcurridas desde el inicio del incidente hasta la recuperación completa de los servicios.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la estimación se realiza al inicio del incidente, con la información disponible en ese momento, antes de comenzar la recuperación y antes de elaborar el informe final.
- **Costo de los errores:**
  - Subestimar el tiempo obliga a anunciar varias prórrogas y genera desconfianza en las autoridades y los usuarios.
  - Sobrestimar el tiempo provoca suspensiones innecesarias de actividades (clases, trámites).
  - La UIT considera aceptable un error de hasta 4 horas en la mayoría de los incidentes.
- **Usuarios del resultado:** el jefe de la UIT, que comunica el tiempo estimado a las autoridades, y el equipo de turno.
- **Particularidades de los datos:**
  - La UIT realiza **simulacros de recuperación** programados (código de incidente que comienza con `SIM-`). Se registran como incidentes, aunque no hubo una interrupción real.
  - `antiguedad_respaldo_dias` está vacía cuando el servidor **no tenía respaldo**.
  - El tipo de incidente lo escribe el técnico que lo registra, por lo que no siempre está escrito igual.
  - Cuando el sistema de tickets se reinicia, vuelve a enviar algunos registros.
  - Algunos registros tienen el tamaño del respaldo mal informado.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/incidentes_servidores.csv` | 2 020 | Un registro por incidente (gestiones 2025 y 2026) |

**Diccionario de datos** (según la información proporcionada por la Unidad de Infraestructura Tecnológica (UIT)):

| Columna | Descripción |
|---|---|
| `incidente_id` | Código del incidente. |
| `fecha_inicio` | Fecha y hora de inicio del incidente. |
| `servidor_principal` | Nombre del servidor principal afectado. |
| `tipo_incidente` | Tipo de incidente registrado por el técnico. |
| `servidores_afectados` | Cantidad de servidores afectados. |
| `criticidad` | Criticidad del servicio afectado: 1 (baja), 2 (media), 3 (alta). |
| `tamano_respaldo_gb` | Tamaño del respaldo a restaurar, en GB. |
| `antiguedad_respaldo_dias` | Días desde el último respaldo disponible. Vacío si no había respaldo. |
| `equipo_turno` | Equipo técnico de turno (A, B o C). |
| `edificio_datacenter` | Edificio del centro de datos. |
| `version_hipervisor` | Versión del software de virtualización. |
| `horas_informe_final` | Horas de interrupción indicadas en el informe final del incidente. |
| `costo_total_bs` | Costo total del incidente calculado por la UIT al cierre (horas de personal, servicios externos). |
| `horas_recuperacion` | Variable objetivo: horas desde el inicio hasta la recuperación completa. |

## 6. Hipótesis planteadas por el cliente

La Unidad de Infraestructura Tecnológica (UIT) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** Los incidentes de ransomware tardan en promedio más del doble que las fallas de hardware.
- **H2.** El equipo de turno C es el más lento: su tiempo promedio de recuperación es claramente mayor que el de los demás.
- **H3.** La columna `horas_informe_final` permitirá construir un modelo casi perfecto.
- **H4.** Los incidentes sin respaldo tardan, en promedio, más del doble que los incidentes con respaldo.

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
El estudiante deberá entrenar los modelos definidos en la sección 8: regresión lineal y Random Forest (obligatorios) y, opcionalmente, k-NN o árbol de decisión.
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
| División de datos | `train_test_split(X, y, test_size=0.25, random_state=42)` |
| Preprocesamiento | Imputación, escalado y codificación dentro de un `Pipeline` / `ColumnTransformer`, ajustados solo con los datos de entrenamiento |
| Modelo obligatorio 1 | `LinearRegression()` |
| Modelo obligatorio 2 | `RandomForestRegressor(n_estimators=200, random_state=42)` |
| Métricas | MAE, RMSE y R² sobre el conjunto de prueba |
| Análisis de errores | Error absoluto medio por tipo y proporción de predicciones con error ≤ 4 horas |
| Validación cruzada | `KFold(n_splits=5, shuffle=True, random_state=42)`, métrica MAE |

## 9. Estructura obligatoria del notebook

El estudiante deberá utilizar el notebook base `notebook_P10.ipynb`. Se pueden agregar celdas dentro de cada
sección, pero no cambiar su orden ni sus títulos.

| Sección | Contenido esperado |
|---|---|
| 1. Carga de datos | Lectura del archivo y dimensiones |
| 2. Comprensión de los datos | Tipos, faltantes, duplicados, valores imposibles, categorías, registros no reales |
| 3. Preparación de los datos | Cada decisión con el formato **Decisión → Evidencia → Justificación** |
| 4. Contraste de hipótesis | H1 a H4 con evidencia |
| 5. Modelado | División y modelos según el protocolo (sección 8) |
| 6. Evaluación | Métricas, gráfico real vs. predicho, errores por grupo y validación cruzada |
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
| 1 | Notebook completo, basado en `notebook_P10.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a la Unidad de Infraestructura Tecnológica (UIT) (máximo una página, sin código) | `.pdf` o `.md` |

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
