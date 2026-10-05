# Plan de Construcción — Parte 3
## Regresión Lineal: Predicción de Horas de Producción
### Serie: Machine Learning from Scratch | Laboratorio *Neon Skies* | INT210

---

## Visión General

**Entrada:** `characters_features.csv` generado en la Parte 2  
**Salida:** Modelo entrenado, predicciones, visualizaciones, métricas de evaluación  
**Variable Objetivo (Target):** `production_hours`  
**Librerías requeridas:** `pandas`, `numpy`, `matplotlib`, `sklearn`

**Filosofía del notebook:**  
Esta parte sigue el espíritu de "Machine Learning *from scratch*": primero se implementa la regresión lineal *manualmente* con NumPy para comprender la matemática, luego se valida con `scikit-learn`. El estudiante ve que ambos enfoques producen los mismos coeficientes, consolidando la comprensión.

**Métricas a calcular:**
- R² (coeficiente de determinación)
- MAE (Error Absoluto Medio)
- RMSE (Raíz del Error Cuadrático Medio)

**Resultado esperado del modelo final (regresión múltiple):**  
Con features `num_frames_total`, `screen_time_ratio`, `num_states`, `fps`, `has_special_fx`:
- R² ≈ 0.98 (con datos de entrenamiento, 20 muestras pequeño)
- RMSE ≈ 5–8 horas

---

## Estructura del Notebook

### Sección de Título

**Título:** `Regresión Lineal desde Cero: Predicción de Horas de Producción de Personajes 2D`  
**Subtítulo/Serie:** Machine Learning from Scratch | Parte 3 de 3 — Regresión Lineal, Evaluación y Visualización

**Contexto:**  
En las partes anteriores limpiamos el dataset (Parte 1) y seleccionamos las características más relevantes mediante análisis de correlación (Parte 2). Ahora aplicamos regresión lineal para predecir cuántas horas tomará producir un personaje basándonos en sus características. Primero implementamos la solución manualmente usando álgebra matricial (ecuación normal), y luego validamos con `scikit-learn`.

**Objetivos de Aprendizaje:**
- Comprender la intuición geométrica de la regresión lineal (minimizar distancias al hiperplano)
- Implementar la Ecuación Normal `β = (XᵀX)⁻¹ Xᵀy` con NumPy
- Dividir datos en conjuntos de entrenamiento y prueba (`train_test_split`)
- Entrenar y evaluar un modelo con `sklearn.linear_model.LinearRegression`
- Calcular e interpretar métricas: R², MAE, RMSE
- Visualizar predicciones vs. valores reales y analizar residuos
- Identificar cuáles características tienen mayor peso en el modelo (coeficientes)

---

## Ejercicio 3.0 — Repaso de Conceptos Matemáticos (Celda Teórica)

**Tipo de celda:** Solo Markdown (celda de lectura, sin código que completar)

**Contenido a incluir:**

**¿Qué es la Regresión Lineal?**
El modelo supone que existe una relación lineal entre las características X y la variable objetivo y:

```
ŷ = β₀ + β₁·x₁ + β₂·x₂ + ... + βₙ·xₙ
```

El objetivo es encontrar los coeficientes β que minimicen el **Error Cuadrático Medio (MSE)**:

```
MSE = (1/n) Σ (yᵢ - ŷᵢ)²
```

**Ecuación Normal (solución algebraica exacta):**
```
β = (XᵀX)⁻¹ Xᵀy
```

Donde:
- `X` = matriz de características con columna de unos para el intercepto (bias)
- `y` = vector de valores reales de `production_hours`
- `β` = vector de coeficientes + intercepto

**¿Por qué NumPy antes que sklearn?**  
Saber que `sklearn` resuelve exactamente esta ecuación internamente permite al estudiante confiar en la herramienta y entender sus parámetros, en lugar de usarla como caja negra.

---

## Ejercicio 3.1 — Carga de Datos y Preparación de Matrices

**Concepto a demostrar:** `pd.read_csv`, `df.values`, separar X e y, `numpy.column_stack`, columna de bias

**Ejemplo funcional (no modificar):**
```python
import numpy as np
import pandas as pd
data = pd.DataFrame({"x1": [1,2,3], "x2": [4,5,6], "y": [7,9,11]})
X = data[["x1","x2"]].values
y = data["y"].values
ones = np.ones((len(y), 1))
X_b = np.hstack([ones, X])
print("Matriz X_b con bias:\n", X_b)
```

**Tarea del estudiante:**
1. Cargar `characters_features.csv` en `df`
2. Definir las columnas de características en `feature_cols` y el target `target_col`
3. Extraer la matriz `X` y el vector `y` como arrays NumPy
4. Agregar la columna de unos (bias) para obtener `X_b`
5. Imprimir las formas de `X_b` e `y`

**Placeholders a completar:**
```python
df = pd.read_csv(???)
feature_cols = [???, ???, ???, ???, ???]
target_col = ???

X = df[feature_cols].???
y = df[target_col].???
ones = np.ones((len(y), ???))
X_b = np.hstack([???, X])
print("Forma de X_b:", X_b.???)
print("Forma de y:", y.???)
```

**Salida esperada:**
- `X_b.shape`: `(20, 6)` — 20 muestras, 5 features + 1 columna bias
- `y.shape`: `(20,)`

**Pregunta Lógica 3.1:**
- a) ¿Cuántas columnas tiene la matriz `X_b`? ¿Por qué difiere de la cantidad de features seleccionadas?
- b) ¿Por qué es necesario agregar una columna de unos a la matriz de características?

---

## Ejercicio 3.2 — Regresión Lineal Simple (From Scratch)

**Concepto a demostrar:** Ecuación Normal con el mejor predictor individual (`num_frames_total`)

**Ejemplo funcional (no modificar):**
```python
# Regresión lineal simple: y = β₀ + β₁·x
x = np.array([10, 20, 30, 40])
y_ex = np.array([25, 45, 65, 85])
X_ex = np.column_stack([np.ones(len(x)), x])
beta = np.linalg.inv(X_ex.T @ X_ex) @ X_ex.T @ y_ex
print(f"β₀ (intercepto): {beta[0]:.2f}")
print(f"β₁ (pendiente) : {beta[1]:.2f}")
```

**Tarea del estudiante:**
1. Usar solo `num_frames_total` como única característica
2. Construir `X_simple` con columna de bias y la columna de frames
3. Aplicar la Ecuación Normal: `beta = np.linalg.inv(X.T @ X) @ X.T @ y`
4. Imprimir los coeficientes e interpretarlos
5. Calcular las predicciones: `y_pred = X_simple @ beta`
6. Graficar los valores reales vs. línea de regresión

**Placeholders a completar:**
```python
x_simple = df["num_frames_total"].???
X_simple = np.column_stack([np.ones(???), x_simple])

beta_simple = np.linalg.???(X_simple.T @ X_simple) @ X_simple.T @ y

print(f"Intercepto (β₀): {beta_simple[???]:.4f}")
print(f"Pendiente  (β₁): {beta_simple[???]:.4f}")
print(f"Interpretación: por cada fotograma adicional, se estiman {beta_simple[1]:.2f} horas más de producción")

y_pred_simple = ??? @ beta_simple
```

**Salida esperada:**
```
Intercepto (β₀):  9.3917
Pendiente  (β₁):  1.0413
Interpretación: por cada fotograma adicional, se estiman 1.04 horas más de producción
```

**Gráfico:** Scatter de `num_frames_total` vs `production_hours` con la recta de regresión superpuesta  
Puntos reales: azul. Línea de regresión: roja. Eje X: "Total de Fotogramas", Eje Y: "Horas de Producción"

**Pregunta Lógica 3.2:**
- a) Según el modelo simple, ¿cuántas horas se predicen para un personaje con 120 fotogramas?
- b) ¿Qué representa el intercepto β₀ en el contexto de este problema?
- c) ¿Un personaje con 0 fotogramas tendría ≈9.39 horas de producción en el modelo? ¿Tiene sentido?

---

## Ejercicio 3.3 — Evaluación del Modelo Simple (Métricas)

**Concepto a demostrar:** R², MAE, RMSE implementados desde cero con NumPy

**Ejemplo funcional (no modificar):**
```python
y_real = np.array([100, 50, 80])
y_pred = np.array([95, 55, 75])
residuos = y_real - y_pred
mse = np.mean(residuos**2)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse:.2f}")
```

**Tarea del estudiante:**
1. Calcular los residuos: `residuos = y - y_pred_simple`
2. Calcular MAE: media del valor absoluto de los residuos
3. Calcular RMSE: raíz de la media de los cuadrados de los residuos
4. Calcular R²: `1 - SS_res / SS_tot` donde `SS_tot = sum((y - mean(y))²)`
5. Interpretar los resultados

**Fórmulas que se proveen en celda Markdown (no calcular, solo referencia):**
```
MAE  = (1/n) Σ |yᵢ - ŷᵢ|
RMSE = √[(1/n) Σ (yᵢ - ŷᵢ)²]
R²   = 1 - [Σ(yᵢ - ŷᵢ)²] / [Σ(yᵢ - ȳ)²]
```

**Placeholders a completar:**
```python
residuos = y - y_pred_simple
mae  = np.mean(np.???(residuos))
rmse = np.???(np.mean(residuos???))
ss_res = np.sum(residuos???)
ss_tot = np.sum((y - np.mean(y))???)
r2 = 1 - (??? / ???)

print(f"MAE  (Error Absoluto Medio) : {mae:.2f} horas")
print(f"RMSE (Error Cuadrático Med.): {rmse:.2f} horas")
print(f"R²   (Coef. Determinación)  : {r2:.4f}")
```

**Salida esperada:**
```
MAE  (Error Absoluto Medio) :  6.85 horas
RMSE (Error Cuadrático Med.):  9.12 horas
R²   (Coef. Determinación)  :  0.9567
```

**Pregunta Lógica 3.3:**
- a) ¿Qué significa un R² de 0.957 para este modelo?
- b) ¿El MAE indica que el modelo está prediciendo con un error de ±6.85 horas en promedio?
- c) ¿Cuál de las dos métricas (MAE vs RMSE) penaliza más los errores grandes y por qué?

---

## Ejercicio 3.4 — Regresión Múltiple con scikit-learn

**Concepto a demostrar:** `train_test_split`, `LinearRegression`, `.fit()`, `.predict()`, `.coef_`, `.intercept_`

**Ejemplo funcional (no modificar):**
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_ex = np.array([[1,2],[3,4],[5,6],[7,8]])
y_ex = np.array([5, 11, 17, 23])
X_train, X_test, y_train, y_test = train_test_split(X_ex, y_ex, test_size=0.25, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
print("Coeficientes:", model.coef_)
print("Intercepto:", model.intercept_)
```

**Tarea del estudiante:**
1. Dividir `X` (con todas las features seleccionadas) e `y` en 80% train / 20% test con `random_state=42`
2. Crear un modelo `LinearRegression()` y entrenarlo con `fit(X_train, y_train)`
3. Generar predicciones sobre `X_test` con `predict`
4. Imprimir los coeficientes e intercepto del modelo
5. Comparar coeficientes con los del ejercicio 3.2 para `num_frames_total`

**Placeholders a completar:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_multi = df[feature_cols].???
y_multi = df[target_col].???

X_train, X_test, y_train, y_test = train_test_split(
    X_multi, y_multi, test_size=???, random_state=???
)
print(f"Entrenamiento: {X_train.???[0]} muestras | Prueba: {X_test.???[0]} muestras")

model = LinearRegression()
model.???(X_train, y_train)

y_pred_multi = model.???(X_test)
print("\nCoeficientes:")
for feature, coef in zip(feature_cols, model.???):
    print(f"  {feature:20s}: {coef:.4f}")
print(f"\nIntercepto: {model.???:.4f}")
```

**Salida esperada (aproximada — depende de random_state):**
```
Entrenamiento: 16 muestras | Prueba: 4 muestras
Coeficientes:
  num_frames_total    :  0.9823
  screen_time_ratio   : 58.4210
  num_states          :  3.1500
  fps                 :  0.8742
  has_special_fx      :  8.9300
Intercepto: -12.4100
```

**Pregunta Lógica 3.4:**
- a) ¿Cuántas muestras hay en el conjunto de prueba? ¿Por qué tan pocas?
- b) ¿Qué representa el coeficiente de `has_special_fx` en el modelo?
- c) ¿Qué ventaja tiene usar `random_state=42` al dividir los datos?

---

## Ejercicio 3.5 — Evaluación del Modelo Múltiple

**Concepto a demostrar:** `sklearn.metrics` (R², MAE, RMSE), comparar modelo simple vs. múltiple

**Ejemplo funcional (no modificar):**
```python
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
y_true = np.array([100, 50, 80, 130])
y_pred = np.array([95,  52, 78, 135])
print(f"R²  : {r2_score(y_true, y_pred):.4f}")
print(f"MAE : {mean_absolute_error(y_true, y_pred):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_true, y_pred)):.2f}")
```

**Tarea del estudiante:**
1. Calcular las 3 métricas para el conjunto de **prueba** del modelo múltiple
2. Crear una tabla comparativa entre el modelo simple (Ejercicio 3.3) y el modelo múltiple
3. Interpretar cuál modelo es mejor y por qué

**Placeholders a completar:**
```python
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

r2_multi  = r2_score(???, ???)
mae_multi = mean_absolute_error(???, ???)
rmse_multi = np.sqrt(mean_squared_error(???, ???))

print("="*45)
print(f"{'Métrica':<20} {'Simple':>10} {'Múltiple':>10}")
print("="*45)
print(f"{'R²':<20} {r2_simple:>10.4f} {???:>10.4f}")
print(f"{'MAE (horas)':<20} {mae_simple:>10.2f} {???:>10.2f}")
print(f"{'RMSE (horas)':<20} {rmse_simple:>10.2f} {???:>10.2f}")
print("="*45)
```

**Pregunta Lógica 3.5:**
- a) ¿El modelo múltiple mejora el R² respecto al simple?
- b) Si el RMSE del modelo múltiple es menor que el del simple, ¿qué indica?
- c) Con solo 4 datos de prueba, ¿confiarías completamente en el R² del conjunto de prueba?

---

## Ejercicio 3.6 — Visualización: Predicciones vs. Valores Reales

**Concepto a demostrar:** Gráfico de dispersión `y_real vs. y_pred`, línea de referencia perfecta

**Ejemplo funcional (no modificar):**
```python
y_real_ex = [100, 50, 80, 130]
y_pred_ex  = [95,  52, 78, 135]
plt.scatter(y_real_ex, y_pred_ex, color="steelblue", label="Predicciones")
plt.plot([50,130],[50,130], "r--", label="Predicción perfecta")
plt.xlabel("Valor Real"); plt.ylabel("Valor Predicho"); plt.legend(); plt.show()
```

**Tarea del estudiante:**
1. Crear el gráfico de dispersión `y_test` (eje X) vs `y_pred_multi` (eje Y)
2. Trazar la línea diagonal de referencia perfecta `y = x`
3. Anotar cada punto con el nombre del personaje correspondiente
4. Agregar título, etiquetas y leyenda

**Placeholders a completar:**
```python
nombres_test = df.iloc[y_test.???]["name"].values

plt.figure(figsize=(8, 6))
plt.scatter(???, y_pred_multi, color="steelblue", s=80, label="Personajes (prueba)")
for i, nombre in enumerate(nombres_test):
    plt.annotate(nombre, (y_test.values[i], y_pred_multi[i]), textcoords="offset points", xytext=(5,5))

min_val = min(y_test.min(), y_pred_multi.???)
max_val = max(y_test.max(), y_pred_multi.???)
plt.plot([min_val, max_val], [min_val, max_val], "r--", label="Predicción perfecta (y=x)")

plt.xlabel(???)
plt.ylabel(???)
plt.title("Predicciones vs. Valores Reales — Regresión Múltiple")
plt.legend()
plt.tight_layout()
plt.show()
```

**Pregunta Lógica 3.6:**
- a) ¿Qué significa que un punto esté por encima de la línea `y=x`?
- b) ¿Qué significa que un punto esté exactamente sobre la línea `y=x`?
- c) Si Blaze estuviera en el conjunto de prueba, ¿esperarías que estuviera cerca de la línea perfecta dado su R² alto?

---

## Ejercicio 3.7 — Análisis de Residuos

**Concepto a demostrar:** Gráfico de residuos, detección de patrones sistemáticos, supuesto de homocedasticidad

**Ejemplo funcional (no modificar):**
```python
residuos_ex = np.array([2, -3, 1, 4, -2])
predichos_ex = np.array([95, 55, 78, 130, 75])
plt.scatter(predichos_ex, residuos_ex, color="coral")
plt.axhline(y=0, color="black", linestyle="--")
plt.xlabel("Predicción"); plt.ylabel("Residuo"); plt.show()
```

**Tarea del estudiante:**
1. Calcular los residuos del conjunto de prueba: `residuos_test = y_test - y_pred_multi`
2. Generar el gráfico de residuos: eje X = predicciones, eje Y = residuos
3. Trazar la línea horizontal en y=0
4. Identificar si hay algún patrón sistemático

**Nota Pedagógica:** Dado el tamaño pequeño del dataset (4 puntos en test), el análisis de residuos es ilustrativo. Se debe explicar que con datasets reales de cientos de registros este análisis es esencial.

**Placeholders a completar:**
```python
residuos_test = ??? - ???
plt.figure(figsize=(7, 4))
plt.scatter(y_pred_multi, ???, color="coral", s=80, edgecolors="black")
plt.axhline(y=???, color="black", linestyle="--", label="Residuo = 0")
plt.xlabel("Valores Predichos (ŷ)")
plt.ylabel(???)
plt.title("Análisis de Residuos — Conjunto de Prueba")
plt.legend()
plt.tight_layout()
plt.show()
```

**Pregunta Lógica 3.7:**
- a) Si todos los residuos son positivos (por encima de la línea `y=0`), ¿qué indica?
- b) ¿Qué se llama "heterocedasticidad" y cómo se detecta en el gráfico de residuos?
- c) ¿Por qué es problemático si los residuos siguen un patrón sistemático (p.ej., curva en forma de U)?

---

## Ejercicio 3.8 — Predicción para un Nuevo Personaje

**Concepto a demostrar:** Uso del modelo entrenado para inferencia sobre datos nuevos, `model.predict([[...]])`

**Ejemplo funcional (no modificar):**
```python
nuevo = np.array([[120, 0.25, 5, 24, 1]])   # [num_frames, screen_time, states, fps, fx]
prediccion = model.predict(nuevo)
print(f"Predicción: {prediccion[0]:.1f} horas")
```

**Tarea del estudiante:**  
Crear el personaje nuevo `Nova` con las siguientes características y predecir sus horas de producción:
- `num_frames_total`: 96  
- `screen_time_ratio`: 0.20  
- `num_states`: 4  
- `fps`: 24  
- `has_special_fx`: 1

**Placeholders a completar:**
```python
nova = {
    "num_frames_total" : ???,
    "screen_time_ratio": ???,
    "num_states"       : ???,
    "fps"              : ???,
    "has_special_fx"   : ???,
}
X_nova = np.array([[nova[col] for col in ???]])
pred_nova = model.???(X_nova)
print(f"Horas de producción estimadas para Nova: {pred_nova[???]:.1f} horas")
print(f"(Para comparación, el promedio del dataset es {df['production_hours'].mean():.1f} horas)")
```

**Salida esperada:**
```
Horas de producción estimadas para Nova: 118.3 horas
(Para comparación, el promedio del dataset es 96.3 horas)
```

**Pregunta Lógica 3.8:**
- a) Si `has_special_fx` de Nova cambia de 1 a 0, ¿en cuántas horas aproximadamente cambia la predicción?
- b) ¿Por qué la predicción para Nova es mayor al promedio del dataset?
- c) ¿Qué supuesto importante de la regresión lineal se viola si los residuos no son independientes entre sí?

---

## Ejercicio 3.9 — Resumen y Conclusiones

**Tipo de celda:** Markdown + código de resumen final

**Tarea del estudiante:**
1. Completar una tabla resumen en Markdown con los hallazgos del notebook
2. Responder en celda Markdown: ¿qué característica fue la más influyente y por qué?
3. Ejecutar una celda de código final que imprima el "reporte del estudio"

**Celda de resumen (código):**
```python
print("=" * 55)
print("  REPORTE FINAL — LAB NEON SKIES: Regresión Lineal")
print("=" * 55)
print(f"  Dataset: {len(df)} personajes | {len(feature_cols)} features")
print(f"  Feature más correlacionada : num_frames_total (r={???:.3f})")
print(f"  Modelo simple  → R²={r2_simple:.3f}, RMSE={rmse_simple:.1f} h")
print(f"  Modelo múltiple→ R²={r2_multi:.3f}, RMSE={rmse_multi:.1f} h")
print(f"  Nova estimado  : {pred_nova[0]:.1f} horas de producción")
print("=" * 55)
```

---

## Notas Pedagógicas del Notebook

### Estructura de celdas por ejercicio
Mismo patrón que Partes 1 y 2:
1. **Celda Markdown:** Concepto matemático + propósito del ejercicio
2. **Celda Código (ejemplo):** Resuelto, no modificable
3. **Celda Markdown:** Enunciado de la tarea
4. **Celda Código (estudiante):** Con placeholders `???`
5. **Celda Markdown:** Pregunta Lógica

### Preguntas Lógicas clave para Moodle
- PL 3.1: forma de `X_b`, propósito de la columna de unos
- PL 3.2: predicción del modelo para 120 fotogramas, interpretación del intercepto
- PL 3.3: significado de R², diferencia MAE vs RMSE
- PL 3.4: cantidad de datos de prueba, interpretación de coeficientes
- PL 3.5: comparación simple vs múltiple con tabla de métricas
- PL 3.6: interpretación de puntos sobre/debajo/sobre la línea perfecta
- PL 3.7: heterocedasticidad, patrones en residuos
- PL 3.8: sensibilidad del modelo a `has_special_fx`

### Conceptos clave para preguntas de código (drag-and-drop Moodle)
- `np.ones((n, 1))` — columna de bias
- `np.hstack([ones, X])` — agregar columna a la izquierda
- `np.linalg.inv(A)` — inversa de una matriz
- `A.T` o `A.T @ B` — transpuesta y multiplicación matricial
- `train_test_split(X, y, test_size=0.2, random_state=42)` — división de datos
- `LinearRegression()` — instanciar el modelo
- `model.fit(X_train, y_train)` — entrenar
- `model.predict(X_test)` — predecir
- `model.coef_` — coeficientes de las características
- `model.intercept_` — intercepto β₀
- `r2_score(y_real, y_pred)` — coeficiente de determinación
- `mean_absolute_error(y_real, y_pred)` — error absoluto medio
- `np.sqrt(mean_squared_error(y_real, y_pred))` — RMSE

---

## Archivos de Salida de la Parte 3

| Archivo | Descripción |
|---|---|
| `Practica_01_Parte3_Regresion_Lineal.ipynb` | Notebook del estudiante (con `???`) |
| `Practica_01_Parte3_Regresion_Lineal_SOLUCIONES.ipynb` | Solucionario con celdas ejecutadas |
| `Practica_01_Parte3_Regresion_Lineal_ES.ipynb` | Versión en español del notebook estudiante |
| `Practica_01_Parte3_Regresion_Lineal_SOLUCIONES_ES.ipynb` | Solucionario en español |
| `Moodle/BancoPreguntas_Parte3_RegresionLineal.md` | Banco de preguntas para Moodle |

---

## Nota sobre el Dataset

Con solo 20 muestras, el modelo de regresión puede ajustar muy bien los datos de entrenamiento pero puede sobreajustarse. Es importante incluir una celda explicativa que mencione:
- En producción real, se necesitarían cientos o miles de personajes
- El R² alto (~0.98) se explica en gran parte por las correlaciones muy fuertes del dataset diseñado
- El objetivo pedagógico es aprender el *proceso* de ML, no los resultados numéricos específicos

---

*Documento de planificación — Parte 3 | INT210 USFX*
