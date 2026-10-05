# Banco de Preguntas Moodle — Parte 2: Análisis Exploratorio con Pandas
## Lab: Diseño de Personajes 2D — Serie *Neon Skies*
### Machine Learning from Scratch | INT210

---

> **Convenciones de este documento**
>
> Cada pregunta indica su tipo sugerido para Moodle:
> - **[COMPLETAR]** → Cloze / Drag-and-Drop (el estudiante arrastra o escribe el comando/argumento exacto en el espacio en blanco)
> - **[SELECCIÓN]** → Opción múltiple (el estudiante elige el fragmento de código, resultado o afirmación correcta entre opciones)
> - **[CONCEPTUAL]** → Pregunta teórica o explicativa (propósito, justificación matemática o metodológica)
> - **[LÓGICA]** → Basada en la salida real del notebook ejecutado (diseñada como control anti-plagio/anti-IA, requiere haber corrido el código)
> - **[V/F]** → Verdadero o Falso con justificación
>
> Las respuestas correctas se indican con ✅. Los distractores plausibles se indican con ❌.

---

## Sección 0 — Configuración e Importación de Librerías

---

### P01 [COMPLETAR] — Configuración
**Completa la línea para importar la librería Pandas bajo su alias convencional.**

```python
import pandas as _____
```

Opciones: `pd` / `np` / `plt` / `sns`

✅ **Respuesta:** `pd`

---

### P02 [SELECCIÓN] — Configuración
**¿Cuál de las siguientes importaciones es la recomendada para la visualización estadística complementaria a Matplotlib?**

A) `import seaborn as sns` ✅  
B) `import sklearn.visualization as sns` ❌  
C) `import pandas.plots as sns` ❌  
D) `import matplotlib.seaborn as sns` ❌  

---

### P03 [CONCEPTUAL] — Configuración
**¿Cuál es la diferencia de enfoque principal entre `matplotlib` y `seaborn`?**

A) `matplotlib` es exclusivamente para 3D y `seaborn` para 2D. ❌  
B) `matplotlib` es una librería base de bajo nivel para control fino de figuras y ejes, mientras que `seaborn` provee interfaces estadísticas de alto nivel integradas directamente con DataFrames de Pandas. ✅  
C) `seaborn` no requiere DataFrames ni arrays, solo listas nativas. ❌  
D) `seaborn` reemplaza por completo el motor de renderizado de `matplotlib` sin usar sus figuras. ❌  

---

## Sección 1 — Ejercicio 2.1: Ingesta e Inspección Estructural del Dataset

---

### P04 [COMPLETAR] — Ejercicio 2.1
**Completa la función de Pandas para leer el archivo CSV en un DataFrame.**

```python
df = pd.____("characters_clean.csv")
```

Opciones: `read_csv` / `load_csv` / `from_csv` / `read_table`

✅ **Respuesta:** `read_csv`

---

### P05 [COMPLETAR] — Ejercicio 2.1
**Completa el método para visualizar únicamente los primeros 5 registros de un DataFrame.**

```python
print(df.____(5))
```

Opciones: `head` / `top` / `first` / `tail`

✅ **Respuesta:** `head`

---

### P06 [COMPLETAR] — Ejercicio 2.1
**Completa el atributo (no método) para obtener la tupla de dimensiones `(filas, columnas)` del DataFrame.**

```python
dimensiones = df.____
```

Opciones: `shape` / `size` / `dimensions` / `len`

✅ **Respuesta:** `shape`

---

### P07 [LÓGICA] — Ejercicio 2.1
**¿Cuáles son las dimensiones exactas del dataset `characters_clean.csv` tras ser cargado correctamente en Pandas?**

A) (20, 10) ❌  
B) (20, 12) ✅  
C) (100, 12) ❌  
D) (12, 20) ❌  

---

### P08 [COMPLETAR] — Ejercicio 2.1
**Completa el atributo para consultar el tipo de dato técnico de cada columna en el DataFrame.**

```python
tipos = df.____
```

Opciones: `dtypes` / `types` / `dtype` / `data_types`

✅ **Respuesta:** `dtypes`

---

### P09 [LÓGICA] — Ejercicio 2.1
**Al inspeccionar `df.dtypes`, ¿cuáles columnas presentan el tipo `object` (cadenas de texto) en lugar de un tipo numérico?**

A) `fps`, `screen_time_ratio`, `production_hours` ❌  
B) `name`, `role`, `style` ✅  
C) Solo la columna `name` ❌  
D) `has_special_fx`, `palette`, `states` ❌  

---

### P10 [COMPLETAR] — Ejercicio 2.1
**Completa el método para calcular el resumen de estadísticas descriptivas (media, desviación, mínimo, percentiles y máximo) de las columnas numéricas.**

```python
resumen = df.____().round(2)
```

Opciones: `describe` / `summary` / `stats` / `info`

✅ **Respuesta:** `describe`

---

### P11 [LÓGICA] — Ejercicio 2.1
**Según la salida de `df.describe()`, ¿cuál es el rango de valores (mínimo y máximo) de la variable objetivo `production_hours`?**

A) Mínimo: 0.0 h | Máximo: 200.0 h ❌  
B) Mínimo: 18.00 h | Máximo: 185.00 h ✅  
C) Mínimo: 30.00 h | Máximo: 168.00 h ❌  
D) Mínimo: 48.00 h | Máximo: 142.00 h ❌  

---

### P12 [LÓGICA] — Ejercicio 2.1
**¿A qué personaje específico corresponde el valor mínimo de 18.00 horas de producción y a cuál el valor máximo de 185.00 horas?**

A) Mínimo: Pip | Máximo: Seraph ❌  
B) Mínimo: Olmo | Máximo: Blaze ✅  
C) Mínimo: Crux | Máximo: Kael ❌  
D) Mínimo: Sela | Máximo: Asha ❌  

---

### P13 [V/F] — Ejercicio 2.1
**El método `df.describe()` por defecto omite las columnas no numéricas (`name`, `role`, `style`) a menos que se especifique el argumento `include="all"`.**

✅ **Verdadero.** En DataFrames mixtos, `describe()` resume únicamente columnas con tipos numéricos (`int64`, `float64`).

---

## Sección 2 — Ejercicio 2.2: Distribución y Detección de Outliers

---

### P14 [COMPLETAR] — Ejercicio 2.2
**Completa el código para generar histogramas de las columnas seleccionadas con 8 intervalos (bins).**

```python
cols_num = ["fps", "screen_time_ratio", "num_states", "num_frames_total", "production_hours"]
df[cols_num].hist(bins=____, figsize=(12, 8))
```

Opciones: `8` / `5` / `10` / `20`

✅ **Respuesta:** `8`

---

### P15 [COMPLETAR] — Ejercicio 2.2
**Completa el argumento para definir el tipo de gráfico como diagrama de caja (boxplot).**

```python
df[cols_num].plot(kind=____, figsize=(12, 5))
```

Opciones: `"box"` / `"boxplot"` / `"bar"` / `"hist"`

✅ **Respuesta:** `"box"`

---

### P16 [CONCEPTUAL] — Ejercicio 2.2
**En un diagrama de caja (boxplot), ¿cómo se define formalmente el Rango Intercuartílico (IQR)?**

A) $\text{IQR} = \text{Media} - \text{Mediana}$ ❌  
B) $\text{IQR} = Q3 - Q1$ (Tercer cuartil menos primer cuartil) ✅  
C) $\text{IQR} = \text{Máximo} - \text{Mínimo}$ ❌  
D) $\text{IQR} = 1.5 \times \sigma$ ❌  

---

### P17 [CONCEPTUAL] — Ejercicio 2.2
**¿Qué criterio matemático convencional se utiliza en un boxplot para marcar un punto como valor atípico (outlier)?**

A) Cualquier valor mayor a la media más una desviación estándar. ❌  
B) Cualquier valor que esté por encima de $Q3 + 1.5 \times \text{IQR}$ o por debajo de $Q1 - 1.5 \times \text{IQR}$. ✅  
C) Cualquier valor que exceda el percentil 90. ❌  
D) Todo valor con frecuencia absoluta menor a 2. ❌  

---

### P18 [LÓGICA] — Ejercicio 2.2
**Al examinar la distribución de `fps`, ¿por qué no forma una curva continua y cuáles son sus tres únicos valores presentes en el dataset?**

A) Es continua pero el tamaño de muestra es muy pequeño. ❌  
B) Porque representa tasas de fotogramas estándar de la industria de animación: solo toma los valores discretos 8, 12 y 24 fps. ✅  
C) Porque hubo errores de captura en los fotogramas de los personajes de soporte. ❌  
D) Solo toma valores pares entre 10 y 30 fps. ❌  

---

### P19 [LÓGICA] — Ejercicio 2.2
**¿Qué personaje se sitúa como el valor atípico superior extremo en `num_frames_total` con 168 fotogramas?**

A) Seraph ❌  
B) Gorr ❌  
C) Blaze ✅  
D) Asha ❌  

---

### P20 [SELECCIÓN] — Ejercicio 2.2
**¿Qué comando de Matplotlib se utiliza para agregar un título principal centrado sobre un conjunto de subgráficos generados con `df.hist()`?**

A) `plt.title()` ❌ — Agrega título solo al eje actual  
B) `plt.suptitle()` ✅  
C) `plt.main_title()` ❌  
D) `df.set_title()` ❌  

---

## Sección 3 — Ejercicio 2.3: Análisis Categórico y Agregaciones

---

### P21 [COMPLETAR] — Ejercicio 2.3
**Completa el método para calcular la frecuencia de cada categoría en la columna `role`.**

```python
conteo_roles = df["role"].____()
```

Opciones: `value_counts` / `count_values` / `frequencies` / `unique_counts`

✅ **Respuesta:** `value_counts`

---

### P22 [LÓGICA] — Ejercicio 2.3
**¿Cuántos personajes corresponden a cada rol según `df["role"].value_counts()`?**

A) protagonist: 4, antagonist: 7, support: 9 ✅  
B) protagonist: 10, antagonist: 5, support: 5 ❌  
C) protagonist: 7, antagonist: 7, support: 6 ❌  
D) protagonist: 2, antagonist: 8, support: 10 ❌  

---

### P23 [LÓGICA] — Ejercicio 2.3
**¿Cuántos personajes corresponden a cada estilo según `df["style"].value_counts()`?**

A) painted: 10, flat: 5, cel_shaded: 5 ❌  
B) painted: 7, flat: 7, cel_shaded: 6 ✅  
C) painted: 8, flat: 8, cel_shaded: 4 ❌  
D) painted: 6, flat: 7, cel_shaded: 7 ❌  

---

### P24 [COMPLETAR] — Ejercicio 2.3
**Completa el código para calcular el promedio de horas de producción agrupado por rol.**

```python
avg_role = df.groupby(____)[____].mean().round(2)
```

Opciones: `"role"`, `"production_hours"` / `"production_hours"`, `"role"` / `"style"`, `"production_hours"` / `"role"`, `"fps"`

✅ **Respuesta:** `"role"`, `"production_hours"`

---

### P25 [LÓGICA] — Ejercicio 2.3
**¿Cuál es el promedio de horas de producción para los personajes de rol `protagonist` frente a los de rol `support`?**

A) Protagonistas: 120.93 h | Soporte: 99.50 h ❌  
B) Protagonistas: 162.50 h | Soporte: 47.78 h ✅  
C) Protagonistas: 145.00 h | Soporte: 52.00 h ❌  
D) Protagonistas: 185.00 h | Soporte: 18.00 h ❌  

---

### P26 [LÓGICA] — Ejercicio 2.3
**¿Cuál de los tres estilos de animación requiere en promedio la menor cantidad de horas de producción?**

A) `painted` (149.93 h) ❌  
B) `cel_shaded` (99.50 h) ❌  
C) `flat` (40.00 h) ✅  
D) Todos los estilos requieren tiempos similares ❌  

---

### P27 [SELECCIÓN] — Ejercicio 2.3
**¿Cuál de los siguientes fragmentos genera un gráfico de barras con Seaborn para graficar las horas promedio por estilo?**

A) `sns.lineplot(x=avg_style.index, y=avg_style.values)` ❌  
B) `sns.barplot(x=avg_style.index, y=avg_style.values)` ✅  
C) `sns.histplot(x=avg_style.index, y=avg_style.values)` ❌  
D) `sns.scatter(x=avg_style.index, y=avg_style.values)` ❌  

---

### P28 [CONCEPTUAL] — Ejercicio 2.3
**¿Por qué los personajes protagonistas demandan significativamente más horas que los de soporte en un estudio de animación?**

A) Porque tienen más estados de animación (correr, saltar, ataques especiales), mayor tasa de fotogramas (24 fps) y mayor tiempo en pantalla. ✅  
B) Porque se dibujan exclusivamente en estilo `flat`. ❌  
C) Porque tienen menor cantidad de colores en su paleta. ❌  
D) Porque se animan a 8 fps lo que requiere mayor detalle manual. ❌  

---

## Sección 4 — Ejercicio 2.4: Matriz de Correlación y Mapa de Calor

---

### P29 [COMPLETAR] — Ejercicio 2.4
**Completa el método de Pandas para filtrar y seleccionar únicamente las columnas de tipo numérico.**

```python
df_num = df.select_dtypes(include=____)
```

Opciones: `"number"` / `"numeric"` / `"float"` / `"int"`

✅ **Respuesta:** `"number"`

---

### P30 [COMPLETAR] — Ejercicio 2.4
**Completa el método para calcular la matriz de coeficientes de correlación de Pearson.**

```python
corr_matrix = df_num.____()
```

Opciones: `corr` / `correlation` / `cov` / `pearson`

✅ **Respuesta:** `corr`

---

### P31 [COMPLETAR] — Ejercicio 2.4
**Completa la llamada a Seaborn para dibujar un mapa de calor con anotación de valores numéricos en cada celda.**

```python
sns.heatmap(corr_matrix, annot=____, cmap="coolwarm", fmt=".2f")
```

Opciones: `True` / `False` / `"yes"` / `1`

✅ **Respuesta:** `True`

---

### P32 [LÓGICA] — Ejercicio 2.4
**¿Cuál es el coeficiente de correlación de Pearson ($r$) entre `num_frames_total` y `production_hours`?**

A) +0.7623 ❌  
B) +0.9181 ❌  
C) +0.9782 ✅  
D) +0.2883 ❌  

---

### P33 [CONCEPTUAL] — Ejercicio 2.4
**¿Qué indica un coeficiente de correlación lineal de $r = +0.9782$?**

A) Que no existe ninguna relación entre ambas variables. ❌  
B) Una relación lineal positiva prácticamente perfecta: a mayor cantidad de fotogramas totales, mayor es el tiempo de producción de forma proporcional. ✅  
C) Que `production_hours` causa que se incrementen los fotogramas en el guión. ❌  
D) Que el modelo tiene un error de predicción del 97.82%. ❌  

---

### P34 [LÓGICA] — Ejercicio 2.4
**¿Qué variable numérica presenta una correlación negativa moderada con `production_hours` ($r = -0.5491$)?**

A) `color_contrast` ❌  
B) `screen_time_ratio` ❌  
C) `avg_brightness` ✅  
D) `has_special_fx` ❌  

---

### P35 [CONCEPTUAL] — Ejercicio 2.4
**¿Cómo se interpreta la correlación negativa entre `avg_brightness` y `production_hours` en el contexto del diseño artístico de *Neon Skies*?**

A) Los personajes con mayor brillo promedio (paletas claras y tonos pastel de personajes de soporte sencillos) requieren menos horas de producción, mientras que personajes oscuros y ricamente sombreados demandan más tiempo. ✅  
B) Aumentar el brillo del monitor reduce el tiempo que tarda el artista en dibujar. ❌  
C) Indica un error en el cálculo de brillo durante la Parte 1. ❌  
D) Significa que los colores brillantes se renderizan más rápido en el motor de juego. ❌  

---

### P36 [LÓGICA] — Ejercicio 2.4
**¿Cuál es la correlación de `color_contrast` con `production_hours`?**

A) +0.9404 ❌  
B) +0.2883 ✅  
C) -0.5491 ❌  
D) +0.6585 ❌  

---

### P37 [CONCEPTUAL] — Ejercicio 2.4
**¿Por qué un valor de $r = 0.2883$ descarta a `color_contrast` como buena candidata para un modelo de regresión lineal?**

A) Porque los coeficientes menores a 0.30 reflejan una relación lineal débil o casi nula; la variable aporta principalmente ruido al modelo. ✅  
B) Porque las correlaciones positivas no pueden usarse en regresión lineal. ❌  
C) Porque causaría que los coeficientes del modelo sean números imaginarios. ❌  
D) Porque `color_contrast` es una variable cualitativa no continua. ❌  

---

### P38 [COMPLETAR] — Ejercicio 2.4
**Completa el código para ordenar las correlaciones con la variable objetivo de mayor a menor.**

```python
corr_target = corr_matrix["production_hours"].drop("production_hours").sort_values(ascending=____)
```

Opciones: `False` / `True` / `"desc"` / `None`

✅ **Respuesta:** `False`

---

## Sección 5 — Ejercicio 2.5: Codificación de Variables Categóricas

---

### P39 [COMPLETAR] — Ejercicio 2.5
**Completa la función de Pandas para aplicar codificación One-Hot (variables dummy) a columnas categóricas.**

```python
df_encoded = pd.____(df, columns=["role"], drop_first=True)
```

Opciones: `get_dummies` / `one_hot` / `dummy_encode` / `to_dummies`

✅ **Respuesta:** `get_dummies`

---

### P40 [CONCEPTUAL] — Ejercicio 2.5
**¿Cuál es el propósito del parámetro `drop_first=True` en `pd.get_dummies` al preparar datos para regresión lineal?**

A) Acelerar el tiempo de cómputo eliminando el 50% de las observaciones. ❌  
B) Evitar la trampa de la variable dummy (multicolinealidad perfecta), garantizando que las columnas dummy no sumen 1 con el término constante y la matriz $X^T X$ sea invertible. ✅  
C) Eliminar valores nulos que puedan existir en la primera fila. ❌  
D) Forzar a que todos los coeficientes resultantes sean positivos. ❌  

---

### P41 [LÓGICA] — Ejercicio 2.5
**Si la columna `role` tiene 3 categorías únicas (`antagonist`, `protagonist`, `support`), ¿cuántas columnas nuevas genera `pd.get_dummies(df, columns=["role"], drop_first=True)`?**

A) 1 columna ❌  
B) 2 columnas (`role_protagonist` y `role_support`) ✅  
C) 3 columnas ❌  
D) 6 columnas ❌  

---

### P42 [CONCEPTUAL] — Ejercicio 2.5
**En el caso anterior con `drop_first=True`, ¿cómo se representa matemáticamente a un personaje cuyo rol original es `antagonist`?**

A) `role_protagonist = 1` y `role_support = 1` ❌  
B) `role_protagonist = 0` y `role_support = 0` (categoría base de referencia) ✅  
C) Con un valor de -1 en ambas columnas ❌  
D) No se puede representar y debe descartarse ❌  

---

### P43 [COMPLETAR] — Ejercicio 2.5
**Completa el diccionario de mapeo ordinal para transformar la jerarquía de estilos en enteros.**

```python
style_map = {
    "flat": ____,
    "cel_shaded": ____,
    "painted": ____
}
```

Opciones: `0, 1, 2` / `1, 2, 3` / `"low", "medium", "high"` / `0.1, 0.5, 1.0`

✅ **Respuesta:** `0, 1, 2`

---

### P44 [COMPLETAR] — Ejercicio 2.5
**Completa el método para aplicar el diccionario de mapeo a la serie `df["style"]`.**

```python
df["style_code"] = df["style"].____(style_map)
```

Opciones: `map` / `apply` / `transform` / `replace_dict`

✅ **Respuesta:** `map`

---

### P45 [LÓGICA] — Ejercicio 2.5
**Dado el mapeo `{"flat": 0, "cel_shaded": 1, "painted": 2}`, ¿qué valor numérico tiene la columna `style_code` para el personaje `Lyra`?**

A) 0 ❌  
B) 1 (su estilo es `cel_shaded`) ✅  
C) 2 ❌  
D) `None` ❌  

---

### P46 [LÓGICA] — Ejercicio 2.5
**¿Qué valor numérico tiene `style_code` para el personaje `Blaze`?**

A) 0 ❌  
B) 1 ❌  
C) 2 (su estilo es `painted`) ✅  
D) 3 ❌  

---

### P47 [V/F] — Ejercicio 2.5
**Una variable nominal sin orden jerárquico como `role` debe codificarse preferentemente con One-Hot Encoding (`get_dummies`), mientras que una variable con niveles de complejidad natural como `style` puede mapearse ordinalmente.**

✅ **Verdadero.** Las variables nominales no admiten orden cuantitativo arbitrario; las variables ordinales sí reflejan una escala relativa.

---

## Sección 6 — Ejercicio 2.6: Selección de Características y Exportación

---

### P48 [COMPLETAR] — Ejercicio 2.6
**Completa la condición de lista por comprensión para filtrar las características con valor absoluto de correlación superior o igual al umbral.**

```python
threshold = 0.60
selected = [col for col in corr_target.index if abs(corr_target[col]) >= ____]
```

Opciones: `threshold` / `0.50` / `corr_target` / `1.0`

✅ **Respuesta:** `threshold`

---

### P49 [LÓGICA] — Ejercicio 2.6
**Al aplicar el umbral de correlación $|r| \ge 0.60$, ¿cuáles variables numéricas son seleccionadas?**

A) Solo `num_frames_total` y `fps` ❌  
B) `num_frames_total`, `screen_time_ratio`, `num_states`, `fps`, `has_special_fx`, `num_colors` ✅  
C) Todas las columnas numéricas incluyendo `color_contrast` ❌  
D) Solo variables con $r > 0.95$ ❌  

---

### P50 [CONCEPTUAL] — Ejercicio 2.6
**¿Por qué se decide excluir `num_colors` del conjunto final de características para regresión múltiple a pesar de tener $r = 0.6585$?**

A) Porque es una variable categórica. ❌  
B) Para evitar redundancia y multicolinealidad, dado que la complejidad del personaje ya está fuertemente capturada por `num_frames_total` y `num_states`. ✅  
C) Porque los colores no son numéricos. ❌  
D) Porque su correlación fue calculada con signo negativo. ❌  

---

### P51 [LÓGICA] — Ejercicio 2.6
**¿Cuáles son las dimensiones exactas (filas y columnas) del DataFrame `df_features` exportado?**

A) (20, 6) ❌  
B) (20, 7) — 20 personajes y 7 columnas (`name` + 5 predictores + `production_hours`) ✅  
C) (16, 7) ❌  
D) (20, 12) ❌  

---

### P52 [COMPLETAR] — Ejercicio 2.6
**Completa el método y argumento para exportar el DataFrame a CSV sin incluir el índice numérico de filas.**

```python
df_features.to_csv("characters_features.csv", index=____)
```

Opciones: `False` / `True` / `None` / `0`

✅ **Respuesta:** `False`

---

### P53 [CONCEPTUAL] — Ejercicio 2.6
**¿Por qué es fundamental exportar con `index=False` al generar datasets para Machine Learning?**

A) Porque de lo contrario Pandas agrega una columna sin nombre con los números de fila (`0, 1, 2...`), que luego puede confundirse erróneamente con una característica predictora al reabrir el archivo. ✅  
B) Porque de lo contrario el archivo no puede guardarse en Windows. ❌  
C) Porque el formato CSV no soporta texto con índices. ❌  
D) Porque reduce el tamaño del archivo a la mitad. ❌  

---

### P54 [CONCEPTUAL] — Ejercicio 2.6
**¿Por qué conservamos la columna `name` en `characters_features.csv` si no se usará como variable matemática en la regresión?**

A) Para cumplir con los requerimientos de sintaxis de Pandas. ❌  
B) Para actuar como identificador único que permita rastrear personajes en el análisis de errores, etiquetar puntos en gráficos de dispersión y validar predicciones individuales (como la del personaje `Nova`). ✅  
C) Para usar su longitud en caracteres como característica adicional. ❌  
D) No tiene ninguna utilidad y se incluyó por error. ❌  

---

## Sección 7 — Preguntas Integradoras y de Síntesis del Módulo

---

### P55 [SELECCIÓN] — Síntesis
**¿Cuál de las siguientes afirmaciones describe con mayor precisión la secuencia metodológica aplicada en este laboratorio?**

A) Carga de datos → Eliminación de outliers con IQR → Entrenamiento de modelo → Exportación a SQL ❌  
B) Carga e inspección estructural → Análisis univariado (distribuciones) → Análisis bivariado (agrupaciones y correlación) → Codificación categórica → Selección de características por umbral → Exportación a CSV ✅  
C) Normalización de variables → Análisis PCA → Reducción t-SNE → Gráficos de barras ❌  
D) Limpieza de strings → Codificación manual → Gráficos de pastel → Clasificación k-NN ❌  

---

### P56 [V/F] — Síntesis
**Una correlación de Pearson alta ($r = 0.978$) entre `num_frames_total` y `production_hours` garantiza que un modelo de regresión lineal simple sobre esta única característica tendrá un coeficiente de determinación $R^2$ cercano a $0.95$.**

✅ **Verdadero.** En regresión lineal simple, el coeficiente de determinación es exactamente igual al cuadrado del coeficiente de correlación de Pearson: $R^2 = r^2 = (0.9782)^2 \approx 0.9569$.

---

### P57 [LÓGICA] — Síntesis
**En el dataset exportado `characters_features.csv`, ¿cuál es el valor de `num_frames_total` y `production_hours` para el personaje `Kael`?**

A) 120 fotogramas y 138.5 horas ✅  
B) 144 fotogramas y 168.0 horas ❌  
C) 96 fotogramas y 115.0 horas ❌  
D) 48 fotogramas y 78.0 horas ❌  

---

### P58 [LÓGICA] — Síntesis
**¿Cuál de los siguientes personajes de la serie tiene el atributo `has_special_fx = 0` y pertenece al subgrupo de 12 fps?**

A) Lyra ❌ (24 fps, fx=1)  
B) Mira ✅ (12 fps, fx=0)  
C) Vela ❌ (12 fps, fx=1)  
D) Drak ❌ (24 fps, fx=1)  

---

*Fin del Banco de Preguntas Moodle — Parte 2: Análisis Exploratorio con Pandas (INT210)*
