# Banco de Preguntas Moodle — Parte 3: Regresión Lineal desde Cero
## Lab: Diseño de Personajes 2D — Serie *Neon Skies*
### Machine Learning from Scratch | INT210

---

> **Convenciones de este documento**
>
> Cada pregunta indica su tipo sugerido para Moodle:
> - **[COMPLETAR]** → Cloze / Drag-and-Drop (el estudiante arrastra o escribe el comando, función o argumento en el espacio en blanco)
> - **[SELECCIÓN]** → Opción múltiple (el estudiante elige el fragmento de código, resultado o afirmación correcta entre opciones)
> - **[CONCEPTUAL]** → Pregunta teórica o metodológica (justificación matemática, supuestos de OLS)
> - **[LÓGICA]** → Basada en la salida real del notebook ejecutado (diseñada como control anti-plagio/anti-IA, requiere haber corrido el código)
> - **[V/F]** → Verdadero o Falso con justificación
>
> Las respuestas correctas se indican con ✅. Los distractores plausibles se indican con ❌.

---

## Sección 0 — Fundamentos Teóricos (Ejercicio 3.0)

---

### P01 [CONCEPTUAL] — Ejercicio 3.0
**En el modelo de regresión lineal $\hat{y} = \beta_0 + \beta_1 x_1 + \dots + \beta_n x_n$, ¿qué representa el parámetro $\beta_0$ (intercepto o término de bias)?**

A) La tasa de cambio de $y$ por cada incremento unitario en la primera variable. ❌  
B) El valor estimado de la variable objetivo cuando todas las variables predictoras son iguales a cero. ✅  
C) El error estándar residual del modelo. ❌  
D) El coeficiente de correlación de Pearson global. ❌  

---

### P02 [CONCEPTUAL] — Ejercicio 3.0
**¿Cuál es la función de costo que minimiza el método de Mínimos Cuadrados Ordinarios (OLS) en la regresión lineal?**

A) Error Absoluto Medio (MAE) ❌  
B) Error Cuadrático Medio (MSE): $J(\boldsymbol{\beta}) = \frac{1}{m} \sum_{i=1}^m (y_i - \hat{y}_i)^2$ ✅  
C) Entropía Cruzada Binaria ❌  
D) Divergencia de Kullback-Leibler ❌  

---

### P03 [SELECCIÓN] — Ejercicio 3.0
**¿Cuál es la fórmula algebraica de la Ecuación Normal para encontrar el vector óptimo de parámetros $\boldsymbol{\beta}$?**

A) $\boldsymbol{\beta} = \mathbf{X}_b^T \mathbf{y}$ ❌  
B) $\boldsymbol{\beta} = (\mathbf{X}_b^T \mathbf{X}_b)^{-1} \mathbf{X}_b^T \mathbf{y}$ ✅  
C) $\boldsymbol{\beta} = (\mathbf{X}_b \mathbf{X}_b^T)^{-1} \mathbf{y}$ ❌  
D) $\boldsymbol{\beta} = \mathbf{X}_b (\mathbf{X}_b^T \mathbf{y})^{-1}$ ❌  

---

### P04 [V/F] — Ejercicio 3.0
**La Ecuación Normal calcula la solución analítica exacta de los parámetros $\boldsymbol{\beta}$ en un solo paso matricial, sin requerir iteraciones ni tasa de aprendizaje (learning rate) como el Descenso de Gradiente.**

✅ **Verdadero.** Al ser una función cuadrática convexa, igualar la derivada a cero permite resolver el mínimo global analíticamente mediante inversión matricial.

---

## Sección 1 — Ejercicio 3.1: Ingesta y Ensamblaje Matricial

---

### P05 [COMPLETAR] — Ejercicio 3.1
**Completa el atributo para extraer los datos de un DataFrame de Pandas como un array de NumPy.**

```python
X = df[feature_cols].____
```

Opciones: `values` / `to_numpy` / `array` / `matrix`

✅ **Respuesta:** `values` (o `to_numpy()`)

---

### P06 [COMPLETAR] — Ejercicio 3.1
**Completa la función de NumPy para generar un vector columna de unos para el término de intercepto.**

```python
ones = np.____((len(y), 1))
```

Opciones: `ones` / `zeros` / `identity` / `full`

✅ **Respuesta:** `ones`

---

### P07 [COMPLETAR] — Ejercicio 3.1
**Completa la función de NumPy para apilar horizontalmente la columna de unos y la matriz de características `X`.**

```python
X_b = np.____([ones, X])
```

Opciones: `hstack` / `vstack` / `concatenate` / `column_stack`

✅ **Respuesta:** `hstack`

---

### P08 [LÓGICA] — Ejercicio 3.1
**¿Cuáles son las dimensiones exactas de la matriz `X_b` y del vector objetivo `y` en este dataset?**

A) `X_b`: (20, 5) | `y`: (20, 1) ❌  
B) `X_b`: (20, 6) | `y`: (20,) ✅  
C) `X_b`: (16, 6) | `y`: (16,) ❌  
D) `X_b`: (20, 12) | `y`: (20,) ❌  

---

### P09 [CONCEPTUAL] — Ejercicio 3.1
**¿Por qué `X_b` tiene 6 columnas si solo seleccionamos 5 características en la Parte 2?**

A) Porque se duplicó la columna `num_frames_total`. ❌  
B) Porque se agregó una columna de unos a la izquierda para representar el término constante $\beta_0$ (bias). ✅  
C) Porque incluye la columna del target `production_hours`. ❌  
D) Porque incluye la columna de nombres de los personajes. ❌  

---

## Sección 2 — Ejercicio 3.2: Regresión Lineal Simple desde Cero

---

### P10 [COMPLETAR] — Ejercicio 3.2
**Completa la función de álgebra lineal de NumPy para calcular la inversa de una matriz.**

```python
beta_simple = np.linalg.____(X_simple.T @ X_simple) @ X_simple.T @ y
```

Opciones: `inv` / `inverse` / `pinv` / `det`

✅ **Respuesta:** `inv`

---

### P11 [COMPLETAR] — Ejercicio 3.2
**Completa el operador matemático de Python para realizar multiplicación matricial (dot product) entre matrices y vectores.**

```python
y_pred_simple = X_simple ____ beta_simple
```

Opciones: `@` / `*` / `dot` / `**`

✅ **Respuesta:** `@`

---

### P12 [LÓGICA] — Ejercicio 3.2
**¿Cuáles son los valores calculados de $\beta_0$ (intercepto) y $\beta_1$ (pendiente) para la regresión simple sobre `num_frames_total`?**

A) $\beta_0 = 0.0000$ | $\beta_1 = 1.5000$ ❌  
B) $\beta_0 = 17.5948$ | $\beta_1 = 1.0094$ ✅  
C) $\beta_0 = -37.0913$ | $\beta_1 = 0.8580$ ❌  
D) $\beta_0 = 96.3200$ | $\beta_1 = 0.9782$ ❌  

---

### P13 [CONCEPTUAL] — Ejercicio 3.2
**¿Qué significa en términos prácticos de producción de animación una pendiente de $\beta_1 = 1.0094$?**

A) Que cada hora de trabajo produce 100 fotogramas. ❌  
B) Que por cada fotograma adicional requerido por el diseño del personaje, la carga estimada de producción aumenta en aproximadamente 1.01 horas de trabajo. ✅  
C) Que el modelo tiene un error del 1.01%. ❌  
D) Que todos los personajes tardan al menos 1 fotograma en dibujarse. ❌  

---

### P14 [LÓGICA] — Ejercicio 3.2
**Usando el modelo simple $\hat{y} = 17.5948 + 1.0094 \times x$, ¿cuántas horas de producción se pronostican para un personaje que requiere exactamente 120 fotogramas?**

A) 120.00 horas ❌  
B) 138.72 horas ✅  
C) 168.00 horas ❌  
D) 96.32 horas ❌  

---

### P15 [CONCEPTUAL] — Ejercicio 3.2
**¿Por qué un personaje hipotético con 0 fotogramas tendría un tiempo predicho de aproximadamente 17.59 horas ($\beta_0$)?**

A) Es un error matemático del modelo. ❌  
B) Refleja el costo fijo de preproducción: tiempo dedicado a explorar conceptos, diseñar la paleta de colores, elaborar model sheets y configurar rigs antes de animar. ✅  
C) Corresponde al tiempo de renderizado de la computadora. ❌  
D) Representa el tiempo de descanso obligatorio de los animadores. ❌  

---

## Sección 3 — Ejercicio 3.3: Métricas de Evaluación desde Cero

---

### P16 [COMPLETAR] — Ejercicio 3.3
**Completa la función de NumPy para calcular el valor absoluto de los residuos en el cálculo del MAE.**

```python
mae = np.mean(np.____(residuos))
```

Opciones: `abs` / `absolute` / `fabs` / `sqrt`

✅ **Respuesta:** `abs`

---

### P17 [COMPLETAR] — Ejercicio 3.3
**Completa la función para calcular la raíz cuadrada en el cálculo de RMSE.**

```python
rmse = np.____(np.mean(residuos**2))
```

Opciones: `sqrt` / `root` / `square_root` / `std`

✅ **Respuesta:** `sqrt`

---

### P18 [LÓGICA] — Ejercicio 3.3
**¿Cuáles son los valores calculados de MAE, RMSE y $R^2$ para el modelo de regresión lineal simple sobre todo el dataset?**

A) MAE: 17.39 h | RMSE: 23.42 h | $R^2$: 0.8580 ❌  
B) MAE: 8.47 h | RMSE: 10.30 h | $R^2$: 0.9569 ✅  
C) MAE: 3.45 h | RMSE: 4.41 h | $R^2$: 0.9929 ❌  
D) MAE: 5.00 h | RMSE: 5.00 h | $R^2$: 0.9000 ❌  

---

### P19 [CONCEPTUAL] — Ejercicio 3.3
**¿Qué representa un coeficiente de determinación $R^2 = 0.9569$?**

A) Que el modelo tiene un error de predicción del 95.69%. ❌  
B) Que el 95.69% de la variabilidad observada en las horas de producción es explicada por la cantidad total de fotogramas del personaje. ✅  
C) Que el 4.31% de los personajes tienen errores de dibujo. ❌  
D) Que la correlación entre fotogramas y horas es de 0.9569. ❌  

---

### P20 [CONCEPTUAL] — Ejercicio 3.3
**¿Por qué en este modelo (y generalmente en problemas de regresión) el RMSE ($10.30$ h) es mayor que el MAE ($8.47$ h)?**

A) Porque el RMSE incluye una corrección por grados de libertad. ❌  
B) Porque el RMSE eleva las diferencias al cuadrado antes de promediar, otorgando un peso desproporcionadamente mayor a errores grandes en personajes complejos (como Blaze). ✅  
C) Porque el MAE no mide distancias euclidianas. ❌  
D) Es una anomalía de este dataset en particular. ❌  

---

### P21 [LÓGICA] — Ejercicio 3.3
**Para el personaje `Lyra` (horas reales: 142.0 h, fotogramas: 120), si el modelo simple predice $\hat{y} = 138.72$ h, ¿cuál es su residuo $e = y - \hat{y}$?**

A) $-3.28$ horas (sobrestimado) ❌  
B) $+3.28$ horas (subestimado) ✅  
C) $+0.00$ horas (exacto) ❌  
D) $+14.20$ horas ❌  

---

## Sección 4 — Ejercicio 3.4: Regresión Múltiple con scikit-learn

---

### P22 [COMPLETAR] — Ejercicio 3.4
**Completa la función de scikit-learn para dividir los datos en conjunto de entrenamiento y conjunto de prueba.**

```python
from sklearn.model_selection import ____
```

Opciones: `train_test_split` / `cross_val_score` / `KFold` / `split_data`

✅ **Respuesta:** `train_test_split`

---

### P23 [COMPLETAR] — Ejercicio 3.4
**Completa el argumento para reservar el 20% de las muestras para evaluación.**

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=____, random_state=42)
```

Opciones: `0.20` / `0.80` / `20` / `0.50`

✅ **Respuesta:** `0.20`

---

### P24 [LÓGICA] — Ejercicio 3.4
**Al usar `test_size=0.20` sobre los 20 personajes, ¿cuántos registros se asignan a entrenamiento y cuántos a prueba?**

A) 10 en entrenamiento y 10 en prueba ❌  
B) 16 en entrenamiento y 4 en prueba ✅  
C) 18 en entrenamiento y 2 en prueba ❌  
D) 15 en entrenamiento y 5 en prueba ❌  

---

### P25 [LÓGICA] — Ejercicio 3.4
**¿Cuáles 4 personajes integran el conjunto de prueba obtenido con `random_state=42`?**

A) Seraph, Pip, Crux, Drak ❌  
B) Lyra, Olmo, Blaze, Kael ✅  
C) Zorn, Fenn, Vela, Asha ❌  
D) Thorn, Lune, Rex, Cleo ❌  

---

### P26 [COMPLETAR] — Ejercicio 3.4
**Completa el método para entrenar la instancia del modelo `LinearRegression` con los datos de entrenamiento.**

```python
model = LinearRegression()
model.____(X_train, y_train)
```

Opciones: `fit` / `train` / `learn` / `optimize`

✅ **Respuesta:** `fit`

---

### P27 [COMPLETAR] — Ejercicio 3.4
**Completa el método para generar pronósticos sobre datos nuevos con un modelo entrenado.**

```python
y_pred_test = model.____(X_test)
```

Opciones: `predict` / `forecast` / `transform` / `score`

✅ **Respuesta:** `predict`

---

### P28 [COMPLETAR] — Ejercicio 3.4
**Completa los atributos de scikit-learn para inspeccionar los coeficientes y el intercepto calculados.**

```python
print("Coeficientes:", model.____)
print("Intercepto  :", model.____)
```

Opciones: `coef_`, `intercept_` / `coefficients_`, `bias_` / `weights_`, `bias_` / `params_`, `intercept_`

✅ **Respuesta:** `coef_`, `intercept_`

---

### P29 [LÓGICA] — Ejercicio 3.4
**¿Cuál es el valor aproximado del coeficiente obtenido para la variable binaria `has_special_fx` en el modelo múltiple?**

A) $+0.8742$ ❌  
B) $+4.7547$ ✅  
C) $-37.0913$ ❌  
D) $+15.8923$ ❌  

---

### P30 [CONCEPTUAL] — Ejercicio 3.4
**¿Cómo se interpreta el coeficiente de `has_special_fx` ($+4.75$ horas) en el modelo múltiple?**

A) Que los efectos especiales causan un 4.75% de errores de animación. ❌  
B) Que manteniendo constantes las demás variables (fotogramas, estados, fps, ratio de pantalla), dotar a un personaje de efectos especiales complejos agrega en promedio 4.75 horas a su producción. ✅  
C) Que un personaje tarda al menos 4.75 horas en renderizar los efectos. ❌  
D) Que solo se pueden incluir 4 efectos especiales por escena. ❌  

---

## Sección 5 — Ejercicio 3.5: Evaluación y Comparación de Modelos

---

### P31 [COMPLETAR] — Ejercicio 3.5
**Completa las funciones importadas de `sklearn.metrics` para calcular las tres métricas.**

```python
from sklearn.metrics import ____, ____, ____
```

Opciones: `r2_score`, `mean_absolute_error`, `mean_squared_error` / `r2`, `mae`, `mse` / `score`, `abs_error`, `sq_error` / `accuracy_score`, `mae`, `rmse`

✅ **Respuesta:** `r2_score`, `mean_absolute_error`, `mean_squared_error`

---

### P32 [LÓGICA] — Ejercicio 3.5
**¿Cuáles son los valores de $R^2$, MAE y RMSE obtenidos para el modelo de regresión múltiple en el conjunto de prueba (Test)?**

A) $R^2 = 0.9929$ | MAE = 3.45 h | RMSE = 4.41 h ❌ (Conjunto de Entrenamiento)  
B) $R^2 = 0.8580$ | MAE = 17.39 h | RMSE = 23.42 h ✅ (Conjunto de Prueba)  
C) $R^2 = 0.5000$ | MAE = 25.00 h | RMSE = 30.00 h ❌  
D) $R^2 = 0.9569$ | MAE = 8.47 h | RMSE = 10.30 h ❌ (Modelo Simple)  

---

### P33 [CONCEPTUAL] — Ejercicio 3.5
**¿Por qué el $R^2$ en el conjunto de entrenamiento es $0.9929$ mientras que en el conjunto de prueba cae a $0.8580$?**

A) Porque el modelo se programó incorrectamente. ❌  
B) Es el fenómeno fundamental de Machine Learning: los parámetros del modelo se optimizaron exactamente sobre los datos de entrenamiento; al evaluar sobre datos no vistos, el error de generalización reduce el rendimiento. ✅  
C) Porque los datos de prueba tenían errores de captura. ❌  
D) Porque scikit-learn penaliza artificialmente los conjuntos de prueba pequeños. ❌  

---

### P34 [CONCEPTUAL] — Ejercicio 3.5
**¿Por qué un evaluador prudente no debe descalificar el modelo al ver un RMSE de $23.42$ h con solo $N=4$ muestras en prueba?**

A) Porque el RMSE siempre se ignora en producción. ❌  
B) Porque con 4 personajes, el héroe extremo `Blaze` (185 horas reales vs 148.9 predichas, error = 36.1 h) ejerce un apalancamiento desmedido al elevarse al cuadrado en la fórmula de RMSE. ✅  
C) Porque el conjunto de prueba no debe contener protagonistas. ❌  
D) Porque el MAE de 17.39 h indica que el modelo es perfecto. ❌  

---

## Sección 6 — Ejercicio 3.6: Gráfico Valor Real vs. Predicho

---

### P35 [CONCEPTUAL] — Ejercicio 3.6
**En un gráfico de dispersión Valor Real (eje X) vs. Valor Predicho (eje Y), ¿qué representa la línea diagonal de referencia $y = x$?**

A) El promedio del conjunto de datos. ❌  
B) La línea de predicción perfecta: cualquier punto situado sobre ella indica que el modelo predijo exactamente el valor real (residuo = 0). ✅  
C) La asíntota del error máximo permitido. ❌  
D) La frontera de decisión de una máquina de soporte vectorial. ❌  

---

### P36 [CONCEPTUAL] — Ejercicio 3.6
**Si un punto en el gráfico Real vs. Predicho se sitúa por debajo de la línea diagonal $y = x$, ¿qué significa?**

A) El modelo sobrestimó el tiempo de producción ($\hat{y} > y$). ❌  
B) El modelo subestimó el tiempo de producción ($\hat{y} < y$); el personaje tardó más horas en la realidad de lo pronosticado. ✅  
C) El personaje tiene datos nulos. ❌  
D) La observación debe ser eliminada por ser inválida. ❌  

---

### P37 [LÓGICA] — Ejercicio 3.6
**¿Para qué personaje del conjunto de prueba el modelo múltiple logró su predicción más exacta (menor error absoluto)?**

A) `Blaze` (Error: $-36.1$ h) ❌  
B) `Lyra` (Real: 142.0 h | Predicho: 144.5 h | Error: $+2.5$ h) ✅  
C) `Olmo` (Error: $+18.2$ h) ❌  
D) `Kael` (Error: $-12.8$ h) ❌  

---

### P38 [COMPLETAR] — Ejercicio 3.6
**Completa la función de Matplotlib para colocar etiquetas de texto junto a cada punto en un gráfico de dispersión.**

```python
plt.____(nombre, (x_pos, y_pos))
```

Opciones: `annotate` / `text` / `label` / `legend`

✅ **Respuesta:** `annotate`

---

## Sección 7 — Ejercicio 3.7: Análisis de Residuos

---

### P39 [COMPLETAR] — Ejercicio 3.7
**Completa la función de Matplotlib para trazar una línea de referencia horizontal en $y = 0$.**

```python
plt.____(y=0, color="black", linestyle="--")
```

Opciones: `axhline` / `hline` / `plot_h` / `line`

✅ **Respuesta:** `axhline`

---

### P40 [CONCEPTUAL] — Ejercicio 3.7
**¿Qué propiedad matemática se comprueba si los residuos se distribuyen en una banda horizontal aleatoria de dispersión constante a lo largo de todo el rango de predicciones?**

A) Multicolinealidad ❌  
B) Homocedasticidad (varianza constante del término de error) ✅  
C) Normalidad asintótica ❌  
D) No estacionariedad ❌  

---

### P41 [CONCEPTUAL] — Ejercicio 3.7
**¿Qué problema estructural indicaría si los residuos formaran un patrón en forma de U o curva clara en el gráfico de residuos?**

A) Que el modelo tiene sobreajuste severo. ❌  
B) Que existe una relación no lineal entre las variables que el modelo lineal no logra capturar (violación del supuesto de linealidad). ✅  
C) Que las etiquetas de los personajes están invertidas. ❌  
D) Que la tasa de aprendizaje fue demasiado alta. ❌  

---

## Sección 8 — Ejercicio 3.8: Inferencia para un Nuevo Personaje (Nova)

---

### P42 [LÓGICA] — Ejercicio 3.8
**¿Cuál es el pronóstico exacto de horas de producción generado por el modelo para el nuevo personaje `Nova`?**

A) 96.32 horas ❌  
B) 120.97 horas ✅  
C) 142.00 horas ❌  
D) 185.00 horas ❌  

---

### P43 [LÓGICA] — Ejercicio 3.8
**Considerando una jornada laboral estándar de estudio de 40 horas semanales por animador, ¿a cuántas semanas de trabajo a tiempo completo equivale la producción de Nova (120.97 h)?**

A) 1.5 semanas ❌  
B) Aproximadamente 3.0 semanas (3.02 semanas) ✅  
C) 5.2 semanas ❌  
D) Menos de una semana ❌  

---

### P44 [LÓGICA] — Ejercicio 3.8
**Mediante el análisis de sensibilidad en el notebook, ¿cuántas horas de producción se ahorraría el estudio si decide eliminar los efectos especiales de Nova (`has_special_fx = 0`)?**

A) 15.89 horas ❌  
B) 4.75 horas (exactamente el valor de $\beta_5$) ✅  
C) 24.00 horas ❌  
D) 0 horas ❌  

---

### P45 [CONCEPTUAL] — Ejercicio 3.8
**¿Por qué para hacer inferencia con `model.predict` es indispensable pasar los atributos en un array bidimensional con el mismo orden de columnas que en el entrenamiento?**

A) Porque de lo contrario scikit-learn genera números aleatorios sin avisar. ❌  
B) Porque el modelo multiplica vectorialmente cada columna por su coeficiente correspondiente según su posición posicional; alterar el orden asignaría erróneamente el coeficiente de fotogramas a la tasa de fps. ✅  
C) Porque los arrays unidimensionales solo son válidos para clasificación. ❌  
D) Es una limitación exclusiva del sistema operativo Windows. ❌  

---

## Sección 9 — Ejercicio 3.9: Síntesis Ejecutiva y Preguntas Integradoras

---

### P46 [SELECCIÓN] — Síntesis
**¿Cuál de las siguientes conclusiones sintetiza de forma más rigurosa los hallazgos de todo el pipeline (Partes 1, 2 y 3)?**

A) Las horas de producción dependen únicamente del estilo de color y la iluminación de los fondos. ❌  
B) `num_frames_total` es el predictor dominante de la carga de animación ($r = 0.978$), permitiendo que un modelo simple explique el $95.7\%$ de la varianza. El modelo múltiple afina la predicción incorporando el tiempo en pantalla, los estados y los efectos especiales ($R^2_{\\text{train}} = 0.993$). ✅  
C) La regresión lineal no es aplicable a problemas de diseño digital por la no linealidad de los gráficos vectoriales. ❌  
D) El modelo simple es preferible en todos los casos porque nunca puede sobreajustar. ❌  

---

### P47 [V/F] — Síntesis
**Si implementamos la Ecuación Normal manualmente con NumPy o usamos `LinearRegression` de scikit-learn sobre los mismos datos sin regularización, ambos métodos producen matemáticamente los mismos coeficientes e intercepto.**

✅ **Verdadero.** `LinearRegression` de scikit-learn utiliza internamente mínimos cuadrados basados en descomposición SVD/Ecuación Normal para resolver el mismo problema analítico de optimización.

---

### P48 [LÓGICA] — Síntesis
**En la serie *Neon Skies*, ¿cuál es el personaje más laborioso de todo el estudio según los datos reales?**

A) `Kael` (138.5 h) ❌  
B) `Seraph` (168.0 h) ❌  
C) `Blaze` (185.0 h, con 168 fotogramas y 7 estados) ✅  
D) `Asha` (155.0 h) ❌  

---

*Fin del Banco de Preguntas Moodle — Parte 3: Regresión Lineal desde Cero (INT210)*
