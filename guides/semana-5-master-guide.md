# Guía Curricular y Docente Maestra: Semana 5
## Módulo 2: Modelos Avanzados de Clasificación y Ciberseguridad
### Tema: Support Vector Machines (SVM), Hiperplanos de Margen Máximo y el Truco del Kernel

---

## 1. Información General y Planificación de la Semana
* **Duración total:** 6 horas cronológicas.
* **Distribución:** 3 sesiones de 2 horas (1 hora y 30 minutos de instrucción teórica y aprendizaje activo; 30 minutos de taller/laboratorio interactivo).
* **Materia:** Machine Learning aplicado a la Ciberseguridad y el Diseño/Animación Digital.
* **Objetivos de Aprendizaje:**
  1. Comprender la formulación geométrica y analítica del hiperplano de separación óptimo y los vectores de soporte.
  2. Analizar el impacto de la regularización con margen suave ($C$) en el balance sesgo-varianza.
  3. Aplicar el truco del kernel (RBF, Polinomial y Lineal) para resolver problemas no linealmente separables sin proyectar explícitamente los datos.
  4. Implementar en Google Colab un clasificador de detección de anomalías de red sobre el dataset real **NSL-KDD**, comparando SVM vs. Random Forest y realizando la defensa analítica con la Matriz de Confusión.

---

## 2. Sesión 5.1 (2 Horas): Fundamentos Geométricos de Support Vector Machines y Margen Óptimo

### 2.1. Estructura de Tiempo de la Sesión
* **00:00 - 00:20 (20 min):** Introducción intuitiva con la analogía infantil de los dos reinos y el río fronterizo más ancho posible.
* **00:20 - 01:00 (40 min):** Formalización matemática del hiperplano, margen funcional, margen geométrico y formulación primal de optimización cuadrática.
* **01:00 - 01:30 (30 min):** Preguntas interactivas proyectadas para los estudiantes: deducción de vectores de soporte e interpretación geométrica.
* **01:30 - 02:00 (30 min):** Taller interactivo de código: graficación de márgenes y vectores de soporte con scikit-learn.

---

### 2.2. La Analogía Infantil ("El Río más Ancho entre Dos Reinos")
> **Enfoque para un niño de 10 años:**
> Imagina que hay dos reinos vecinos: el Reino de las Fichas Rojas y el Reino de las Fichas Azules. Cada reino ha colocado campamentos cerca de la frontera.
> Los gobernantes deciden cavar un canal en línea recta para separarlos. Para evitar conflictos, el canal debe ser **lo más ancho posible**, dejando la mayor distancia de seguridad entre los campamentos más cercanos de cada bando.
> 
> Muchos ingenieros proponen trazar el canal en distintas direcciones, pero solo hay una orientación exacta donde el ancho de la franja de seguridad alcanza su valor máximo.
> ¿Quiénes determinan por dónde pasa el canal? No todos los campamentos: ¡únicamente los que están situados en la orilla, en las posiciones más avanzadas! Si un campamento lejano en el interior se mueve, el canal no cambia. Pero si uno de los campamentos de la orilla se mueve un centímetro, el canal debe recalcularse.
> 
> En Machine Learning:
> * El canal recto es el **hiperplano de decisión**.
> * El ancho de la franja de seguridad es el **margen**.
> * Los campamentos situados exactamente en las orillas son los **vectores de soporte** (*Support Vectors*).
> * La máquina de vectores de soporte (SVM) es el algoritmo matemático que encuentra el canal con el margen más amplio posible.

---

### 2.3. Rigor Académico y Formalización Matemática

En un problema de clasificación binaria supervisada con etiquetas $y_i \in \{-1, +1\}$ y vectores de características $\mathbf{x}_i \in \mathbb{R}^d$:
Un hiperplano separador afín se define formalmente como:
$$h(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b = 0$$

Donde $\mathbf{w} \in \mathbb{R}^d$ es el vector normal ortogonal al hiperplano y $b \in \mathbb{R}$ es el término de sesgo (*bias*). La regla de decisión para una nueva instancia $\mathbf{x}^*$ es:
$$\hat{y} = \text{sign}(\mathbf{w}^T \mathbf{x}^* + b)$$

#### A. Margen Geométrico y Vectores de Soporte
Para un conjunto de datos linealmente separable, exigimos que todas las instancias queden fuera de la banda del margen:
$$y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1, \quad \forall i \in \{1, \dots, n\}$$

Los hiperplanos canónicos que delimitan el margen son:
$$\mathbf{w}^T \mathbf{x} + b = +1 \quad \text{y} \quad \mathbf{w}^T \mathbf{x} + b = -1$$

La distancia ortogonal desde el hiperplano central ($h(\mathbf{x})=0$) hasta cualquiera de los hiperplanos canónicos es $\frac{1}{\|\mathbf{w}\|_2}$. Por lo tanto, el **ancho total del margen** ($\gamma$) es:
$$\gamma = \frac{2}{\|\mathbf{w}\|_2}$$

Maximizar el margen $\gamma$ equivale a minimizar la norma del vector de pesos $\|\mathbf{w}\|_2$, lo que se formula como un problema de programación cuadrática (**Formulación Primal de Margen Duro**):
$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|_2^2 \quad \text{sujeto a} \quad y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1, \quad i = 1, \dots, n$$

#### B. Multiplicadores de Lagrange y Condiciones KKT
Introduciendo multiplicadores de Lagrange $\alpha_i \ge 0$, la función lagrangiana primal es:
$$\mathcal{L}(\mathbf{w}, b, \boldsymbol{\alpha}) = \frac{1}{2} \|\mathbf{w}\|^2 - \sum_{i=1}^n \alpha_i \left[ y_i (\mathbf{w}^T \mathbf{x}_i + b) - 1 \right]$$

Anulando derivadas parciales con respecto a $\mathbf{w}$ y $b$:
$$\mathbf{w} = \sum_{i=1}^n \alpha_i y_i \mathbf{x}_i, \qquad \sum_{i=1}^n \alpha_i y_i = 0$$

Sustituyendo en la lagrangiana obtenemos el **Problema Dual de Wolfe**:
$$\max_{\boldsymbol{\alpha}} \sum_{i=1}^n \alpha_i - \frac{1}{2} \sum_{i=1}^n \sum_{j=1}^n \alpha_i \alpha_j y_i y_j (\mathbf{x}_i^T \mathbf{x}_j)$$
$$\text{sujeto a} \quad \alpha_i \ge 0, \quad \sum_{i=1}^n \alpha_i y_i = 0$$

Por las **condiciones de holgura complementaria KKT**:
$$\alpha_i \left[ y_i (\mathbf{w}^T \mathbf{x}_i + b) - 1 \right] = 0$$
* Si $y_i (\mathbf{w}^T \mathbf{x}_i + b) > 1$ (punto alejado del margen), entonces $\alpha_i = 0$.
* Si $\alpha_i > 0$, entonces $y_i (\mathbf{w}^T \mathbf{x}_i + b) = 1$. Estos puntos son los **vectores de soporte** que determinan la frontera.

---

### 2.4. Preguntas Abiertas de Interpretación y Código para Estudiantes

#### Pregunta 1 (Geométrica / Conceptual):
> *"Si entrenamos un clasificador SVM lineal con 5,000 registros de tráfico de red y el optimizador identifica 18 vectores de soporte, ¿qué ocurre con el hiperplano si eliminamos los 4,982 registros que tienen $\alpha_i = 0$ y reentrenamos el modelo?"*
* **Respuesta Esperada:** El hiperplano resultante es idéntico. Los puntos con $\alpha_i = 0$ no intervienen en el cálculo del vector normal $\mathbf{w}$ ni del sesgo $b$.

#### Pregunta 2 (Completar Código en Clase):
```python
from sklearn.svm import SVC
import numpy as np

# Datos de muestra: tasa de transferencia vs. frecuencia de peticiones
X_demo = np.array([[1.0, 2.0], [2.0, 3.0], [3.0, 3.0], [6.0, 5.0], [7.0, 8.0], [8.0, 6.0]])
y_demo = np.array([-1, -1, -1, 1, 1, 1])

# [COMPLETAR]: Instancia un clasificador SVM lineal con margen estricto (C alto)
# modelo_svm = SVC(kernel=_______, C=_______)
modelo_svm = SVC(kernel='linear', C=1e5)
modelo_svm.fit(X_demo, y_demo)

# [COMPLETAR]: Obtén los vectores de soporte
# print("Vectores de soporte:\n", modelo_svm._____________)
print("Vectores de soporte:\n", modelo_svm.support_vectors_)
```

---

## 3. Sesión 5.2 (2 Horas): Margen Suave ($C$), Truco del Kernel y Fronteras No Lineales

### 3.1. Estructura de Tiempo de la Sesión
* **00:00 - 00:20 (20 min):** Analogía de la sábana elástica tridimensional (proyección espacial).
* **00:20 - 01:00 (40 min):** Margen suave, variables de holgura ($\xi_i$), parámetro $C$ y el Teorema de Mercer con formulación del Kernel RBF.
* **01:00 - 01:30 (30 min):** Preguntas interactivas: balance de hiperparámetros $C$ y $\gamma$.
* **01:30 - 02:00 (30 min):** Taller interactivo de visualización de fronteras no lineales en 2D y 3D.

---

### 3.2. La Analogía Infantil ("El Salto Mágico a la Tercera Dimensión")
> **Enfoque para un niño de 10 años:**
> Imagina una hoja de papel donde dibujas un círculo de fichas rojas en el centro y las rodeas con fichas azules alrededor. Si intentas trazar una sola línea recta en la hoja para separar todas las rojas de las azules, te darás cuenta de que es imposible.
> 
> Pero si levantamos la hoja justo en el centro donde están las fichas rojas (como si fuera una cama elástica empujada hacia arriba), las fichas rojas quedan elevadas en el aire, mientras que las fichas azules se quedan abajo.
> Ahora es muy fácil pasar una tabla plana de cartón horizontal por debajo de las rojas y por encima de las azules. ¡Hemos separado ambos grupos con un plano recto!
> 
> En Machine Learning:
> * La hoja plana es el **espacio de características bidimensional**.
> * Levantar las fichas rojas al aire es la **transformación a una dimensión superior** ($\phi(\mathbf{x})$).
> * La tabla plana de cartón es el **hiperplano en la dimensión superior**.
> * El **Truco del Kernel** es la fórmula matemática que calcula ese corte exacto sin tener que construir la tercera dimensión en memoria.

---

### 3.3. Rigor Académico y Formalización del Kernel

#### A. Margen Suave (Soft-Margin SVM) y Variables de Holgura
Para tolerar muestras ruidosas o solapadas, se introducen variables de holgura $\xi_i \ge 0$:
$$y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0, \quad \forall i$$

El problema de optimización primal penalizado es:
$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{i=1}^n \xi_i$$
$$\text{sujeto a} \quad y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0$$

* **Impacto del Hiperparámetro $C$:**
  * $C$ alto: Penaliza severamente las violaciones del margen, reduciendo el ancho del canal y aumentando el riesgo de **sobreajuste (alta varianza)**.
  * $C$ bajo: Tolera más infracciones a cambio de un margen más amplio, mejorando la generalización pero arriesgando **subajuste (alto sesgo)**.

#### B. El Truco del Kernel (Kernel Trick)
Mediante un mapeo no lineal $\phi: \mathbb{R}^d \to \mathcal{H}$ a un espacio de Hilbert, el producto escalar en el problema dual se sustituye por una función núcleo:
$$K(\mathbf{x}_i, \mathbf{x}_j) = \langle \phi(\mathbf{x}_i), \phi(\mathbf{x}_j) \rangle$$

Por el **Teorema de Mercer**, cualquier función simétrica y semidefinida positiva es un kernel válido.

* **Kernel Gaussiano RBF (Radial Basis Function):**
  $$K(\mathbf{x}_i, \mathbf{x}_j) = \exp\left( -\gamma \|\mathbf{x}_i - \mathbf{x}_j\|_2^2 \right)$$
  * $\gamma$ alto: Radio de influencia estrecho alrededor de cada vector de soporte (fronteras complejas e irregulares).
  * $\gamma$ bajo: Radio de influencia amplio (fronteras suaves y regulares).

---

### 3.4. Preguntas Abiertas de Interpretación y Código para Estudiantes

#### Pregunta 1 (Diagnóstico de Generalización):
> *"Si tu modelo SVM RBF obtiene 99.7% de precisión en entrenamiento y 68.1% en prueba, ¿hacia dónde debes mover los valores de $C$ y $\gamma$ para corregir el desajuste?"*
* **Respuesta Esperada:** Reducir $\gamma$ (para suavizar el radio de curvatura gaussiano) y reducir $C$ (para ensanchar el margen y tolerar ruido).

#### Pregunta 2 (Completar Código en Clase):
```python
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# [COMPLETAR]: Define la cuadrícula para optimizar C y gamma en un kernel RBF
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.001, 0.01, 0.1, 1.0],
    'kernel': ['rbf']
}

# [COMPLETAR]: Instancia GridSearchCV con 5 pliegues y métrica f1_weighted
grid_search = GridSearchCV(estimator=SVC(), param_grid=param_grid, cv=5, scoring='f1_weighted')
```

---

## 4. Sesión 5.3 (2 Horas): Laboratorio Autónomo y Desafío Práctico (Google Colab)

### 4.1. Ficha Técnica del Laboratorio
* **Título:** Detección de Tráfico Anómalo de Red mediante Modelos de Margen Máximo y Ensambles.
* **Dataset Real:** **NSL-KDD Dataset** (Canadian Institute for Cybersecurity / UNB).
  * Procedencia: Repositorio público de evaluación de sistemas de detección de intrusiones.
* **Descripción:** 41 características técnicas por conexión de red (duración, protocolo, volumen de datos en bytes, tasas de error y contadores de servicio). La columna objetivo clasifica la sesión como normal o anómala.

---

### 4.2. Ingesta, Diccionario de Datos y Consultas Avanzadas con Pandas

#### Bloque de Código 1: Carga y Mapeo Estructurado
```python
import pandas as pd
import numpy as np

# Estructura formal de atributos del estándar NSL-KDD
column_names = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'class', 'difficulty_level'
]

# Carga del dataset local o descargado previamente
df_raw = pd.read_csv('KDDTrain+.txt', names=column_names, index_col=False)

# Mapeo binario de la variable objetivo: 0 = Tráfico Normal, 1 = Conexión Anómala
df_raw['target_binary'] = df_raw['class'].apply(lambda x: 0 if x == 'normal' else 1)

print(f"Dimensiones del dataset cargado: {df_raw.shape}")
print(df_raw['target_binary'].value_counts(normalize=True))
```

#### Explicación Línea por Línea del Bloque 1:
1. `column_names = [...]`: Define la lista explícita de nombres de columna requerida para estructurar el archivo fuente sin encabezados.
2. `df_raw = pd.read_csv(...)`: Carga el contenido tabular en un DataFrame de Pandas sin indexar columnas adicionales.
3. `df_raw['target_binary'] = df_raw['class'].apply(...)`: Codifica la variable dependiente en formato binario estandarizado (0 para normal y 1 para anomalías).
4. `df_raw['target_binary'].value_counts(normalize=True)`: Evalúa la proporción relativa entre clases para diagnosticar balance de datos.

---

#### Bloque de Código 2: Consultas Especializadas (Queries) con Pandas
```python
# Consulta 1: Conexiones TCP con alta tasa de error de sincronización
query_syn_errors = df_raw.query("protocol_type == 'tcp' and serror_rate > 0.8 and logged_in == 0")
print(f"Conexiones con fallos de sincronización: {len(query_syn_errors)}")

# Consulta 2: Transferencias asimétricas de gran volumen
query_high_transfer = df_raw.query("src_bytes > 50000 and dst_bytes < 1000 and target_binary == 1")
print(f"Sesiones con transferencia asimétrica anómala: {len(query_high_transfer)}")

# Consulta 3: Matriz de correlación en servicios web HTTP
df_http = df_raw[df_raw['service'] == 'http'].copy()
metricas = ['duration', 'src_bytes', 'dst_bytes', 'count', 'srv_count', 'target_binary']
print("\nCorrelación con la variable objetivo en HTTP:")
print(df_http[metricas].corr()['target_binary'].sort_values(ascending=False))
```

#### Explicación Línea por Línea del Bloque 2:
1. `query_syn_errors = df_raw.query(...)`: Filtra registros donde la tasa de errores de paquetes supera el 80% sin sesión iniciada, indicio típico de saturación de puertos.
2. `query_high_transfer = df_raw.query(...)`: Aísla sesiones con alta emisión de bytes y baja recepción, identificando posibles patrones de exfiltración de información.
3. `df_http = df_raw[df_raw['service'] == 'http'].copy()`: Crea un sub-dataset enfocado en tráfico web.
4. `df_http[metricas].corr()[...]`: Calcula coeficientes de correlación de Pearson para ordenar las variables continuas más asociadas a eventos anómalos.

---

### 4.3. Pipeline y Comparación Multimodelo (SVM vs. Random Forest)

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

# Muestra estratificada representativa para optimizar el cómputo
df_sample = df_raw.sample(n=10000, random_state=42, stratify=df_raw['target_binary'])

features_cat = ['protocol_type', 'flag']
features_num = ['duration', 'src_bytes', 'dst_bytes', 'count', 'srv_count', 
                'serror_rate', 'same_srv_rate', 'diff_srv_rate', 'dst_host_count']

X = df_sample[features_cat + features_num]
y = df_sample['target_binary']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), features_num),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), features_cat)
    ]
)

X_train_proc = preprocessor.fit_transform(X_train)
X_test_proc = preprocessor.transform(X_test)

# Modelo 1: Support Vector Classifier con Kernel RBF
svm_model = SVC(kernel='rbf', C=5.0, gamma='scale', random_state=42)
svm_model.fit(X_train_proc, y_train)
y_pred_svm = svm_model.predict(X_test_proc)

# Modelo 2: Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train_proc, y_train)
y_pred_rf = rf_model.predict(X_test_proc)
```

---

### 4.4. Defensa Analítica con la Matriz de Confusión

```python
cm_svm = confusion_matrix(y_test, y_pred_svm)
cm_rf = confusion_matrix(y_test, y_pred_rf)

print("Matriz de Confusión - SVM (RBF):\n", cm_svm)
print("\nMatriz de Confusión - Random Forest:\n", cm_rf)
```

```
Estructura de la Matriz:
                     Predicción: Normal (0)      Predicción: Anomalía (1)
Real: Normal (0)     Verdaderos Negativos (VN)   Falsos Positivos (FP)
Real: Anomalía (1)   Falsos Negativos (FN)       Verdaderos Positivos (VP)
```

#### Rúbrica de Defensa y Evaluación Operativa:

| Cuadrante | Significado Técnico | Impacto en el Negocio / Operaciones |
| :--- | :--- | :--- |
| **Verdaderos Positivos (VP)** | Una conexión anómala es detectada y contenida a tiempo. | Integridad de la red preservada sin fugas de datos. |
| **Verdaderos Negativos (VN)** | El tráfico legítimo de usuarios y diseñadores fluye con normalidad. | Continuidad operativa asegurada sin interrupciones en la entrega de proyectos. |
| **Falsos Positivos (FP)** | Una conexión normal es etiquetada erróneamente como anómala. | Bloqueo temporal a usuarios válidos y sobrecarga de revisión para los analistas de seguridad. |
| **Falsos Negativos (FN)** | Un evento anómalo pasa desapercibido como si fuera tráfico normal. | Riesgo crítico de compromiso del sistema, pérdida de confidencialidad y costos de remediación elevados. |

> **Pregunta de Defensa Técnica para el Alumno:**  
> *"Si Random Forest logra un Accuracy del 97.2% con 35 Falsos Negativos y SVM alcanza 96.0% pero reduce los Falsos Negativos a 5, ¿cuál estimador es técnicamente preferible en un perímetro crítico y qué métrica formal respalda tu decisión?"*  
> **Criterio de Evaluación:** El estudiante debe priorizar el modelo con mayor **Sensibilidad (Recall)** para minimizar los Falsos Negativos, justificando que el costo de una intrusión omitida supera ampliamente el costo de revisar un Falso Positivo.

---

## 5. Tarea para la Casa (Homework Challenge para Moodle)

* **Título:** Detección de Anomalías en Texturas Digitales mediante One-Class SVM.
* **Modalidad:** Individual. Entrega en archivo Google Colab documentado.
* **Consigna:**
  1. Investigar el funcionamiento de `OneClassSVM` para estimación de fronteras de densidad en problemas de una sola clase.
  2. Cargar un subconjunto de imágenes de texturas o dígitos (ej. MNIST clase '0') para representar patrones estándar de renderizado.
  3. Entrenar el modelo con datos no contaminados ($y = 1$) ajustando el hiperparámetro de tolerancia $\nu$ (*nu*).
  4. Introducir un 10% de imágenes de clases distintas simulando distorsiones o texturas corruptas.
  5. Graficar la matriz de confusión resultante y fundamentar el valor óptimo elegido para $\nu$.

---

## 6. Banco de Preguntas en Formato Aiken (Para Importar en Moodle)

```text
¿Cuál es la función matemática del vector de pesos w en un hiperplano separador SVM lineal?
A. Determina la posición del origen del sistema coordenado.
B. Actúa como el vector normal ortogonal al hiperplano separador.
C. Mide la varianza total explicada por los componentes principales.
D. Representa la constante de sesgo para calibrar probabilidades.
ANSWER: B

En una SVM con margen suave, ¿qué efecto genera fijar un valor muy elevado del parámetro C?
A. Ensancha el margen y tolera múltiples infracciones a la frontera.
B. Convierte el modelo en un algoritmo no supervisado de agrupamiento.
C. Penaliza drásticamente las violaciones al margen, aumentando el riesgo de sobreajuste.
D. Modifica el kernel seleccionado por un kernel sigmoide.
ANSWER: C

¿Qué teorema matemático asegura que una función K(x, z) puede operar como un Kernel válido sin calcular la transformación explícita de dimensiones?
A. Teorema de Bayes.
B. Teorema Central del Límite.
C. Teorema de Mercer.
D. Teorema del Valor Medio.
ANSWER: C

¿Qué definen los vectores de soporte seleccionados durante el ajuste de una SVM?
A. Las instancias situadas sobre o dentro de los hiperplanos que delimitan el margen.
B. Los valores atípicos que fueron descartados previamente en la etapa de limpieza.
C. Los centroides promediados de cada una de las clases de entrenamiento.
D. Las variables con menor peso estadístico en el análisis de correlación.
ANSWER: A

En un sistema de monitoreo de seguridad informática, ¿cuál de los cuadrantes de la Matriz de Confusión implica el escenario de mayor riesgo operacional?
A. Verdaderos Negativos (VN).
B. Falsos Positivos (FP).
C. Verdaderos Positivos (VP).
D. Falsos Negativos (FN).
ANSWER: D
```

---

## 7. Referencias Bibliográficas y Fuentes

1. **Müller, A. C., & Guido, S. (2016).** *Introduction to Machine Learning with Python: A Guide for Data Scientists*. O'Reilly Media. (Capítulo 2: Supervised Learning - Support Vector Machines, pp. 92–104).
2. **Sridhar, S. (2021).** *Machine Learning*. Oxford University Press. (Capítulo 5: Support Vector Machines - Maximal Margin Hyperplane, Dual Formulation and Mercer Kernels, pp. 142–178).
3. **Grus, J. (2019).** *Data Science from Scratch: First Principles with Python* (2nd ed.). O'Reilly Media. (Capítulo 4: Linear Algebra, y Capítulo 11: Machine Learning).
4. **Janapati, R., Desai, U., et al. (2026).** *Applied Artificial Intelligence and Machine Learning Techniques for Engineering Applications*. CRC Press / Taylor & Francis. (Capítulo de modelos supervisados y optimización).
5. **Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009).** *A detailed analysis of the KDD CUP 99 data set*. IEEE CISDA.
6. **Reis, J., & Housley, M. (2022).** *Fundamentals of Data Engineering*. O'Reilly Media. (Capítulo 3: The Data Engineering Lifecycle).
