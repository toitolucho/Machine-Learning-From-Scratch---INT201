# -*- coding: utf-8 -*-
"""Nivel DIFÍCIL (Q39-Q50): combinar varios conceptos y razonar sobre la validez del resultado."""
import numpy as np
from motor import (AZUL, NARANJA, VERDE, GRIS, TINTA, TINTA2, figura, etiquetas_barras,
                   matriz_confusion)

DIF, CAT = "Difícil", "3 - Difícil"
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
PPS39 = [50, 120, 250, 400, 600, 900, 1100, 1500]
Y39 = [0, 0, 0, 0, 1, 1, 1, 1]


def lin39(x):
    return -0.29 + 0.0016 * np.asarray(x)


def g39():
    fig, ax = figura(7.0, 3.8)
    xs = np.linspace(0, 1600, 200)
    ax.scatter(PPS39, Y39, s=60, color=TINTA, zorder=3, label="Datos (0 = normal, 1 = ataque)")
    ax.plot(xs, lin39(xs), color=NARANJA, lw=2, label="Regresión lineal")
    ax.plot(xs, 1 / (1 + np.exp(-(xs - 500) / 80)), color=AZUL, lw=2, label="Regresión logística (sigmoide)")
    ax.axhspan(1, 2.3, color="#fde6dc", alpha=0.6)
    ax.axhspan(-0.5, 0, color="#fde6dc", alpha=0.6)
    ax.text(1580, -0.4, "zona imposible para una probabilidad (< 0 o > 1)", fontsize=9, color=TINTA2, ha="right")
    ax.set_ylim(-0.5, 2.3)
    ax.set_xlabel("paquetes por segundo")
    ax.set_ylabel("salida del modelo")
    ax.legend(loc="upper left", fontsize=9, facecolor="#fcfcfb", frameon=True, edgecolor=GRIS)
    ax.set_title("¿Lineal o logística para detectar ataques?")
    return fig


reg(codigo="Q39", tipo="multichoice", titulo="Regresión lineal para clasificar ataques",
    tema="Regresión lineal vs logística", tema_tag="Regresion logistica", grafico=g39,
    contexto="<p>Un practicante quiere estimar la <strong>probabilidad de ataque</strong> según los paquetes por "
             "segundo (pps) que recibe un servidor. Ajustó una <strong>regresión lineal</strong> sobre la etiqueta "
             "0/1: <code>salida = −0.29 + 0.0016 × pps</code>.</p>"
             + nota("una probabilidad <strong>siempre</strong> está entre 0 y 1. La función sigmoide de la regresión "
                    "logística «aplasta» cualquier valor dentro de ese rango."),
    datos=(["pps", "ataque (real)", "salida lineal"],
           [[x, y, f"{v:.2f}"] for x, y, v in zip(PPS39, Y39, lin39(PPS39)) if x in (50, 400, 900, 1500)]),
    hipotesis="La salida de la regresión lineal puede interpretarse como la probabilidad de ataque.",
    pregunta="<p>¿Qué conclusión es correcta?</p>",
    opciones=[(True, "Falsa: la recta produce valores menores que 0 y mayores que 1 (−0.21 y 2.11), imposibles como "
                     "probabilidad; la regresión logística usa la sigmoide para mantenerse entre 0 y 1."),
              (False, "Verdadera: una salida de 2.11 significa que el ataque es «doblemente seguro»."),
              (False, "Falsa, pero se arregla escalando pps con StandardScaler; así la recta queda entre 0 y 1."),
              (False, "Verdadera: basta con redondear la salida al entero más cercano.")],
    pista="El recuadro fija el rango válido; la tabla y la zona sombreada del gráfico muestran valores fuera de él.",
    retro="<p>Con 50 pps la recta da −0.21 y con 1 500 pps da 2.11: no son probabilidades. Escalar no cambia la "
          "forma de la recta (sigue siendo ilimitada). La regresión logística aplica la sigmoide y además se ajusta "
          "mejor a la forma «escalón» de los datos.</p>")


# ---------------------------------------------------------------------------
def g40():
    fig, axes = figura(8.6, 3.9, ncols=2)
    matriz_confusion(axes[0], [[1750, 40], [10, 200]], "Modelo A", etq0="Legítimo", etq1="Phishing", vmax=2000)
    matriz_confusion(axes[1], [[1640, 150], [2, 208]], "Modelo B", etq0="Legítimo", etq1="Phishing", vmax=2000)
    fig.suptitle("Phishing a empleados del banco - 2 000 correos de prueba", fontweight="bold", color=TINTA)
    return fig


reg(codigo="Q40", tipo="cloze", titulo="Elegir modelo por costo, no por exactitud",
    tema="Costo de errores y matriz de confusión", tema_tag="Metricas clasificacion", grafico=g40,
    contexto="<p>Un banco evalúa dos detectores de phishing. Seguridad estimó el costo promedio de cada error:</p>"
             "<ul><li><strong>Falso negativo</strong> (phishing que llega al empleado): <strong>5 000 Bs</strong> "
             "(fraude, recuperación de cuentas).</li>"
             "<li><strong>Falso positivo</strong> (correo legítimo bloqueado): <strong>50 Bs</strong> (tiempo de un "
             "analista).</li></ul>"
             + nota("costo total = FN × 5 000 + FP × 50. En la matriz, FN = abajo-izquierda y FP = arriba-derecha."),
    datos=(["modelo", "TN", "FP", "FN", "TP"], [["A", 1750, 40, 10, 200], ["B", 1640, 150, 2, 208]]),
    hipotesis="El modelo con mayor exactitud es también el más conveniente para el banco.",
    pregunta="<p>Completa:</p><ul>"
             "<li>Exactitud A = {1:NUMERICAL:=0.975:0.005} · Exactitud B = {1:NUMERICAL:=0.924:0.005}</li>"
             "<li>Costo A = {2:NUMERICAL:=52000:0} Bs · Costo B = {2:NUMERICAL:=17500:0} Bs</li>"
             "<li>El modelo más conveniente es {1:MULTICHOICE:=B~A} y la hipótesis "
             "{1:MULTICHOICE:=no se cumple~se cumple}</li></ul>"
             "<p><em>Escribe los costos sin puntos ni espacios (ej. 12500).</em></p>" + DEC,
    pista="El recuadro da la fórmula del costo y dónde está cada error en la matriz.",
    retro="<p>Exactitud A = (1750 + 200)/2000 = 0.975; B = (1640 + 208)/2000 = 0.924. Costo A = 10 × 5 000 + 40 × 50 "
          "= 52 000 Bs; Costo B = 2 × 5 000 + 150 × 50 = 17 500 Bs. B es menos exacto pero cuesta 3 veces menos: la "
          "hipótesis no se cumple.</p>")


# ---------------------------------------------------------------------------
def g41():
    fig, ax = figura(7.0, 3.5)
    et = ["Código original\n(escalar antes de dividir)", "Pipeline correcto\n(escalar solo train)",
          "Datos nuevos de la\nsemana siguiente"]
    b = ax.bar(et, [0.97, 0.95, 0.94], color=[NARANJA, AZUL, VERDE], width=0.55)
    etiquetas_barras(ax, b, "{:.2f}", dx=0.003)
    ax.set_ylim(0.85, 1.0)
    ax.set_ylabel("Exactitud")
    ax.set_title("k-NN para tráfico malicioso")
    return fig


reg(codigo="Q41", tipo="multi", titulo="Escalar antes de dividir: ¿resultado confiable?",
    tema="Fuga de información en el preprocesamiento", tema_tag="Data leakage", grafico=g41,
    contexto="<p>Un estudiante escribió este código para detectar tráfico malicioso:</p>"
             "<pre><code>scaler = StandardScaler()\n"
             "X_esc = scaler.fit_transform(X)          # TODO el dataset\n"
             "X_train, X_test, y_train, y_test = train_test_split(X_esc, y, test_size=0.2)\n"
             "modelo = KNeighborsClassifier().fit(X_train, y_train)</code></pre>"
             + nota("<code>fit</code> <strong>aprende</strong> algo de los datos (el escalador aprende la media y la "
                    "desviación). Si aprende de <em>todo</em> el dataset, los datos de prueba ya «influyeron» antes "
                    "de evaluar."),
    datos=(["experimento", "exactitud"],
           [["Código original", 0.97], ["Pipeline (escalador ajustado solo con train)", 0.95],
            ["Pipeline evaluado con datos nuevos", 0.94]]),
    hipotesis="El 0.97 obtenido con el código original es una medida confiable del desempeño real.",
    pregunta="<p>Selecciona <strong>todas</strong> las afirmaciones correctas (las incorrectas restan):</p>",
    opciones=[(True, "fit_transform(X) se aplica antes de dividir, así que la media y la desviación incluyen "
                     "información del conjunto de prueba."),
              (True, "Lo correcto es dividir primero y ajustar el escalador solo con X_train (por ejemplo, con un Pipeline)."),
              (True, "El 0.95 del Pipeline es una estimación más honesta: se parece más al desempeño con datos nuevos (0.94)."),
              (False, "k-NN no necesita escalado, así que el StandardScaler sobra."),
              (False, "Para evitar el problema también hay que escalar y_train."),
              (False, "La diferencia 0.97 vs 0.95 demuestra que el Pipeline es un peor modelo.")],
    pista="El recuadro explica qué aprende fit; el gráfico compara cada experimento con los datos nuevos.",
    retro="<p>El código original tiene una fuga leve: el escalador «vio» la prueba. El resultado (0.97) es optimista; "
          "el Pipeline (0.95) coincide mejor con los datos nuevos (0.94). k-NN sí necesita escalado y la etiqueta y "
          "no se escala en clasificación. La hipótesis es falsa.</p>")


# ---------------------------------------------------------------------------
rng42 = np.random.default_rng(42)
B42 = np.r_[rng42.lognormal(np.log(20_000), 1.1, 600)]


def g42():
    fig, axes = figura(8.8, 3.5, ncols=2)
    axes[0].hist(B42, bins=40, color=AZUL, edgecolor="#fcfcfb")
    axes[0].set_title("Original: bytes_descargados")
    axes[0].set_xlabel("bytes")
    axes[0].ticklabel_format(axis="x", style="plain")
    axes[0].tick_params(axis="x", labelrotation=30)
    axes[1].hist(np.log10(B42), bins=30, color=VERDE, edgecolor="#fcfcfb")
    axes[1].set_title("Transformada: log10(bytes)")
    axes[1].set_xlabel("log10(bytes)")
    for a in axes:
        a.set_ylabel("Frecuencia")
    return fig


reg(codigo="Q42", tipo="multichoice", titulo="Gaussian Naive Bayes y la transformación logarítmica",
    tema="Naive Bayes: supuestos y transformaciones", tema_tag="Naive Bayes", grafico=g42,
    contexto="<p>Se usa <strong>Gaussian Naive Bayes</strong> para detectar descargas sospechosas. La variable "
             "<code>bytes_descargados</code> tiene muchísimos valores pequeños y unos pocos enormes. Se probó aplicar "
             "<code>log10</code>.</p>"
             + nota("Gaussian Naive Bayes <strong>supone que cada variable numérica tiene forma de campana "
                    "(distribución normal)</strong> dentro de cada clase. Si la forma real es muy distinta, sus "
                    "probabilidades salen mal calculadas."),
    datos=(["descarga", "bytes_descargados", "log10(bytes)"],
           [[f"D{i + 1}", f"{B42[i]:,.0f}".replace(",", " "), f"{np.log10(B42[i]):.2f}"] for i in range(5)]),
    hipotesis="Aplicar logaritmo a <code>bytes_descargados</code> puede ayudar a Gaussian Naive Bayes.",
    pregunta="<p>Compara los dos histogramas. ¿Qué conclusión es correcta?</p>",
    opciones=[(True, "Verdadera: el logaritmo transforma una distribución muy sesgada en una forma parecida a una "
                     "campana, que es lo que asume Gaussian Naive Bayes."),
              (False, "Falsa: Naive Bayes no supone ninguna forma para las variables numéricas."),
              (False, "Verdadera, porque el logaritmo elimina del dataset las filas con valores atípicos."),
              (False, "Falsa: las transformaciones logarítmicas solo sirven para la regresión lineal.")],
    pista="El recuadro dice qué forma asume GaussianNB; el histograma de la derecha muestra esa forma.",
    retro="<p>El histograma original tiene cola larga a la derecha; tras <code>log10</code> se ve como una campana. "
          "Las filas no se eliminan: solo cambia la escala. Así el supuesto gaussiano se cumple mejor.</p>")


# ---------------------------------------------------------------------------
def g43():
    fig, ax = figura(7.0, 3.3)
    m = ["Árbol de decisión", "Naive Bayes", "Reg. logística", "k-NN"]
    v = [0.89, 0.88, 0.90, 0.91]
    b = ax.bar(m, v, color=AZUL, width=0.55)
    etiquetas_barras(ax, b, "{:.2f}", dx=0.003)
    ax.set_ylim(0.8, 0.95)
    ax.set_ylabel("Exactitud promedio (CV)")
    ax.set_title("Torneo de clasificadores: resultados muy parecidos")
    return fig


reg(codigo="Q43", tipo="matching", titulo="Elegir el clasificador según la necesidad del equipo",
    tema="Comparación de clasificadores", tema_tag="Comparacion de modelos", grafico=g43,
    contexto="<p>Cuatro equipos de TI necesitan un clasificador. En el «torneo» todos obtuvieron exactitud "
             "parecida, así que la decisión depende de <strong>otras características</strong> del modelo.</p>"
             + nota("piensa en la «personalidad» de cada modelo: el árbol se puede <em>leer</em> como reglas; Naive "
                    "Bayes <em>cuenta</em> frecuencias (muy rápido con palabras); la regresión logística da una "
                    "<em>probabilidad</em> con coeficientes interpretables; k-NN <em>compara</em> con los casos más "
                    "parecidos."),
    datos=(["modelo", "¿reglas legibles?", "¿necesita escalado?", "¿da probabilidad?", "velocidad con texto"],
           [["Árbol de decisión", "sí", "no", "aprox.", "media"], ["Naive Bayes", "no", "no", "sí", "muy alta"],
            ["Regresión logística", "coeficientes", "sí", "sí", "alta"], ["k-NN", "no", "sí", "aprox.", "baja"]]),
    hipotesis="Como los cuatro modelos tienen exactitud parecida, da igual cuál se use en cada equipo.",
    pregunta="<p>Empareja cada necesidad con el modelo más adecuado (sobra una opción):</p>",
    pares=[("Auditoría exige reglas «si… entonces…» que una persona pueda leer y justificar.", "Árbol de decisión"),
           ("Clasificar millones de correos por las palabras que contienen, reentrenando cada noche muy rápido.", "Naive Bayes"),
           ("Riesgo necesita una probabilidad de phishing y explicar el peso de cada variable con coeficientes.", "Regresión logística"),
           ("Clasificar un dispositivo nuevo buscando los dispositivos ya conocidos más parecidos.", "k-NN")],
    distractores=["Regresión lineal"],
    pista="El recuadro describe la «personalidad» de cada modelo con un verbo: leer, contar, probabilidad, comparar.",
    retro="<p>La exactitud no es el único criterio: interpretabilidad, velocidad y tipo de salida también importan. "
          "La regresión lineal no es un clasificador. La hipótesis es falsa.</p>")


# ---------------------------------------------------------------------------
def g44():
    fig, axes = figura(8.4, 3.4, ncols=2)
    b = axes[0].bar(["Normales", "Ataques"], [99, 1], color=[AZUL, NARANJA], width=0.5)
    etiquetas_barras(axes[0], b, "{:.0f} %", dx=1)
    axes[0].set_ylim(0, 112)
    axes[0].set_title("Composición del tráfico")
    b = axes[1].bar(["Ataques\n(alarma correcta)", "Normales\n(falsa alarma)"], [95, 5], color=[NARANJA, AZUL], width=0.5)
    etiquetas_barras(axes[1], b, "{:.0f} %", dx=1)
    axes[1].set_ylim(0, 112)
    axes[1].set_title("% de cada grupo que dispara alarma")
    return fig


reg(codigo="Q44", tipo="cloze", titulo="IDS: ¿qué tan confiable es una alarma?",
    tema="Teorema de Bayes y tasa base", tema_tag="Naive Bayes", grafico=g44,
    contexto="<p>Un IDS analiza <strong>10 000 conexiones</strong>. Solo el 1 % son ataques. El IDS detecta el 95 % "
             "de los ataques, pero también lanza alarma en el 5 % de las conexiones normales.</p>"
             + nota("trabaja con <strong>cantidades</strong>, no con porcentajes: primero cuántos ataques y normales "
                    "hay, luego cuántas alarmas genera cada grupo.<br><code>P(ataque | alarma) = alarmas de ataques / "
                    "total de alarmas</code>."),
    datos=(["grupo", "% del tráfico", "% que dispara alarma"], [["Ataques", "1 %", "95 %"], ["Normales", "99 %", "5 %"]]),
    hipotesis="Si el IDS lanza una alarma, hay 95 % de probabilidad de que sea un ataque real.",
    pregunta="<p>Completa:</p><ul>"
             "<li>Ataques reales = {1:NUMERICAL:=100:0} · Conexiones normales = {1:NUMERICAL:=9900:0}</li>"
             "<li>Alarmas por ataques reales = {1:NUMERICAL:=95:0} · Falsas alarmas = {1:NUMERICAL:=495:0}</li>"
             "<li>Total de alarmas = {1:NUMERICAL:=590:0}</li>"
             "<li>P(ataque | alarma) = {2:NUMERICAL:=0.161:0.005}</li>"
             "<li>La mayoría de las alarmas son {1:MULTICHOICE:=falsas alarmas~ataques reales} y la hipótesis "
             "{1:MULTICHOICE:=no se cumple~se cumple}</li></ul>" + DEC,
    pista="El recuadro pide pasar a cantidades: 1 % de 10 000, 95 % de ese grupo, 5 % de los normales.",
    retro="<p>100 ataques → 95 alarmas; 9 900 normales → 495 falsas alarmas; total 590. P(ataque | alarma) = "
          "95/590 ≈ 0.161. Aunque el detector es «95 % bueno», como los ataques son raros, 5 de cada 6 alarmas son "
          "falsas. Confundir P(alarma | ataque) con P(ataque | alarma) es un error clásico.</p>")


# ---------------------------------------------------------------------------
N45 = [100, 250, 500, 1000, 2000, 3000, 5000]
TR45 = [0.80, 0.77, 0.75, 0.73, 0.72, 0.72, 0.72]
VA45 = [0.60, 0.65, 0.68, 0.70, 0.71, 0.71, 0.71]


def g45():
    fig, ax = figura(7.0, 3.6)
    ax.plot(N45, TR45, "-o", color=AZUL, lw=2, label="Entrenamiento")
    ax.plot(N45, VA45, "-o", color=NARANJA, lw=2, label="Validación")
    ax.axhline(0.95, color=GRIS, ls=":", lw=1.5)
    ax.text(5000, 0.935, "meta: 0.95", ha="right", fontsize=9.5, color=TINTA2)
    ax.set_ylim(0.55, 1.0)
    ax.set_xlabel("Cantidad de correos de entrenamiento")
    ax.set_ylabel("Exactitud")
    ax.legend(loc="lower right")
    ax.set_title("Curva de aprendizaje - spam con 2 variables")
    return fig


reg(codigo="Q45", tipo="multichoice", titulo="Curva de aprendizaje: ¿más datos?",
    tema="Curvas de aprendizaje y subajuste", tema_tag="Overfitting", grafico=g45,
    contexto="<p>Un filtro de spam usa regresión logística con solo dos variables: <code>longitud_correo</code> y "
             "<code>cantidad_mayusculas</code>. Se entrenó con cantidades crecientes de correos.</p>"
             + nota("si las dos curvas <strong>ya se juntaron</strong> y se quedaron <strong>planas en un valor "
                    "bajo</strong>, el modelo es demasiado simple (subajuste): más datos del mismo tipo casi no "
                    "ayudan. Si siguen <strong>separadas</strong>, más datos sí suelen ayudar."),
    datos=(["correos", "entrenamiento", "validación"], [[n, a, b] for n, a, b in zip(N45, TR45, VA45)]),
    hipotesis="Si conseguimos 50 000 correos más, la exactitud de validación llegará a 0.95.",
    pregunta="<p>¿Qué conclusión es correcta?</p>",
    opciones=[(True, "Es poco probable: las curvas convergen en ≈ 0.71 (subajuste); conviene agregar variables más "
                     "informativas (palabras, enlaces, remitente) o un modelo más flexible."),
              (False, "Es muy probable: más datos siempre mejoran cualquier modelo."),
              (False, "El modelo sobreajusta; hay que simplificarlo aún más."),
              (False, "Hay fuga de información, porque las curvas se juntan.")],
    pista="El recuadro describe exactamente el patrón del gráfico: curvas juntas y planas en un valor bajo.",
    retro="<p>Desde ~2 000 correos ambas curvas quedan en 0.71–0.72: el modelo ya aprendió todo lo que dos "
          "variables permiten. El cuello de botella son las variables, no la cantidad de datos.</p>")


# ---------------------------------------------------------------------------
rng46 = np.random.default_rng(8)
P46_norm = np.clip(rng46.beta(2, 6, 400), 0, 1)
P46_atq = np.clip(rng46.beta(5, 3, 60), 0, 1)


def g46():
    fig, ax = figura(7.0, 3.5)
    bins = np.linspace(0, 1, 21)
    ax.hist(P46_norm, bins=bins, color=AZUL, alpha=0.75, label="Normal (real)")
    ax.hist(P46_atq, bins=bins, color=NARANJA, alpha=0.85, label="Ataque (real)")
    for u, s in ((0.3, ":"), (0.5, "--")):
        ax.axvline(u, color=TINTA, ls=s, lw=1.5)
        ax.text(u + 0.01, ax.get_ylim()[1] * 0.9, f"umbral {u}", fontsize=9.5)
    ax.set_xlabel("probabilidad de ataque (predict_proba, columna 1)")
    ax.set_ylabel("Conexiones")
    ax.legend(loc="upper right")
    ax.set_title("Distribución de probabilidades del modelo")
    return fig


reg(codigo="Q46", tipo="ddwtos", titulo="Cambiar el umbral y medir el recall",
    tema="Umbral, predict_proba y métricas", tema_tag="Umbral", grafico=g46,
    contexto="<p>El SOC quiere usar un <strong>umbral de 0.3</strong> (en lugar de 0.5) para detectar más ataques, y "
             "medir <strong>qué porcentaje de los ataques reales</strong> detecta el modelo.</p>"
             + nota("<code>predict</code> devuelve 0/1 con umbral 0.5; <code>predict_proba</code> devuelve dos "
                    "columnas: <code>[:, 0]</code> = P(normal) y <code>[:, 1]</code> = P(ataque). El porcentaje de "
                    "ataques reales detectados es el <strong>recall</strong>."),
    datos=(["conexión", "P(normal)", "P(ataque)", "real"],
           [[1, 0.82, 0.18, 0], [2, 0.64, 0.36, 1], [3, 0.21, 0.79, 1], [4, 0.55, 0.45, 0]]),
    hipotesis="Con umbral 0.3 la conexión 2 (P(ataque) = 0.36) pasa a ser detectada como ataque.",
    pregunta="<p>Arrastra las opciones para completar el código:</p>"
             "<pre><code>probs  = modelo.[[1]](X_test)[:, [[2]]]\n"
             "y_pred = (probs &gt;= [[3]]).astype(int)\n"
             "print([[4]](y_test, y_pred))</code></pre>",
    huecos=[("predict_proba", 1), ("1", 2), ("0.3", 3), ("recall_score", 4)],
    distractores=[("predict", 1), ("0", 2), ("0.5", 3), ("precision_score", 4), ("accuracy_score", 4)],
    pista="El recuadro explica las dos columnas de predict_proba y nombra la métrica pedida.",
    retro="<p><code>predict_proba(X_test)[:, 1]</code> da P(ataque); <code>probs &gt;= 0.3</code> aplica el nuevo "
          "umbral; <code>recall_score</code> mide los ataques detectados. La hipótesis es verdadera: 0.36 ≥ 0.3.</p>")


# ---------------------------------------------------------------------------
def _datos47():
    from sklearn.datasets import make_moons
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    X, y = make_moons(n_samples=400, noise=0.33, random_state=4)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
    res = {}
    for k in (1, 25):
        m = KNeighborsClassifier(n_neighbors=k).fit(Xtr, ytr)
        res[k] = (m, m.score(Xtr, ytr), m.score(Xte, yte))
    return Xtr, ytr, res


X47, Y47, R47 = _datos47()


def g47():
    from matplotlib.colors import ListedColormap
    fig, axes = figura(8.8, 3.8, ncols=2)
    xx, yy = np.meshgrid(np.linspace(-2, 3, 250), np.linspace(-1.6, 2.1, 250))
    for ax, k in zip(axes, (1, 25)):
        z = R47[k][0].predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, z, cmap=ListedColormap(["#a9c9f1", "#f6bba3"]))
        ax.scatter(X47[:, 0], X47[:, 1], c=[AZUL if v == 0 else NARANJA for v in Y47], s=14,
                   edgecolors="white", linewidths=0.4)
        ax.set_title(f"k = {k}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    fig.suptitle("Fronteras de decisión de k-NN (azul = normal, naranja = ataque)", fontweight="bold", color=TINTA)
    return fig


reg(codigo="Q47", tipo="multichoice", titulo="Fronteras de decisión de k-NN: k = 1 vs k = 25",
    tema="k-NN: fronteras de decisión", tema_tag="kNN", grafico=g47,
    contexto="<p>Se entrenó k-NN con dos valores de k para separar flujos de red normales y de ataque. Las zonas "
             "coloreadas muestran qué predice el modelo en cada punto del plano.</p>"
             + nota("una frontera <strong>muy irregular</strong>, con «islas» alrededor de puntos sueltos, indica que el "
                    "modelo <strong>memoriza el ruido</strong>. Una frontera suave que sigue la forma general de los "
                    "grupos suele <strong>generalizar</strong> mejor."),
    datos=(["k", "exactitud entrenamiento", "exactitud prueba"],
           [[k, f"{R47[k][1]:.2f}", f"{R47[k][2]:.2f}"] for k in (1, 25)]),
    hipotesis="El modelo con k = 1 es el mejor, porque su frontera clasifica correctamente todos los puntos de "
              "entrenamiento.",
    pregunta="<p>¿Qué conclusión es correcta?</p>",
    opciones=[(True, f"Falsa: k = 1 tiene frontera irregular con islas (sobreajuste, {R47[1][1]:.2f} vs "
                     f"{R47[1][2]:.2f}); k = 25 generaliza mejor (prueba {R47[25][2]:.2f})."),
              (False, "Verdadera: 100 % en entrenamiento garantiza el mejor modelo."),
              (False, "Falsa: k = 25 sobreajusta porque su frontera es suave."),
              (False, "Ambos son equivalentes, porque usan el mismo algoritmo.")],
    pista="El recuadro relaciona la forma de la frontera con memorizar vs generalizar; la tabla da los números.",
    retro=f"<p>Con k = 1 cada punto «se vota a sí mismo»: entrenamiento {R47[1][1]:.2f} pero prueba "
          f"{R47[1][2]:.2f}. Con k = 25 la frontera es suave y la prueba sube a {R47[25][2]:.2f}.</p>")


# ---------------------------------------------------------------------------
F48 = [0.80, 0.85, 0.90, 0.75, 0.70]


def g48():
    fig, ax = figura(7.0, 3.5)
    et = [f"Fold {i}" for i in range(1, 6)] + ["División\núnica"]
    v = F48 + [0.95]
    b = ax.bar(et, v, color=[AZUL] * 5 + [NARANJA], width=0.55)
    etiquetas_barras(ax, b, "{:.2f}")
    ax.axhline(np.mean(F48), color=TINTA, ls="--", lw=1.5, label="promedio de la validación cruzada")
    ax.legend(loc="lower left", facecolor="#fcfcfb", frameon=True, edgecolor=GRIS)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Recall de ataques")
    ax.set_title("Una división «con suerte» vs validación cruzada")
    return fig


reg(codigo="Q48", tipo="cloze", titulo="Una división con suerte vs validación cruzada",
    tema="Validación cruzada", tema_tag="Validacion cruzada", grafico=g48,
    contexto="<p>Un estudiante reportó <strong>recall = 0.95</strong> detectando ataques con una sola división "
             "train/test. El docente repitió la evaluación con <strong>validación cruzada de 5 folds</strong>.</p>"
             + nota("una sola división puede salir «con suerte» (casos fáciles en prueba). La validación cruzada "
                    "evalúa varias veces y se reporta el <strong>promedio</strong>; el <strong>rango</strong> (máximo − "
                    "mínimo) muestra cuánto varía."),
    datos=(["evaluación", "recall"], [[f"Fold {i + 1}", v] for i, v in enumerate(F48)] + [["División única", 0.95]]),
    hipotesis="El 0.95 representa el desempeño esperado del modelo con datos nuevos.",
    pregunta="<p>Completa:</p><ul>"
             "<li>Promedio de la validación cruzada = {1:NUMERICAL:=0.80:0.005}</li>"
             "<li>Rango (máximo − mínimo) de los folds = {1:NUMERICAL:=0.20:0.005}</li>"
             "<li>Diferencia entre la división única y el promedio = {1:NUMERICAL:=0.15:0.005}</li>"
             "<li>El valor más confiable para reportar es {1:MULTICHOICE:=el promedio de la validación cruzada~"
             "el 0.95 de la división única~el mejor fold (0.90)}</li>"
             "<li>La hipótesis {1:MULTICHOICE:=no se cumple~se cumple}</li></ul>" + DEC,
    pista="El recuadro dice qué se reporta (promedio) y cómo se calcula el rango.",
    retro="<p>Promedio = (0.80 + 0.85 + 0.90 + 0.75 + 0.70)/5 = 0.80; rango = 0.90 − 0.70 = 0.20; diferencia = "
          "0.95 − 0.80 = 0.15. El 0.95 es mayor que cualquier fold: fue una división con suerte.</p>")


# ---------------------------------------------------------------------------
ARB49 = [0.79, 0.84, 0.76, 0.83, 0.81]
RF49 = [0.90, 0.89, 0.91, 0.90, 0.90]


def g49():
    fig, axes = figura(8.8, 3.6, ncols=2)
    x = np.arange(2)
    b1 = axes[0].bar(x - 0.18, [1.00, 0.99], 0.34, color=AZUL, label="Entrenamiento")
    b2 = axes[0].bar(x + 0.18, [0.81, 0.90], 0.34, color=NARANJA, label="Prueba")
    etiquetas_barras(axes[0], list(b1) + list(b2), "{:.2f}")
    axes[0].set_xticks(x, ["Árbol (sin límite)", "Random Forest"])
    axes[0].set_ylim(0, 1.18)
    axes[0].legend(loc="upper center", ncol=2, fontsize=9)
    axes[0].set_title("Exactitud promedio")
    for i, (v, c) in enumerate(((ARB49, AZUL), (RF49, NARANJA))):
        axes[1].scatter([i] * 5, v, s=60, color=c, zorder=3)
    axes[1].set_xticks([0, 1], ["Árbol", "Random Forest"])
    axes[1].set_xlim(-0.6, 1.6)
    axes[1].set_ylim(0.7, 0.95)
    axes[1].set_ylabel("Exactitud de prueba")
    axes[1].set_title("Prueba en 5 ejecuciones (semillas)")
    return fig


reg(codigo="Q49", tipo="multi", titulo="Árbol único vs Random Forest",
    tema="Árboles vs Random Forest", tema_tag="Random Forest", grafico=g49,
    contexto="<p>Se compararon un árbol de decisión <strong>sin límite de profundidad</strong> y un Random Forest de "
             "200 árboles para detectar URLs maliciosas. Cada modelo se entrenó 5 veces con distintas semillas "
             "aleatorias.</p>"
             + nota("un Random Forest combina muchos árboles entrenados con muestras distintas; al <strong>promediar "
                    "votos</strong> reduce el sobreajuste y la <strong>variación</strong> entre ejecuciones."),
    datos=(["ejecución", "árbol (prueba)", "random forest (prueba)"],
           [[i + 1, a, r] for i, (a, r) in enumerate(zip(ARB49, RF49))]),
    hipotesis="Un Random Forest siempre es peor que un solo árbol porque es más complejo.",
    pregunta="<p>Selecciona <strong>todas</strong> las afirmaciones correctas (las incorrectas restan):</p>",
    opciones=[(True, "El árbol sin límite de profundidad muestra sobreajuste (1.00 en entrenamiento vs 0.81 en prueba)."),
              (True, "El Random Forest generaliza mejor: mayor exactitud de prueba y resultados más estables entre ejecuciones."),
              (True, "Limitar max_depth del árbol podría reducir su sobreajuste."),
              (False, "Es imposible que un Random Forest sobreajuste, porque promedia muchos árboles."),
              (False, "El árbol es mejor porque su exactitud de entrenamiento es 1.00."),
              (False, "La diferencia se debe a que el árbol necesita StandardScaler.")],
    pista="El recuadro anticipa los dos efectos del bosque: menos sobreajuste y menos variación (gráfico derecho).",
    retro="<p>Árbol: 1.00 vs 0.81 y resultados entre 0.76 y 0.84. RF: 0.90 estable (0.89–0.91). Un RF puede "
          "sobreajustar (aunque menos), y los árboles no necesitan escalado. La hipótesis es falsa.</p>")


# ---------------------------------------------------------------------------
def g50():
    fig, ax = figura(7.0, 3.4)
    et = ["Dataset completo\n(2 000)", "Train sin stratify\n(1 600)", "Test sin stratify\n(400)",
          "Test con stratify\n(400)"]
    v = [2.0, 38 / 1600 * 100, 2 / 400 * 100, 8 / 400 * 100]
    b = ax.bar(et, v, color=[GRIS, AZUL, NARANJA, VERDE], width=0.55)
    etiquetas_barras(ax, b, "{:.1f} %", dx=0.05)
    ax.set_ylim(0, 3)
    ax.set_ylabel("% de ataques")
    ax.set_title("Proporción de ataques en cada conjunto")
    return fig


reg(codigo="Q50", tipo="multichoice", titulo="Recall 100 % con solo 2 ataques en prueba",
    tema="División estratificada y clases raras", tema_tag="Train test split", grafico=g50,
    contexto="<p>Hay 2 000 registros de inicio de sesión, de los cuales <strong>40 son ataques</strong> (2 %). Se "
             "dividió con <code>train_test_split(X, y, test_size=0.2)</code> <strong>sin</strong> "
             "<code>stratify</code>. Por azar, la prueba quedó con solo <strong>2 ataques</strong>, y el modelo "
             "detectó ambos.</p>"
             + nota("con muy pocos casos, una métrica cambia muchísimo por <strong>un solo</strong> acierto o error. "
                    "<code>stratify=y</code> mantiene la <strong>misma proporción de clases</strong> en entrenamiento y "
                    "prueba."),
    datos=(["conjunto", "filas", "ataques", "% ataques"],
           [["Completo", 2000, 40, "2.0 %"], ["Train (sin stratify)", 1600, 38, "2.4 %"],
            ["Test (sin stratify)", 400, 2, "0.5 %"], ["Test (con stratify)", 400, 8, "2.0 %"]]),
    hipotesis="El modelo detecta el 100 % de los ataques (recall = 1.0), así que está listo para producción.",
    pregunta="<p>¿Qué conclusión es correcta?</p>",
    opciones=[(True, "Falsa: con solo 2 ataques en prueba el recall de 100 % no es confiable (si fallara uno, sería "
                     "50 %); hay que usar stratify=y (≈ 8 ataques en prueba) y, mejor aún, validación cruzada."),
              (False, "Verdadera: recall 1.0 significa que el modelo nunca fallará."),
              (False, "Falsa: hay que quitar los ataques del entrenamiento para que el modelo no se confunda."),
              (False, "Falsa: el problema se resuelve escalando las variables con StandardScaler.")],
    pista="El recuadro explica el efecto de pocos casos y qué hace stratify; el gráfico muestra 0.5 % vs 2 %.",
    retro="<p>2/2 = 100 %, pero 1/2 sería 50 %: la métrica no es estable con 2 casos. Con <code>stratify=y</code> la "
          "prueba tendría 2 % de 400 = 8 ataques, igual que el dataset completo.</p>")
