# Plan de Construcción — Parte 2
## Análisis Exploratorio con Pandas y Selección de Características
### Serie: Machine Learning from Scratch | Laboratorio *Neon Skies* | INT210

---

## Visión General

**Entrada:** `characters_clean.csv` generado en la Parte 1  
**Salida:** `characters_features.csv` — subconjunto de características seleccionadas con variable objetivo  
**Variable Objetivo (Target):** `production_hours`  
**Librerías requeridas:** `pandas`, `matplotlib`, `seaborn`

**Correlaciones con `production_hours` (Pearson, calculadas sobre el dataset):**

| Campo | Correlación | Interpretación |
|---|---|---|
| `num_frames_total` | **+0.978** | Muy alta — mejor predictor simple |
| `screen_time_ratio` | **+0.946** | Muy alta |
| `num_states` | **+0.940** | Muy alta |
| `fps` | **+0.918** | Alta |
| `has_special_fx` | **+0.762** | Moderada-alta |
| `num_colors` | **+0.659** | Moderada |
| `avg_brightness` | **−0.549** | Moderada negativa |
| `color_contrast` | **+0.288** | Baja — candidata a descartar |

**Conclusión de selección de características para la Parte 3:**  
Características seleccionadas: `num_frames_total`, `screen_time_ratio`, `num_states`, `fps`, `has_special_fx`  
Características descartadas: `color_contrast` (correlación < 0.30), `avg_brightness` (correlación negativa moderada, multicolinealidad potencial con `num_frames_total`), `num_colors` (redundante dado que `num_frames_total` ya captura complejidad)

---

## Estructura del Notebook

### Sección de Título

**Título:** `Análisis Exploratorio de Datos con Pandas: Laboratorio de Diseño de Personajes 2D`  
**Subtítulo/Serie:** Machine Learning from Scratch | Parte 2 de 3 — Pandas, Visualización y Selección de Características

**Contexto:**  
Explica que el dataset `characters_clean.csv` fue preparado en la Parte 1 y contiene 20 registros de personajes de la serie *Neon Skies* con campos numéricos derivados. El objetivo de esta parte es usar Pandas para explorar la distribución de los datos, identificar relaciones entre variables mediante análisis de correlación, aplicar codificación a variables categóricas y seleccionar las características más relevantes para alimentar el modelo de regresión lineal de la Parte 3.

**Objetivos de Aprendizaje:**
- Cargar y explorar un dataset con Pandas (`read_csv`, `head`, `describe`, `dtypes`, `shape`)
- Identificar distribuciones con histogramas y boxplots (`matplotlib` / `seaborn`)
- Calcular y visualizar la matriz de correlación con mapa de calor (`heatmap`)
- Codificar variables categóricas con `pd.get_dummies` y `map`
- Seleccionar características basándose en criterios de correlación con la variable objetivo
- Exportar el conjunto de datos de características final a CSV

---

## Ejercicio 2.1 — Carga e Inspección Inicial del Dataset

**Concepto a demostrar:** `pd.read_csv`, `df.head()`, `df.shape`, `df.dtypes`, `df.describe()`

**Ejemplo funcional (no modificar):**
```python
import pandas as pd
sample = pd.DataFrame({"nombre": ["Alpha","Beta"], "fps": [24, 12], "horas": [120.0, 48.0]})
print(sample.head())
print("Forma:", sample.shape)
print("Tipos:\n", sample.dtypes)
```

**Tarea del estudiante:**
1. Cargar `characters_clean.csv` con `pd.read_csv` en una variable `df`
2. Imprimir las primeras 5 filas con `df.head()`
3. Imprimir la forma (`df.shape`) e interpretar: cuántas filas y columnas
4. Imprimir los tipos de cada columna con `df.dtypes`
5. Imprimir el resumen estadístico con `df.describe()`

**Placeholders a completar:**
```python
df = pd.read_csv(???)
print(df.???(5))
print("Forma:", df.???)
print("Tipos:\n", df.???)
print(df.???())
```

**Salida esperada:**
- 20 filas × 12 columnas
- Columnas `role` y `style` serán de tipo `object`; el resto numérico
- `describe()` muestra min/max/mean/std de columnas numéricas
- `production_hours`: min=18.0, max=185.0, mean≈96.33

**Pregunta Lógica 2.1:**
- a) ¿Cuántas filas y columnas tiene el dataset?
- b) ¿Qué columnas tienen tipo `object` en lugar de numérico?
- c) ¿Cuál es el valor mínimo y máximo de `production_hours`?

---

## Ejercicio 2.2 — Distribución de Variables Numéricas

**Concepto a demostrar:** `df.hist()`, `df.plot(kind="box")`, `matplotlib.pyplot`

**Ejemplo funcional (no modificar):**
```python
import matplotlib.pyplot as plt
sample = pd.DataFrame({"horas": [30, 48, 78, 120, 185]})
sample["horas"].plot(kind="hist", bins=5, title="Distribución de Horas")
plt.xlabel("Horas")
plt.tight_layout()
plt.show()
```

**Tarea del estudiante:**
1. Seleccionar las columnas numéricas relevantes: `fps`, `screen_time_ratio`, `num_states`, `num_frames_total`, `production_hours`
2. Generar un histograma de cada columna con `df[cols].hist(bins=8, figsize=(12, 8))`
3. Generar un boxplot con `df[cols].plot(kind="box", figsize=(12, 5), rot=30)`
4. Agregar título y etiquetas de ejes apropiados

**Placeholders a completar:**
```python
cols_num = [???, ???, ???, ???, ???]
df[cols_num].hist(???, figsize=(12, 8))
plt.suptitle(???)
plt.tight_layout()
plt.show()
```

**Salida esperada:**
- Los histogramas revelan que `num_frames_total` y `production_hours` tienen distribución sesgada hacia la derecha con outlier en Blaze (168 fotogramas, 185 horas)
- El boxplot muestra que `fps` solo tiene 3 valores posibles (8, 12, 24), visible como puntos discretos

**Pregunta Lógica 2.2:**
- a) ¿Qué columna muestra la mayor dispersión según el boxplot?
- b) ¿Qué personaje corresponde al outlier visible en `num_frames_total`?
- c) ¿Cuántos valores distintos tiene la columna `fps`?

---

## Ejercicio 2.3 — Análisis de Variables Categóricas

**Concepto a demostrar:** `df["col"].value_counts()`, `df.groupby()`, gráfico de barras con `seaborn`

**Ejemplo funcional (no modificar):**
```python
import seaborn as sns
data = pd.DataFrame({"estilo": ["flat","painted","flat","cel_shaded"], "horas": [48, 168, 52, 78]})
print(data["estilo"].value_counts())
promedios = data.groupby("estilo")["horas"].mean()
promedios.plot(kind="bar", title="Horas promedio por estilo")
plt.show()
```

**Tarea del estudiante:**
1. Imprimir `df["role"].value_counts()` y `df["style"].value_counts()`
2. Calcular el promedio de `production_hours` agrupado por `role` usando `groupby`
3. Calcular el promedio de `production_hours` agrupado por `style` usando `groupby`
4. Graficar ambos promedios como gráficos de barras con `seaborn.barplot`

**Placeholders a completar:**
```python
print(df[???].value_counts())
avg_by_role = df.groupby(???)[???].mean().round(2)
print(avg_by_role)
sns.barplot(x=avg_by_role.index, y=avg_by_role.values)
plt.title(???)
plt.show()
```

**Salida esperada:**
- `role`: support=9, antagonist=7, protagonist=4
- `style`: flat=7, painted=7, cel_shaded=6
- Promedio por rol: protagonist≈162.5h, antagonist≈116.4h, support≈52.2h
- Promedio por estilo: painted≈144.9h, cel_shaded≈99.2h, flat≈40.3h

**Pregunta Lógica 2.3:**
- a) ¿Qué rol tiene el mayor promedio de horas de producción?
- b) ¿Qué estilo de animación está asociado al menor promedio de horas?
- c) ¿Cuántos personajes tienen el estilo `"painted"`?

---

## Ejercicio 2.4 — Matriz de Correlación y Mapa de Calor

**Concepto a demostrar:** `df.corr()`, `seaborn.heatmap()`, interpretación de correlación Pearson

**Ejemplo funcional (no modificar):**
```python
data = pd.DataFrame({"x": [1,2,3,4,5], "y": [2,4,5,4,6], "z": [5,3,2,1,0]})
corr = data.corr()
print(corr.round(2))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlación")
plt.show()
```

**Tarea del estudiante:**
1. Seleccionar solo las columnas numéricas del dataset (excluir `name`, `role`, `style`)
2. Calcular la matriz de correlación con `df_num.corr()`
3. Visualizar el mapa de calor con `seaborn.heatmap(annot=True, cmap="coolwarm", fmt=".2f")`
4. Imprimir la correlación de cada columna con `production_hours` ordenada de mayor a menor

**Placeholders a completar:**
```python
df_num = df.select_dtypes(include=???)
corr_matrix = df_num.???()
sns.heatmap(???, annot=???, cmap=???, fmt=???)
plt.title("Matriz de Correlación — Neon Skies Dataset")
plt.tight_layout()
plt.show()
corr_target = corr_matrix["production_hours"].drop(???).???(ascending=False)
print("Correlación con production_hours:\n", corr_target.round(4))
```

**Salida esperada (correlaciones con `production_hours`):**
```
num_frames_total    +0.978
screen_time_ratio   +0.946
num_states          +0.940
fps                 +0.918
has_special_fx      +0.762
num_colors          +0.659
avg_brightness      -0.549
color_contrast      +0.288
```

**Pregunta Lógica 2.4:**
- a) ¿Qué variable tiene la correlación más alta con `production_hours`?
- b) ¿Qué variables tienen correlación negativa con `production_hours`?
- c) ¿Qué indica una correlación de +0.978 entre `num_frames_total` y `production_hours`?
- d) ¿Por qué `color_contrast` podría descartarse como característica para el modelo?

---

## Ejercicio 2.5 — Codificación de Variables Categóricas

**Concepto a demostrar:** `pd.get_dummies()`, `df["col"].map({})`, por qué ML requiere variables numéricas

**Ejemplo funcional (no modificar):**
```python
sample = pd.DataFrame({"estilo": ["flat", "painted", "flat", "cel_shaded"], "fps": [12, 24, 12, 24]})
encoded = pd.get_dummies(sample, columns=["estilo"])
print(encoded)
```

**Tarea del estudiante:**
1. Explicar por qué columnas como `role` y `style` no pueden usarse directamente en un modelo de ML
2. Crear variables dummy para `role` con `pd.get_dummies(df, columns=["role"], drop_first=True)`
3. Crear un mapeo manual para `style`: `{"flat": 0, "cel_shaded": 1, "painted": 2}` usando `df["style"].map({...})`
4. Imprimir las nuevas columnas y verificar que son numéricas

**Placeholders a completar:**
```python
df_encoded = pd.get_dummies(df, columns=[???], drop_first=???)
print("Columnas tras codificación:", df_encoded.columns.tolist())

style_map = {???}
df["style_code"] = df["style"].???(style_map)
print(df[["style", "style_code"]].drop_duplicates().sort_values("style_code"))
```

**Salida esperada:**
- `get_dummies` con `drop_first=True` sobre `role` crea columnas `role_protagonist`, `role_support` (antagonist es la categoría de referencia)
- `style_code`: flat=0, cel_shaded=1, painted=2

**Pregunta Lógica 2.5:**
- a) ¿Por qué se utiliza `drop_first=True` en `pd.get_dummies`?
- b) ¿Cuántas columnas nuevas genera `get_dummies` con `drop_first=True` para una variable con 3 categorías?
- c) ¿Cuál es el `style_code` asignado al personaje Lyra?

---

## Ejercicio 2.6 — Selección de Características y Construcción del Dataset Final

**Concepto a demostrar:** Criterio de umbral de correlación, `df[lista_columnas]`, exportación de features

**Ejemplo funcional (no modificar):**
```python
correlaciones = {"fps": 0.92, "color_contrast": 0.29, "num_states": 0.94}
umbral = 0.60
seleccionadas = [col for col, r in correlaciones.items() if abs(r) >= umbral]
print("Características seleccionadas:", seleccionadas)
```

**Tarea del estudiante:**
1. Establecer un umbral de correlación mínima de `0.60`
2. Usar la correlación calculada en el Ejercicio 2.4 para filtrar las columnas que superen el umbral
3. Construir el DataFrame `df_features` con las columnas seleccionadas más `production_hours`
4. Imprimir el DataFrame final y sus estadísticas básicas
5. Exportar a `characters_features.csv`

**Placeholders a completar:**
```python
umbral = ???
selected_cols = [col for col in corr_target.index if abs(corr_target[col]) >= ???]
print("Características seleccionadas:", selected_cols)

df_features = df_num[selected_cols + [???]]
print(df_features.head())
print(df_features.describe().round(2))

df_features.to_csv(???, index=???)
print("Exportado: characters_features.csv")
```

**Salida esperada:**
- Características seleccionadas: `["num_frames_total", "screen_time_ratio", "num_states", "fps", "has_special_fx", "num_colors"]`
- `color_contrast` (0.288) y `avg_brightness` (-0.549) quedan por debajo o se discute su exclusión
- Dataset final: 20 filas × 7 columnas (6 features + 1 target)

**Pregunta Lógica 2.6:**
- a) ¿Qué columnas quedan excluidas al aplicar el umbral de 0.60?
- b) ¿Por qué `avg_brightness` podría excluirse aunque su correlación absoluta sea mayor al umbral?
- c) ¿Cuántas filas y columnas tiene `df_features`?

---

## Notas Pedagógicas del Notebook

### Estructura de celdas por ejercicio
Cada ejercicio sigue el patrón establecido en la Parte 1:
1. **Celda Markdown:** Referencia conceptual + propósito de la operación
2. **Celda Código (ejemplo):** Resuelto, no modificable
3. **Celda Markdown:** Enunciado de la tarea (qué completar)
4. **Celda Código (estudiante):** Con placeholders `???`
5. **Celda Markdown:** Pregunta Lógica (basada en la salida real)

### Preguntas Lógicas clave para Moodle
- PL 2.1: shape del dataset, tipos de columnas, rango de production_hours
- PL 2.2: columna con mayor dispersión, outlier visible en boxplot
- PL 2.3: rol con mayor promedio de horas, estilo con menor promedio
- PL 2.4: variable con mayor correlación, interpretación de r=0.978
- PL 2.5: propósito de `drop_first`, número de columnas generadas
- PL 2.6: columnas excluidas, justificación de selección

### Conceptos clave para preguntas de código (drag-and-drop Moodle)
- `pd.read_csv("archivo.csv")` — carga un CSV en un DataFrame
- `df.head(n)` — primeras n filas
- `df.shape` — tupla (filas, columnas)
- `df.dtypes` — tipo de cada columna
- `df.describe()` — estadísticas descriptivas
- `df["col"].value_counts()` — frecuencia de categorías
- `df.groupby("col")["target"].mean()` — promedio por grupo
- `df.select_dtypes(include="number")` — seleccionar solo numéricas
- `df.corr()` — matriz de correlación
- `seaborn.heatmap(df.corr(), annot=True, cmap="coolwarm")` — mapa de calor
- `pd.get_dummies(df, columns=["col"], drop_first=True)` — codificación one-hot
- `df["col"].map({dict})` — mapeo de categorías a enteros
- `df.to_csv("archivo.csv", index=False)` — exportar sin índice

---

## Archivos de Salida de la Parte 2

| Archivo | Descripción |
|---|---|
| `Practica_01_Parte2_Pandas_EDA.ipynb` | Notebook del estudiante (con `???`) |
| `Practica_01_Parte2_Pandas_EDA_SOLUCIONES.ipynb` | Solucionario con celdas ejecutadas |
| `Practica_01_Parte2_Pandas_EDA_ES.ipynb` | Versión en español del notebook estudiante |
| `Practica_01_Parte2_Pandas_EDA_SOLUCIONES_ES.ipynb` | Solucionario en español |
| `characters_features.csv` | Dataset de características exportado |
| `Moodle/BancoPreguntas_Parte2_Pandas.md` | Banco de preguntas para Moodle |

---

*Documento de planificación — Parte 2 | INT210 USFX*
