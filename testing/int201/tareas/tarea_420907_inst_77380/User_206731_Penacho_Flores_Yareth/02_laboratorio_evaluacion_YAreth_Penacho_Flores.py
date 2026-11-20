# -*- coding: utf-8 -*-
"""02_Laboratorio_Evaluacion.ipynb

# Laboratorio Evaluado: WBCD y Evaluación Multimodelo

**Reto Autónomo: Clínica Oncológica**

Eres el Consultor IA de un hospital. El dataset WBCD contiene radios y perímetros de células. Debes entrenar k-NN y Árboles de Decisión, y validar qué pasa si no escalas los datos.

## 1. Carga de Datos y Exploración
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score

# ============================================================
# 1. Carga de datos y exploración
# ============================================================
base = ["radio", "textura", "perimetro", "area", "suavidad",
        "compacidad", "concavidad", "puntos_concavos", "simetria", "dim_fractal"]
columnas = (["id", "diagnosis"]
            + [f"{b}_media" for b in base]
            + [f"{b}_error" for b in base]
            + [f"{b}_peor" for b in base])

# Dataset WDBC (Wisconsin Diagnostic Breast Cancer) incluido en scikit-learn
from sklearn.datasets import load_breast_cancer
d = load_breast_cancer()
df_wbcd = pd.DataFrame(d.data, columns=columnas[2:])
df_wbcd.insert(0, "diagnosis", ["M" if t == 0 else "B" for t in d.target])  # en sklearn 0 = maligno
df_wbcd.insert(0, "id", range(len(df_wbcd)))

print("Dimensiones:", df_wbcd.shape)
print(df_wbcd["diagnosis"].value_counts(), "\n")

# ============================================================
# 2. Preprocesamiento
# ============================================================
df_wbcd["diagnosis"] = df_wbcd["diagnosis"].map({"M": 1, "B": 0})   # 1 = maligno, 0 = benigno

X = df_wbcd.drop(columns=["id", "diagnosis"])
y = df_wbcd["diagnosis"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

# ============================================================
# 3. Escalamiento (solo para k-NN)
# ============================================================
scaler = StandardScaler()
X_train_esc = scaler.fit_transform(X_train)   
X_test_esc = scaler.transform(X_test)         

# ============================================================
# 4. Modelado y matrices de confusión
# ============================================================
knn = KNeighborsClassifier(n_neighbors=5).fit(X_train_esc, y_train)
arbol = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train, y_train)

pred_knn = knn.predict(X_test_esc)
pred_arbol = arbol.predict(X_test)

def reportar(nombre, y_real, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_real, y_pred).ravel()
    print(f"=== {nombre} ===")
    print("Matriz de confusión (filas = real, columnas = predicho)")
    print("            Pred B   Pred M")
    print(f"Real B     {tn:6d}   {fp:6d}")
    print(f"Real M     {fn:6d}   {tp:6d}")
    print(f"Accuracy: {accuracy_score(y_real, y_pred):.4f} | "
          f"Recall (sensibilidad maligno): {recall_score(y_real, y_pred):.4f} | "
          f"Falsos negativos: {fn}\n")

reportar("k-NN (escalado)", y_test, pred_knn)
reportar("Árbol de Decisión (sin escalar)", y_test, pred_arbol)

# ---- Validación extra: ¿qué pasa si NO escalamos k-NN? y ¿si escalamos el árbol? ----
knn_sin = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
reportar("k-NN SIN escalar", y_test, knn_sin.predict(X_test))

arbol_esc = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train_esc, y_train)
reportar("Árbol CON datos escalados", y_test, arbol_esc.predict(X_test_esc))

# ============================================================
# Evaluación Teórica / Decisión de Negocios
# ============================================================
"""
1. En este escenario médico, ¿qué implica un Error Tipo II (Falso Negativo)
   y por qué cuesta vidas?

   Un Error Tipo II (falso negativo) ocurre cuando el modelo clasifica como
   BENIGNO un tumor que en realidad es MALIGNO. La paciente se va a casa sin
   tratamiento ni estudios adicionales, el cáncer sigue avanzando sin ser
   detectado y, cuando finalmente se diagnostica, puede estar en una etapa
   mucho más avanzada, con menos opciones terapéuticas y menor probabilidad de
   supervivencia. Un falso positivo, en cambio, solo genera estudios extra
   (por ejemplo una biopsia) y angustia, pero no pone en riesgo la vida. Por
   eso, en este contexto, la métrica clave es el recall (sensibilidad) de la
   clase maligna y no solo el accuracy global. En los resultados, el k-NN
   escalado dejó pasar 4 tumores malignos y el Árbol de Decisión dejó pasar 8.

2. ¿Por qué el Árbol de Decisión no falló estrepitosamente incluso si no
   hubieses escalado los datos?

   Porque el árbol no calcula distancias: cada nodo evalúa una regla del tipo
   "¿variable > umbral?" sobre UNA sola variable a la vez. Escalar es una
   transformación monótona que no cambia el orden de las observaciones dentro
   de cada variable, así que los cortes que el árbol encuentra separan a los
   mismos pacientes, solo cambia el valor numérico del umbral. Por eso el
   árbol da el mismo resultado con datos escalados o sin escalar (91.2 % y 8
   falsos negativos en ambos casos). El k-NN, en cambio, depende de la
   distancia euclidiana: variables con números grandes (como el área, de
   cientos o miles) dominan sobre variables pequeñas (como la suavidad, ~0.1).
   Sin escalar, su accuracy bajó de 95.6 % a 91.2 % y los falsos negativos
   subieron de 4 a 9.
"""
