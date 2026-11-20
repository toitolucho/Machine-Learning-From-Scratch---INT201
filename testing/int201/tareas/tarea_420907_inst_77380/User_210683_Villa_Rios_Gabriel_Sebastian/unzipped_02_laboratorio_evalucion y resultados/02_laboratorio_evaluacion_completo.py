# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


# 1. CARGA DE DATOS Y EXPLORACION
print("\n1. CARGA DE DATOS Y EXPLORACION")
# Es el mismo conjunto de datos WBCD, incluido dentro de scikit-learn.
datos = load_breast_cancer()
df_wbcd = pd.DataFrame(datos.data, columns=datos.feature_names)
# En este laboratorio usamos M = 1 (maligno) y B = 0 (benigno).
# En sklearn el target original es 0 = maligno, 1 = benigno.
df_wbcd["diagnosis"] = 1 - datos.target

print("Primeras 5 filas:")
print(df_wbcd.head())
print("\nDimensiones del dataset:", df_wbcd.shape)
print("\nCantidad por diagnostico (0 = benigno, 1 = maligno):")
print(df_wbcd["diagnosis"].value_counts().sort_index())
print("\nValores faltantes:", df_wbcd.isnull().sum().sum())


# 2. PREPROCESAMIENTO
print("\n2. PREPROCESAMIENTO")
# diagnosis ya se encuentra convertida a binario (M=1, B=0).
X = df_wbcd.drop(columns=["diagnosis"])
y = df_wbcd["diagnosis"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print("Datos de entrenamiento:", X_train.shape[0])
print("Datos de prueba:", X_test.shape[0])


# 3. ESCALAMIENTO (SOLO PARA k-NN)
print("\n3. ESCALAMIENTO")
escalador = StandardScaler()
X_train_escalado = escalador.fit_transform(X_train)
X_test_escalado = escalador.transform(X_test)
print("Escalamiento realizado con StandardScaler.")


# 4. MODELADO Y MATRICES DE CONFUSION
print("\n4. MODELOS Y MATRICES DE CONFUSION")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_escalado, y_train)
pred_knn = knn.predict(X_test_escalado)

arbol = DecisionTreeClassifier(max_depth=4, random_state=42)
arbol.fit(X_train, y_train)  # El arbol no necesita escalamiento.
pred_arbol = arbol.predict(X_test)

print("\nMatriz de confusion de KNN (con escalamiento):")
print(confusion_matrix(y_test, pred_knn, labels=[0, 1]))
print("Exactitud KNN:", round(accuracy_score(y_test, pred_knn) * 100, 2), "%")

print("\nMatriz de confusion del Arbol de Decision (sin escalamiento):")
print(confusion_matrix(y_test, pred_arbol, labels=[0, 1]))
print("Exactitud Arbol:", round(accuracy_score(y_test, pred_arbol) * 100, 2), "%")

# Experimento adicional pedido en el reto: KNN sin escalamiento.
knn_sin_escalar = KNeighborsClassifier(n_neighbors=5)
knn_sin_escalar.fit(X_train, y_train)
pred_knn_sin_escalar = knn_sin_escalar.predict(X_test)
print("\nMatriz de confusion de KNN SIN escalamiento:")
print(confusion_matrix(y_test, pred_knn_sin_escalar, labels=[0, 1]))
print("Exactitud KNN sin escalar:", round(accuracy_score(y_test, pred_knn_sin_escalar) * 100, 2), "%")

# Para verificar directamente que el arbol es casi insensible al escalamiento.
arbol_escalado = DecisionTreeClassifier(max_depth=4, random_state=42)
arbol_escalado.fit(X_train_escalado, y_train)
pred_arbol_escalado = arbol_escalado.predict(X_test_escalado)
print("\nExactitud Arbol CON escalamiento:",
      round(accuracy_score(y_test, pred_arbol_escalado) * 100, 2), "%")

print("\nREPORTE DE CLASIFICACION - KNN ESCALADO:")
print(classification_report(y_test, pred_knn, target_names=["Benigno", "Maligno"], zero_division=0))
print("Nota: matrices en orden [Benigno (0), Maligno (1)].")
print("En la matriz, un falso negativo es la fila Maligno, columna Benigno.")


# 5. EVALUACION TEORICA / DECISION DE NEGOCIOS
print("\n5. RESPUESTAS TEORICAS")
print("""
1. ¿Que implica un error tipo II (falso negativo) y por que es peligroso?
   Ocurre cuando un tumor realmente maligno se clasifica como benigno.
   Esto puede retrasar otros estudios y la atencion necesaria. En un
   contexto clinico, esa demora puede empeorar el pronostico del paciente.
   Por eso es importante observar los falsos negativos y la sensibilidad
   del modelo, no solo su exactitud general.

2. ¿Por que el Arbol de Decision no falla gravemente sin escalar los datos?
   Porque el Arbol de Decision toma decisiones mediante comparaciones
   y puntos de corte de cada caracteristica, en vez de calcular
   distancias entre muestras. Cambiar la escala de una variable
   generalmente no cambia el orden de sus valores ni las particiones
   que el arbol puede realizar. KNN, en cambio, utiliza distancias y
   puede verse dominado por variables con valores numericos grandes.

CONCLUSION:
El escalamiento es importante para KNN porque compara distancias.
El Arbol de Decision normalmente no lo necesita. Para aplicaciones
medicas reales, estos resultados son solo educativos: ningun modelo
puede usarse para diagnosticar pacientes sin validacion clinica rigurosa.
""")
