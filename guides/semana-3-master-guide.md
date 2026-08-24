# Guía de Diseño Curricular y Documento Maestro: Semana 3
## Curso: Machine Learning aplicado a la Ciberseguridad y el Diseño/Animación Digital
### Unidad Temática: Modelos Supervisados de Clasificación Clásica (k-NN y Regresión Logística)

---

## Estructura General de la Semana 3 (6 Horas Totales)
Esta semana se divide en tres sesiones estructuradas de **2 horas cada una**. Cada sesión dedica **1 hora y 30 minutos (90 minutos) a la enseñanza y aprendizaje activo** (teoría interactiva, resolución guiada de código y defensa analítica), dejando los **30 minutos restantes para la configuración de entornos, resolución autónoma de bugs y retroalimentación personalizada**.

*   **Sesión 3.1 (2 Horas / 1h 30m de enseñanza activa):** Fundamentos Teóricos de k-NN y Regresión Logística.
*   **Sesión 3.2 (2 Horas / 1h 30m de enseñanza activa):** Laboratorio Guiado en Google Colab: Exploración con Pandas de un Dataset Real de Phishing.
*   **Sesión 3.3 (2 Horas / 1h 30m de enseñanza activa):** Laboratorio Autónomo, Evaluación Multimodelo, Defensa de la Matriz de Confusión y Quiz de Moodle.

---

## Sesión 3.1: Fundamentos Teóricos de k-NN y Regresión Logística (2 Horas)
*   **Distribución del Tiempo:** 90 minutos de clase magistral interactiva y formulación matemática. 30 minutos de debate sobre dilemas éticos y analogías cotidianas.

### 1. La Analogía "Para Niños" (10 años)

#### A. k-Vecinos Más Cercanos (k-NN): "Dime con quién andas y te diré quién eres"
> Imagina que te mudas a un nuevo vecindario y quieres saber si a los niños de la calle les gusta jugar videojuegos o jugar fútbol. No los conoces, así que decides observar a los **3 vecinos más cercanos** a tu casa ($k = 3$). 
> * Si observas que 2 de esos vecinos juegan al fútbol por las tardes y solo 1 juega videojuegos, tú asumes que en esa zona del vecindario lo más popular es jugar al fútbol. ¡Ganó la mayoría!
> * Si en lugar de 3 vecinos miras a los **5 más cercanos** ($k = 5$), y descubres que 4 juegan videojuegos y 1 juega fútbol, tu predicción cambia a videojuegos. 
> En Machine Learning, el algoritmo **k-NN** clasifica un dato nuevo simplemente mirando de qué color o tipo son sus vecinos más cercanos en el mapa de datos.

#### B. Regresión Logística: "La rampa clasificadora de pelotas"
> Imagina un tobogán de madera que tiene una forma de "S" muy suave. En el suelo hay dos cajas: la caja de la izquierda (el número **0**, que representa correos buenos de tus amigos) y la caja de la derecha (el número **1**, que representa correos malos o Spam con virus). 
> Cuando lanzas una pelota por el tobogán, la altura o el empuje que le das representa qué tan sospechoso es el correo (por ejemplo, si tiene faltas de ortografía o pide dinero). 
> * Si la pelota es muy pesada o sospechosa, el tobogán la desliza suavemente hacia la derecha, dándote un **99% de probabilidad** de que caiga en la caja de Spam (1).
> * Si la pelota es ligera y normal, resbala hacia la izquierda, dándote un **5% de probabilidad** de Spam, por lo que cae en la caja de correos buenos (0).
> La Regresión Logística es como este tobogán en forma de "S" (llamado curva sigmoide) que toma cualquier sospecha y la convierte en una probabilidad suave entre 0% y 100%.

---

### 2. Rigor Académico y Formalización Matemática

#### A. Espacio Mapeado y Algoritmo k-NN
Dado un conjunto de entrenamiento conteniendo $n$ muestras $\mathcal{D} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \dots, (\mathbf{x}_n, y_n)\}$, donde cada vector de características $\mathbf{x}_i \in \mathbb{R}^d$ representa los atributos normalizados de un sitio web, y la etiqueta de clase $y_i \in \{0, 1\}$ (0 para legítimo, 1 para Phishing).

Para clasificar una nueva muestra de prueba $\mathbf{x}$, el algoritmo k-NN identifica las $k$ muestras más cercanas en el espacio métrico $\mathbb{R}^d$ utilizando una función de distancia.

1. **Distancia Euclídea ($L_2$ Norm):**
   $$d(\mathbf{x}, \mathbf{x}_i) = \|\mathbf{x} - \mathbf{x}_i\|_2 = \sqrt{\sum_{j=1}^{d} (x^{(j)} - x_i^{(j)})^2}$$

2. **Distancia de Manhattan ($L_1$ Norm):**
   $$d(\mathbf{x}, \mathbf{x}_i) = \|\mathbf{x} - \mathbf{x}_i\|_1 = \sum_{j=1}^{d} |x^{(j)} - x_i^{(j)}|$$

Una vez identificados los $k$ vecinos más cercanos indexados en el conjunto de índices $\mathcal{N}_k(\mathbf{x})$, la probabilidad condicional de pertenecer a la clase $c \in \{0, 1\}$ se calcula como la fracción de votos:
$$P(y = c \mid \mathbf{x}) = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x})} \mathbb{I}(y_i = c)$$
Donde $\mathbb{I}(\cdot)$ es la función indicadora que devuelve 1 si la condición es verdadera y 0 en caso contrario. La clase predicha $\hat{y}$ se define por mayoría simple:
$$\hat{y} = \arg\max_{c \in \{0, 1\}} P(y = c \mid \mathbf{x})$$

#### B. Regresión Logística y la Función Sigmoide
A diferencia de k-NN (un método no paramétrico basado en memoria), la Regresión Logística es un modelo paramétrico que estima probabilidades binarias utilizando una combinación lineal de las variables de entrada ponderadas por un vector de pesos $\mathbf{w} \in \mathbb{R}^d$ y un sesgo (bias) $b \in \mathbb{R}$:
$$z = \mathbf{w}^T \mathbf{x} + b = \sum_{j=1}^{d} w_j x^{(j)} + b$$

Para mapear este valor continuo de sospecha $z \in (-\infty, +\infty)$ al intervalo acotado de probabilidades $[0, 1]$, aplicamos la **Función Sigmoide** (o logística):
$$\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{e^z + 1}$$

La probabilidad estimada de que la muestra $\mathbf{x}$ pertenezca a la clase positiva (Phishing, $y=1$) es:
$$\hat{y} = P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b)$$

#### Optimización y Función de Pérdida (Binary Cross-Entropy)
Para encontrar los pesos óptimos $\mathbf{w}$ y $b$, minimizamos la función de costo de entropía cruzada binaria (también conocida como Log-Loss):
$$\mathcal{L}(\mathbf{w}, b) = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$

Esta función de pérdida es convexa, lo que garantiza que el método numérico de optimización (como el Gradiente Descendente) converja de manera global al conjunto óptimo de parámetros.

---

## Sesión 3.2: Práctica Guiada - Exploración de Phishing con Pandas (2 Horas)
*   **Distribución del Tiempo:** 90 minutos de codificación en vivo, explicación del funcionamiento interno de Pandas y carga de datos. 30 minutos de resolución de fallos de sintaxis en Colab.

### 1. Cargado de Datos y Contexto del Dataset Real
Utilizaremos el **Phishing Websites Dataset** del repositorio de Machine Learning de la UCI. Este conjunto de datos contiene atributos estructurales de páginas web que sirven para discriminar si un sitio es legítimo o un portal fraudulento de Phishing diseñado para robar datos de diseñadores digitales o profesionales de TI.

#### Diccionario de Datos Clave (Columnas):
*   `having_IP_Address` (Categoría: {1, -1}): Define si el dominio utiliza una IP directa en lugar de un nombre legible.
*   `URL_Length` (Categoría: {1, 0, -1}): Longitud de la URL (1: Largo/Sospechoso, 0: Moderado, -1: Corto/Seguro).
*   `SSLfinal_State` (Categoría: {1, 0, -1}): Estado del certificado SSL (1: Sí y de confianza, 0: Sí pero no confiable, -1: Sin SSL).
*   `Result` (Categoría: {1, -1}): Variable objetivo (1: Sitio Legítimo, -1: Sitio de Phishing).

---

### 2. Bloque de Código de Google Colab (Hands-on)

```python
# ==============================================================================
# IMPORTACIÓN DE LIBRERÍAS Y CARGA DEL DATASET REAL DESDE UCI / KAGGLE
# ==============================================================================
import pandas as pd
import numpy as np

# Carga del dataset desde un repositorio público directo
url_dataset = "https://raw.githubusercontent.com/MarcosAng/Datasets-ML/main/phishing_dataset.csv"
df = pd.read_csv(url_dataset)

# Visualización de las primeras 5 filas para inspección ocular
print("--- PRIMERAS 5 FILAS DEL DATASET DE PHISHING ---")
print(df.head())

# ==============================================================================
# QUERIES AVANZADAS CON PANDAS PARA COMPRENSIÓN PROFUNDA DEL COMPORTAMIENTO
# ==============================================================================

# Consulta 1: Filtrar sitios que NO usan SSL y ver cuántos de ellos resultan ser Phishing
no_ssl_query = df[df['SSLfinal_State'] == -1]
total_no_ssl = len(no_ssl_query)
phishing_no_ssl = len(no_ssl_query[no_ssl_query['Result'] == -1])
pct_phishing_no_ssl = (phishing_no_ssl / total_no_ssl) * 100

print("\n--- CONSULTA 1: IMPACTO DE LA AUSENCIA DE SSL ---")
print(f"Total de páginas web sin certificado SSL en la muestra: {total_no_ssl}")
print(f"Páginas sin SSL clasificadas como Phishing: {phishing_no_ssl}")
print(f"Probabilidad empírica de Phishing si carece de SSL: {pct_phishing_no_ssl:.2f}%")

# Consulta 2: Intersección lógica: URLs sospechosas con longitud alta que usan IPs directas
suspicious_urls = df[(df['URL_Length'] == 1) & (df['having_IP_Address'] == 1)]
total_suspicious = len(suspicious_urls)
legitimate_suspicious = len(suspicious_urls[suspicious_urls['Result'] == 1])

print("\n--- CONSULTA 2: INTERSECCIÓN DE INDICADORES DE RIESGO ---")
print(f"Páginas con URLs largas que además exponen su IP directa: {total_suspicious}")
print(f"De estas páginas de alto riesgo, ¿cuántas lograron ser legítimas?: {legitimate_suspicious}")

# Consulta 3: Matriz de correlación lineal enfocada en la variable objetivo 'Result'
correlation_matrix = df.corr()
target_correlation = correlation_matrix['Result'].sort_values(ascending=False)

print("\n--- CONSULTA 3: CORRELACIÓN DE ATRIBUTOS CON EL RESULTADO FINAL ---")
print("Atributos más fuertemente correlacionados con la legitimidad (1) o Phishing (-1):")
print(target_correlation)
```

---

### 3. Explicación Técnica Detallada del Código (Paso a Paso)

1.  `df = pd.read_csv(url_dataset)`: Importa el archivo CSV estructurado de la web y lo carga en un objeto bidimensional `DataFrame` de Pandas en memoria RAM.
2.  `df['SSLfinal_State'] == -1`: Retorna una serie de booleanos (`True` o `False`) que actúa como máscara lógica para identificar qué registros carecen de certificado SSL de seguridad.
3.  `no_ssl_query = df[...]`: Aplica la máscara lógica para filtrar y extraer únicamente las filas de la base de datos que cumplen con la condición de ausencia de SSL.
4.  `df[(df['URL_Length'] == 1) & (df['having_IP_Address'] == 1)]`: Demuestra la sintaxis de indexación booleana múltiple usando el operador a nivel de bits `&` (AND). En Pandas, es mandatorio agrupar cada condición individual entre paréntesis para asegurar la precedencia correcta de los operadores.
5.  `df.corr()`: Calcula el coeficiente de correlación de Pearson entre todas las variables numéricas del dataset de forma paralela. Permite identificar de manera cuantitativa qué atributos tienen mayor peso para distinguir páginas web seguras de portales maliciosos.

---

## Sesión 3.3: Laboratorio Autónomo y Evaluación Multimodelo (2 Horas)
*   **Distribución del Tiempo:** 90 minutos de codificación autónoma de modelos por los estudiantes y redacción de su defensa de negocio. 30 minutos de resolución de quiz y evaluación síncrona.

### 1. El Desafío del Estudiante (Hands-on)
El alumno debe completar un notebook en Google Colab para entrenar, evaluar y comparar dos modelos de aprendizaje supervisado distintos sobre el Phishing Websites Dataset:
*   **Modelo A:** Clasificador k-NN (ajustando $k=5$, usando la métrica de distancia Euclídea).
*   **Modelo B:** Regresión Logística (utilizando un factor de regularización estándar $C=1.0$).

Los estudiantes deberán implementar la división de datos en **80% para entrenamiento (Train)** y **20% para pruebas (Test)**, entrenar ambos clasificadores en scikit-learn, y graficar sus respectivas matrices de confusión utilizando `ConfusionMatrixDisplay` de scikit-learn.

---

### 2. Plantilla de Código para el Estudiante (Google Colab)

```python
# ==============================================================================
# ENTORNO DE EVALUACIÓN MULTIMODELO - TAREA DEL ESTUDIANTE
# ==============================================================================
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Separar características (X) y etiquetas objetivo (y)
X = df.drop(columns=['Result'])
y = df['Result']

# Re-mapear etiquetas de result: -1 (Phishing) a 0, y 1 (Legítimo) a 1
# Esto es necesario para evitar confusiones en métricas estándar
y = y.replace({-1: 0, 1: 1})

# División del dataset en conjuntos de entrenamiento y prueba (80/20)
# Se define un random_state constante para reproducibilidad
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# ------------------------------------------------------------------------------
# MODELO 1: k-NEAREST NEIGHBORS (k-NN)
# ------------------------------------------------------------------------------
print("--- ENTRENANDO MODELO 1: k-NN (k=5) ---")
knn_model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn_model.fit(X_train, y_train)

# Predicciones del modelo k-NN
y_pred_knn = knn_model.predict(X_test)

# ------------------------------------------------------------------------------
# MODELO 2: REGRESIÓN LOGÍSTICA
# ------------------------------------------------------------------------------
print("\n--- ENTRENANDO MODELO 2: REGRESIÓN LOGÍSTICA ---")
log_model = LogisticRegression(C=1.0, max_iter=1000)
log_model.fit(X_train, y_train)

# Predicciones del modelo de Regresión Logística
y_pred_log = log_model.predict(X_test)

# ==============================================================================
# SECCIÓN DE ANÁLISIS DE RENDIMIENTO: MATRIZ DE CONFUSIÓN
# ==============================================================================

# Calcular matrices de confusión
cm_knn = confusion_matrix(y_test, y_pred_knn)
cm_log = confusion_matrix(y_test, y_pred_log)

# Imprimir reportes de clasificación en consola
print("\n--- REPORTE DE CLASIFICACIÓN: k-NN ---")
print(classification_report(y_test, y_pred_knn, target_names=['Phishing', 'Legítimo']))

print("\n--- REPORTE DE CLASIFICACIÓN: REGRESIÓN LOGÍSTICA ---")
print(classification_report(y_test, y_pred_log, target_names=['Phishing', 'Legítimo']))

# Graficar la Matriz de Confusión para ambos modelos
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ConfusionMatrixDisplay(confusion_matrix=cm_knn, display_labels=['Phishing', 'Legítimo']).plot(ax=ax[0], cmap='Blues')
ax[0].set_title("Matriz de Confusión: k-NN")

ConfusionMatrixDisplay(confusion_matrix=cm_log, display_labels=['Phishing', 'Legítimo']).plot(ax=ax[1], cmap='Purples')
ax[1].set_title("Matriz de Confusión: Regresión Logística")

plt.tight_layout()
plt.show()
```

---

### 3. Defensa Analítica y de Negocio (Requisito de Evaluación)
Los estudiantes deben redactar un informe ejecutivo (en formato markdown dentro del mismo notebook) respondiendo con rigor técnico a las siguientes interrogantes del negocio:

*   **Verdaderos Positivos (VP):** ¿Qué representa en este escenario?
    *   *Respuesta Esperada:* Páginas web de Phishing real que el modelo identificó correctamente como Phishing. El sistema de ciberseguridad puede bloquear el acceso a estos dominios impidiendo ataques.
*   **Verdaderos Negativos (VN):** ¿Qué representa?
    *   *Respuesta Esperada:* Páginas web legítimas seguras que el modelo catalogó correctamente como Legítimas, permitiendo el libre tráfico de los usuarios sin interrupciones operativas.
*   **Falsos Positivos (FP):** ¿Cuál es su costo e impacto para la organización?
    *   *Respuesta Esperada:* Sitios web institucionales y legítimos (como el servidor de portafolios de diseño o el portal escolar) que el modelo cataloga erróneamente como "Phishing". El costo es operativo: usuarios bloqueados por error, quejas en la mesa de soporte técnico y retrasos en los flujos de entrega creativos.
*   **Falsos Negativos (FN):** ¿Cuál es su costo de seguridad?
    *   *Respuesta Esperada:* Un sitio de Phishing real que el modelo clasifica de manera errónea como "Legítimo". El costo es catastrófico: el usuario confía en la página, ingresa credenciales bancarias o contraseñas institucionales, resultando en un robo masivo de información y un compromiso absoluto de la infraestructura corporativa.
*   **Dilema de Decisión:** Si el modelo de Regresión Logística obtiene menor precisión global (*accuracy*) pero reduce los Falsos Negativos a la mitad en comparación con k-NN, ¿cuál de los dos modelos debería ser implementado por el Director de Ciberseguridad de la empresa? ¿Por qué?

---

### 4. Evaluación Síncrona: Quiz de Moodle (Formato Aiken)
Copia este bloque de texto, guárdalo como `.txt` y súbelo directamente a tu banco de preguntas en Moodle en la categoría "Semana 3":

```text
¿Cuál es la principal diferencia conceptual entre el algoritmo k-NN y la Regresión Logística?
A. k-NN es un modelo paramétrico estructurado y la Regresión Logística es no paramétrica.
B. k-NN clasifica por votación de vecindad sin entrenar parámetros, mientras que la Regresión Logística optimiza pesos para calcular probabilidades lógicas.
C. k-NN solo calcula regresiones lineales y la Regresión Logística resuelve problemas de clustering no supervisado.
D. k-NN requiere que los datos tengan etiquetas cualitativas continuas obligatoriamente.
ANS: B

¿Por qué es indispensable normalizar o escalar los datos numéricos antes de entrenar un modelo k-NN?
A. Porque el algoritmo utiliza funciones de distancia como la Euclídea, por lo que atributos con magnitudes numéricas grandes dominarían artificialmente el cálculo sobre las variables pequeñas.
B. Para acelerar la optimización analítica de los coeficientes de peso de scikit-learn.
C. Porque k-NN no funciona si se le ingresan datos con valores decimales o flotantes.
D. Para evitar que el conjunto de prueba sea más grande que el conjunto de entrenamiento.
ANS: A

En un sistema de ciberseguridad diseñado para filtrar correos de Phishing, ¿cuál de las siguientes situaciones representa el mayor riesgo de seguridad para la organización?
A. Un Falso Positivo (FP).
B. Un Verdadero Negativo (VN).
C. Un Falso Negativo (FN).
D. Un Verdadero Positivo (VP).
ANS: C

¿Qué rango de salida produce la función de activación Sigmoide (o logística) utilizada en los modelos supervisados de clasificación?
A. Rango abierto de [-1.0, 1.0]
B. Rango cerrado de [0.0, 1.0] que representa un espacio probabilístico.
C. Rango de [-infinity, +infinity] continuo.
D. Rango discreto que contiene únicamente los enteros {-1, 1}.
ANS: B

Si el parámetro n_neighbors del algoritmo KNeighborsClassifier se establece en un número extremadamente pequeño (ej. k=1), ¿qué comportamiento experimentará el modelo?
A. El modelo tendrá un sesgo muy alto y será incapaz de aprender de los datos (Underfitting).
B. El clasificador se comportará exactamente igual que una Regresión Logística lineal.
C. El modelo se volverá insensible a los valores atípicos (outliers) presentes en el dataset.
D. El modelo tendrá una alta varianza y tenderá a sobreajustarse a los ruidos del conjunto de entrenamiento (Overfitting).
ANS: D
```

---

### 5. Tarea para la Casa (Homework Challenge)
1. **Optimización de Parámetros:** Modifica el parámetro `n_neighbors` de k-NN (prueba valores de $k$ de 1 a 15) y el parámetro de regularización $C$ de la Regresión Logística (prueba valores de $0.01$, $0.1$, $1.0$, $10.0$).
2. **Curva de Aprendizaje:** Grafica la precisión en entrenamiento frente a la precisión en pruebas para identificar el punto exacto donde el modelo de k-NN experimenta sobreajuste (*Overfitting*).

---

### 6. Fuentes y Referencias Bibliográficas (Alineación Curricular)
*   **Müller, A. C., & Guido, S.** *Introduction to Machine Learning with Python*. Capítulo 2: "Supervised Learning" (Secciones específicas sobre k-Nearest Neighbors y Linear Models for Classification).
*   **Grus, J.** *Data Science from Scratch*. Capítulo 12: "k-Nearest Neighbors" y Capítulo 16: "Logistic Regression" (Implementación paso a paso de distancias y optimización por gradiente de la sigmoide).
*   **Sridhar, S.** *Machine Learning*. Capítulo sobre algoritmos paramétricos y modelos lineales clásicos de clasificación.
