# Nombre: Loza Torres Wilson Mijael                 Carrera: Ing.  Ciberseguridad
"""02_Laboratorio_Evaluacion.ipynb

# Laboratorio Evaluado: WBCD y Evaluación Multimodelo

**Reto Autónomo: Clínica Oncológica**

Eres el Consultor IA de un hospital. El dataset WBCD contiene radios y perímetros de células. Debes entrenar k-NN y Árboles de Decisión, y validar qué pasa si no escalas los datos.

"""

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

datos = load_breast_cancer(as_frame=True)

df_wbcd = datos.data.copy()
df_wbcd["diagnosis"] = datos.target.map({0: "M", 1: "B"})

print(df_wbcd.shape)                     
print(df_wbcd["diagnosis"].value_counts()) 
print(df_wbcd.head())

df_wbcd["diagnosis"] = df_wbcd["diagnosis"].map({"M": 1, "B": 0})

X = df_wbcd.drop(columns=["diagnosis"])
y = df_wbcd["diagnosis"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

print("Entrenamiento:", X_train.shape, "| Prueba:", X_test.shape)

scaler = StandardScaler()

X_train_esc = scaler.fit_transform(X_train)

X_test_esc = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_esc, y_train)
pred_knn = knn.predict(X_test_esc)

arbol = DecisionTreeClassifier(max_depth=4, random_state=42)
arbol.fit(X_train, y_train)
pred_arbol = arbol.predict(X_test)

print("Matriz de confusión k-NN (con escalado):")
print(confusion_matrix(y_test, pred_knn))
print()
print("Matriz de confusión Árbol de Decisión (sin escalar):")
print(confusion_matrix(y_test, pred_arbol))

knn_sin_escalar = KNeighborsClassifier(n_neighbors=5)
knn_sin_escalar.fit(X_train, y_train)
pred_knn_sin = knn_sin_escalar.predict(X_test)
print()
print("Matriz de confusión k-NN SIN escalar:")
print(confusion_matrix(y_test, pred_knn_sin))

arbol_esc = DecisionTreeClassifier(max_depth=4, random_state=42)
arbol_esc.fit(X_train_esc, y_train)
print()
print("Matriz de confusión Árbol CON escalado:")
print(confusion_matrix(y_test, arbol_esc.predict(X_test_esc)))

""" Evaluación Teórica / Decisión de Negocios

1. En este escenario médico, ¿qué implica un Error Tipo II (Falso Negativo) y por qué cuesta vidas?
2. ¿Por qué crees que el Árbol de Decisión no falló estrepitosamente incluso si no hubieses escalado los datos?

*Respuestas:*

1. Un falso negativo es una paciente con tumor maligno a quien el modelo clasifica como benigna.
Sale de la clínica sin tratamiento, el tumor sigue creciendo y el diagnóstico llega tarde, cuando
las opciones de tratamiento y la supervivencia ya son menores. El error contrario (falso positivo,
una paciente sana marcada como maligna) cuesta estudios adicionales, dinero y angustia, pero se
corrige con una biopsia. Por eso en medicina se prioriza reducir los falsos negativos (alta
sensibilidad o recall), aunque suban un poco los falsos positivos. En la matriz de confusión es el
valor de abajo a la izquierda: en mi corrida, k-NN con datos escalados y el árbol tuvieron 3 falsos
negativos cada uno, y k-NN sin escalar tuvo 5.

2. Porque el árbol no calcula distancias. Solo hace preguntas de umbral sobre una columna a la vez
(por ejemplo "¿área > 700?") y escalar una columna no cambia el orden de sus valores: el mismo corte
separa a los mismos pacientes, solo cambia el número del umbral. Se comprobó en el código: la matriz
del árbol es idéntica con y sin escalado. k-NN, en cambio, mide distancias entre pacientes, y una
columna con valores grandes como area (cientos) pesa mucho más que smoothness (decimales). En esta
prueba k-NN sin escalar mantuvo una exactitud global parecida (95.6 %), pero dejó pasar 5 casos de
cáncer frente a 3 con escalado, que es justo el error más grave.
"""
