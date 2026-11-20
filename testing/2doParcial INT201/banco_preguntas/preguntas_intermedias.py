# -*- coding: utf-8 -*-
"""Nivel INTERMEDIO (Q21-Q38): requiere calcular o comparar a partir de datos/gráficos."""
import numpy as np
from motor import (AZUL, NARANJA, VERDE, GRIS, TINTA, TINTA2, figura, etiquetas_barras,
                   matriz_confusion)

DIF, CAT = "Intermedio", "2 - Intermedio"
PREGUNTAS = []
DEC = "<p><em>Usa punto decimal (ej. 0.75). Se acepta un margen de ±0.005.</em></p>"


def reg(**q):
    q.setdefault("dif", DIF)
    q.setdefault("cat", CAT)
    PREGUNTAS.append(q)


def nota(txt):
    return (f'<p style="background:#eef3fb;border-radius:6px;padding:6px 10px;margin:6px 0">'
            f"<strong>Recuerda:</strong> {txt}</p>")


# ---------------------------------------------------------------------------
def g21():
    fig, ax = figura(5.2, 3.9)
    matriz_confusion(ax, [[935, 15], [5, 45]], "IDS - 1 000 conexiones de prueba", vmax=1000)
    return fig


reg(codigo="Q21", tipo="cloze", titulo="Métricas del IDS desde la matriz de confusión",
    tema="Precisión, recall y exactitud", tema_tag="Metricas clasificacion", grafico=g21,
    contexto="<p>Un sistema de detección de intrusiones (IDS) se evaluó con 1 000 conexiones. «Positivo» = "
             "<em>ataque</em>.</p>"
             + nota("<strong>Precisión</strong> = TP / (TP + FP): de las alarmas, ¿cuántas eran ataques reales?<br>"
                    "<strong>Recall</strong> = TP / (TP + FN): de los ataques reales, ¿cuántos detectamos?<br>"
                    "<strong>Exactitud</strong> = (TP + TN) / total."),
    datos=(["conexión", "predicción", "real", "celda"],
           [["#101", "ataque", "ataque", "TP"], ["#102", "ataque", "normal", "FP"], ["#103", "normal", "ataque", "FN"],
            ["#104", "normal", "normal", "TN"]]),
    hipotesis="El IDS detecta 9 de cada 10 ataques reales.",
    pregunta="<p>Completa con los datos de la matriz:</p><ul>"
             "<li>TP = {1:NUMERICAL:=45:0} · FP = {1:NUMERICAL:=15:0} · FN = {1:NUMERICAL:=5:0}</li>"
             "<li>Precisión = {1:NUMERICAL:=0.75:0.005}</li>"
             "<li>Recall = {1:NUMERICAL:=0.90:0.005}</li>"
             "<li>Exactitud = {1:NUMERICAL:=0.98:0.005}</li>"
             "<li>De cada 4 alarmas, aproximadamente {1:MULTICHOICE:=3~1~2~4} son ataques reales.</li>"
             "<li>La hipótesis {1:MULTICHOICE:=se cumple~no se cumple}.</li></ul>" + DEC,
    pista="El recuadro trae las tres fórmulas y la tabla muestra cómo se nombra cada celda.",
    retro="<p>Precisión = 45/60 = 0.75 (3 de cada 4 alarmas son reales). Recall = 45/50 = 0.90 → la hipótesis se "
          "cumple. Exactitud = (45 + 935)/1 000 = 0.98.</p>")


# ---------------------------------------------------------------------------
def g22():
    fig, ax = figura(6.8, 3.5)
    x = np.arange(2)
    b1 = ax.bar(x - 0.18, [0.95, 0.70], 0.34, color=AZUL, label="Precisión")
    b2 = ax.bar(x + 0.18, [0.60, 0.96], 0.34, color=NARANJA, label="Recall")
    etiquetas_barras(ax, list(b1) + list(b2), "{:.2f}")
    ax.set_xticks(x, ["Modelo A", "Modelo B"])
    ax.set_ylim(0, 1.15)
    ax.legend(loc="upper center", ncol=2)
    ax.set_title("Detección de ransomware")
    return fig


reg(codigo="Q22", tipo="multichoice", titulo="Ransomware: ¿precisión o recall?",
    tema="Precisión vs recall", tema_tag="Precision vs Recall", grafico=g22,
    contexto="<p>Dos modelos detectan ransomware en los servidores de la universidad. Si un ransomware "
             "<strong>no se detecta</strong>, puede cifrar todos los servidores (días sin sistema académico). Si hay "
             "una <strong>falsa alarma</strong>, un analista revisa el servidor durante 5 minutos.</p>"
             + nota("<strong>Recall</strong> alto = se escapan pocos ataques. <strong>Precisión</strong> alta = pocas "
                    "falsas alarmas. Se prioriza la métrica asociada al error <em>más costoso</em>."),
    datos=(["modelo", "exactitud", "precisión", "recall"],
           [["A", 0.97, 0.95, 0.60], ["B", 0.95, 0.70, 0.96]]),
    hipotesis="Debemos elegir el Modelo A porque tiene mayor exactitud y mayor precisión.",
    pregunta="<p>¿Qué modelo conviene y por qué?</p>",
    opciones=[(True, "Modelo B: su recall es 0.96, deja escapar muy pocos ransomware; las falsas alarmas cuestan poco."),
              (False, "Modelo A: su exactitud es mayor, y la exactitud siempre es la métrica principal."),
              (False, "Modelo A: con precisión 0.95 casi no molesta a los analistas, que es lo más importante."),
              (False, "Ninguno: con exactitudes de 0.95 y 0.97 los dos son equivalentes.")],
    pista="El contexto compara el costo de cada error; el recuadro dice qué métrica protege del error caro.",
    retro="<p>El error caro es el falso negativo (ransomware no detectado), así que se prioriza el recall. El "
          "Modelo A deja escapar 40 % de los ransomware. La hipótesis es falsa.</p>")


# ---------------------------------------------------------------------------
K23 = [1, 3, 5, 7, 9, 11, 15, 21, 31]
TR23 = [1.00, 0.95, 0.93, 0.92, 0.91, 0.90, 0.88, 0.86, 0.83]
VA23 = [0.78, 0.85, 0.88, 0.91, 0.90, 0.89, 0.87, 0.84, 0.80]


def g23():
    fig, ax = figura(7.0, 3.6)
    ax.plot(K23, TR23, "-o", color=AZUL, lw=2, label="Entrenamiento")
    ax.plot(K23, VA23, "-o", color=NARANJA, lw=2, label="Validación")
    ax.set_xticks(K23)
    ax.set_ylim(0.7, 1.03)
    ax.set_xlabel("k (número de vecinos)")
    ax.set_ylabel("Exactitud")
    ax.set_title("k-NN: dispositivos IoT comprometidos")
    ax.legend(loc="lower left")
    return fig


reg(codigo="Q23", tipo="multichoice", titulo="Elegir el mejor k para k-NN",
    tema="k-NN y sobreajuste", tema_tag="kNN", grafico=g23,
    contexto="<p>Se usa k-NN para detectar cámaras IoT comprometidas en la red del campus. Se probaron varios "
             "valores de k.</p>"
             + nota("con <strong>k muy pequeño</strong> el modelo copia el ruido (memoriza); con <strong>k muy "
                    "grande</strong> se vuelve demasiado simple. Se elige el k con <strong>mejor validación</strong>, "
                    "no con mejor entrenamiento."),
    datos=(["k", "exactitud entrenamiento", "exactitud validación"],
           [[k, f"{a:.2f}", f"{b:.2f}"] for k, a, b in zip(K23, TR23, VA23)]),
    hipotesis="k = 1 es el mejor valor porque obtiene 100 % en entrenamiento.",
    pregunta="<p>¿Qué valor de k conviene elegir?</p>",
    opciones=[(True, "k = 7: tiene la mayor exactitud de validación (0.91); con k = 1 hay sobreajuste."),
              (False, "k = 1: tiene 100 % en entrenamiento."),
              (False, "k = 31: es el modelo más simple, por lo tanto el mejor."),
              (False, "k = 3: es el segundo mejor en entrenamiento.")],
    pista="El recuadro dice que se elige por validación: buscar el punto más alto de la curva naranja.",
    retro="<p>La validación es máxima en k = 7 (0.91). k = 1: 1.00 vs 0.78 → sobreajuste. k = 31: ambas bajan → "
          "subajuste.</p>")


# ---------------------------------------------------------------------------
P24 = {"A": (0.5, 0.4, "ataque"), "B": (0.2, 0.5, "normal"), "C": (0.6, 0.8, "ataque"), "D": (0.9, 0.1, "normal")}


def g24():
    fig, ax = figura(5.6, 4.4)
    for k, (x, y, c) in P24.items():
        ax.scatter(x, y, s=110, color=NARANJA if c == "ataque" else AZUL, edgecolor=TINTA, zorder=3)
        ax.text(x + 0.025, y + 0.03, k, fontsize=12, fontweight="bold")
    ax.scatter(0.2, 0.8, marker="*", s=380, color="#f5c400", edgecolor=TINTA, zorder=4)
    ax.text(0.23, 0.83, "N", fontsize=12, fontweight="bold")
    ax.scatter([], [], color=AZUL, label="normal")
    ax.scatter([], [], color=NARANJA, label="ataque")
    ax.legend(loc="lower left")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_yticks(np.arange(0, 1.01, 0.1))
    ax.set_xlabel("x1: intentos_fallidos (0-1)")
    ax.set_ylabel("x2: actividad fuera de horario (0-1)")
    ax.set_title("Login nuevo N y vecinos conocidos")
    return fig


reg(codigo="Q24", tipo="cloze", titulo="Distancia euclidiana y votación en k-NN",
    tema="k-NN: distancia euclidiana", tema_tag="kNN", grafico=g24,
    contexto="<p>Las variables ya están escaladas entre 0 y 1. Llega un login nuevo <strong>N = (0.2, 0.8)</strong>.</p>"
             + nota("distancia euclidiana: <code>d = √((x1 − x1')² + (x2 − x2')²)</code>. Ejemplo: entre (0, 0) y "
                    "(0.3, 0.4) → √(0.09 + 0.16) = √0.25 = 0.5."),
    datos=(["punto", "x1", "x2", "clase"], [[k, x, y, c] for k, (x, y, c) in P24.items()]),
    hipotesis="El resultado de k-NN puede cambiar según el valor de k.",
    pregunta="<p>Completa:</p><ul>"
             "<li>d(N, A) = {1:NUMERICAL:=0.5:0.005}</li>"
             "<li>d(N, B) = {1:NUMERICAL:=0.3:0.005}</li>"
             "<li>d(N, C) = {1:NUMERICAL:=0.4:0.005}</li>"
             "<li>El vecino más cercano es {1:MULTICHOICE:=B~A~C~D}</li>"
             "<li>Con k = 1, N se clasifica como {1:MULTICHOICE:=normal~ataque}</li>"
             "<li>Con k = 3, N se clasifica como {1:MULTICHOICE:=ataque~normal}</li>"
             "<li>La hipótesis {1:MULTICHOICE:=se cumple~no se cumple}</li></ul>" + DEC,
    pista="El recuadro trae la fórmula y un ejemplo con la misma estructura que d(N, A).",
    retro="<p>d(N,A) = √(0.3² + 0.4²) = 0.5; d(N,B) = √(0² + 0.3²) = 0.3; d(N,C) = √(0.4² + 0²) = 0.4; "
          "d(N,D) = √(0.7² + 0.7²) ≈ 0.99. k = 1 → B (normal). k = 3 → B, C, A → 2 ataques vs 1 normal → "
          "ataque. El resultado cambia con k: la hipótesis se cumple.</p>")


# ---------------------------------------------------------------------------
H25 = ["00h", "01h", "02h", "03h", "04h", "05h", "06h"]
V25 = [48, 52, 45, 80, 51, 49, 55]


def g25():
    fig, ax = figura(6.8, 3.4)
    ax.bar(H25, V25, color=[NARANJA if h == "03h" else AZUL for h in H25], width=0.6)
    ax.axhline(50, color=TINTA, ls="--", lw=1.5, label="media histórica = 50")
    ax.legend(loc="upper right", facecolor="#fcfcfb", frameon=True, edgecolor=GRIS)
    ax.set_ylim(0, 98)
    ax.set_ylabel("Inicios de sesión")
    ax.set_title("Inicios de sesión por hora en el servidor VPN")
    return fig


reg(codigo="Q25", tipo="shortanswer", titulo="Valor z (StandardScaler) de un pico de logins",
    tema="Escalado: estandarización", tema_tag="Escalado", grafico=g25,
    contexto="<p>Históricamente, el servidor VPN recibe en promedio <strong>50</strong> inicios de sesión por hora "
             "con una desviación estándar de <strong>10</strong>. A las 03:00 hubo un pico.</p>"
             + nota("<code>StandardScaler</code> transforma cada valor en <strong>z = (x − media) / desviación</strong>. "
                    "z indica a cuántas desviaciones estándar está el valor de la media."),
    datos=(["hora", "inicios de sesión"], [[h, v] for h, v in zip(H25, V25)]),
    hipotesis="Un valor z mayor a 2 indica que la hora es inusual y merece revisión.",
    pregunta="<p>Calcula el valor <strong>z</strong> de las 03:00. <em>(Escribe solo el número.)</em></p>",
    respuestas=["3", "3.0", "3,0", "+3", "3.00"],
    pista="El recuadro trae la fórmula; los valores de x (tabla), media y desviación (contexto) están dados.",
    retro="<p>z = (80 − 50) / 10 = <strong>3</strong>. Está a 3 desviaciones de la media: según la hipótesis es una "
          "hora inusual que merece revisión (posible ataque de fuerza bruta).</p>")


# ---------------------------------------------------------------------------
M26 = {"Modelo A": (0.61, 0.59), "Modelo B": (0.99, 0.71), "Modelo C": (0.90, 0.88)}


def g26():
    fig, ax = figura(7.0, 3.5)
    x = np.arange(3)
    tr = [v[0] for v in M26.values()]
    te = [v[1] for v in M26.values()]
    b1 = ax.bar(x - 0.18, tr, 0.34, color=AZUL, label="Entrenamiento")
    b2 = ax.bar(x + 0.18, te, 0.34, color=NARANJA, label="Prueba")
    etiquetas_barras(ax, list(b1) + list(b2), "{:.2f}")
    ax.set_xticks(x, list(M26))
    ax.set_ylim(0, 1.3)
    ax.set_ylabel("Exactitud")
    ax.legend(loc="upper left", ncol=2)
    ax.set_title("Tres filtros de spam")
    return fig


reg(codigo="Q26", tipo="matching", titulo="Diagnóstico: subajuste, sobreajuste o buen ajuste",
    tema="Sobreajuste y subajuste", tema_tag="Overfitting", grafico=g26,
    contexto="<p>El equipo de correo institucional entrenó tres filtros de spam con distinta complejidad.</p>"
             + nota("compara dos cosas: (1) ¿qué tan <strong>alto</strong> es el desempeño? y (2) ¿qué tan "
                    "<strong>separadas</strong> están las barras de entrenamiento y prueba? Bajo y juntas = no "
                    "aprendió; alto en entrenamiento pero separadas = memorizó; altas y juntas = generaliza."),
    datos=(["modelo", "exactitud entrenamiento", "exactitud prueba"], [[k, *v] for k, v in M26.items()]),
    hipotesis="El Modelo B es el mejor porque tiene la mayor exactitud de entrenamiento.",
    pregunta="<p>Empareja cada modelo con su diagnóstico (sobra una opción):</p>",
    pares=[("Modelo A", "Subajuste (underfitting)"), ("Modelo B", "Sobreajuste (overfitting)"),
           ("Modelo C", "Buen ajuste (generaliza bien)")],
    distractores=["Fuga de información (data leakage)"],
    pista="El recuadro traduce cada patrón de barras a un diagnóstico.",
    retro="<p>A: ambas bajas (≈0.60) → subajuste. B: 0.99 vs 0.71 → sobreajuste. C: altas y cercanas → buen ajuste. "
          "La hipótesis es falsa: el mejor es C (mayor exactitud de prueba).</p>")


# ---------------------------------------------------------------------------
def g27():
    fig, axes = figura(8.4, 3.4, ncols=2)
    b = axes[0].bar(["Phishing", "Legítimo"], [0.30, 0.70], color=[NARANJA, AZUL], width=0.5)
    etiquetas_barras(axes[0], b, "{:.0%}")
    axes[0].set_ylim(0, 0.85)
    axes[0].set_title("¿Qué parte de los correos es...?")
    b = axes[1].bar(["Phishing", "Legítimo"], [0.60, 0.10], color=[NARANJA, AZUL], width=0.5)
    etiquetas_barras(axes[1], b, "{:.0%}")
    axes[1].set_ylim(0, 0.85)
    axes[1].set_title("% que contiene «urgente»")
    return fig


reg(codigo="Q27", tipo="cloze", titulo="Naive Bayes: la palabra «urgente»",
    tema="Naive Bayes / Teorema de Bayes", tema_tag="Naive Bayes", grafico=g27,
    contexto="<p>Un filtro Naive Bayes analiza correos. Del histórico se sabe que el 30 % de los correos son "
             "phishing; la palabra <strong>«urgente»</strong> aparece en el 60 % de los phishing y en el 10 % de los "
             "legítimos.</p>"
             + nota("piensa en 100 correos: 30 phishing y 70 legítimos. ¿Cuántos de cada grupo dicen «urgente»?<br>"
                    "<code>P(phishing | urgente) = P(urgente y phishing) / P(urgente)</code>"),
    datos=(["correo", "contiene «urgente»", "clase"],
           [["#1", "sí", "phishing"], ["#2", "no", "legítimo"], ["#3", "sí", "legítimo"], ["#4", "sí", "phishing"],
            ["#5", "no", "phishing"]]),
    hipotesis="Si un correo contiene «urgente», es más probable que sea phishing que legítimo.",
    pregunta="<p>Completa (como proporciones):</p><ul>"
             "<li>P(urgente y phishing) = 0.30 × 0.60 = {1:NUMERICAL:=0.18:0.005}</li>"
             "<li>P(urgente y legítimo) = 0.70 × 0.10 = {1:NUMERICAL:=0.07:0.005}</li>"
             "<li>P(urgente) = {1:NUMERICAL:=0.25:0.005}</li>"
             "<li>P(phishing | urgente) = {2:NUMERICAL:=0.72:0.005}</li>"
             "<li>Un correo con «urgente» se clasifica como {1:MULTICHOICE:=phishing~legítimo} y la hipótesis "
             "{1:MULTICHOICE:=se cumple~no se cumple}</li></ul>" + DEC,
    pista="El recuadro sugiere pensar en 100 correos: 18 phishing con «urgente» y 7 legítimos con «urgente».",
    retro="<p>De 100 correos: 18 phishing y 7 legítimos contienen «urgente» → 25 en total. P(phishing | urgente) = "
          "18/25 = 0.72 &gt; 0.5 → phishing. La hipótesis se cumple.</p>")


# ---------------------------------------------------------------------------
rng28 = np.random.default_rng(11)
E28 = rng28.integers(1, 25, 60)
U28 = np.clip(np.round(E28 * 0.55 + rng28.normal(0, 1.2, 60)), 0, None)
R28 = np.corrcoef(E28, U28)[0, 1]


def g28():
    fig, ax = figura(6.4, 3.6)
    ax.scatter(E28, U28, s=40, color=AZUL, alpha=0.8)
    ax.text(1.5, U28.max() - 0.5, f"r = {R28:.2f}", fontsize=11, color=TINTA)
    ax.set_xlabel("num_enlaces")
    ax.set_ylabel("num_urls_acortadas")
    ax.set_title("Correos de phishing: enlaces vs URLs acortadas")
    return fig


reg(codigo="Q28", tipo="truefalse", titulo="Supuesto de independencia de Naive Bayes",
    tema="Naive Bayes: supuestos", tema_tag="Naive Bayes", grafico=g28,
    contexto="<p>Un filtro Naive Bayes usa, entre otras, las variables <code>num_enlaces</code> y "
             "<code>num_urls_acortadas</code> (bit.ly, tinyurl…).</p>"
             + nota("Naive Bayes es «ingenuo» porque <strong>supone que las variables son independientes</strong> "
                    "dentro de cada clase. Si conocer una variable te permite <em>adivinar</em> la otra, no son "
                    "independientes."),
    datos=(["correo", "num_enlaces", "num_urls_acortadas"],
           [[f"#{i + 1}", int(E28[i]), int(U28[i])] for i in range(5)]),
    hipotesis="En este dataset se cumple el supuesto de independencia de Naive Bayes entre <code>num_enlaces</code> "
              "y <code>num_urls_acortadas</code>.",
    pregunta="<p>Observa el gráfico. ¿La hipótesis es verdadera o falsa?</p>",
    verdadero=False,
    pista="El recuadro da el criterio (¿una permite adivinar la otra?) y el gráfico muestra r cercano a 1.",
    retro=f"<p><strong>Falso.</strong> La correlación es r = {R28:.2f}: a más enlaces, más URLs acortadas. El "
          "supuesto se rompe; Naive Bayes «cuenta dos veces» la misma evidencia. A veces igual funciona bien, pero "
          "conviene saberlo (o quedarse con una de las dos variables).</p>")


# ---------------------------------------------------------------------------
F29 = [0.91, 0.62, 0.93, 0.90, 0.92]


def g29():
    fig, ax = figura(6.6, 3.4)
    b = ax.bar([f"Fold {i}" for i in range(1, 6)], F29, color=[NARANJA if v < 0.8 else AZUL for v in F29], width=0.55)
    etiquetas_barras(ax, b, "{:.2f}")
    ax.axhline(np.mean(F29), color=TINTA, ls="--", lw=1.5, label="promedio de los 5 folds")
    ax.legend(loc="lower left", facecolor="#fcfcfb", frameon=True, edgecolor=GRIS)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Exactitud")
    ax.set_title("Validación cruzada (5 folds) - clasificador de malware")
    return fig


reg(codigo="Q29", tipo="multichoice", titulo="Validación cruzada inestable",
    tema="Validación cruzada", tema_tag="Validacion cruzada", grafico=g29,
    contexto="<p>Se evaluó un clasificador de malware con <strong>validación cruzada de 5 folds</strong>.</p>"
             + nota("en validación cruzada se entrena y evalúa 5 veces, cada vez con una parte distinta como prueba. "
                    "Se reporta el <strong>promedio</strong>; si los folds <strong>varían mucho</strong>, el modelo es "
                    "inestable o alguna parte de los datos es diferente."),
    datos=(["fold", "exactitud"], [[i + 1, v] for i, v in enumerate(F29)]),
    hipotesis="El modelo tiene un desempeño estable de alrededor de 0.90 en cualquier parte de los datos.",
    pregunta="<p>¿Qué conclusión es correcta?</p>",
    opciones=[(True, "La hipótesis es falsa: el promedio es ≈ 0.86 y el fold 2 (0.62) muestra inestabilidad; hay "
                     "que revisar qué datos contiene ese fold."),
              (False, "La hipótesis es verdadera: se debe reportar 0.93, el mejor fold."),
              (False, "La hipótesis es verdadera: los folds bajos son errores y se eliminan del promedio."),
              (False, "La hipótesis es falsa porque la validación cruzada solo sirve para regresión.")],
    pista="El recuadro dice que se reporta el promedio y que mucha variación indica inestabilidad.",
    retro="<p>Promedio = (0.91 + 0.62 + 0.93 + 0.90 + 0.92) / 5 = 0.856. El fold 2 cae a 0.62: tal vez contiene una "
          "familia de malware que no aparece en los otros folds. No se eliminan resultados incómodos.</p>")


# ---------------------------------------------------------------------------
F30 = [0.88, 0.90, 0.87, 0.91, 0.89]


def g30():
    fig, ax = figura(6.4, 3.2)
    b = ax.bar([f"Fold {i}" for i in range(1, 6)], F30, color=AZUL, width=0.55)
    etiquetas_barras(ax, b, "{:.2f}")
    ax.axhline(np.mean(F30), color=NARANJA, ls="--", lw=1.5)
    ax.set_ylim(0.8, 0.95)
    ax.set_ylabel("Exactitud")
    ax.set_title("Resultado esperado: Pipeline + validación cruzada")
    return fig


reg(codigo="Q30", tipo="ddwtos", titulo="Pipeline: escalado + k-NN con validación cruzada",
    tema="Pipelines y validación cruzada", tema_tag="Pipeline", grafico=g30,
    contexto="<p>Para clasificar tráfico como normal/ataque con k-NN, el equipo usa un <strong>Pipeline</strong>: "
             "primero <strong>estandariza</strong> (media 0, desviación 1) y luego aplica el "
             "<strong>clasificador</strong> de vecinos. El desempeño se mide con <strong>validación cruzada de "
             "5 folds</strong>.</p>"
             + nota("los clasificadores terminan en <code>Classifier</code> y los de regresión en "
                    "<code>Regressor</code>. <code>cross_val_score</code> hace la validación cruzada; "
                    "<code>train_test_split</code> solo divide una vez."),
    datos=(["paquetes", "bytes", "duración (s)", "clase"], [[120, 54000, 3.2, 0], [950, 61000, 0.4, 1], [64, 9800, 1.1, 0]]),
    hipotesis="Con el Pipeline, el escalador se ajusta solo con los datos de entrenamiento de cada fold, evitando "
              "fuga de información.",
    pregunta="<p>Arrastra las opciones para completar el código:</p>"
             "<pre><code>pipe = Pipeline([\n"
             "    (\"escalar\", [[1]]()),\n"
             "    (\"modelo\",  [[2]](n_neighbors=5))\n"
             "])\n"
             "scores = [[3]](pipe, X, y, cv=[[4]])\n"
             "print(scores.mean())</code></pre>",
    huecos=[("StandardScaler", 1), ("KNeighborsClassifier", 2), ("cross_val_score", 3), ("5", 4)],
    distractores=[("OneHotEncoder", 1), ("KNeighborsRegressor", 2), ("train_test_split", 3), ("0.2", 4)],
    pista="El contexto describe cada paso con palabras y el recuadro diferencia Classifier/Regressor y las dos funciones.",
    retro="<p><code>StandardScaler</code> → <code>KNeighborsClassifier</code> (es clasificación) → "
          "<code>cross_val_score(pipe, X, y, cv=5)</code>. La hipótesis es verdadera: dentro de cada fold el Pipeline "
          "hace <code>fit</code> del escalador solo con la parte de entrenamiento.</p>")


# ---------------------------------------------------------------------------
U31 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
R31 = [0.99, 0.97, 0.94, 0.91, 0.85, 0.78, 0.69, 0.55, 0.38]
P31 = [0.40, 0.52, 0.63, 0.72, 0.80, 0.86, 0.91, 0.95, 0.98]


def g31():
    fig, ax = figura(7.0, 3.6)
    ax.plot(U31, P31, "-o", color=AZUL, lw=2, label="Precisión")
    ax.plot(U31, R31, "-o", color=NARANJA, lw=2, label="Recall")
    ax.axhline(0.90, color=GRIS, ls=":", lw=1.5)
    ax.text(0.12, 0.915, "política: recall ≥ 0.90", fontsize=9.5, color=TINTA2)
    ax.set_xticks(U31)
    ax.set_xlabel("Umbral de decisión")
    ax.set_ylabel("Valor de la métrica")
    ax.set_ylim(0.3, 1.03)
    ax.legend(loc="center left", facecolor="#fcfcfb", frameon=True, edgecolor=GRIS)
    ax.set_title("Precisión y recall según el umbral (phishing)")
    return fig


reg(codigo="Q31", tipo="multichoice", titulo="Elegir el umbral según la política del SOC",
    tema="Umbral de decisión", tema_tag="Umbral", grafico=g31,
    contexto="<p>Una regresión logística detecta phishing. La política del SOC dice: <strong>detectar al menos el "
             "90 % del phishing</strong> (recall ≥ 0.90) y, entre los umbrales que cumplan eso, elegir el de "
             "<strong>mayor precisión</strong> para no saturar a los analistas.</p>"
             + nota("al <strong>subir</strong> el umbral, el modelo es más exigente: sube la precisión y baja el "
                    "recall. Primero filtra los umbrales que cumplen la condición y luego compara."),
    datos=(["umbral", "precisión", "recall"], [[u, p, r] for u, p, r in zip(U31, P31, R31)]),
    hipotesis="El umbral por defecto (0.5) cumple la política del SOC.",
    pregunta="<p>¿Qué umbral se debe elegir?</p>",
    opciones=[(True, "0.4: es el umbral más alto con recall ≥ 0.90 (0.91), y por eso el de mayor precisión (0.72) "
                     "entre los que cumplen."),
              (False, "0.5: es el valor por defecto y cumple la política."),
              (False, "0.1: tiene el mayor recall (0.99)."),
              (False, "0.9: tiene la mayor precisión (0.98).")],
    pista="El recuadro indica el orden: primero filtrar recall ≥ 0.90 (0.1 a 0.4), luego la mayor precisión.",
    retro="<p>Cumplen recall ≥ 0.90: 0.1, 0.2, 0.3 y 0.4. De ellos, la mayor precisión es la de 0.4 (0.72). Con 0.5 "
          "el recall es 0.85 → la hipótesis es falsa.</p>")


# ---------------------------------------------------------------------------
F32 = ["intentos_fallidos_1h", "pais_distinto_habitual", "hora_login", "tipo_navegador", "longitud_usuario"]
I32 = [0.42, 0.27, 0.15, 0.10, 0.06]


def g32():
    fig, ax = figura(7.0, 3.4)
    b = ax.barh(F32, I32, color=AZUL, height=0.6)
    etiquetas_barras(ax, b, "{:.2f}", horizontal=True)
    ax.invert_yaxis()
    ax.set_xlim(0, 0.5)
    ax.set_xlabel("Importancia (feature_importances_)")
    ax.set_title("Random Forest: cuentas comprometidas")
    ax.grid(axis="y", visible=False)
    return fig


reg(codigo="Q32", tipo="multichoice", titulo="Interpretar la importancia de variables",
    tema="Random Forest: importancia de variables", tema_tag="Random Forest", grafico=g32,
    contexto="<p>Un Random Forest detecta cuentas de correo comprometidas. Se graficó "
             "<code>feature_importances_</code>.</p>"
             + nota("la importancia mide <strong>cuánto ayudó cada variable al bosque a separar las clases</strong>. "
                    "No indica causa, ni dirección (si sube o baja el riesgo), y las importancias suman 1."),
    datos=(["variable", "importancia"], [[f, i] for f, i in zip(F32, I32)]),
    hipotesis="<code>intentos_fallidos_1h</code> es la variable que más aporta al modelo para separar cuentas "
              "comprometidas de cuentas normales.",
    pregunta="<p>¿Qué afirmación es correcta?</p>",
    opciones=[(True, "La hipótesis es verdadera: intentos_fallidos_1h es la más útil para separar; longitud_usuario "
                     "aporta poco y se podría probar quitarla."),
              (False, "Tener muchos intentos fallidos causa que una cuenta sea comprometida, porque su importancia es 0.42."),
              (False, "hora_login decide exactamente el 15 % de los casos."),
              (False, "longitud_usuario es la más importante porque tiene el valor más pequeño.")],
    pista="El recuadro advierte que importancia ≠ causa y ≠ porcentaje de casos.",
    retro="<p>La importancia es una medida de utilidad para las divisiones del bosque, no de causalidad. "
          "longitud_usuario (0.06) es candidata a eliminarse y volver a evaluar.</p>")


# ---------------------------------------------------------------------------
def g33():
    f = ["estado_final_ticket", "severidad_alerta", "ip_en_lista_negra", "hora_alerta"]
    v = [0.88, 0.06, 0.04, 0.02]
    fig, ax = figura(7.0, 3.0)
    b = ax.barh(f, v, color=[NARANJA, AZUL, AZUL, AZUL], height=0.6)
    etiquetas_barras(ax, b, "{:.2f}", horizontal=True)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Importancia")
    ax.set_title("Modelo con 99.8 % de exactitud")
    ax.grid(axis="y", visible=False)
    return fig


reg(codigo="Q33", tipo="shortanswer", titulo="¿Cómo se llama el problema del 99.8 %?",
    tema="Fuga de información (data leakage)", tema_tag="Data leakage", grafico=g33,
    contexto="<p>El SOC quiere predecir, <strong>en el momento en que llega una alerta</strong>, si terminará siendo "
             "un incidente real. Un modelo logró 99.8 % de exactitud. La columna <code>estado_final_ticket</code> la "
             "escribe el analista <strong>días después</strong>, cuando cierra el caso.</p>"
             + nota("pregúntate: <em>¿esa información existe en el momento en que el modelo debe predecir?</em> "
                    "Cuando datos del futuro (o la propia respuesta) se «filtran» a las variables de entrada, el "
                    "modelo hace trampa."),
    datos=(["alerta", "severidad_alerta", "ip_en_lista_negra", "estado_final_ticket", "fue_incidente (y)"],
           [["A-301", "alta", "sí", "cerrado: incidente", 1], ["A-302", "baja", "no", "cerrado: falso positivo", 0],
            ["A-303", "media", "no", "cerrado: falso positivo", 0]]),
    hipotesis="El 99.8 % de exactitud se mantendrá cuando el modelo se use en tiempo real.",
    pregunta="<p>La hipótesis es falsa. ¿Cómo se llama este problema? <em>(en español o inglés)</em></p>",
    respuestas=["fuga de datos", "fuga de información", "fuga de informacion", "data leakage", "leakage",
                "filtración de datos", "filtracion de datos", "fuga de informacion (data leakage)", "fuga"],
    pista="El recuadro usa la palabra «se filtran»; en inglés el término es leakage.",
    retro="<p><strong>Fuga de información (data leakage)</strong>: <code>estado_final_ticket</code> contiene la "
          "respuesta y no existe al momento de predecir. Hay que eliminarla y reentrenar.</p>")


# ---------------------------------------------------------------------------
rng34 = np.random.default_rng(21)
T34 = np.round(np.r_[rng34.lognormal(np.log(170), 0.35, 470), rng34.uniform(1500, 4500, 30)])
MED34, MEA34 = float(np.median(T34)), float(T34.mean())


def g34():
    fig, ax = figura(7.0, 3.4)
    ax.hist(T34, bins=np.arange(0, 4700, 150), color=AZUL, edgecolor="#fcfcfb")
    ax.axvline(MED34, color=TINTA, lw=2, label=f"Mediana = {MED34:.0f} ms")
    ax.axvline(MEA34, color=NARANJA, lw=2, ls="--", label=f"Media = {MEA34:.0f} ms")
    ax.legend(loc="upper right")
    ax.annotate("30 mediciones durante el DDoS\n(1 500 – 4 500 ms, barras muy bajas)", xy=(3000, 3),
                xytext=(1900, 110), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color=TINTA2))
    ax.set_xlabel("tiempo_respuesta (ms)")
    ax.set_ylabel("Mediciones")
    ax.set_title("Tiempo de respuesta del portal (500 mediciones)")
    return fig


reg(codigo="Q34", tipo="multichoice", titulo="Imputar nulos: ¿media o mediana?",
    tema="Imputación de valores nulos", tema_tag="Valores nulos", grafico=g34,
    contexto="<p>El 6 % de las mediciones de <code>tiempo_respuesta</code> del portal están vacías (el monitor se "
             "reinició). Durante algunos minutos hubo un ataque DDoS con tiempos altísimos.</p>"
             + nota("la <strong>media</strong> se «jala» hacia los valores extremos; la <strong>mediana</strong> "
                    "(valor del medio) casi no cambia con ellos."),
    datos=(["medición", "tiempo_respuesta (ms)"],
           [[1, 162], [2, "<em>NaN</em>"], [3, 3980], [4, 175], [5, 148]]),
    hipotesis=f"Rellenar los nulos con la media ({MEA34:.0f} ms) representa bien un tiempo de respuesta típico.",
    pregunta="<p>¿Qué valor conviene usar para imputar?</p>",
    opciones=[(True, f"La mediana ({MED34:.0f} ms): la distribución tiene cola larga y la media está inflada por los "
                     "minutos de DDoS."),
              (False, f"La media ({MEA34:.0f} ms): siempre es la mejor medida del centro."),
              (False, "0 ms: si no hay dato, el portal no respondió."),
              (False, "El valor máximo, para ser conservadores.")],
    pista="El recuadro explica cuál de las dos líneas es sensible a extremos; el gráfico muestra la cola por DDoS.",
    retro=f"<p>La media ({MEA34:.0f} ms) queda lejos de la mayoría de datos por los valores de DDoS; la mediana "
          f"({MED34:.0f} ms) representa el caso típico. La hipótesis es falsa.</p>")


# ---------------------------------------------------------------------------
D35 = [("Lun", 120, 118), ("Mar", 95, 99), ("Mié", 140, 139), ("Jue", 110, 113)]


def g35():
    fig, ax = figura(6.8, 3.4)
    x = np.arange(4)
    ax.bar(x - 0.18, [d[1] for d in D35], 0.34, color=AZUL, label="Real")
    ax.bar(x + 0.18, [d[2] for d in D35], 0.34, color=NARANJA, label="Predicho")
    ax.set_xticks(x, [d[0] for d in D35])
    ax.set_ylim(80, 150)
    ax.set_ylabel("Conexiones VPN")
    ax.legend(loc="upper left", ncol=2)
    ax.set_title("Conexiones VPN: real vs predicho")
    return fig


reg(codigo="Q35", tipo="multichoice", titulo="Error absoluto medio (MAE) del modelo de VPN",
    tema="Regresión: métricas de error", tema_tag="MAE", grafico=g35,
    contexto="<p>Una regresión lineal predice cuántas conexiones VPN habrá cada día para dimensionar el servidor.</p>"
             + nota("<strong>error = real − predicho</strong>. El <strong>MAE</strong> es el promedio de los errores "
                    "en <strong>valor absoluto</strong> (sin signo), para que los positivos y negativos no se "
                    "cancelen."),
    datos=(["día", "real", "predicho"], [list(d) for d in D35]),
    hipotesis="En promedio, el modelo se equivoca en menos de 3 conexiones por día.",
    pregunta="<p>¿Cuál es el MAE y se cumple la hipótesis?</p>",
    opciones=[(True, "MAE = 2.5; sí se cumple."), (False, "MAE = −1.0; sí se cumple."),
              (False, "MAE = 10; no se cumple."), (False, "MAE = 0; los errores se cancelan.")],
    pista="El recuadro dice que se toma el valor absoluto antes de promediar.",
    retro="<p>Errores: 2, −4, 1, −3 → absolutos 2, 4, 1, 3 → MAE = 10/4 = <strong>2.5</strong> &lt; 3. Si no se usa "
          "valor absoluto: (2 − 4 + 1 − 3)/4 = −1, que no tiene sentido como «tamaño» del error.</p>")


# ---------------------------------------------------------------------------
def g36():
    fig, ax = figura(6.8, 3.5)
    x = np.arange(2)
    b1 = ax.bar(x - 0.18, [0.91, 0.72], 0.34, color=GRIS, label="Sin escalar")
    b2 = ax.bar(x + 0.18, [0.91, 0.90], 0.34, color=AZUL, label="Con StandardScaler")
    etiquetas_barras(ax, list(b1) + list(b2), "{:.2f}")
    ax.set_xticks(x, ["Árbol de decisión", "k-NN"])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Exactitud (prueba)")
    ax.legend(loc="upper right", ncol=2)
    ax.set_title("Detección de escaneo de puertos")
    return fig


reg(codigo="Q36", tipo="truefalse", titulo="¿El escalado mejora a todos los modelos?",
    tema="Escalado y tipo de modelo", tema_tag="Escalado", grafico=g36,
    contexto="<p>Se compararon un árbol de decisión y k-NN para detectar escaneos de puertos, con y sin escalar "
             "las variables (<code>bytes</code>, <code>puertos_distintos</code>, <code>duración</code>).</p>"
             + nota("un árbol hace preguntas del tipo <em>«¿puertos_distintos &gt; 100?»</em>. Escalar solo cambia "
                    "el número de corte, no el orden de los datos. k-NN, en cambio, calcula distancias."),
    datos=(["modelo", "sin escalar", "con StandardScaler"], [["Árbol", 0.91, 0.91], ["k-NN", 0.72, 0.90]]),
    hipotesis="Escalar las variables mejora a ambos modelos por igual.",
    pregunta="<p>¿La hipótesis es verdadera o falsa?</p>",
    verdadero=False,
    pista="El recuadro explica por qué un árbol no depende de la escala; el gráfico lo confirma.",
    retro="<p><strong>Falso.</strong> El árbol queda igual (0.91 → 0.91) porque solo compara valores con un corte. "
          "k-NN mejora mucho (0.72 → 0.90) porque depende de distancias.</p>")


# ---------------------------------------------------------------------------
F37 = ["dias_sin_actualizar", "sitios_riesgo_visitados", "usuario_es_admin", "mes_de_compra",
       "numero_de_escritorio", "color_fondo_pantalla"]
C37 = [0.71, 0.64, 0.38, 0.03, 0.02, 0.01]


def g37():
    fig, ax = figura(7.2, 3.5)
    b = ax.barh(F37, C37, color=AZUL, height=0.6)
    etiquetas_barras(ax, b, "{:.2f}", horizontal=True)
    ax.invert_yaxis()
    ax.set_xlim(0, 0.85)
    ax.set_xlabel("|correlación| con «equipo_infectado»")
    ax.set_title("Relación de cada variable con la infección")
    ax.grid(axis="y", visible=False)
    return fig


reg(codigo="Q37", tipo="multi", titulo="Seleccionar variables irrelevantes",
    tema="Selección de variables", tema_tag="Seleccion de variables", grafico=g37,
    contexto="<p>Se quiere predecir si una computadora del laboratorio <strong>se infectará</strong> con malware el "
             "próximo mes. El dataset tiene variables útiles y otras que se agregaron «por si acaso».</p>"
             + nota("para decidir, combina dos criterios: (1) ¿tiene <strong>lógica</strong> que la variable influya "
                    "en una infección? y (2) ¿su <strong>relación</strong> con la etiqueta es casi cero?"),
    datos=(["equipo", "dias_sin_actualizar", "usuario_es_admin", "numero_de_escritorio", "color_fondo_pantalla", "infectado"],
           [["LAB-01", 3, "no", 12, "azul", 0], ["LAB-02", 95, "sí", 7, "negro", 1], ["LAB-03", 40, "sí", 3, "azul", 1]]),
    hipotesis="Mientras más columnas tenga el modelo, mejor será su predicción.",
    pregunta="<p>Selecciona <strong>todas</strong> las variables que conviene <strong>eliminar</strong>:</p>",
    opciones=[(True, "numero_de_escritorio"), (True, "color_fondo_pantalla"), (True, "mes_de_compra"),
              (False, "dias_sin_actualizar"), (False, "usuario_es_admin")],
    pista="El recuadro da los dos criterios: sin lógica y con correlación casi cero.",
    retro="<p>Las tres últimas no tienen relación lógica con una infección y su correlación es ≈ 0: solo agregan "
          "ruido. La hipótesis es falsa: más columnas irrelevantes pueden empeorar modelos como k-NN.</p>")


# ---------------------------------------------------------------------------
D38 = [(10, 42), (20, 63), (30, 92), (50, 141), (60, 162)]


def g38():
    fig, ax = figura(6.8, 3.5)
    ax.scatter([d[0] for d in D38], [d[1] for d in D38], s=60, color=AZUL, zorder=3, label="Restauraciones")
    xs = np.linspace(0, 70, 50)
    ax.plot(xs, 15 + 2.5 * xs, color=NARANJA, lw=2, label="tiempo = 15 + 2.5 × GB")
    ax.scatter([40], [130], s=90, marker="D", color=VERDE, edgecolor=TINTA, zorder=4, label="Caso real: 40 GB")
    ax.set_xlabel("Tamaño del respaldo (GB)")
    ax.set_ylabel("Minutos para restaurar")
    ax.legend(loc="upper left")
    ax.set_title("Tiempo de restauración de servidores")
    return fig


reg(codigo="Q38", tipo="cloze", titulo="Regresión lineal: restaurar un respaldo",
    tema="Regresión lineal: predicción y residuo", tema_tag="Regresion lineal", grafico=g38,
    contexto="<p>Tras un ataque, TI debe restaurar servidores desde respaldos. Se ajustó:</p>"
             "<p style='text-align:center'><code>minutos = 15 + 2.5 × GB</code></p>"
             + nota("en <code>y = b + m·x</code>: <code>b</code> es el <strong>intercepto</strong> (valor cuando x = 0) "
                    "y <code>m</code> la <strong>pendiente</strong>. El <strong>residuo</strong> = real − predicho. "
                    "2 horas = 120 minutos."),
    datos=(["respaldo (GB)", "minutos reales"], [list(d) for d in D38] + [[40, 130]]),
    hipotesis="Restaurar un respaldo de 40 GB toma menos de 2 horas según el modelo.",
    pregunta="<p>Completa:</p><ul>"
             "<li>Intercepto = {1:NUMERICAL:=15:0} · Pendiente = {1:NUMERICAL:=2.5:0.005}</li>"
             "<li>Predicción para 40 GB = {1:NUMERICAL:=115:0} minutos</li>"
             "<li>Si el caso real tardó 130 minutos, el residuo es {1:NUMERICAL:=15:0}</li>"
             "<li>La relación entre GB y minutos es {1:MULTICHOICE:=positiva~negativa~nula}</li>"
             "<li>La hipótesis {1:MULTICHOICE:=se cumple~no se cumple}</li></ul>",
    pista="El recuadro define intercepto, pendiente, residuo y recuerda que 2 h = 120 min.",
    retro="<p>15 + 2.5 × 40 = 115 min &lt; 120 → la hipótesis se cumple (según el modelo). Residuo = 130 − 115 = 15 "
          "(el modelo subestimó). Pendiente positiva: más GB → más minutos.</p>")
