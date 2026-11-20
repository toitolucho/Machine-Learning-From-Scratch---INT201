# Proyecto {{CÓDIGO}}: {{TÍTULO DEL PROYECTO}}

**Asignatura:** INT201 – Machine Learning
**Evaluación:** Segundo Parcial – Gestión 02-2026
**Modalidad:** {{individual / en parejas}}
**Fecha de entrega:** {{fecha}} · **Defensa oral:** {{fecha}}

---

## 1. Objetivos

**Objetivo general.** Desarrollar una solución de aprendizaje automático para el problema planteado por
{{cliente}}, desde la exploración de los datos hasta la recomendación final, justificando cada decisión con
evidencia.

**Objetivos específicos.** Al concluir el proyecto, el estudiante deberá ser capaz de:

1. Interpretar el contexto del caso e identificar las restricciones que condicionan la solución.
2. Explorar el conjunto de datos y detectar problemas de calidad.
3. Decidir y justificar qué filas y columnas se conservan, corrigen, transforman o excluyen.
4. Entrenar y comparar al menos dos modelos vistos en la asignatura.
5. Seleccionar la métrica de evaluación adecuada al caso y justificar el modelo recomendado.
6. Contrastar las hipótesis planteadas por el cliente con evidencia.
7. Comunicar los resultados en un lenguaje comprensible para el cliente.

## 2. Descripción del caso

<!-- Uno o dos párrafos en tercera persona: quién es el cliente, qué ocurrió y por qué es importante.
     Lenguaje del negocio; no mencionar técnicas de ML ni pasos de limpieza. -->

{{Descripción del escenario}}

## 3. Pregunta de negocio y variable objetivo

- **Pregunta de negocio:** {{¿Qué necesita responder o predecir el cliente?}}
- **Variable objetivo:** `{{columna_objetivo}}` — {{significado de cada valor}}.

## 4. Restricciones y condiciones del caso

<!-- Información que el estudiante debe considerar para tomar decisiones. Aquí se ubican las pistas:
     momento de la predicción (fuga de información), costo de los errores (métrica), usuarios del
     resultado (interpretabilidad) y particularidades de los datos (filtrado). -->

- **Momento de la predicción:** {{cuándo se usará el modelo y qué información existe en ese momento}}.
- **Costo de los errores:** {{consecuencia de un falso negativo y de un falso positivo}}.
- **Usuarios del resultado:** {{quién usará la predicción y qué necesita}}.
- **Particularidades de los datos:** {{procesos del negocio que afectan los registros}}.

## 5. Descripción de los datos

| Archivo | Registros | Descripción |
|---|---|---|
| `data/{{archivo}}.csv` | {{n}} | {{contenido}} |

**Diccionario de datos** (según la información proporcionada por el cliente):

<!-- Descripción honesta de cada columna (incluido cuándo se registra), sin indicar qué hacer con ella. -->

| Columna | Descripción |
|---|---|
| `{{columna}}` | {{descripción}} |

## 6. Hipótesis planteadas por el cliente

<!-- Entre 2 y 4 afirmaciones; al menos una verdadera y una falsa. -->

El cliente plantea las siguientes hipótesis, que el estudiante deberá **confirmar o refutar** con evidencia
(conteos, tablas, gráficos o métricas):

- **H1.** {{hipótesis}}
- **H2.** {{hipótesis}}
- **H3.** {{hipótesis}}

## 7. Actividades a desarrollar

El proyecto no sigue una secuencia de pasos predefinida. El estudiante deberá decidir qué tratamiento aplicar a
los datos y justificar cada decisión en la bitácora. Las preguntas orientadoras de cada fase sirven como guía.

### Fase 1. Comprensión de los datos
El estudiante deberá describir la estructura del conjunto de datos y su calidad.
- ¿Qué representa cada registro? ¿Cuántos registros hay de cada clase?
- ¿Existen valores faltantes, repetidos, imposibles o escritos de formas distintas?
- ¿Todos los registros corresponden a la situación real que el cliente desea predecir?

### Fase 2. Preparación de los datos
El estudiante deberá definir y aplicar el tratamiento de los datos.
- ¿Qué columnas aportan información útil, cuáles no aportan y cuáles no deberían usarse según las condiciones
  del caso (sección 4)?
- ¿Qué registros deben excluirse o corregirse, y qué efecto tendría conservarlos?
- ¿Existe información contenida en alguna columna que pueda transformarse en una variable más útil?
- ¿Qué transformaciones requieren las variables para ser utilizadas por los modelos (codificación, escalado,
  tratamiento de faltantes)?

### Fase 3. Modelado
El estudiante deberá entrenar y comparar al menos dos modelos vistos en la asignatura (regresión logística,
k-NN, árbol de decisión, Naive Bayes, Random Forest).
- ¿Cómo se dividieron los datos y por qué la evaluación es válida?

### Fase 4. Evaluación
El estudiante deberá seleccionar la métrica principal según las condiciones del caso y justificar el modelo
recomendado.
- ¿Qué métrica refleja mejor el costo de los errores descrito en la sección 4?
- ¿Qué modelo, configuración y umbral de decisión se recomiendan?
- ¿Cada hipótesis del cliente se cumple o no se cumple? ¿Con qué evidencia?

### Fase 5. Conclusiones y recomendación
El estudiante deberá presentar la solución en lenguaje del cliente.
- ¿Qué hace la solución, qué tan bien funciona y qué limitaciones tiene?
- ¿Qué datos adicionales permitirían mejorarla?

## 8. Requisitos mínimos

1. El notebook debe ejecutarse completo, de principio a fin, sin errores.
2. Cada decisión sobre los datos debe estar registrada en la bitácora con su evidencia.
3. Se deben comparar al menos dos modelos con la misma división de datos.
4. La métrica principal debe justificarse con las condiciones del caso.
5. Todas las hipótesis del cliente deben responderse.

## 9. Entregables

| N.º | Entregable | Formato |
|---|---|---|
| 1 | Notebook con el desarrollo completo | `.ipynb` |
| 2 | Bitácora de decisiones (plantilla adjunta) | `.md` |
| 3 | Resumen ejecutivo dirigido al cliente (máximo una página, sin código) | `.pdf` o `.md` |

## 10. Defensa oral

La defensa tiene una duración de {{10}} minutos y se desarrolla en tres partes:

1. **Presentación** ({{3}} min): el estudiante expone la solución como si se dirigiera al cliente.
2. **Preguntas** ({{4}} min): el docente consulta sobre las decisiones registradas en la bitácora y los
   resultados obtenidos.
3. **Tarea en el notebook** ({{3}} min): el docente solicita una modificación o un análisis adicional en el
   notebook; el estudiante deberá realizarlo y explicar el resultado.

El estudiante deberá contar con su notebook abierto y ejecutable durante la defensa.

## 11. Criterios de evaluación

| Criterio | Ponderación |
|---|---|
| Comprensión del caso y de sus restricciones | 15 % |
| Preparación de datos justificada en la bitácora | 25 % |
| Modelado y evaluación (división válida, comparación, métrica pertinente) | 20 % |
| Contraste de hipótesis con evidencia | 10 % |
| Resumen ejecutivo para el cliente | 10 % |
| Defensa oral (explicación, respuestas y tarea en el notebook) | 20 % |

La calificación del trabajo escrito se ajusta según la defensa: las decisiones que el estudiante no pueda
explicar no se consideran parte de su trabajo.
