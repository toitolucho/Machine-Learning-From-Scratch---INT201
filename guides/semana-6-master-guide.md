# Guia Curricular y Docente Maestra - Semana 6
# Materia: Machine Learning aplicado a la Ciberseguridad y el Diseno/Animacion Digital
# Duracion Semanal: 6 Horas (3 Sesiones de 2 Horas cada una)
# Enfoque Pedagogico: 1h 30m Ensenanza Activa / 30m Taller y Laboratorio Hands-on

---

## Modulo 2: Modelos Avanzados de Clasificacion y Ciberseguridad
### Semana 6: Arboles de Decision, Ganancia de Informacion, Diagnostico de Sobreajuste y Ensambles (Random Forest)

---

## 1. Planificacion Curricular y Distribucion del Tiempo

| Sesion | Duracion | Tipo | Contenido Principal |
| :--- | :--- | :--- | :--- |
| **Sesion 6.1** | 2 Horas | Teorica e Interactiva | Particionado ortogonal, Entropia de Shannon, Impureza de Gini y Ganancia de Informacion. |
| **Sesion 6.2** | 2 Horas | Modelado e Hiperparametros | Sobreajuste (Overfitting), Criterios de Prepoda y Fundamentos de Random Forest (Bagging). |
| **Sesion 6.3** | 2 Horas | Laboratorio Hands-on | Clasificacion en CIC-IDS2017, consultas analiticas en Pandas y Defensa de Matriz de Confusion. |

---
## 2. Sesion 6.1 (2 Horas): Fundamentos de Arboles de Decision, Entropia y Ganancia de Informacion

### 2.1. Objetivos Pedagogicos
1. Comprender la particion geometrica recursiva del espacio de caracteristicas mediante hiperplanos ortogonales a los ejes coordenados.
2. Formalizar matematicamente la reduccion de incertidumbre mediante la Entropia de Shannon y el Indice de Impureza de Gini.
3. Evaluar la Ganancia de Informacion como criterio algoritmico rector de algoritmos clasicos como ID3, C4.5 y CART.

---

### 2.2. La Analogia Infantil (Enfoque 'Para Ninos de 10 Anos')
> **El Detective del Cumpleanos y el Juego de las 20 Preguntas:**  
> Imagina que estas en una fiesta con 100 ninos y uno de ellos se comio todo el pastel de chocolate. Tienes que descubrir al culpable haciendo preguntas de 'SI' o 'NO'.  
> - Si preguntas: *'Llevas zapatos rojos?'*, y solo 2 ninos llevan zapatos rojos, casi no aprendiste nada porque todavia te quedan 98 sospechosos en un grupo enorme. Esa fue una pregunta con **poca ganancia de informacion**.  
> - Pero si preguntas: *'Tienes las manos manchadas de chocolate?'*, y exactamente la mitad del salon levanta la mano, dividiste el misterio en dos grupos limpios y redujiste el desorden a la mitad.  
> En Inteligencia Artificial, un **Arbol de Decision** es exactamente ese detective astuto: en cada paso busca la pregunta perfecta que divida los datos de la forma mas limpia posible, hasta que en cada grupo queden solo sospechosos o solo inocentes.

---

### 2.3. Rigor Academico y Formalizacion Matematica

#### A. Entropia de Shannon (Incertidumbre de la Distribucion)
Dado un conjunto de entrenamiento $ con $ clases objetivo discretas, la proporcion de muestras pertenecientes a la clase $ se define como  = rac{|S_c|}{|S|}$. La Entropia de Shannon cuantifica el desorden o la falta de pureza en $:
10H(S) = - \sum_{c=1}^C p_c \log_2(p_c)10

*Propiedades clave:*
- Si el nodo es completamente puro ( = 1$ y {c 
eq k} = 0$), (S) = 0$.
- Si las clases estan uniformemente distribuidas ( = rac{1}{C}$), la entropia alcanza su maximo: (S) = \log_2(C)$.

#### B. Indice de Impureza de Gini (Criterio CART)
Utilizado por defecto en , mide la probabilidad de que una muestra seleccionada al azar sea clasificada incorrectamente:
10I_G(S) = 1 - \sum_{c=1}^C p_c^210

#### C. Ganancia de Informacion ($)
Al evaluar un atributo continuo o categorico $ que particiona el conjunto $ en subconjuntos $\{S_v\}$ segun umbrales de division:
10IG(S, A) = H(S) - \sum_{v \in 	ext{Valores}(A)} rac{|S_v|}{|S|} H(S_v)10
El algoritmo selecciona en cada nodo el split que maximiza (S, A)$ (o maximiza la reduccion de impureza de Gini).

---

### 2.4. Codigo Fuente Conceptual: Entropia y Gini 'From Scratch' (Google Colab)



#### Explicacion Linea por Linea:
1. : Identifica los identificadores de clase unicos en el subconjunto del nodo y contabiliza su frecuencia absoluta.
2. : Normaliza las frecuencias para estimar la probabilidad empirica $ de cada clase.
3. : Implementa fielmente la formula de Shannon; el nodo mixto arroja 1.0000 bits y el nodo puro arroja 0.0000 bits.
4. : Calcula la metrica de Gini. Para 2 clases equilibradas arroja 0.5000, y 0.0000 para pureza absoluta.

---

### 2.5. Preguntas Interactivas para la Clase
Observa el siguiente bloque de codigo incompleto para calcular la Ganancia de Informacion:

*Pregunta al estudiante:* Cuales son las expresiones correctas para  y ?  
*Respuesta tecnica esperada:*  y .

---
## 3. Sesión 6.2 (2 Horas): Diagnóstico de Sobreajuste, Prepoda y Random Forest

### 3.1. Objetivos Pedagógicos
1. Demostrar empíricamente cómo un árbol de decisión sin restricciones de profundidad memoriza el ruido del conjunto de entrenamiento.
2. Aplicar hiperparámetros de prepoda (`max_depth`, `min_samples_split`, `min_samples_leaf`).
3. Construir la arquitectura de un ensamble Bagging mediante **Random Forest** (muestreo Bootstrap y subespacios aleatorios de características).

---

### 3.2. La Analogía Infantil (Enfoque "Para Niños de 10 Años")
> **El Estudiante Memorizador vs. El Jurado de 100 Profesores:**  
> - Si un estudiante solo memoriza exactamente las comas y los puntos de las preguntas del examen del año pasado, sacará un 10 perfecto si le repiten el mismo examen. Pero si el profesor cambia una sola palabra, el estudiante no sabe qué responder y saca cero. A esto le llamamos **Sobreajuste (Overfitting)**: memorizó el ruido en lugar de aprender el concepto general.  
> - Para resolver esto, creamos un **Random Forest (Bosque Aleatorio)**: en lugar de confiar en un solo estudiante que memorizó todo, llamamos a 100 profesores diferentes. A cada profesor le damos un conjunto ligeramente distinto de datos y le prohibimos ver todas las preguntas. Cuando llega un problema nuevo y difícil, todos votan y la mayoría decide. ¡El jurado en equipo jamás comete los errores individuales de un estudiante solitario!

---

### 3.3. Rigor Académico y Reducción de Varianza

#### A. Sobreajuste en Árboles (Alta Varianza)
Un árbol CART no podado continúa dividiendo nodos hasta que todas las hojas son puras ($H(S) = 0$) o contienen menos muestras que `min_samples_split`. Esto genera fronteras de decisión extremadamente irregulares y no generalizables.

#### B. Muestreo Bootstrap y Estimación Out-Of-Bag (OOB)
Para un dataset de $N$ observaciones, un remuestreo con reemplazo de tamaño $N$ tiene una probabilidad de que una muestra particular no sea seleccionada de:
$$\lim_{N 	o \infty} \left(1 - rac{1}{N}ight)^N = rac{1}{e} pprox 0.368$$
El $36.8\%$ de los datos no utilizados (datos Out-Of-Bag) funciona como conjunto de validación gratuito sin requerir partición adicional.

#### C. Subespacios Aleatorios de Características (Feature Subsampling)
En cada división de cada árbol del bosque, el algoritmo evalúa un subconjunto aleatorio de tamaño:
$$m = \lfloor \sqrt{d} floor \quad 	ext{(en clasificación)}$$
Esto descorrelaciona los árboles del ensamble, reduciendo drásticamente la varianza del modelo final:
$$	ext{Var}(ar{X}) = ho \sigma^2 + rac{1 - ho}{B} \sigma^2$$
Donde $ho$ es la correlación promedio entre árboles y $B$ es el número de estimadores (`n_estimators`).

---

### 3.4. Código Fuente en Colab: Diagnóstico de Overfitting y Comparación

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X_data, y_data = make_classification(n_samples=1500, n_features=25, n_informative=10, 
                                     n_classes=2, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X_data, y_data, test_size=0.3, random_state=42)

# 1. Árbol Sobreajustado (Sin poda)
tree_overfit = DecisionTreeClassifier(max_depth=None, random_state=42)
tree_overfit.fit(X_tr, y_tr)

# 2. Árbol Regularizado (Con prepoda)
tree_pruned = DecisionTreeClassifier(max_depth=5, min_samples_leaf=15, random_state=42)
tree_pruned.fit(X_tr, y_tr)

# 3. Ensamble Random Forest
rf_model = RandomForestClassifier(n_estimators=100, max_features='sqrt', 
                                  max_depth=10, random_state=42)
rf_model.fit(X_tr, y_tr)

print("--- EVALUACIÓN DE GENERALIZACIÓN ---")
print(f"Árbol Sin Podar  -> Train Acc: {accuracy_score(y_tr, tree_overfit.predict(X_tr)):.4f} | Test Acc: {accuracy_score(y_te, tree_overfit.predict(X_te)):.4f}")
print(f"Árbol con Prepoda-> Train Acc: {accuracy_score(y_tr, tree_pruned.predict(X_tr)):.4f} | Test Acc: {accuracy_score(y_te, tree_pruned.predict(X_te)):.4f}")
print(f"Random Forest    -> Train Acc: {accuracy_score(y_tr, rf_model.predict(X_tr)):.4f} | Test Acc: {accuracy_score(y_te, rf_model.predict(X_te)):.4f}")
```

---
## 4. Sesión 6.3 (2 Horas): Laboratorio Autónomo y Desafío Práctico (Google Colab)

### 4.1. Dataset Real y Público: CIC-IDS2017
- Canadian Institute for Cybersecurity (Universidad de New Brunswick).
### 4.2. Ingesta y Exploracion con Pandas
### 4.2. Ingesta de Datos con Pandas

```python
import pandas as pd
import numpy as np

# Dataset de Clasificacion
df_data = pd.read_csv("dataset_clasificacion.csv")
print("Data cargada con exito")
```
## 7. Bibliografia

1. Muller, A. C., and Guido, S. (2016). Introduction to Machine Learning with Python. O'Reilly.
2. Grus, J. (2019). Data Science from Scratch. O'Reilly.
3. Sridhar, S. (2021). Machine Learning. Oxford University Press.
## 4. Sesion 6.3: Laboratorio Hands-on y Evaluacion

### 4.1. Dataset Real: Canadian Institute for Cybersecurity
Dataset de trafico de red y diagnostico de eventos anomalos.
### 4.2. Ingesta y Consultas en Pandas

```python
import pandas as pd
import numpy as np

# Carga de datos de trafico de red
df_data = pd.read_csv("network_traffic.csv")

# 1. Query con Pandas
query_analisis = df_data.query("duracion < 100 and paquetes <= 3")
print(f"Registros analizados: {len(query_analisis)}")

# 2. Correlacion de Spearman
corr_spearman = df_data[['duracion', 'bytes_in', 'bytes_out']].corr(method='spearman')
print("Correlacion de Spearman:
", corr_spearman)

# 3. Subdataset de indagacion especifica
df_sub = df_data.query("puerto_servicio <= 1023").copy()
print(f"Muestras filtradas: {len(df_sub)}")
```
### 4.3. Modelado y Evaluacion Multimodelo

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

X = df_data.drop(columns=['etiqueta'])
y = df_data['etiqueta']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# Modelo A: Arbol de Decision con Prepoda
tree_mod = DecisionTreeClassifier(max_depth=6, min_samples_leaf=20, random_state=42)
tree_mod.fit(X_train, y_train)

# Modelo B: Random Forest
rf_mod = RandomForestClassifier(n_estimators=100, max_depth=12, max_features='sqrt', random_state=42)
rf_mod.fit(X_train, y_train)

print("Matriz de Confusion - Arbol:
", confusion_matrix(y_test, tree_mod.predict(X_test)))
print("
Matriz de Confusion - Random Forest:
", confusion_matrix(y_test, rf_mod.predict(X_test)))
```

### 4.4. Guia de Defensa Analitica (Matriz de Confusion)

| Cuadrante | Significado Operativo | Impacto en el Negocio |
| :--- | :--- | :--- |
| **Verdadero Positivo (VP)** | Evento anomalo clasificado correctamente. | Mitigacion oportuna y proteccion de activos. |
| **Verdadero Negativo (VN)** | Operacion regular aprobada. | Continuidad normal de operaciones. |
| **Falso Positivo (FP)** | Operacion regular marcada como anomala. | Friccion con usuarios y revision administrativa. |
| **Falso Negativo (FN)** | Evento anomalo que elude la deteccion. | **Critico:** Incidente no detectado que compromete el sistema. |

---

## 5. Asignacion para Moodle (Homework Challenge)

- **Titulo:** Analisis de Importancia de Variables con Random Forest.
- **Entregable:** Cuaderno en Google Colab donde el alumno grafique el atributo `feature_importances_` y explique el comportamiento de la impureza de Gini ante variables numericas continuas.

---

## 6. Banco de Preguntas en Formato Aiken para Moodle

```
Que valor arroja la Entropia de Shannon en un nodo donde todas las muestras pertenecen a una sola clase?
A. 1.0 bits
B. 0.5 bits
C. 0.0 bits
D. Infinito
ANSWER: C

Cual es el proposito principal de limitar el hiperparametro max_depth en un Arbol de Decision?
A. Mitigar el sobreajuste y mejorar la generalizacion.
B. Forzar que las hojas sean puras.
C. Obligar al arbol a usar una regresion logistica.
D. Eliminar el uso de divisiones binarias.
ANSWER: A

En un Random Forest para clasificacion con d caracteristicas, cual es el valor estandar recomendado para max_features?
A. d / 2
B. Raiz cuadrada de d
C. log2(d)
D. d^2
ANSWER: B

Que porcentaje aproximado de datos queda fuera de la bolsa (Out-Of-Bag) en un muestreo bootstrap?
A. 10.5%
B. 50.0%
C. 36.8%
D. 0.0%
ANSWER: C

En una clasificacion de incidentes de seguridad, que cuadrante representa el mayor peligro operativo?
A. Verdadero Positivo
B. Verdadero Negativo
C. Falso Positivo
D. Falso Negativo
ANSWER: D
```
