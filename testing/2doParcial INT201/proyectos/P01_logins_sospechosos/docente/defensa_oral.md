# Defensa oral – Proyecto P01: Detección de inicios de sesión sospechosos

> **Documento reservado para el docente.** Pauta para conducir la defensa (10 minutos) y verificar que el
> estudiante comprende su propio trabajo. Los valores de referencia provienen de `solucion_P01.ipynb`
> (sección 9, «Anexo: tareas de la defensa oral»).

## Procedimiento

1. **Presentación (3 min).** El estudiante expone la solución dirigida a la DTI.
2. **Preguntas (4 min).** Seleccionar 3 o 4 preguntas de la Parte A, de bloques distintos.
3. **Tarea en vivo (3 min).** Seleccionar 1 tarea de la Parte B. El estudiante la realiza en su notebook y
   explica el resultado.

Las respuestas esperadas son una referencia. Se valora que el estudiante razone con sus propias palabras y con
los números de **su** notebook, que pueden diferir ligeramente de los de referencia según sus decisiones.

---

## Parte A. Preguntas con respuesta esperada

### Bloque 1. Comprensión del caso

| N.º | Pregunta | Respuesta esperada |
|---|---|---|
| A1 | ¿En qué momento se utiliza el modelo y qué información **no** existe todavía en ese momento? | Cuando el usuario presiona «Ingresar», antes de que la sesión comience. No existen la duración de la sesión (`duracion_sesion_min`) ni la decisión de la Mesa de Ayuda (`bloqueado_por_soporte`), que se registran después. |
| A2 | ¿Qué consecuencia tiene para la universidad un falso negativo? ¿Y un falso positivo? | Falso negativo: un ataque ingresa sin control y puede modificar datos o calificaciones (costo alto). Falso positivo: un usuario legítimo debe escribir un código 2FA (≈ 30 s, costo bajo). Por eso se prioriza el recall. |
| A3 | ¿Qué son las cuentas `qa_bot_*` y por qué afectan al modelo? | Son pruebas automáticas del equipo de QA. Se comportan como ataques (muchos intentos rápidos de madrugada) pero están etiquetadas como normales. Si se conservan, el modelo aprende que ese patrón puede ser normal y pierde recall (0.873 → 0.818 en la referencia). |
| A4 | ¿Por qué la DTI no acepta un modelo que detecte todos los ataques marcando como sospechoso a todo el mundo? | Porque la condición del caso limita las falsas alarmas: si más de la mitad de las alertas son falsas (precisión < 0.5), los usuarios rechazan el mecanismo. |

### Bloque 2. Justificación de decisiones

| N.º | Pregunta | Respuesta esperada |
|---|---|---|
| A5 | ¿Con cuántos registros empezó y con cuántos terminó? Explique cada diferencia. | 4 270 → 4 150 al eliminar 120 duplicados (reenvío de registros) → 4 000 al excluir 150 registros de cuentas QA. |
| A6 | ¿Por qué eliminó `duracion_sesion_min` si no es la variable objetivo? | Porque solo se conoce cuando la sesión termina, después de la predicción. Usarla es fuga de información: en la evaluación da métricas ≈ 1.0, pero en producción el valor no existe. |
| A7 | ¿Por qué no eliminó los registros sin país? | Porque el faltante es informativo: la tasa de ataque sin país es 14 % frente a 4.3 % con país. Eliminarlos quitaría 66 de 219 ataques (≈ 30 %). Se reemplazó por la categoría «desconocido». |
| A8 | ¿Qué hizo con valores como «CHROME» y « Chrome»? ¿Qué habría ocurrido sin ese tratamiento? | Se normalizaron (quitar espacios y unificar minúsculas). Sin ello, One-Hot crea varias columnas para el mismo navegador, dividiendo la información entre ellas. |
| A9 | ¿Por qué excluyó `usuario`, `ip_origen` y `evento_id`? | Son identificadores con casi un valor distinto por registro: no se repiten en usuarios nuevos y solo permiten memorizar. La información útil (tipo de cuenta, país) ya está en `rol` y `pais_geo`. |
| A10 | ¿Qué hizo con los valores 999 y −1, y por qué usó esa estrategia? | Son imposibles (error del contador y de los relojes). Se convirtieron en faltantes y se imputaron con la mediana dentro del pipeline, porque las variables tienen valores extremos y la mediana no se ve afectada por ellos. |

### Bloque 3. Interpretación de resultados

| N.º | Pregunta | Respuesta esperada |
|---|---|---|
| A11 | Su recall es 0.945. Expréselo en palabras. | De cada 100 ataques reales, el modelo detecta aproximadamente 94 y deja pasar 6. |
| A12 | ¿Por qué la exactitud no es su métrica principal? ¿Qué exactitud tiene un modelo que siempre responde «normal»? | Por el desbalance: solo ≈ 5.5 % son ataques. Ese modelo tiene ≈ 0.945 de exactitud y detecta 0 ataques. |
| A13 | Señale en su matriz de confusión cuántos usuarios legítimos recibirían 2FA. | La celda de falsos positivos (real normal, predicho ataque): 13 de 945 intentos legítimos en prueba con umbral 0.3 (≈ 1.4 %). |
| A14 | ¿Cuál es la variable más importante del modelo? ¿Tiene sentido desde la seguridad? | Segundos desde el intento anterior (o intentos fallidos). Sí: los ataques automatizados prueban contraseñas en pocos segundos y acumulan intentos fallidos; un usuario normal no. |
| A15 | ¿Por qué eligió ese modelo y no la regresión logística, que tiene mayor recall? | Respuesta aceptable si se justifica con la condición del caso. Referencia: el Random Forest con umbral 0.3 alcanza recall 0.945 con precisión 0.80; la regresión logística con umbral 0.5 tiene recall 0.927 y precisión 0.73. También es válido elegir la regresión logística por su interpretabilidad (coeficientes). |

### Bloque 4. Escenarios alternativos

| N.º | Pregunta | Respuesta esperada |
|---|---|---|
| A16 | Si QA cambia sus cuentas a `test_01…` y nadie avisa, ¿cómo lo notaría? | El filtro por `qa_` dejaría de funcionar. Se notaría por registros etiquetados como normales con patrón de ataque desde la IP interna 10.0.99.x; conviene filtrar también por IP o pedir a QA que marque sus pruebas. |
| A17 | Si el SOC solo puede revisar 10 alertas por día, ¿qué cambiaría? | Subir el umbral para generar menos alertas y priorizar precisión; o mantener 2FA automático para todos los sospechosos y enviar al SOC solo los de probabilidad más alta. |
| A18 | Un atacante con contraseña robada ingresa de día, desde Bolivia, con Chrome y un dispositivo conocido. ¿Lo detectaría el modelo? | No: ese intento no tiene ninguna de las señales aprendidas (probabilidad ≈ 0 en la referencia). Es una limitación; se necesitarían otros datos (ubicación habitual del usuario, cambios recientes de correo de recuperación). |
| A19 | Si se usara k-NN sin escalar con los segundos originales, ¿qué variable dominaría la distancia? | `segundos_desde_intento_anterior`, cuya desviación estándar (≈ 51 000) es miles de veces mayor que la de las variables 0/1. |
| A20 | Si la DTI entrega `bloqueado_por_soporte` de los próximos meses, ¿sirve para algo? | Sí, como **etiqueta** para reentrenar o validar el modelo con datos nuevos; no como variable de entrada. |

---

## Parte B. Tareas en vivo sobre el notebook

### B1. Cambiar el umbral de decisión

- **Instrucción al estudiante:** «Clasifique el conjunto de prueba con un umbral de 0.3 en lugar de 0.5 y
  reporte recall, precisión, cantidad de alertas y ataques no detectados en ambos casos.»
- **Código de referencia:**

```python
prob = modelo.predict_proba(X_test)[:, 1]
for u in (0.5, 0.3):
    p = (prob >= u).astype(int)
    print(u, recall_score(y_test, p), precision_score(y_test, p), p.sum(), ((p == 0) & (y_test == 1)).sum())
```

- **Resultado esperado (RF):** umbral 0.5 → recall 0.873, precisión 0.889, 54 alertas, 7 FN. Umbral 0.3 →
  recall 0.945, precisión 0.800, 65 alertas, 3 FN.
- **Explicación esperada:** al bajar el umbral, el modelo marca más intentos como sospechosos: detecta 4
  ataques más a cambio de 11 alertas adicionales. Es aceptable porque el costo de un 2FA es bajo y la precisión
  sigue sobre 0.5.
- **Aspectos a observar:** usar `predict` en lugar de `predict_proba`; tomar la columna 0 (probabilidad de
  normal) en lugar de la 1.

### B2. Efecto de eliminar los registros sin país

- **Instrucción al estudiante:** «Calcule cuántos ataques se perderían si se eliminaran los registros sin país.»
- **Código de referencia:**

```python
print(df["es_ataque"].sum(), df.loc[df["pais_geo"].isna(), "es_ataque"].sum())
# (si ya imputó: df.loc[df["origen"] == "desconocido", "es_ataque"].sum())
```

- **Resultado esperado:** 66 de 219 ataques (≈ 30 %).
- **Explicación esperada:** el faltante no es un error aleatorio; ocurre con más frecuencia en ataques (VPN,
  Tor). Por eso se conserva como categoría.
- **Aspectos a observar:** si el estudiante ya reemplazó los faltantes, debe saber dónde quedaron.

### B3. Clasificar un intento escrito a mano

- **Instrucción al estudiante:** «Construya un registro nuevo: 0 intentos fallidos, un día desde el intento
  anterior, dispositivo conocido, sin VPN, de día, Chrome en Windows, desde Bolivia. Obtenga la probabilidad de
  ataque. Luego cambie a 8 intentos, 2 segundos, dispositivo nuevo, madrugada, python-requests en Linux, país
  desconocido.»
- **Código de referencia:**

```python
nuevo = pd.DataFrame([{"intentos_fallidos_previos_1h": 0, "log_segundos": np.log10(86400 + 1),
                       "dispositivo_nuevo": 0, "usa_vpn": 0, "madrugada": 0, "navegador": "chrome",
                       "sistema_operativo": "Windows", "origen": "bolivia"}])
modelo.predict_proba(nuevo)[0, 1]
```

- **Resultado esperado:** primer caso ≈ 0.0; segundo caso ≈ 1.0.
- **Explicación esperada:** el modelo reconoce los ataques automatizados, pero no un acceso con contraseña
  robada que imita el comportamiento normal. Es una limitación que debe comunicarse a la DTI.
- **Aspectos a observar:** el registro debe tener **las mismas columnas y transformaciones** que el
  entrenamiento (por ejemplo, logaritmo de los segundos, categorías en minúsculas).

### B4. k-NN sin escalar frente a k-NN escalado

- **Instrucción al estudiante:** «Entrene k-NN (k = 7) con los segundos originales, una vez sin escalar y otra
  con StandardScaler. Compare el recall y explique la diferencia.»
- **Código de referencia:**

```python
for escalar in (False, True):
    pasos = [SimpleImputer(strategy="median")] + ([StandardScaler()] if escalar else [])
    ...  # mismo preprocesamiento, cambiando solo el escalado
print(X_train[columnas_numericas].std())
```

- **Resultado esperado:** sin escalar → recall 0.455; escalado → recall 0.509. Desviación estándar de los
  segundos ≈ 51 000 frente a < 1.5 en las demás.
- **Explicación esperada:** k-NN calcula distancias; sin escalar, los segundos dominan la distancia y las
  demás variables casi no influyen. (La mejora es mayor si además se aplica logaritmo, como en la solución.)
- **Aspectos a observar:** que el escalado se aplique dentro del pipeline (solo con datos de entrenamiento).

### B5. Validación cruzada

- **Instrucción al estudiante:** «Evalúe su modelo con validación cruzada estratificada de 5 particiones,
  usando recall. Reporte la media y la desviación.»
- **Código de referencia:**

```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
s = cross_val_score(pipeline, X, y, cv=cv, scoring="recall")
print(s, s.mean(), s.std())
```

- **Resultado esperado (RF, umbral 0.5):** recall por partición 0.79–0.93; media 0.858; desviación 0.045.
- **Explicación esperada:** el desempeño es estable entre particiones (desviación baja); la media es una
  estimación más confiable que una sola división. La validación cruzada usa el umbral 0.5, por eso es menor que
  el recall con umbral 0.3.
- **Aspectos a observar:** aplicar validación cruzada al pipeline completo (no a datos ya escalados).

### B6. Tasa de ataque por rol (hipótesis H2)

- **Instrucción al estudiante:** «Muestre, para cada rol, la cantidad de registros, de ataques y la tasa de
  ataque.»
- **Código de referencia:**

```python
df.groupby("rol")["es_ataque"].agg(registros="size", ataques="sum", tasa="mean")
```

- **Resultado esperado:** administrativo 402 / 19 / 0.047; docente 596 / 28 / 0.047; estudiante 3 002 / 172 /
  0.057.
- **Explicación esperada:** H2 no se cumple: la tasa es similar en los tres roles. Hay más ataques a
  estudiantes en número absoluto solo porque hay más cuentas de estudiantes.
- **Aspectos a observar:** confundir cantidad con proporción.

### B7. Árbol de profundidad 3 e interpretación

- **Instrucción al estudiante:** «Entrene un árbol de decisión con `max_depth=3`, muestre sus reglas con
  `export_text` e interprete la primera división.»
- **Código de referencia:**

```python
from sklearn.tree import export_text
arbol = Pipeline([("prep", preprocesador_sin_escalar),
                  ("modelo", DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=42))])
arbol.fit(X_train, y_train)
print(export_text(arbol.named_steps["modelo"],
                  feature_names=list(arbol.named_steps["prep"].get_feature_names_out())))
```

- **Resultado esperado:** primera división `log_segundos <= 3.48` (≈ 3 000 segundos, unos 50 minutos);
  recall 0.909, precisión 0.32.
- **Explicación esperada:** la primera pregunta del árbol separa los intentos muy seguidos (posible ataque
  automatizado) de los espaciados. El árbol es fácil de explicar a los analistas, pero con poca profundidad
  genera muchas falsas alarmas (precisión 0.32 < 0.5), por lo que no cumple la condición de la DTI.
- **Aspectos a observar:** si el estudiante escaló los datos, los umbrales aparecen en unidades estandarizadas;
  debe saber explicarlo.

### B8. Usuarios legítimos que recibirían 2FA

- **Instrucción al estudiante:** «Con su umbral elegido, indique qué porcentaje de los intentos legítimos de
  prueba recibiría una solicitud de 2FA.»
- **Código de referencia:**

```python
tn, fp, fn, tp = confusion_matrix(y_test, (prob >= 0.3).astype(int)).ravel()
print(fp / (fp + tn))
```

- **Resultado esperado:** umbral 0.3 → TN 932, FP 13, FN 3, TP 52; ≈ 1.4 % de los intentos legítimos.
- **Explicación esperada:** el impacto en los usuarios es bajo: aproximadamente 1 de cada 70 inicios de sesión
  legítimos pediría un código.
- **Aspectos a observar:** calcular sobre todos los registros (no solo sobre los legítimos) o confundir FP con FN.

---

## Hoja de registro

| Estudiante | Presentación (0–3) | Preguntas (0–4) | Tarea en vivo (0–3) | Total (0–10) | Observaciones |
|---|---|---|---|---|---|
| | | | | | |
