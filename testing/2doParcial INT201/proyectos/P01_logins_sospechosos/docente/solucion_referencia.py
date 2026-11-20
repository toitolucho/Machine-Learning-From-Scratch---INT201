# -*- coding: utf-8 -*-
"""
P01 – Solución de referencia (CONFIDENCIAL). Calcula los números de la guía docente:
hipótesis, efecto de cada trampa y desempeño de una solución razonable.

    python solucion_referencia.py
"""
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "estudiante", "data", "logins_sia.csv")
SEED = 42


def limpiar(df, quitar_qa=True):
    df = df.drop_duplicates().copy()                                             # T1
    if quitar_qa:
        df = df[~df["usuario"].str.startswith("qa_")]                           # T2
    df["navegador"] = df["navegador"].str.strip().str.title()                    # T8
    df["navegador"] = df["navegador"].replace({"Python-Requests": "python-requests", "Curl": "curl"})
    df["pais_geo"] = df["pais_geo"].str.strip().str.lower().replace({"bo": "bolivia"}).str.title()
    df["pais_geo"] = df["pais_geo"].fillna("Desconocido")                        # T9: nulo informativo
    df["origen"] = np.where(df["pais_geo"] == "Bolivia", "Bolivia",
                            np.where(df["pais_geo"] == "Desconocido", "Desconocido", "Extranjero"))
    df.loc[df["intentos_fallidos_previos_1h"] >= 999, "intentos_fallidos_previos_1h"] = np.nan   # T10
    df.loc[df["segundos_desde_intento_anterior"] < 0, "segundos_desde_intento_anterior"] = np.nan
    for c in ("intentos_fallidos_previos_1h", "segundos_desde_intento_anterior"):
        df[c] = df[c].fillna(df[c].median())
    df["log_segundos"] = np.log10(df["segundos_desde_intento_anterior"] + 1)
    df["hora"] = pd.to_datetime(df["fecha_hora"]).dt.hour                        # T11
    df["madrugada"] = (df["hora"] < 6).astype(int)
    return df


NUM = ["intentos_fallidos_previos_1h", "log_segundos", "dispositivo_nuevo", "usa_vpn", "madrugada"]
CAT = ["navegador", "sistema_operativo", "origen"]


def evaluar(df, num, cat, modelo, nombre):
    X, y = df[num + cat], df["es_ataque"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=SEED)
    prep = ColumnTransformer([("num", StandardScaler(), num),
                              ("cat", OneHotEncoder(handle_unknown="ignore"), cat)])
    pipe = Pipeline([("prep", prep), ("modelo", modelo)]).fit(Xtr, ytr)
    p = pipe.predict(Xte)
    print(f"  {nombre:<55} acc={accuracy_score(yte, p):.3f}  prec={precision_score(yte, p, zero_division=0):.3f}"
          f"  recall={recall_score(yte, p):.3f}")
    return pipe, Xte, yte


def main():
    crudo = pd.read_csv(CSV)
    df = limpiar(crudo)
    print(f"Filas: crudo={len(crudo)}  sin duplicados={len(crudo.drop_duplicates())}  limpio={len(df)}")
    print(f"Ataques en limpio: {df.es_ataque.sum()} ({df.es_ataque.mean():.1%})")

    print("\nHIPÓTESIS")
    atq = df[df.es_ataque == 1]
    print(f"  H1 ataques en madrugada (00-06): {atq.madrugada.mean():.1%}  | normales: {df[df.es_ataque == 0].madrugada.mean():.1%}")
    print("  H2 tasa de ataque por rol:", df.groupby("rol").es_ataque.mean().round(3).to_dict())
    print(f"  H3 bloqueado_por_soporte vs es_ataque coinciden: {(df.bloqueado_por_soporte == df.es_ataque).mean():.1%}")
    nul = crudo.drop_duplicates()
    print(f"  H4 % de ataques con pais_geo vacío: {nul[nul.es_ataque == 1].pais_geo.isna().mean():.1%}"
          f"  (normales: {nul[nul.es_ataque == 0].pais_geo.isna().mean():.1%})")

    print("\nEFECTO DE LAS TRAMPAS (Random Forest, 200 árboles)")
    rf = lambda: RandomForestClassifier(n_estimators=200, random_state=SEED, class_weight="balanced")
    evaluar(df, NUM + ["bloqueado_por_soporte"], CAT, rf(), "T3 con bloqueado_por_soporte (fuga evidente)")
    evaluar(df, NUM + ["duracion_sesion_min"], CAT, rf(), "T4 con duracion_sesion_min (fuga sutil)")
    evaluar(limpiar(crudo, quitar_qa=False), NUM, CAT, rf(), "T2 sin quitar cuentas qa_* (se evalúa sobre todo)")
    df_drop = limpiar(crudo).pipe(lambda d: d[crudo.drop_duplicates().loc[d.index, "pais_geo"].notna()])
    evaluar(df_drop, NUM, CAT, rf(), f"T9 eliminando filas con país vacío ({df_drop.es_ataque.sum()} ataques)")

    print("\nSOLUCIÓN RAZONABLE (sin fugas, limpia)")
    evaluar(df, NUM, CAT, LogisticRegression(max_iter=1000, class_weight="balanced"), "Regresión logística (balanced)")
    evaluar(df, NUM, CAT, rf(), "Random Forest (balanced)")
    evaluar(df, NUM, CAT, KNeighborsClassifier(n_neighbors=7), "k-NN k=7 (escalado dentro del pipeline)")

    print("\nk-NN SIN ESCALAR (T13) – segundos crudos vs variables 0/1")
    X = df[["intentos_fallidos_previos_1h", "segundos_desde_intento_anterior", "dispositivo_nuevo", "usa_vpn", "madrugada"]]
    Xtr, Xte, ytr, yte = train_test_split(X, df.es_ataque, test_size=0.25, stratify=df.es_ataque, random_state=SEED)
    for nombre, m in (("sin escalar", KNeighborsClassifier(7)),
                      ("con StandardScaler", Pipeline([("s", StandardScaler()), ("k", KNeighborsClassifier(7))]))):
        p = m.fit(Xtr, ytr).predict(Xte)
        print(f"  k-NN {nombre:<20} recall={recall_score(yte, p):.3f}  prec={precision_score(yte, p, zero_division=0):.3f}")

    print("\nMODELO 'PEREZOSO' (siempre normal)")
    print(f"  exactitud = {1 - df.es_ataque.mean():.3f}, recall = 0.000")


if __name__ == "__main__":
    main()
