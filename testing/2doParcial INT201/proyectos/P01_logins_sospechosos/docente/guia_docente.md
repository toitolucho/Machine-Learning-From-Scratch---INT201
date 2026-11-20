# Guía docente – Proyecto P01: Detección de inicios de sesión sospechosos en el Sistema Académico

> **Documento reservado para el docente.** Contiene los problemas incorporados en los datos, la solución de
> referencia y la pauta de evaluación. A los estudiantes se entrega únicamente la carpeta `estudiante/`.

## Materiales del docente

| Archivo | Contenido |
|---|---|
| `guia_docente.md` | Este documento: problemas incorporados, pistas, resultados de referencia y rúbrica |
| `solucion_P01.ipynb` | Notebook de solución paso a paso (Decisión → Evidencia → Justificación), con anexo de tareas de defensa |
| `defensa_oral.md` | 20 preguntas y 8 tareas en vivo para la defensa, con la respuesta esperada |
| `generar_datos.py` | Generador del conjunto de datos (semilla 2026, resultados reproducibles) |
| `construir_notebook_solucion.py` | Regenera `solucion_P01.ipynb` |
| `solucion_referencia.py` | Cálculo resumido de los efectos de cada problema (verificación rápida) |

## 1. Ficha del proyecto

| Campo | Valor |
|---|---|
| Tipo de problema | Clasificación binaria con clases desbalanceadas |
| Variable objetivo | `es_ataque` (219 ataques de 4 000 registros válidos, 5.5 %) |
| Contenidos evaluados | Duplicados, filtrado de registros, faltantes informativos, categorías inconsistentes, valores imposibles, creación de variables, fuga de información, codificación, escalado, desbalance, precisión y recall, umbral, validación cruzada, comparación de modelos |
| Nivel de dificultad | Medio (proyecto modelo para los demás) |
| Conjunto de datos | `estudiante/data/logins_sia.csv` (4 270 registros, 17 columnas) |

**Recorrido de registros esperado:** 4 270 originales → **4 150** sin duplicados → **4 000** sin cuentas QA.

## 2. Problemas incorporados en los datos

| N.º | Problema | Ubicación | Forma de detección | Tratamiento esperado | Indicador de que no fue comprendido |
|---|---|---|---|---|---|
| T1 | 120 registros duplicados exactos (reenvío de registros) | Todas las columnas, incluido `evento_id` | `df.duplicated().sum()` | Eliminar antes de dividir los datos | No los detecta, o los elimina después de la división |
| T2 | 150 registros de cuentas `qa_bot_*` (IP 10.0.99.x), con patrón de ataque y etiqueta «normal» | `usuario`, `ip_origen` | Filtro por usuario o IP | Excluirlos: no son usuarios reales | Los conserva; el recall baja de 0.873 a 0.818 |
| T3 | `bloqueado_por_soporte`: se registra 1 a 3 días después; coincide 99.4 % con la etiqueta | Columna | Diccionario, coincidencia con la etiqueta, métricas ≈ 1.0 | Excluir (fuga de información). Refutar H3 | Presenta exactitud ≈ 0.997 como un logro |
| T4 | `duracion_sesion_min`: solo existe al terminar la sesión; media 0.3 min en ataques y 46 min en normales | Columna | Momento de la predicción + diccionario | Excluir (fuga de información) | La conserva porque «no es la etiqueta»; métricas = 1.0 |
| T5 | Identificadores: `evento_id`, `usuario`, `ip_origen` | Columnas | Casi un valor distinto por registro | Excluir | Los codifica con One-Hot (miles de columnas) |
| T6 | Columna constante `version_app` | Columna | `nunique() == 1` | Excluir | La procesa sin notar que no varía |
| T7 | Columna irrelevante `tema_interfaz` (tasa de ataque 5.6 % vs 5.4 %) | Columna | Sin relación lógica ni diferencia entre valores | Excluir o demostrar que no aporta | La conserva sin justificación |
| T8 | Categorías inconsistentes: `navegador` (33 variantes → 8 reales) y `pais_geo` (Bolivia, BOLIVIA, BO…) | Columnas | `value_counts()` | Normalizar antes de codificar | Aplica One-Hot directamente |
| T9 | 471 registros sin país: tasa de ataque 14 % frente a 4.3 % con país | `pais_geo` | Tasa de ataque según faltante | Categoría «desconocido». Refutar H4 | Usa `dropna()`: pierde 66 de 219 ataques |
| T10 | Valores imposibles: 18 registros con `intentos = 999` y 9 con `segundos = −1` | Columnas | `describe()` | Tratar como faltantes e imputar con la mediana (o excluir, justificado) | No los detecta; distorsionan el escalado |
| T11 | La hora está contenida en `fecha_hora` | Columna | La hipótesis H1 obliga a revisarla | Crear `hora` o `madrugada` | Descarta la columna o la usa como texto |
| T12 | Desbalance: 5.5 % de ataques | Variable objetivo | `value_counts()` | División estratificada, recall y precisión, `class_weight` | Reporta solo exactitud (el modelo trivial obtiene 0.945) |
| T13 | Escalas muy distintas: desviación de los segundos ≈ 51 000 frente a < 1.5 en las demás | Columnas | `describe()` | Escalar (y opcionalmente logaritmo) para k-NN y regresión logística | Usa k-NN sin escalar |

## 3. Pistas incluidas en el enunciado

| Problema | Texto del enunciado que lo sugiere |
|---|---|
| T1 | «Cuando el servidor de registros se reinicia, reenvía algunos registros que ya había enviado.» |
| T2 | «El equipo de Control de Calidad (QA) ejecuta pruebas automáticas… con las cuentas `qa_bot_01` a `qa_bot_05`… simulan, de forma intencional, numerosos intentos rápidos.» |
| T3 | Diccionario: «Se actualiza al cerrar el ticket, normalmente entre 1 y 3 días después.» Sección 4: «antes de que cualquier persona revise el caso». |
| T4 | Diccionario: «Se registra cuando el usuario cierra la sesión o esta expira.» Sección 4: «antes de que la sesión comience». |
| T5–T7 | Fase 2: «¿Qué columnas aportan información útil, cuáles no aportan…?» |
| T8 | Diccionario: «su formato no es uniforme» / «su formato varía». |
| T9 | «El servicio de geolocalización no siempre logra determinar el país… VPN o red Tor» + H4. |
| T10 | Diccionario: «El contador presentó errores en algunos registros» / «relojes de varios servidores». |
| T11 | H1 («de madrugada»). |
| T12 | Sección 4: preferencia por no permitir ataques; Fase 3: «considerando la proporción de ataques». |
| T13 | Fase 2: «¿Qué transformaciones requieren las variables… (escalado…)?» |

## 4. Solución de referencia

**Tratamiento mínimo esperado:** eliminar duplicados → excluir cuentas QA → normalizar `navegador` y
`pais_geo` → faltantes de país como «desconocido» (variable `origen`) → valores imposibles como faltantes →
crear `madrugada` y `log_segundos` → excluir identificadores, constante, irrelevante y las dos fugas →
pipeline (imputación con mediana, escalado, One-Hot) → división estratificada 75/25.

**Resultados de referencia** (`solucion_P01.ipynb`; prueba = 1 000 registros, 55 ataques):

| Escenario | Exactitud | Precisión | Recall | FP | FN |
|---|---|---|---|---|---|
| Modelo trivial (siempre «normal») | 0.945 | 0.000 | 0.000 | 0 | 55 |
| Regresión logística (balanced) | 0.977 | 0.729 | 0.927 | 19 | 4 |
| k-NN (k = 7) | 0.980 | 0.973 | 0.655 | 1 | 19 |
| Árbol (max_depth = 5) | 0.953 | 0.545 | 0.873 | 40 | 7 |
| Random Forest (umbral 0.5) | 0.987 | 0.889 | 0.873 | 6 | 7 |
| **Random Forest (umbral 0.3) – recomendado** | – | **0.800** | **0.945** | 13 | 3 |
| RF + `bloqueado_por_soporte` (fuga) | 0.997 | 1.000 | 0.945 | 0 | 3 |
| RF + `duracion_sesion_min` (fuga) | 1.000 | 1.000 | 1.000 | 0 | 0 |
| RF entrenado con cuentas QA | 0.985 | 0.900 | 0.818 | 5 | 10 |

Validación cruzada (5 particiones, recall): regresión logística 0.963 ± 0.052; Random Forest 0.858 ± 0.045.

**Criterio de evaluación del modelo elegido:** se aceptan el Random Forest o la regresión logística si la
elección se justifica con la condición del caso (recall alto con precisión ≥ 0.5). Un resultado ≥ 0.99 en todas
las métricas indica casi con certeza una fuga de información.

**Contraste de hipótesis:**

| Hipótesis | Resultado | Evidencia |
|---|---|---|
| H1. La mayoría de los ataques ocurre de madrugada | Se cumple | 55.3 % de los ataques entre 00:00 y 05:59, frente a 5.7 % de los intentos normales |
| H2. Las cuentas docentes son las más atacadas | No se cumple | Tasa de ataque: docente 4.7 %, administrativo 4.7 %, estudiante 5.7 % |
| H3. `bloqueado_por_soporte` dará un detector casi perfecto | No se cumple en la práctica | Coincide 99.4 % con la etiqueta, pero no existe al momento del inicio de sesión |
| H4. Los registros sin país pueden eliminarse | No se cumple | 30.1 % de los ataques no tiene país (66 de 219) |

## 5. Indicadores de trabajo no comprendido

- Métricas ≥ 0.99 presentadas como éxito (casi con certeza conserva T3 o T4).
- No sabe cuántos registros tiene su conjunto final ni por qué.
- Utiliza técnicas no vistas en la asignatura y no puede explicarlas con sus palabras.
- La bitácora es genérica («se limpiaron los datos») y no incluye cantidades ni evidencia.
- El resumen ejecutivo menciona cifras que no aparecen en el notebook.
- No puede realizar en su notebook una tarea sencilla de la Parte B de `defensa_oral.md`.
- Aplica `dropna()` a todo el conjunto sin analizar qué registros se pierden.

## 6. Rúbrica detallada

| Criterio | Excelente (100 %) | Suficiente (60 %) | Insuficiente (20 %) |
|---|---|---|---|
| Comprensión del caso (15 %) | Explica el momento de la predicción y el costo de cada error, y los usa para decidir | Describe el caso, pero no relaciona las restricciones con sus decisiones | Repite el enunciado; no identifica el momento de la predicción |
| Preparación de datos (25 %) | Detecta al menos 9 de los 13 problemas, incluidos T2, T3, T4 y T9, con evidencia en la bitácora | Detecta entre 5 y 8 problemas, incluida al menos una fuga | Tratamiento genérico; conserva alguna fuga |
| Modelado y evaluación (20 %) | Al menos 2 modelos, división estratificada sin fuga, métrica alineada al costo y umbral justificado | Al menos 2 modelos y métrica razonable, sin análisis de umbral | Un solo modelo o solo exactitud |
| Contraste de hipótesis (10 %) | Las 4 hipótesis resueltas con evidencia numérica | 2 o 3 con evidencia | Respuestas sin evidencia |
| Resumen ejecutivo (10 %) | Claro para la DTI, con limitaciones y datos adicionales recomendados | Correcto, con lenguaje técnico | Lista de métricas sin interpretación |
| Defensa oral (20 %) | Responde preguntas de los cuatro bloques y realiza la tarea en vivo explicando el resultado | Responde los bloques 1 a 3; la tarea en vivo queda incompleta | No puede explicar su bitácora ni realizar la tarea |
