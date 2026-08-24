# Guía Curricular y Docente - Semana 4
## Unidad: Modelos Supervisados de Regresión y Regularización (Lasso, Ridge y ElasticNet)
**Duración Total:** 6 Horas (3 sesiones de 2 horas cada una; 1:30 hrs de enseñanza-aprendizaje activo y 0:30 hrs de taller interactivo/laboratorio).

---

## 1. Mapa de Alineación Curricular

| Sesión | Duración | Contenido Principal | Ejemplos Prácticos / Casos | Actividades de Aprendizaje Activo | Referencias Bibliográficas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **4.1** | 2 Horas | Regresión Lineal (Simple, Múltiple y Polinómica) e Inflación de Varianza (VIF). | Tiempos de compilación de código; Escenas 3D complejas. | Análisis interactivo de multicolinealidad. Ejercicio de rellenar código para transformaciones polinómicas. | Müller & Guido (Cap. 2), Grus (Cap. 14, 15), Sridhar (Cap. 4). |
| **4.2** | 2 Horas | Regularización de Atributos mediante Penalizaciones $L_1$ (Lasso), $L_2$ (Ridge) y ElasticNet. | Selección de texturas y atributos en renderizado; Predicción de latencia. | Taller de trazado de coeficientes frente a la fuerza de regularización ($\alpha$). Preguntas de diagnóstico matemático. | Müller & Guido (Cap. 2), Grus (Cap. 14), Sridhar (Cap. 4). |
| **4.3** | 2 Horas | Laboratorio Autónomo: Predicción de Rendimiento de Renderizado en GPU y Análisis de Negocio. | SGEMM GPU Kernel Performance Dataset (UCI). | Programación del flujo completo en Google Colab. Conversión de regresión a clasificación binaria y evaluación de Matriz de Confusión. | Janapati et al. (Cap. 3), Reis & Housley (Cap. 7 - Serving data). |

---

## 2. Sesión 4.1: Regresión Lineal y Diagnóstico de Errores (2 Horas)

### 2.1. Objetivos de Aprendizaje
*   Formalizar matemáticamente el estimador de Mínimos Cuadrados Ordinarios (OLS) mediante álgebra matricial.
*   Diagnosticar problemas de multicolinealidad utilizando el Factor de Inflación de Varianza (VIF).
*   Implementar e interpretar expansiones polinómicas en variables predictoras continuas.

---

### 2.2. Introducción Pedagógica: Enfoque "Para Niños" (10 años)

> **La Analogía del Cordel Elástico y las Montañas Rusas**
> 
> **1. Regresión Lineal (El Cordel Elástico y las Tachuelas Mágicas):**
> Imagina que tienes una gran tabla de madera y has clavado varias tachuelas de colores en diferentes lugares. Tu objetivo es colocar un cordel elástico que pase lo más cerca posible de todas las tachuelas a la vez. El cordel es súper lacio y no se puede doblar; tiene que ser una línea completamente recta. 
> 
> Si jalas el cordel hacia arriba para acercarlo a una tachuela alta, se alejará de una tachuela baja. La computadora hace exactamente esto: busca la posición perfecta del cordel donde la tensión (la distancia total al cuadrado de todas las tachuelas) sea la más pequeña posible. Esa línea recta te permite predecir dónde se clavará la siguiente tachuela.
> 
> **2. Regresión Polinómica (Diseñar la Montaña Rusa):**
> ¿Qué pasa si las tachuelas en la tabla de madera no están alineadas, sino que forman una hermosa curva de subidas y bajadas como una montaña rusa? Si intentas poner un cordel rígido y recto, va a quedar lejísimos de la mayoría de las tachuelas. 
> 
> Para solucionar esto, le inyectamos una "poción mágica" a nuestro cordel que le permite doblarse de forma flexible. Ahora, el cordel puede subir, hacer una curva suave y bajar para tocar casi todas las tachuelas. En matemáticas, permitir que el cordel se doble de esta manera se llama "regresión polinómica". Pero ¡cuidado! Si le damos demasiada flexibilidad, el cordel dará vueltas de forma caótica y se volverá loco, lo que arruinará el diseño de nuestra montaña rusa.

---

### 2.3. Rigor Universitario y Formalización Matemática

En el modelado predictivo de variables continuas, el estimador de **Mínimos Cuadrados Ordinarios (OLS)** asume una relación lineal entre un conjunto de variables independientes y una variable respuesta continuada.

#### Representación Matricial
Dado un conjunto de entrenamiento representado por la matriz de diseño $\mathbf{X} \in \mathbb{R}^{n \times (d+1)}$ (donde la primera columna está rellena de unos para representar el término de intercepto o sesgo) y un vector de etiquetas $\mathbf{y} \in \mathbb{R}^n$, el modelo lineal se define como:

$$\mathbf{y} = \mathbf{X}\mathbf{w} + \boldsymbol{\epsilon}$$

Donde $\mathbf{w} \in \mathbb{R}^{d+1}$ es el vector de coeficientes de peso y $\boldsymbol{\epsilon} \in \mathbb{R}^n$ es el vector de perturbaciones aleatorias (errores).

La función de pérdida que se busca minimizar es la **Suma de Residuos al Cuadrado (RSS)**:

$$\text{RSS}(\mathbf{w}) = \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 = (\mathbf{y} - \mathbf{X}\mathbf{w})^T(\mathbf{y} - \mathbf{X}\mathbf{w})$$

Para encontrar el mínimo global, derivamos con respecto a $\mathbf{w}$ e igualamos a cero:

$$\frac{\partial \text{RSS}(\mathbf{w})}{\partial \mathbf{w}} = -2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\mathbf{w} = 0$$

$$\mathbf{X}^T\mathbf{X}\mathbf{w} = \mathbf{X}^T\mathbf{y}$$

Asumiendo que la matriz $\mathbf{X}^T\mathbf{X}$ es de rango completo (no singular) y por ende invertible, la solución analítica única (Ecuaciones Normales) es:

$$\hat{\mathbf{w}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

#### Diagnóstico de Multicolinealidad: Factor de Inflación de Varianza (VIF)
Cuando existen variables fuertemente correlacionadas en la matriz de diseño, la matriz $\mathbf{X}^T\mathbf{X}$ se aproxima a la singularidad, lo que infla drásticamente la varianza de los coeficientes estimados y destruye la interpretabilidad del modelo. Para diagnosticar esto, calculamos el **VIF** para cada característica $i$:

$$\text{VIF}_i = \frac{1}{1 - R_i^2}$$

Donde $R_i^2$ es el coeficiente de determinación obtenido al regresar la característica $X_i$ contra todas las demás características independientes del dataset. Un $\text{VIF}_i > 5$ indica problemas moderados de multicolinealidad, mientras que un $\text{VIF}_i > 10$ señala una severa redundancia de información que requiere remediación inmediata (como eliminación o regularización).

---

### 2.4. Interacción en el Aula: Preguntas de Interpretación y Completado de Código

El profesor proyectará las siguientes diapositivas y seleccionará a estudiantes para completar el código directamente en la pizarra o explicar la salida técnica.

#### Pregunta 1: Completar la Transformación Polinómica
**Instrucción:** El siguiente código tiene como objetivo transformar un dataset de una sola característica independiente en una representación polinómica de tercer grado utilizando scikit-learn. Completa los espacios vacíos marcado con `### TU CÓDIGO AQUÍ ###`.

```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures

# Datos de entrada: FPS promedio de un motor de videojuegos
fps_data = np.array([[30], [45], [60], [90]])

# 1. Instanciar el transformador para grado 3 sin incluir la columna de sesgo (bias)
transformer = PolynomialFeatures(degree=3, include_bias=False)

# 2. Ajustar y transformar los datos de entrada
features_poly = transformer.fit_transform(fps_data)

print("Matriz transformada:\n", features_poly)
```

**Preguntas de discusión interactiva para la clase:**
1. Al desactivar `include_bias=False`, ¿qué columna matemática estándar eliminamos de la matriz final y por qué es una buena práctica delegarle esto directamente al estimador de regresión (`LinearRegression(fit_intercept=True)`)?
2. Si la entrada original tiene una dimensión $d=2$, ¿cuántas columnas tendrá la matriz resultante si aplicamos un grado polinómico de $degree=2$? *Fórmula de combinación con repetición:* $\frac{(d+g)!}{d!g!} - 1$.

#### Pregunta 2: Interpretación Diagnóstica del VIF
**Instrucción:** Se ha ejecutado el cálculo del VIF en un modelo que intenta predecir el retraso de fotogramas (*frame-drop*) en una animación 3D compleja en función de tres variables físicas:
1. `resolucion_ancho`: Resolución horizontal de la pantalla (píxeles).
2. `resolucion_alto`: Resolución vertical de la pantalla (píxeles).
3. `cantidad_poligonos`: Complejidad del modelo 3D (triángulos).

El script arroja la siguiente salida en consola:

```text
Atributo            | VIF
---------------------------
resolucion_ancho    | 18.45
resolucion_alto     | 19.12
cantidad_poligonos  | 1.24
```

**Preguntas para discusión abierta:**
*   ¿Qué problema matemático de multicolinealidad se evidencia aquí?
*   ¿Por qué `resolucion_ancho` y `resolucion_alto` tienen coeficientes VIF tan destructivos?
*   Si fueras el Lead Data Scientist de este proyecto, ¿qué acción tomarías sobre estas variables para corregir la inestabilidad de la matriz normal de mínimos cuadrados sin perder el poder explicativo de la resolución?

---

## 3. Sesión 4.2: Regularización de Modelos (2 Horas)

### 3.1. Objetivos de Aprendizaje
*   Identificar matemáticamente la diferencia entre las penalizaciones de norma $L_1$ (Lasso) y norma $L_2$ (Ridge).
*   Comprender la formulación de ElasticNet como un puente de regularización híbrida.
*   Interpretar curvas de encogimiento de coeficientes para la selección automática de características críticas.

---

### 3.2. Introducción Pedagógica: Enfoque "Para Niños" (10 años)

> **La Mochila de Campamento y los Inspectores de Peso**
> 
> Imagina que vas a ir de campamento a una montaña lejana y tienes una mochila enorme. Quieres empacar de todo: una linterna, 10 peluches, 5 libros pesados, una brújula, sartenes de cocina y hasta una televisión portátil. Tu mochila representa todas las características (las columnas) que quieres meter en tu modelo de Inteligencia Artificial para hacer predicciones.
> 
> Pero antes de salir, hay un **Inspector de Peso** muy estricto en la puerta de tu casa. El inspector sabe que si llevas demasiado peso innecesario, te cansarás a mitad del camino y no lograrás subir la montaña (esto en Machine Learning se llama sobreajuste u *overfitting*). El inspector penaliza el peso excesivo, obligándote a reducir lo que llevas en la mochila.
> 
> Existen dos tipos de inspectores con diferentes reglas:
> 
> *   **El Inspector Estricto "Lasso" (Penalización $L_1$):**
>     Este inspector odia las cosas que no son indispensables. Te mira fijamente y te dice: *"O llevas la brújula o llevas el mapa, pero no ambos. Y esos 10 peluches se quedan en la basura"*. Lasso aplica una penalización tan severa que obliga a que el peso de los objetos inútiles sea **exactamente cero**. Al final, te obliga a dejar casi todo en casa, permitiéndote llevar únicamente los objetos de supervivencia cruciales. ¡Lasso limpia tu mochila de inmediato!
> 
> *   **El Inspector Amable "Ridge" (Penalización $L_2$):**
>     Este inspector es más comprensivo, pero muy precavido. Él no quiere tirar tus peluches a la basura, pero tampoco quiere que cargues demasiado peso. Así que te dice: *"Puedes llevar todo lo que quieras, pero tienes que encoger el tamaño de todas las cosas. Cambia tu sartén de hierro gigante por una miniatura de juguete, y en lugar de tus libros gigantes, lleva micro-libros del tamaño de un borrador"*. Ridge reduce el peso de todos los objetos por igual, haciendo que pesen **muy poquito**, pero **nunca elimina por completo ningún objeto de tu mochila**.
> 
> Si no sabes cuál de los dos inspectores es el mejor para tu viaje, puedes llamar a **ElasticNet**, que es un inspector sabio que combina un poco del Inspector Lasso y un poco del Inspector Ridge para balancear la mochila de manera perfecta.

---

### 3.3. Rigor Universitario y Formalización Matemática

Para contrarrestar el sobreajuste y la inestabilidad matricial de los mínimos cuadrados ordinarios, se introduce un término de penalización sobre el vector de parámetros $\mathbf{w}$ en la función de costo del optimizador.

```
                    Visualización de Contornos de Penalización
                    
         Norma L1 (Lasso)                       Norma L2 (Ridge)
              w2                                     w2
              ^                                      ^
              |                                      |
            / | \      <-- Contorno                .---.
          /   |   \    de Lasso                   /     \    <-- Contorno
        /     |     \    (Rombo)                 |   o   |   de Ridge
<-------------+-------------> w1         <-------|---+---|-------> w1
        \     |     /                             \     /    (Círculo)
          \   |   /                                '---'
            \ | /                                    |
              v                                      v
```

#### Regresión Ridge (Tikhonov Regularization - Penalización $L_2$)
Ridge añade una penalización proporcional a la norma de Frobenius al cuadrado (norma $L_2$) del vector de coeficientes, excluyendo el intercepto $w_0$:

$$\text{Loss}_{\text{Ridge}}(\mathbf{w}) = \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \alpha \|\mathbf{w}\|_2^2 = \frac{1}{2n} \sum_{i=1}^n \left( y_i - \mathbf{x}_i^T\mathbf{w} \right)^2 + \alpha \sum_{j=1}^d w_j^2$$

Donde $\alpha \ge 0$ es un hiperparámetro de sintonización que controla la fuerza de la penalización.
Derivando analíticamente la función de costo de Ridge, obtenemos una solución de forma cerrada garantizada:

$$\hat{\mathbf{w}}_{\text{Ridge}} = \left( \mathbf{X}^T\mathbf{X} + \lambda \mathbf{I} \right)^{-1} \mathbf{X}^T\mathbf{y}$$

Donde $\lambda = 2n\alpha$ e $\mathbf{I}$ es la matriz identidad. Al sumar una constante a la diagonal principal, $\mathbf{X}^T\mathbf{X} + \lambda \mathbf{I}$ se vuelve estrictamente invertible incluso si $\mathbf{X}^T\mathbf{X}$ tiene columnas linealmente dependientes, solucionando por completo el problema de singularidad.

#### Regresión Lasso (Least Absolute Shrinkage and Selection Operator - Penalización $L_1$)
Lasso penaliza la norma absoluta $L_1$ de los coeficientes:

$$\text{Loss}_{\text{Lasso}}(\mathbf{w}) = \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \alpha \|\mathbf{w}\|_1 = \frac{1}{2n} \sum_{i=1}^n \left( y_i - \mathbf{x}_i^T\mathbf{w} \right)^2 + \alpha \sum_{j=1}^d |w_j|$$

Dado que la función de costo no es diferenciable en $w_j = 0$ debido al valor absoluto, no existe una solución analítica cerrada. Se resuelve numéricamente utilizando algoritmos como el **Descenso de Coordenadas Cíclicas**. 

**Propiedad de Selección de Características:** Geométricamente, los contornos de la penalización $L_1$ forman un polítopo (un rombo en 2D) con esquinas afiladas sobre los ejes coordenados. La elipse de la suma de residuos suele intersecar la restricción en una de estas esquinas, forzando a que algunos coeficientes $w_j$ sean **exactamente cero**, lo que elimina por completo características redundantes o ruidosas de la formulación del modelo.

#### ElasticNet (Regularización Híbrida)
ElasticNet combina de forma balanceada ambas penalizaciones mediante un factor de ponderación $r$ (`l1_ratio`):

$$\text{Loss}_{\text{ElasticNet}}(\mathbf{w}) = \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \alpha \cdot r \cdot \|\mathbf{w}\|_1 + \frac{\alpha (1 - r)}{2} \|\mathbf{w}\|_2^2$$

Donde $r \in [0, 1]$. Si $r=1$, equivale a Lasso; si $r=0$, equivale a Ridge. Esta técnica es extremadamente robusta cuando existen grupos de variables altamente correlacionadas (efecto de agrupamiento o *grouping effect*), donde Lasso tiende a seleccionar solo una de ellas al azar, mientras que ElasticNet las conserva y encoge de manera conjunta en el modelo predictivo.

---

### 3.4. Interacción en el Aula: Diagnóstico de Coeficientes

El profesor proyectará la siguiente gráfica clásica de encogimiento de coeficientes (Path de Coeficientes de Lasso) para discusión grupal:

```text
Coeficiente (Valor de W)
  ^
1.0 |=========\   Feature A (Resolución Pantalla)
    |          \========--------------------
0.5 |-------\               Feature B (Número de Polígonos)
    |        \------------------------------
0.0 |................................\......  Feature C (Color de la GPU - Ruido)
    +-----------------------------------------> Fuerza de Regularización (Alpha)
    0.001     0.01      0.1       1.0
```

**Preguntas de análisis de código e interpretación para los estudiantes:**
1. A medida que incrementamos el hiperparámetro `alpha` ($\alpha$) de `0.001` a `1.0`, ¿cuál es la primera variable independiente cuyo coeficiente es forzado a cero por el algoritmo? ¿Qué nos indica esto respecto a su relevancia predictiva?
2. Si el dataset original tuviera 100 variables altamente correlacionadas (multicolinealidad extrema), ¿por qué usar `Lasso(alpha=0.5)` podría generar una pérdida masiva de información en comparación con `Ridge(alpha=0.5)`? Justifica basándote en la geometría de los contornos de optimización.

---

## 4. Sesión 4.3: Laboratorio Autónomo y Desafío (2 Horas)

### 4.1. Dataset Real de Referencia
*   **Dataset:** **SGEMM GPU Kernel Performance Dataset**
*   **Origen:** UCI Machine Learning Repository / Kaggle
*   **Descripción Académica:** Registra los tiempos de ejecución de un kernel de multiplicación de matrices (SGEMM) sobre una GPU moderna bajo diversas combinaciones de configuración física de hilos y memoria.
*   **Variable Objetivo:** `Run_Time_Sec` (Tiempo total de renderizado/cálculo de la escena en segundos).

---

### 4.2. Diccionario de Datos y Análisis Exploratorio (Pandas Queries)

El estudiante debe ejecutar las siguientes consultas de Pandas para diagnosticar y entender el comportamiento de la matriz de características antes de instanciar los modelos en scikit-learn.

```python
import pandas as pd

# Supongamos que cargamos el dataset real
# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00440/sgemm_product.zip"
# df = pd.read_csv(url)

# Para efectos de la práctica, los estudiantes trabajan sobre la variable promedio de rendimiento:
# df['Run_Time_Sec'] = df[['Run1 (ms)', 'Run2 (ms)', 'Run3 (ms)', 'Run4 (ms)']].mean(axis=1) / 1000.0

# CONSULTA 1: Identificación de correlaciones fuertes que causen multicolinealidad
correlation_matrix = df.corr()
high_corr = correlation_matrix[abs(correlation_matrix['Run_Time_Sec']) > 0.4]['Run_Time_Sec']
print("Atributos con alta correlación lineal directa con el tiempo de renderizado:\n", high_corr)

# CONSULTA 2: Filtrado personalizado para identificar configuraciones ineficientes en GPU
# Queremos ver qué configuraciones de memoria cache (atrib: 'MWG', 'NWG') generan renderizados extremadamente lentos (> 50 segundos)
slow_renders_query = df.query("MWG > 64 and NWG > 64 and Run_Time_Sec > 50.0")
print(f"Muestras de alta latencia con parámetros de memoria sobredimensionados: {len(slow_renders_query)}")
```

---

### 4.3. Implementación de Código Multimodelo

**Desafío Práctico:** El estudiante escribirá el flujo completo para preprocesar los datos, dividir el conjunto (80% Train, 20% Test), realizar una expansión polinómica de grado 2 y comparar un estimador lineal clásico sobreajustado frente a modelos regularizados Lasso y Ridge utilizando validación cruzada.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.metrics import mean_squared_error, r2_score

# 1. Carga de datos real (Sub-dataset simulado de ejemplo para que compile)
np.random.seed(42)
n_samples = 1000
data = {
    'MWG': np.random.choice([16, 32, 64, 128], n_samples),
    'NWG': np.random.choice([16, 32, 64, 128], n_samples),
    'KWG': np.random.choice([16, 32], n_samples),
    'MDIMC': np.random.choice([8, 16, 32], n_samples),
    'NDIMC': np.random.choice([8, 16, 32], n_samples),
    'Run_Time_Sec': np.random.exponential(scale=20.0, size=n_samples) # Distribución de tiempo real
}
df = pd.DataFrame(data)

# Preprocesamiento: Separar variables y escalar
X = df.drop(columns=['Run_Time_Sec'])
y = df['Run_Time_Sec']

# Expansión Polinómica para inducir Overfitting controlado
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Partición del dataset
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Escalado estándar (Obligatorio para regularización equilibrada de coeficientes)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# MODELO 1: Regresión Lineal Clásica (OLS sobreajustada en espacio polinómico)
model_ols = LinearRegression()
model_ols.fit(X_train_scaled, y_train)
preds_ols = model_ols.predict(X_test_scaled)

# MODELO 2: Lasso con búsqueda interna óptima de Alpha mediante validación cruzada (L1)
model_lasso = LassoCV(alphas=np.logspace(-4, 2, 100), cv=5, max_iter=10000)
model_lasso.fit(X_train_scaled, y_train)
preds_lasso = model_lasso.predict(X_test_scaled)

# MODELO 3: Ridge con búsqueda interna óptima de Alpha mediante validación cruzada (L2)
model_ridge = RidgeCV(alphas=np.logspace(-4, 2, 100), cv=5)
model_ridge.fit(X_train_scaled, y_train)
preds_ridge = model_ridge.predict(X_test_scaled)

# Métricas de Evaluación
print(f"--- EVALUACIÓN DE MODELOS (Métricas de Regresión) ---")
print(f"OLS   -> MSE: {mean_squared_error(y_test, preds_ols):.4f} | R2: {r2_score(y_test, preds_ols):.4f}")
print(f"Lasso -> MSE: {mean_squared_error(y_test, preds_lasso):.4f} | R2: {r2_score(y_test, preds_lasso):.4f} | Alpha Óptimo: {model_lasso.alpha_:.4f}")
print(f"Ridge -> MSE: {mean_squared_error(y_test, preds_ridge):.4f} | R2: {r2_score(y_test, preds_ridge):.4f} | Alpha Óptimo: {model_ridge.alpha_:.4f}")
```

---

### 4.4. Defensa Analítica con Matriz de Confusión de Negocio

A pesar de ser un problema de regresión (predicción de un valor numérico continuo), el director del estudio de animación digital impone una restricción de negocio muy severa:

> *"Un fotograma no puede exceder bajo ninguna circunstancia los **30 segundos** de cálculo. Si un fotograma supera ese tiempo, bloqueará la granja de renderizado y causará retrasos masivos en las entregas, costándole miles de dólares al estudio."*

El estudiante debe transformar los valores reales de validación (`y_test`) y las predicciones continuas de los modelos (`preds_ols`, `preds_lasso`, `preds_ridge`) en categorías binarias mediante un operador de umbral lógico:

$$\text{Clase}(y) = \begin{cases} 
1 \quad (\text{"Alerta / Render Lento"}) & \text{si } y > 30 \\ 
0 \quad (\text{"Operación Normal"}) & \text{si } y \le 30 
\end{cases}$$

#### Taller de Construcción de Matriz de Confusión
Utilizando esta clasificación binaria derivada de la regresión, el estudiante graficará y analizará detalladamente la matriz de confusión resultante de sus modelos y deberá redactar un informe ejecutivo defendiendo su elección técnica:

```text
                       MATRIZ DE CONFUSIÓN BINARIA
                       
                       Predicción del Modelo
                      |   Negativo (<=30s)   |   Positivo (>30s)   |
  Real  Negativo      |  Verdadero Negativo  |   Falso Positivo    |
        (<=30s)       |        (VN)          |        (FP)         |
----------------------+----------------------+----------------------+
  Real  Positivo      |    Falso Negativo    |  Verdadero Positivo  |
        (>30s)        |        (FN)          |        (VP)         |
```

##### Guía de Interpretación de Extremos para Defensa de Negocio:
1.  **Verdaderos Positivos (VP):** El modelo predice que el renderizado tardará más de 30 segundos y efectivamente ocurre. *Impacto en el negocio:* Excelente. La GPU asigna preventivamente recursos de renderizado distribuidos o disminuye el muestreo de texturas para evitar el bloqueo del pipeline.
2.  **Verdaderos Negativos (VN):** El modelo predice que el renderizado tardará menos de 30 segundos y el cálculo termina de forma rápida. *Impacto en el negocio:* Flujo de trabajo óptimo y balanceado.
3.  **Falsos Positivos (FP):** El modelo genera una falsa alarma, prediciendo que el renderizado tardará demasiado cuando en realidad iba a terminar rápido. *Impacto en el negocio:* Se asignan servidores de respaldo innecesarios o se reduce la calidad visual del modelado de forma innecesaria, perdiendo fidelidad artística. Es un costo económico menor.
4.  **Falsos Negativos (FN):** El modelo predice que la escena se renderizará de forma rápida (menor a 30 segundos), pero en realidad la GPU se satura y tarda 2 minutos en renderizar el fotograma. *Impacto en el negocio:* **Catastrófico.** El sistema de distribución no previene el bloqueo, la cola de renderizado se congela en cascada y se rompe el acuerdo de nivel de servicio (SLA) de entregas del cliente final.

**Pregunta de Defensa Analítica para el Estudiante:**
*   *"Basándote en los tres modelos implementados (OLS, Lasso, Ridge), calcula la tasa de Falsos Negativos para cada uno. Justifica técnicamente cuál de los modelos regularizados utilizarías para la producción del motor de renderizado sabiendo que tu prioridad número uno es minimizar la probabilidad de Falsos Negativos."*

---

## 5. Tarea para la Casa (Moodle Homework Assignment)

### Proyecto Independiente: Análisis Multivariante de Tráfico de Red con ElasticNet en Google Colab
*   **Contexto de Ciberseguridad:** Los ataques distribuidos de denegación de servicio (DDoS) se caracterizan por ráfagas inusuales de peticiones sobre puertos específicos, saturando la latencia del servidor.
*   **Objetivo de la Actividad:** El estudiante investigará de manera autónoma el hiperparámetro `l1_ratio` de ElasticNet. Utilizará un dataset real de ciberseguridad (ej., registros de tráfico de red legítimo vs. anómalo de Kaggle) para entrenar un modelo que prediga la latencia del servidor (en milisegundos).
*   **Requerimientos de Entrega:**
    1.  Cargar y limpiar el dataset utilizando Pandas (filtrado de nulos e imputación estadística robusta).
    2.  Probar tres valores diferentes de `l1_ratio` (0.2, 0.5, 0.8) y documentar cómo varía el número de variables explicativas supervivientes a la regularización.
    3.  Exportar los coeficientes del modelo final a un DataFrame y graficar los 10 atributos de tráfico de red más determinantes en la predicción de la latencia.
    4.  Subir el notebook de Google Colab a la plataforma Moodle con el comando documentado primero y la explicación técnica detallada línea por línea abajo.

---

## 6. Moodle Quiz formativo (Formato Aiken)

```text
¿Qué diferencia fundamental existe entre la penalización matemática aplicada por Lasso en contraste con Ridge?
A. Ridge eleva los coeficientes al cubo y Lasso utiliza raíces cuadradas.
B. Lasso utiliza la norma absoluta L1 permitiendo forzar coeficientes exactamente a cero, mientras que Ridge utiliza la norma L2 reduciéndolos sin llegar a cero.
C. Ridge realiza una selección drástica de variables descartando la mayoría y Lasso las conserva todas.
D. Lasso solo puede aplicarse en problemas de clasificación multiclase y Ridge en regresiones simples.
ANS: B

¿Para qué sirve calcular el Factor de Inflación de Varianza (VIF) antes de entrenar un estimador lineal de Mínimos Cuadrados?
A. Para predecir el coeficiente de determinación del modelo en el conjunto de prueba.
B. Para evaluar la velocidad computacional del algoritmo medido en notación Big-O.
C. Para diagnosticar problemas de multicolinealidad o correlaciones severas entre las variables independientes.
D. Para forzar de forma inmediata que la varianza de los residuos sea igual a cero.
ANS: C

Si un estudiante de animación gráfica busca minimizar los Falsos Negativos al predecir si un renderizado tardará más del límite óptimo de 30 segundos, ¿cuál de los siguientes casos debe evitar a toda costa?
A. El modelo predice que tardará 10 segundos, pero en la realidad el proceso de cálculo de la GPU se congela y tarda 80 segundos.
B. El modelo predice que tardará 90 segundos y efectivamente la GPU requiere 120 segundos para renderizar el cuadro.
C. El modelo genera una falsa alarma estimando que el cálculo tardará 60 segundos, pero termina de forma exitosa en 15 segundos.
D. El modelo estima de forma exacta que el renderizado tardará 5 segundos y se ejecuta en ese tiempo.
ANS: A

¿Qué efecto ocurre en una Regresión Lasso si incrementamos drásticamente el valor del hiperparámetro de regularización Alpha (a -> infinito)?
A. El modelo se vuelve idéntico a una regresión polinómica sobreajustada.
B. El sesgo del modelo se reduce a cero optimizando la precisión general.
C. Todos los coeficientes de peso asociados a las variables independientes son forzados a cero, dejando solo el intercepto.
D. La matriz normal de diseño se vuelve singular e imposible de invertir numéricamente.
ANS: C

¿En qué escenario se desempeña mejor una regularización híbrida ElasticNet en comparación con una regresión Lasso pura?
A. Cuando el conjunto de datos de entrenamiento no posee variables numéricas continuas y solo contiene datos categóricos.
B. Cuando existen grupos de variables predictoras altamente correlacionadas entre sí, donde Lasso tiende a seleccionar solo una de ellas de forma arbitraria.
C. Únicamente cuando la cantidad de observaciones en el dataset es infinitamente más pequeña que el número de características.
D. Cuando se desea forzar a que el intercepto de la ecuación lineal resultante pase obligatoriamente por el origen de coordenadas.
ANS: B
```

---

## 7. Bibliografía Grounded en las Fuentes

*   **Grus, J. (2019).** *Data Science from Scratch: First Principles with Python*. 2nd Edition. O'Reilly Media. (Capítulo 14: Simple Linear Regression; Capítulo 15: Multiple Regression, regularización y penalizaciones).
*   **Müller, A. C., & Guido, S. (2017).** *Introduction to Machine Learning with Python: A Guide for Data Scientists*. O'Reilly Media. (Capítulo 2: Supervised Learning - Linear Models para clasificación y regresión, Ridge y Lasso).
*   **Sridhar, S. (2018).** *Machine Learning*. Oxford University Press. (Capítulo 4: Linear Regression, minimización de gradiente, regularización, expansión polinómica y diagnóstico de sobredimensión dimensional).
*   **Reis, J., & Housley, M. (2022).** *Fundamentals of Data Engineering: Plan and Build Robust Data Systems*. O'Reilly Media. (Capítulo 7: Ingestion and Serving layer, modelado para consumo continuo).
