# -*- coding: utf-8 -*-
"""Construye solucion_P01.ipynb (notebook de solución del docente). Uso: python construir_notebook_solucion.py"""
import json
import os

CELDAS = []


def md(t):
    CELDAS.append({"cell_type": "markdown", "metadata": {}, "source": t.strip("\n")})


def code(t):
    CELDAS.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                   "source": t.strip("\n")})


# =============================================================================
md("""
# Solución de referencia – Proyecto P01
## Detección de inicios de sesión sospechosos en el Sistema Académico (SIA)

**Documento reservado para el docente.** Este notebook desarrolla la solución paso a paso. Cada decisión se
presenta con el formato **Decisión → Evidencia → Justificación**, que es el mismo que se espera en la bitácora
del estudiante.

| Sección | Contenido |
|---|---|
| 1 | Carga de datos |
| 2 | Comprensión de los datos (Fase 1) |
| 3 | Preparación de los datos (Fase 2) |
| 4 | Contraste de hipótesis |
| 5 | Modelado (Fase 3) |
| 6 | Evidencia de las fugas de información |
| 7 | Evaluación, umbral y validación cruzada (Fase 4) |
| 8 | Conclusiones y resumen ejecutivo (Fase 5) |
| 9 | Anexo: tareas de la defensa oral con su resultado |
""")

md("## 1. Carga de datos")
code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, confusion_matrix,
                             ConfusionMatrixDisplay)

SEMILLA = 42
pd.set_option("display.max_columns", 30)

crudo = pd.read_csv("../estudiante/data/logins_sia.csv")
print("Dimensiones:", crudo.shape)
crudo.head()
""")

# =============================================================================
md("""
## 2. Comprensión de los datos (Fase 1)

### 2.1 Tipos de datos y valores faltantes
""")
code("""
crudo.info()
""")
md("""
**Observación.** Solo `pais_geo` tiene valores faltantes. `fecha_hora` está como texto (`object`): contiene la
hora del intento, que puede convertirse en una variable útil (sección 3.6).
""")

md("### 2.2 Distribución de la variable objetivo")
code("""
print(crudo["es_ataque"].value_counts())
print(crudo["es_ataque"].value_counts(normalize=True).round(3))
""")
md("""
**Observación.** Solo ≈ 5 % de los registros son ataques: las clases están **desbalanceadas**. Un modelo que
siempre responda «normal» tendría ≈ 95 % de exactitud sin detectar ningún ataque, por lo que la exactitud no
puede ser la métrica principal.
""")

md("### 2.3 Registros duplicados")
code("""
print("Filas duplicadas exactas:", crudo.duplicated().sum())
print("evento_id repetidos     :", crudo["evento_id"].duplicated().sum())
""")
md("""
**Observación.** Hay 120 filas idénticas, incluido `evento_id`. Coincide con la condición del caso: el servidor
de registros reenvía eventos al reiniciarse.
""")

md("### 2.4 Estadística descriptiva de las variables numéricas")
code("""
crudo.describe().T
""")
md("""
**Observación.**
- `intentos_fallidos_previos_1h` llega a **999**: valor imposible (el enunciado indica errores del contador).
- `segundos_desde_intento_anterior` tiene mínimo **−1**: un tiempo negativo es imposible (relojes desincronizados).
- `segundos_desde_intento_anterior` varía de 0 a más de 100 000: escala muy distinta a las variables 0/1.
""")
code("""
print("intentos = 999   :", (crudo["intentos_fallidos_previos_1h"] >= 999).sum())
print("segundos negativos:", (crudo["segundos_desde_intento_anterior"] < 0).sum())
""")

md("### 2.5 Columnas categóricas: valores distintos")
code("""
print(crudo.nunique().sort_values())
""")
md("""
**Observación.**
- `version_app` tiene **un solo valor**: no puede ayudar a distinguir clases.
- `evento_id`, `usuario` e `ip_origen` tienen casi un valor distinto por fila: son **identificadores**.
""")
code("""
print(crudo["navegador"].value_counts().head(15))
print()
print(crudo["pais_geo"].value_counts(dropna=False))
""")
md("""
**Observación.** Un mismo valor aparece escrito de varias formas («Chrome», « Chrome», «CHROME»; «Bolivia»,
«BOLIVIA», «BO»). Si se codifica sin corregir, el modelo los tratará como categorías diferentes.
""")

md("### 2.6 Registros que no son usuarios reales")
code("""
qa = crudo["usuario"].str.startswith("qa_")
print("Registros de cuentas qa_bot_*:", qa.sum())
print(crudo.loc[qa, ["usuario", "ip_origen", "intentos_fallidos_previos_1h",
                     "segundos_desde_intento_anterior", "es_ataque"]].head())
print("Etiqueta de esos registros:", crudo.loc[qa, "es_ataque"].value_counts().to_dict())
""")
md("""
**Observación.** Las cuentas de QA tienen el comportamiento típico de un ataque (muchos intentos fallidos, muy
rápidos, de madrugada), pero están etiquetadas como **normales**. No representan a usuarios del SIA.
""")

# =============================================================================
md("""
## 3. Preparación de los datos (Fase 2)

Cada paso se registra con el formato de la bitácora.
""")

md("""
### 3.1 Eliminación de duplicados
- **Decisión:** eliminar las 120 filas duplicadas **antes** de dividir los datos.
- **Evidencia:** sección 2.3; el enunciado indica que los registros se reenvían.
- **Justificación:** un duplicado no es un nuevo intento. Si se conserva, la misma fila puede quedar en
  entrenamiento y en prueba, y la evaluación resultaría optimista.
""")
code("""
df = crudo.drop_duplicates().copy()
print("Registros:", len(crudo), "->", len(df))
""")

md("""
### 3.2 Exclusión de las cuentas de prueba (QA)
- **Decisión:** excluir los registros de `qa_bot_*`.
- **Evidencia:** sección 2.6.
- **Justificación:** el modelo debe aprender de usuarios reales. Estos registros enseñan que «muchos intentos
  rápidos de madrugada» puede ser normal, lo contrario de lo que se busca detectar (sección 6 lo cuantifica).
""")
code("""
df = df[~df["usuario"].str.startswith("qa_")].copy()
print("Registros sin QA:", len(df))
print(df["es_ataque"].value_counts().to_dict())
""")

md("""
### 3.3 Normalización de categorías
- **Decisión:** quitar espacios, unificar mayúsculas/minúsculas y unificar los códigos de país.
- **Evidencia:** sección 2.5.
- **Justificación:** evita que una misma categoría se convierta en varias columnas al aplicar One-Hot.
""")
code("""
df["navegador"] = df["navegador"].str.strip().str.lower()
df["pais_geo"] = df["pais_geo"].str.strip().str.lower().replace({"bo": "bolivia"})
print("Navegadores:", sorted(df["navegador"].unique()))
print("Países     :", sorted(df["pais_geo"].dropna().unique()))
""")

md("""
### 3.4 Valores faltantes en `pais_geo`
Antes de decidir, se compara la tasa de ataque de los registros con y sin país.
""")
code("""
sin_pais = df["pais_geo"].isna()
print("Registros sin país:", sin_pais.sum())
print("Tasa de ataque SIN país:", round(df.loc[sin_pais, "es_ataque"].mean(), 3))
print("Tasa de ataque CON país:", round(df.loc[~sin_pais, "es_ataque"].mean(), 3))
print("Ataques que se perderían con dropna():", df.loc[sin_pais, "es_ataque"].sum(),
      "de", df["es_ataque"].sum())
""")
md("""
- **Decisión:** reemplazar el faltante por la categoría **«desconocido»** y resumir el país en la variable
  `origen` (bolivia / extranjero / desconocido).
- **Evidencia:** la tasa de ataque sin país es varias veces mayor; eliminar esos registros quitaría ≈ 30 % de los
  ataques.
- **Justificación:** el faltante **es información** (VPN, Tor). Agrupar en tres valores evita categorías con
  muy pocos registros.
""")
code("""
df["pais_geo"] = df["pais_geo"].fillna("desconocido")
df["origen"] = np.select([df["pais_geo"] == "bolivia", df["pais_geo"] == "desconocido"],
                         ["bolivia", "desconocido"], default="extranjero")
print(pd.crosstab(df["origen"], df["es_ataque"], normalize="index").round(3))
""")

md("""
### 3.5 Valores imposibles
- **Decisión:** convertir `intentos = 999` y `segundos < 0` en faltantes (`NaN`). La imputación con la
  **mediana** se realiza **dentro del pipeline** (sección 5), para que se calcule solo con datos de entrenamiento.
- **Evidencia:** sección 2.4.
- **Justificación:** 999 intentos en una hora o un tiempo negativo no son posibles. Conservarlos distorsiona el
  escalado y las distancias de k-NN. Se usa la mediana porque ambas variables tienen valores extremos.
""")
code("""
df.loc[df["intentos_fallidos_previos_1h"] >= 999, "intentos_fallidos_previos_1h"] = np.nan
df.loc[df["segundos_desde_intento_anterior"] < 0, "segundos_desde_intento_anterior"] = np.nan
print(df[["intentos_fallidos_previos_1h", "segundos_desde_intento_anterior"]].isna().sum())
""")

md("""
### 3.6 Nuevas variables a partir de las existentes
- **Decisión:** extraer `hora` y `madrugada` (00:00–05:59) de `fecha_hora`; aplicar logaritmo a
  `segundos_desde_intento_anterior`.
- **Evidencia:** la hipótesis H1 se refiere a la madrugada; el histograma de segundos tiene una cola muy larga.
- **Justificación:** la fecha completa no se repite en el futuro, pero la hora sí. El logaritmo reduce la
  diferencia entre «2 segundos» y «2 días» a una escala manejable.
""")
code("""
df["hora"] = pd.to_datetime(df["fecha_hora"]).dt.hour
df["madrugada"] = (df["hora"] < 6).astype(int)
df["log_segundos"] = np.log10(df["segundos_desde_intento_anterior"] + 1)

fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
df["segundos_desde_intento_anterior"].plot.hist(bins=50, ax=ax[0], title="Segundos (original)")
df["log_segundos"].plot.hist(bins=50, ax=ax[1], title="log10(segundos + 1)")
plt.tight_layout(); plt.show()
""")

md("""
### 3.7 Selección de columnas

| Columna | Decisión | Justificación |
|---|---|---|
| `evento_id`, `usuario`, `ip_origen` | Excluir | Identificadores: casi un valor por fila; no generalizan a usuarios nuevos |
| `version_app` | Excluir | Constante: un solo valor |
| `tema_interfaz` | Excluir | Sin relación lógica con un ataque (se verifica abajo) |
| `fecha_hora` | Reemplazar | Se usa `hora` / `madrugada` |
| `pais_geo` | Reemplazar | Se usa `origen` |
| `segundos_desde_intento_anterior` | Reemplazar | Se usa `log_segundos` |
| `duracion_sesion_min` | **Excluir (fuga)** | Solo existe cuando la sesión termina, después de la predicción |
| `bloqueado_por_soporte` | **Excluir (fuga)** | Se registra 1 a 3 días después, al cerrar el ticket |
| `rol` | Conservar para H2, no como predictor | La tasa de ataque es similar en los tres roles (sección 4) |

Evidencia de las dos fugas y de la columna irrelevante:
""")
code("""
print("Coincidencia bloqueado_por_soporte = es_ataque:",
      round((df["bloqueado_por_soporte"] == df["es_ataque"]).mean(), 3))
print("Duración media de la sesión por clase (min):")
print(df.groupby("es_ataque")["duracion_sesion_min"].mean().round(1))
print("Tasa de ataque por tema de interfaz:")
print(df.groupby("tema_interfaz")["es_ataque"].mean().round(3))
""")
code("""
NUMERICAS = ["intentos_fallidos_previos_1h", "log_segundos", "dispositivo_nuevo", "usa_vpn", "madrugada"]
CATEGORICAS = ["navegador", "sistema_operativo", "origen"]
X = df[NUMERICAS + CATEGORICAS]
y = df["es_ataque"]
print("Matriz final:", X.shape, "| ataques:", y.sum())
""")

# =============================================================================
md("## 4. Contraste de hipótesis")
code("""
fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
pd.crosstab(df["hora"], df["es_ataque"], normalize="columns").plot.bar(ax=ax[0], title="Distribución por hora")
df.groupby("rol")["es_ataque"].mean().plot.bar(ax=ax[1], title="Tasa de ataque por rol")
plt.tight_layout(); plt.show()

print("H1 - % de ataques de madrugada :", round(df.loc[df.es_ataque == 1, "madrugada"].mean(), 3))
print("H1 - % de normales de madrugada:", round(df.loc[df.es_ataque == 0, "madrugada"].mean(), 3))
print("H2 - tasa de ataque por rol    :", df.groupby("rol")["es_ataque"].mean().round(3).to_dict())
print("H2 - ataques por rol (conteo)  :", df.loc[df.es_ataque == 1, "rol"].value_counts().to_dict())
print("H4 - % de ataques sin país     :", round((df.loc[df.es_ataque == 1, "origen"] == "desconocido").mean(), 3))
""")
md("""
| Hipótesis | Resultado | Evidencia |
|---|---|---|
| **H1.** La mayoría de los ataques ocurre de madrugada | **Se cumple** | ≈ 55 % de los ataques ocurre entre 00:00 y 05:59, frente a ≈ 6 % de los intentos normales |
| **H2.** Las cuentas docentes son las más atacadas | **No se cumple** | La tasa de ataque es ≈ 5 % en los tres roles. En conteo absoluto hay más ataques a estudiantes, porque hay más estudiantes |
| **H3.** `bloqueado_por_soporte` dará un detector casi perfecto | **No se cumple en la práctica** | Coincide ≈ 99 % con la etiqueta, pero se registra días después: no existe al momento del inicio de sesión (fuga de información, sección 6) |
| **H4.** Los registros sin país pueden eliminarse | **No se cumple** | ≈ 30 % de los ataques no tiene país; eliminarlos quita casi un tercio de los ataques |
""")

# =============================================================================
md("""
## 5. Modelado (Fase 3)

- División **estratificada** 75 % / 25 % para mantener la proporción de ataques en ambos conjuntos.
- **Pipeline**: la imputación, el escalado y la codificación se ajustan solo con los datos de entrenamiento.
- `class_weight="balanced"` compensa el desbalance en los modelos que lo permiten.
""")
code("""
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=SEMILLA)
print("Entrenamiento:", X_train.shape, "ataques:", y_train.sum())
print("Prueba       :", X_test.shape, "ataques:", y_test.sum())

def preprocesador(numericas=NUMERICAS, categoricas=CATEGORICAS, escalar=True):
    pasos_num = [("imputar", SimpleImputer(strategy="median"))]
    if escalar:
        pasos_num.append(("escalar", StandardScaler()))
    return ColumnTransformer([
        ("num", Pipeline(pasos_num), numericas),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categoricas)])

MODELOS = {
    "Regresión logística": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "k-NN (k=7)": KNeighborsClassifier(n_neighbors=7),
    "Árbol (max_depth=5)": DecisionTreeClassifier(max_depth=5, class_weight="balanced", random_state=SEMILLA),
    "Random Forest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=SEMILLA),
}

def evaluar(pipe, Xtr=X_train, ytr=y_train, Xte=X_test, yte=y_test):
    pipe.fit(Xtr, ytr)
    p = pipe.predict(Xte)
    return {"exactitud": accuracy_score(yte, p), "precisión": precision_score(yte, p, zero_division=0),
            "recall": recall_score(yte, p), "falsas alarmas (FP)": int(((p == 1) & (yte == 0)).sum()),
            "ataques no detectados (FN)": int(((p == 0) & (yte == 1)).sum())}

resultados, pipes = {}, {}
for nombre, modelo in MODELOS.items():
    pipes[nombre] = Pipeline([("prep", preprocesador()), ("modelo", modelo)])
    resultados[nombre] = evaluar(pipes[nombre])
tabla = pd.DataFrame(resultados).T
tabla.loc["Modelo perezoso (siempre 0)"] = [1 - y_test.mean(), 0, 0, 0, int(y_test.sum())]
tabla.round(3)
""")
code("""
fig, axes = plt.subplots(1, 4, figsize=(16, 3.6))
for ax, (nombre, pipe) in zip(axes, pipes.items()):
    ConfusionMatrixDisplay.from_estimator(pipe, X_test, y_test, ax=ax, colorbar=False,
                                          display_labels=["normal", "ataque"])
    ax.set_title(nombre)
plt.tight_layout(); plt.show()
""")
md("""
**Lectura.**
- Todos los modelos superan ampliamente al modelo perezoso en recall (0 → 0.65–0.93).
- La **regresión logística** detecta más ataques (mayor recall), con más falsas alarmas.
- El **Random Forest** tiene el mejor equilibrio entre precisión y recall.
- **k-NN** tiene alta precisión pero deja escapar más ataques: no es la opción preferida para la DTI.
""")

# =============================================================================
md("""
## 6. Evidencia de las fugas de información y del efecto de las cuentas QA

Se repite el Random Forest agregando cada columna problemática, para mostrar por qué se excluyeron.
""")
code("""
def rf():
    return RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=SEMILLA)

experimentos = {}
for extra in ["bloqueado_por_soporte", "duracion_sesion_min"]:
    cols = NUMERICAS + [extra] + CATEGORICAS
    Xtr, Xte = X_train.join(df[[extra]]), X_test.join(df[[extra]])
    pipe = Pipeline([("prep", preprocesador(NUMERICAS + [extra])), ("modelo", rf())])
    experimentos[f"RF + {extra} (fuga)"] = evaluar(pipe, Xtr[cols], y_train, Xte[cols], y_test)

# Efecto de conservar las cuentas QA: se agregan solo al entrenamiento
qa_df = crudo.drop_duplicates()
qa_df = qa_df[qa_df["usuario"].str.startswith("qa_")].copy()
qa_df["navegador"] = qa_df["navegador"].str.strip().str.lower()
qa_df["origen"] = "bolivia"
qa_df["hora"] = pd.to_datetime(qa_df["fecha_hora"]).dt.hour
qa_df["madrugada"] = (qa_df["hora"] < 6).astype(int)
qa_df["log_segundos"] = np.log10(qa_df["segundos_desde_intento_anterior"].clip(lower=0) + 1)
Xtr_qa = pd.concat([X_train, qa_df[NUMERICAS + CATEGORICAS]])
ytr_qa = pd.concat([y_train, qa_df["es_ataque"]])
experimentos["RF entrenado CON cuentas QA"] = evaluar(
    Pipeline([("prep", preprocesador()), ("modelo", rf())]), Xtr_qa, ytr_qa, X_test, y_test)
experimentos["RF limpio (referencia)"] = resultados["Random Forest"]
pd.DataFrame(experimentos).T.round(3)
""")
md("""
**Lectura.**
- Con `bloqueado_por_soporte` o `duracion_sesion_min` las métricas se acercan a 1.0. Es un resultado
  **engañoso**: esas columnas no existen cuando el usuario presiona «Ingresar».
- Entrenar con las cuentas QA reduce el recall: el modelo aprende que el patrón de ataque puede ser «normal».
""")

# =============================================================================
md("""
## 7. Evaluación, umbral y validación cruzada (Fase 4)

### 7.1 Métrica principal
La DTI prioriza **no dejar pasar ataques** → métrica principal: **recall**. Condición adicional: no más de la
mitad de las alertas pueden ser falsas → **precisión ≥ 0.5**.

### 7.2 Ajuste del umbral del Random Forest
""")
code("""
rf_pipe = pipes["Random Forest"]
prob = rf_pipe.predict_proba(X_test)[:, 1]
filas = []
for u in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    p = (prob >= u).astype(int)
    filas.append({"umbral": u, "precisión": precision_score(y_test, p, zero_division=0),
                  "recall": recall_score(y_test, p), "alertas": int(p.sum()),
                  "falsas alarmas": int(((p == 1) & (y_test == 0)).sum())})
umbrales = pd.DataFrame(filas).set_index("umbral").round(3)
umbrales
""")
code("""
cumple = umbrales[umbrales["precisión"] >= 0.5]
print("Umbrales que cumplen precisión >= 0.5:")
print(cumple)
UMBRAL = 0.3
print("\\nUmbral elegido:", UMBRAL)
print(umbrales.loc[UMBRAL])
""")
md("""
**Decisión: umbral = 0.3.**
- Todos los umbrales de 0.1 a 0.7 cumplen la condición de precisión ≥ 0.5.
- **0.1** tiene el mayor recall, pero su precisión (≈ 0.53) está en el límite de la condición de la DTI: un
  pequeño cambio en los datos la haría incumplir, y genera ≈ 3.5 veces más falsas alarmas que 0.3 para detectar
  solo 2 ataques más.
- **0.3** detecta los mismos ataques que 0.2 con la mitad de falsas alarmas, y mantiene un margen amplio
  (precisión ≈ 0.80).
- Frente al umbral por defecto (0.5), detecta más ataques a cambio de pocas solicitudes adicionales de 2FA.
""")

md("### 7.3 Validación cruzada (estabilidad)")
code("""
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)
for nombre in ["Regresión logística", "Random Forest"]:
    pipe = Pipeline([("prep", preprocesador()), ("modelo", MODELOS[nombre])])
    s = cross_val_score(pipe, X, y, cv=cv, scoring="recall")
    print(f"{nombre:<22} recall por fold: {np.round(s, 3)}  media={s.mean():.3f}  desv={s.std():.3f}")
""")

md("### 7.4 Importancia de variables (Random Forest)")
code("""
nombres = rf_pipe.named_steps["prep"].get_feature_names_out()
imp = pd.Series(rf_pipe.named_steps["modelo"].feature_importances_, index=nombres).sort_values()
imp.tail(12).plot.barh(figsize=(7, 4), title="Importancia de variables")
plt.tight_layout(); plt.show()
""")
md("""
**Lectura.** Las variables más útiles son coherentes con la seguridad: segundos entre intentos (ataques
automatizados muy rápidos), intentos fallidos, dispositivo nuevo, madrugada y origen desconocido o extranjero.
""")

# =============================================================================
md("""
## 8. Conclusiones y resumen ejecutivo (Fase 5)

**Ejemplo de resumen ejecutivo para la DTI (sin jerga técnica):**

> Se desarrolló un detector que, al momento de iniciar sesión, estima si el intento es sospechoso. Con los datos
> de septiembre y octubre, el detector identifica aproximadamente **9 de cada 10 ataques**, y de cada 10 alertas
> la gran mayoría corresponden a ataques reales. A los usuarios marcados se les solicitará un código 2FA.
>
> Las señales más fuertes de un ataque son: intentos muy rápidos y repetidos, dispositivos no reconocidos,
> conexiones de madrugada y conexiones cuyo país no puede determinarse.
>
> **Limitaciones:** un atacante que use un dispositivo conocido, desde Bolivia y en horario normal (por ejemplo,
> con una contraseña robada) es difícil de detectar. **Se recomienda** registrar el historial de ubicaciones de
> cada usuario y si el correo de recuperación fue modificado recientemente, y reentrenar el modelo cada mes.
> Las cuentas de prueba de QA deben marcarse en el sistema para no confundir al detector.
""")

# =============================================================================
md("""
## 9. Anexo: tareas de la defensa oral

Cada tarea corresponde a la Parte B de `defensa_oral.md`. El resultado que se obtiene aquí es la referencia;
el del estudiante puede variar ligeramente según sus decisiones.
""")

md("### B1. Cambiar el umbral a 0.3 y reportar el efecto")
code("""
p03 = (prob >= 0.3).astype(int)
p05 = (prob >= 0.5).astype(int)
for nombre, p in [("umbral 0.5", p05), ("umbral 0.3", p03)]:
    print(f"{nombre}: recall={recall_score(y_test, p):.3f}  precisión={precision_score(y_test, p):.3f}"
          f"  alertas={p.sum()}  FN={((p == 0) & (y_test == 1)).sum()}")
""")

md("### B2. Cuántos ataques se pierden si se eliminan los registros sin país")
code("""
print("Ataques totales           :", df["es_ataque"].sum())
print("Ataques sin país (perdidos):", df.loc[df["origen"] == "desconocido", "es_ataque"].sum())
""")

md("### B3. Clasificar un intento nuevo escrito a mano")
code("""
nuevo = pd.DataFrame([{
    "intentos_fallidos_previos_1h": 0, "log_segundos": np.log10(86400 + 1), "dispositivo_nuevo": 0,
    "usa_vpn": 0, "madrugada": 0, "navegador": "chrome", "sistema_operativo": "Windows", "origen": "bolivia"}])
print("P(ataque) – atacante con contraseña robada, de día, desde Bolivia:",
      round(rf_pipe.predict_proba(nuevo)[0, 1], 3))
nuevo2 = nuevo.assign(intentos_fallidos_previos_1h=8, log_segundos=np.log10(2 + 1), dispositivo_nuevo=1,
                      madrugada=1, navegador="python-requests", sistema_operativo="Linux", origen="desconocido")
print("P(ataque) – ataque automatizado de madrugada:", round(rf_pipe.predict_proba(nuevo2)[0, 1], 3))
""")

md("### B4. k-NN sin escalar frente a k-NN escalado (con los segundos originales, sin logaritmo)")
code("""
NUM_CRUDAS = ["intentos_fallidos_previos_1h", "segundos_desde_intento_anterior",
              "dispositivo_nuevo", "usa_vpn", "madrugada"]
Xtr_c = df.loc[X_train.index, NUM_CRUDAS + CATEGORICAS]
Xte_c = df.loc[X_test.index, NUM_CRUDAS + CATEGORICAS]
for escalar in (False, True):
    pipe = Pipeline([("prep", preprocesador(NUM_CRUDAS, escalar=escalar)), ("modelo", KNeighborsClassifier(7))])
    r = evaluar(pipe, Xtr_c, y_train, Xte_c, y_test)
    print(f"escalar={escalar!s:<5} recall={r['recall']:.3f}  precisión={r['precisión']:.3f}")
print("Desviación estándar de cada variable numérica (sin escalar):")
print(Xtr_c[NUM_CRUDAS].std().round(2))
""")

md("### B5. Validación cruzada del modelo elegido (recall, 5 folds)")
code("""
s = cross_val_score(Pipeline([("prep", preprocesador()), ("modelo", rf())]), X, y, cv=cv, scoring="recall")
print("Recall por fold:", np.round(s, 3), "| media:", round(s.mean(), 3), "| desviación:", round(s.std(), 3))
""")

md("### B6. Tasa de ataque por rol (hipótesis H2)")
code("""
print(df.groupby("rol")["es_ataque"].agg(registros="size", ataques="sum", tasa="mean").round(3))
""")

md("### B7. Árbol de decisión de profundidad 3 e interpretación de su primera regla")
code("""
from sklearn.tree import export_text
arbol = Pipeline([("prep", preprocesador(escalar=False)),   # sin escalar: reglas en unidades reales
                  ("modelo", DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=SEMILLA))])
print(evaluar(arbol))
print(export_text(arbol.named_steps["modelo"],
                  feature_names=list(arbol.named_steps["prep"].get_feature_names_out()), max_depth=2))
""")

md("### B8. Falsas alarmas: ¿cuántos usuarios legítimos recibirían 2FA?")
code("""
cm = confusion_matrix(y_test, (prob >= UMBRAL).astype(int))
tn, fp, fn, tp = cm.ravel()
print(f"Umbral {UMBRAL}: TN={tn} FP={fp} FN={fn} TP={tp}")
print(f"Porcentaje de intentos legítimos que recibirían 2FA: {fp / (fp + tn):.1%}")
""")

nb = {"cells": CELDAS, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"c{i:03d}"
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solucion_P01.ipynb")
with open(ruta, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("OK", ruta, len(CELDAS), "celdas")
