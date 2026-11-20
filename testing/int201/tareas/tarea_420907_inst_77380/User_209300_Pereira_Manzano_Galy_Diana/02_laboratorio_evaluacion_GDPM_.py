ing: utf-8 -*-# -*- cod
"""02_Laboratorio_Evaluacion (resuelto)

# Laboratorio Evaluado: WBCD y Evaluación Multimodelo

## 1. Carga de Datos y Exploración
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix


medidas = ["radius", "texture", "perimeter", "area", "smoothness",
           "compactness", "concavity", "concave_points", "symmetry",
           "fractal_dimension"]
columnas = ["id", "diagnosis"] + [f"{m}_{s}" for s in ("mean", "se", "worst") for m in medidas]

df_wbcd = pd.read_csv(URL, header=None, names=columnas)

print(df_wbcd.shape)
print(df_wbcd["diagnosis"].value_counts())
print(df_wbcd.isna().sum().sum(), "valores nulos")
# Ojo con las escalas: area_mean va en cientos, smoothness_mean en centésimas
print(df_wbcd[["radius_mean", "perimeter_mean", "area_mean", "smoothness_mean"]].describe().loc[["mean", "std"]])

"""## 2. Preprocesamiento"""

# Diagnosis M/B -> 1/0 (maligno = clase positiva)
df_wbcd["diagnosis"] = df_wbcd["diagnosis"].map({"M": 1, "B": 0})

# X (features) e y (target). El id no aporta nada, se descarta.
X = df_wbcd.drop(columns=["id", "diagnosis"])
y = df_wbcd["diagnosis"]

# 80/20, estratificado para mantener la proporción M/B en ambos conjuntos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

"""## 3. Escalamiento (Solo para k-NN)"""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # aprende media y desviación SOLO con train
X_test_scaled = scaler.transform(X_test)        # test se transforma con lo aprendido (sin fuga de datos)

"""## 4. Modelado y Matrices de Confusión"""

# k-NN con datos escalados
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
cm_knn = confusion_matrix(y_test, knn.predict(X_test_scaled))

# k-NN SIN escalar (para validar qué pasa)
knn_sin_escalar = KNeighborsClassifier(n_neighbors=5)
knn_sin_escalar.fit(X_train, y_train)
cm_knn_raw = confusion_matrix(y_test, knn_sin_escalar.predict(X_test))

# Árbol de decisión (no necesita escalar)
arbol = DecisionTreeClassifier(max_depth=4, random_state=42)
arbol.fit(X_train, y_train)
cm_arbol = confusion_matrix(y_test, arbol.predict(X_test))

# Formato sklearn: [[TN, FP], [FN, TP]]
modelos = {
    "k-NN escalado": cm_knn,
    "k-NN SIN escalar": cm_knn_raw,
    "Árbol (max_depth=4)": cm_arbol,
}
for nombre, cm in modelos.items():
    tn, fp, fn, tp = cm.ravel()
    print(f"\n{nombre}\n{cm}")
    print(f"  Falsos negativos (malignos no detectados): {fn}")
    print(f"  Falsos positivos: {fp}")
    print(f"  Accuracy: {(tp + tn) / cm.sum():.3f} | Recall maligno: {tp / (tp + fn):.3f}")

"""## Evaluación Teórica / Decisión de Negocios

1. En este escenario médico, ¿qué implica un Error Tipo II (Falso Negativo) y por qué cuesta vidas?
2. ¿Por qué crees que el Árbol de Decisión no falló estrepitosamente incluso si no hubieses escalado los datos?

*Escribe tu respuesta aquí:*

**1. Error Tipo II (falso negativo)**

Es cuando el modelo dice "benigno" y el tumor en realidad es maligno. A la paciente
se le comunica que está sana, se va a su casa y el cáncer sigue creciendo sin
tratamiento. Cuando alguien vuelve a consulta, el cáncer suele estar en una etapa
más avanzada, con peor pronóstico y un tratamiento más agresivo. Ahí es donde
se pierden vidas.

El falso positivo es el error contrario y es mucho menos grave. Se asusta a una
paciente sana, se le hace una biopsia de más y la confirmación posterior lo corrige.
Es molesto y caro, pero reversible. Un falso negativo no tiene corrección a tiempo.

Por eso, en una clínica oncológica no basta con mirar el accuracy. Hay que mirar el
recall de la clase maligna, o sea cuántos tumores malignos reales atrapa el modelo.
Y si hace falta, conviene aceptar más falsos positivos a cambio de bajar los falsos
negativos, por ejemplo bajando el umbral de decisión.

**2. Por qué el árbol aguanta sin escalar**

El árbol no calcula distancias. En cada nodo hace una pregunta del tipo
"¿area_worst <= 880?" y solo le importa el orden de los valores de esa columna,
no su magnitud. Si multiplicas o estandarizas una variable, el mejor punto de corte
se mueve junto con ella y la división resultante es exactamente la misma. Cada
variable se evalúa por separado, así que una columna en cientos no le gana a una
columna en centésimas.

k-NN es lo contrario. Mide distancia euclidiana sobre todas las variables a la vez,
y area (cientos) o perimeter (decenas) dominan el cálculo mientras que smoothness
(0.05 a 0.16) casi no pesa. Sin escalar, el modelo en la práctica decide con
dos o tres columnas y desperdicia el resto de la información.
"""
