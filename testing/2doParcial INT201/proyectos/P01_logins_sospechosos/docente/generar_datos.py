# -*- coding: utf-8 -*-
"""
P01 – Inicios de sesión sospechosos en el Sistema Integrado Académico (SIA)
Genera ../estudiante/data/logins_sia.csv con trampas sembradas (ver guia_docente.md).
CONFIDENCIAL: no entregar este script a los estudiantes.

    python generar_datos.py
"""
import os
import numpy as np
import pandas as pd

SEED = 2026
N_REAL = 4000          # eventos reales
TASA_ATAQUE = 0.06     # ~6 % ataques (T12 desbalance)
N_QA = 150             # filas de cuentas de prueba automatizada (T2)
N_DUP = 120            # duplicados por re-envío de logs (T1)
N_999 = 18             # contador roto: intentos = 999 (T10)

rng = np.random.default_rng(SEED)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "estudiante", "data", "logins_sia.csv")


def ensuciar_texto(valores, prob):
    """T8: misma categoría escrita de formas distintas."""
    out = []
    for v in valores:
        if isinstance(v, str) and rng.random() < prob:
            v = rng.choice([v.lower(), v.upper(), v + " ", " " + v])
        out.append(v)
    return out


def eventos_reales(n):
    y = (rng.random(n) < TASA_ATAQUE).astype(int)
    a = y == 1

    # Hora: normales en horario laboral/estudio; 60 % de ataques entre 00 y 06 (H1 verdadera)
    hora = np.where(a, np.where(rng.random(n) < 0.6, rng.integers(0, 6, n), rng.integers(6, 24, n)),
                    np.where(rng.random(n) < 0.06, rng.integers(0, 6, n), np.clip(np.round(rng.normal(14, 3.5, n)), 6, 23))).astype(int)
    dia = rng.integers(0, 61, n)  # 1-sep a 30-oct 2026
    fecha = (pd.Timestamp("2026-09-01") + pd.to_timedelta(dia, "D") + pd.to_timedelta(hora, "h")
             + pd.to_timedelta(rng.integers(0, 3600, n), "s"))

    # Rol: los ataques NO prefieren docentes (H2 falsa)
    rol = rng.choice(["estudiante", "docente", "administrativo"], n, p=[0.75, 0.15, 0.10])

    # Señales de ataque (con solapamiento para que el recall no sea perfecto)
    intentos = np.where(a, np.where(rng.random(n) < 0.55, rng.poisson(6, n), rng.poisson(0.8, n)),
                        np.where(rng.random(n) < 0.05, rng.poisson(4, n), rng.poisson(0.3, n)))
    seg_ant = np.where(a, np.where(rng.random(n) < 0.5, rng.uniform(0.5, 12, n), rng.lognormal(8, 1.5, n)),
                       np.where(rng.random(n) < 0.06, rng.uniform(2, 15, n), rng.lognormal(9.5, 1.2, n))).round(1)
    disp_nuevo = np.where(a, rng.random(n) < 0.60, rng.random(n) < 0.12).astype(int)
    vpn = np.where(a, rng.random(n) < 0.35, rng.random(n) < 0.12).astype(int)

    nav_norm = ["Chrome", "Edge", "Firefox", "Safari", "Chrome Mobile"]
    nav_atq = ["Chrome", "python-requests", "curl", "Firefox", "Headless Chrome"]
    navegador = np.where(a, rng.choice(nav_atq, n, p=[0.55, 0.12, 0.05, 0.20, 0.08]),
                         rng.choice(nav_norm, n, p=[0.45, 0.15, 0.10, 0.10, 0.20]))
    so = np.where(a, rng.choice(["Linux", "Windows", "Android"], n, p=[0.35, 0.50, 0.15]),
                  rng.choice(["Windows", "Android", "iOS", "macOS", "Linux"], n, p=[0.45, 0.30, 0.12, 0.08, 0.05]))

    # País: H4 – los nulos son MÁS frecuentes en ataques (VPN / Tor) → borrar filas pierde ataques
    pais = np.where(a, rng.choice(["Bolivia", "Rusia", "China", "Brasil", "Estados Unidos", "Países Bajos"], n,
                                  p=[0.30, 0.15, 0.15, 0.15, 0.15, 0.10]),
                    rng.choice(["Bolivia", "Argentina", "Chile", "Perú", "Estados Unidos"], n,
                               p=[0.93, 0.02, 0.02, 0.02, 0.01])).astype(object)
    oct3 = pd.Series(rng.integers(0, 255, n)).astype(str) + "." + pd.Series(rng.integers(1, 254, n)).astype(str)
    ip = np.where(pais == "Bolivia", "200.87.", "185.220.") + oct3
    nulo =np.where(a, rng.random(n) < 0.30, rng.random(n) < 0.10)
    pais[nulo] = np.nan
    bol = (pais == "Bolivia") & (rng.random(n) < 0.25)
    pais[bol] = rng.choice(["BO", "bolivia", "BOLIVIA"], bol.sum())

    # T4 fuga sutil: la duración solo se conoce cuando la sesión TERMINA
    dur = np.where(a, np.where(rng.random(n) < 0.85, 0, rng.uniform(1, 4, n)), rng.uniform(3, 90, n)).round(1)
    # T3 fuga evidente: soporte bloquea DESPUÉS de investigar (coincide ~98 % con la etiqueta)
    bloqueado = np.where(a, rng.random(n) < 0.97, rng.random(n) < 0.004).astype(int)

    usuario = np.array([f"u{rng.integers(2019, 2027)}{rng.integers(1000, 9999)}" for _ in range(n)])
    usuario[rol == "docente"] = [f"doc.{rng.integers(100, 999)}" for _ in range((rol == "docente").sum())]
    usuario[rol == "administrativo"] = [f"adm.{rng.integers(100, 999)}" for _ in range((rol == "administrativo").sum())]

    return pd.DataFrame({
        "fecha_hora": fecha.strftime("%Y-%m-%d %H:%M:%S"), "usuario": usuario, "rol": rol, "ip_origen": ip,
        "pais_geo": pais, "navegador": ensuciar_texto(navegador, 0.12), "sistema_operativo": so,
        "intentos_fallidos_previos_1h": intentos, "segundos_desde_intento_anterior": seg_ant,
        "dispositivo_nuevo": disp_nuevo, "usa_vpn": vpn, "duracion_sesion_min": dur,
        "version_app": "4.2.1", "tema_interfaz": rng.choice(["claro", "oscuro"], n),
        "bloqueado_por_soporte": bloqueado, "es_ataque": y,
    })


def eventos_qa(n):
    """T2: pruebas automáticas de QA. Parecen ataques (rápidas, muchos fallos) pero NO lo son."""
    hora = rng.integers(1, 5, n)  # se ejecutan de madrugada
    fecha = (pd.Timestamp("2026-09-01") + pd.to_timedelta(rng.integers(0, 61, n), "D")
             + pd.to_timedelta(hora, "h") + pd.to_timedelta(rng.integers(0, 3600, n), "s"))
    return pd.DataFrame({
        "fecha_hora": fecha.strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": rng.choice([f"qa_bot_0{i}" for i in range(1, 6)], n), "rol": "administrativo",
        "ip_origen": ["10.0.99." + str(v) for v in rng.integers(10, 20, n)], "pais_geo": "Bolivia",
        "navegador": "python-requests", "sistema_operativo": "Linux",
        "intentos_fallidos_previos_1h": rng.poisson(9, n), "segundos_desde_intento_anterior": rng.uniform(0.5, 3, n).round(1),
        "dispositivo_nuevo": 1, "usa_vpn": 0, "duracion_sesion_min": 0.0, "version_app": "4.2.1",
        "tema_interfaz": "claro", "bloqueado_por_soporte": 0, "es_ataque": 0,
    })


def main():
    df = pd.concat([eventos_reales(N_REAL), eventos_qa(N_QA)], ignore_index=True)
    # T10: valores imposibles
    idx = rng.choice(len(df), N_999, replace=False)
    df.loc[idx, "intentos_fallidos_previos_1h"] = 999
    idx = rng.choice(len(df), 9, replace=False)
    df.loc[idx, "segundos_desde_intento_anterior"] = -1.0
    # T1: duplicados exactos (re-envío de logs)
    df = pd.concat([df, df.sample(N_DUP, random_state=SEED)], ignore_index=True)
    df = df.sample(frac=1, random_state=SEED).sort_values("fecha_hora", kind="stable").reset_index(drop=True)
    df.insert(0, "evento_id", [f"EV{i:06d}" for i in range(1, len(df) + 1)])
    # Los duplicados deben ser idénticos también en evento_id: se copia el id del original
    clave = [c for c in df.columns if c != "evento_id"]
    df["evento_id"] = df.groupby(clave, sort=False, dropna=False)["evento_id"].transform("first")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"OK {len(df)} filas -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
