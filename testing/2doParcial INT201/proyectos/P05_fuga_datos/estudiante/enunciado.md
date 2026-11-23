# Proyecto P05: Detección de fuga de información por parte de funcionarios

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** individual
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar un modelo de clasificación que identifique, al cierre de cada día, la actividad de funcionarios que probablemente corresponde a una fuga de información, justificando cada decisión con evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué registros y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar los modelos definidos en el protocolo obligatorio y compararlos.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por la Dirección de Seguridad de la Información (DSI) con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para la Dirección de Seguridad de la Información (DSI).

## 2. Descripción del caso

La Dirección de Seguridad de la Información (DSI) protege la información confidencial de la universidad: planillas
de sueldos, expedientes de estudiantes, contratos y resultados de investigación. En la última gestión se confirmaron
varios casos de funcionarios que copiaron información confidencial a servicios externos o memorias USB.

El sistema de prevención de fuga de datos (DLP) resume la actividad diaria de cada funcionario. La DSI revisó dos
meses de resúmenes y confirmó los casos de fuga. La DSI necesita un modelo que, al cierre de cada día, estime qué
registros de actividad corresponden probablemente a una fuga, para que un analista los revise de forma discreta.

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** ¿Es posible identificar, al cierre de cada día, la actividad de funcionarios que probablemente corresponde a una fuga de información?
- **Variable objetivo:** `fuga_confirmada` — 1 si la DSI confirmó una fuga de información en ese día; 0 en caso contrario.

## 4. Restricciones y condiciones del caso

- **Momento de la predicción:** la decisión se toma al cierre de cada día, con el resumen de actividad de ese día, antes de cualquier investigación o medida administrativa.
- **Costo de los errores:**
  - Una fuga no detectada puede exponer información confidencial de estudiantes y funcionarios, con consecuencias legales.
  - Un registro normal marcado solo genera una revisión discreta por parte de un analista (el funcionario no se entera).
  - La DSI prefiere revisar de más antes que dejar pasar una fuga; sin embargo, el equipo de analistas es pequeño: si más de 6 de cada 10 alertas resultan falsas, no podrá revisarlas todas.
- **Usuarios del resultado:** los analistas de la DSI, que necesitan saber por qué un registro fue marcado.
- **Particularidades de los datos:**
  - Cada noche, la cuenta de servicio `svc_backup` realiza **respaldos automáticos** a la nube institucional, con volúmenes muy grandes. Esa actividad se registra como `fuga_confirmada = 0`.
  - Cuando el servidor del DLP se reinicia, vuelve a enviar algunos resúmenes.
  - La columna `dias_desde_aviso_renuncia` solo tiene valor para los funcionarios que presentaron un aviso de renuncia a Recursos Humanos; para los demás está vacía.
  - Algunos agentes del DLP registraron mal los minutos de actividad fuera de horario.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/actividad_funcionarios.csv` | 4 681 | Un registro por funcionario y día (septiembre y octubre de 2026) |

**Diccionario de datos** (según la información proporcionada por la Dirección de Seguridad de la Información (DSI)):

| Columna | Descripción |
|---|---|
| `registro_id` | Código del resumen. |
| `empleado_id` | Código del funcionario. |
| `fecha` | Día del resumen. |
| `area` | Área del funcionario. |
| `mb_subidos_externos` | MB enviados a servicios externos (nube, correo personal, sitios web). |
| `destinos_externos_distintos` | Cantidad de destinos externos distintos. |
| `uso_usb` | 1 si se conectó una memoria USB. |
| `mb_copiados_usb` | MB copiados a memorias USB. |
| `min_actividad_fuera_horario` | Minutos de actividad fuera del horario laboral. |
| `archivos_confidenciales_accedidos` | Cantidad de archivos clasificados como confidenciales que se abrieron. |
| `correos_externos_con_adjunto` | Correos enviados a direcciones externas con archivos adjuntos. |
| `dias_desde_aviso_renuncia` | Días transcurridos desde que el funcionario presentó su aviso de renuncia. Vacío si no presentó aviso. |
| `piso_oficina` | Piso del edificio donde trabaja el funcionario. |
| `politica_dlp_version` | Versión de la política del DLP aplicada. |
| `bajo_investigacion_rrhh` | 1 si Recursos Humanos abrió una investigación sobre el funcionario por este caso. |
| `acceso_revocado` | 1 si se revocaron los accesos del funcionario como medida por este caso. |
| `fuga_confirmada` | Variable objetivo: 1 si la DSI confirmó una fuga de información en ese día. |

## 6. Hipótesis planteadas por el cliente

La Dirección de Seguridad de la Información (DSI) plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** Los funcionarios con aviso de renuncia presentan una tasa de fuga mucho mayor (al menos 5 veces) que el resto.
- **H2.** El área de Sistemas concentra la mayoría de las fugas confirmadas.
- **H3.** La columna `bajo_investigacion_rrhh` permitirá construir un detector casi perfecto.
- **H4.** Los registros con más de 2 000 MB subidos son errores del sistema y pueden eliminarse sin perder fugas.

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

El estudiante deberá utilizar el notebook base `notebook_P05.ipynb`. Se pueden agregar celdas dentro de cada
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
| 1 | Notebook completo, basado en `notebook_P05.ipynb` | `.ipynb` |
| 2 | Ficha de resultados generada por el notebook | `ficha_resultados.json` |
| 3 | Bitácora de decisiones (`bitacora_decisiones.md`, adjunta) | `.md` |
| 4 | Resumen ejecutivo dirigido a la Dirección de Seguridad de la Información (DSI) (máximo una página, sin código) | `.pdf` o `.md` |

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
