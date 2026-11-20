# -*- coding: utf-8 -*-
"""Nivel FÁCIL (Q01-Q20): escenarios simples de ciberseguridad / TI."""
import numpy as np
import matplotlib.pyplot as plt
from motor import (AZUL, NARANJA, VERDE, GRIS, TINTA, TINTA2, figura, etiquetas_barras,
                   matriz_confusion)

DIF, CAT = "Fácil", "1 - Fácil"
PREGUNTAS = []


def reg(**q):
    q.setdefault("dif", DIF)
    q.setdefault("cat", CAT)
    PREGUNTAS.append(q)


def nota(txt):
    """Recuadro de 'Recuerda' dentro del contexto (pista de lectura)."""
    return (f'<p style="background:#eef3fb;border-radius:6px;padding:6px 10px;margin:6px 0">'
            f"<strong>Recuerda:</strong> {txt}</p>")


# ---------------------------------------------------------------------------
def g01():
    fig, ax = figura(6.4, 3.2)
    b = ax.bar(["Legítimo", "Phishing"], [640, 160], color=[AZUL, NARANJA], width=0.55)
    etiquetas_barras(ax, b, "{:.0f}", dx=8)
    ax.set_ylabel("Cantidad de correos")
    ax.set_title("Correos etiquetados por los analistas (800)")
    ax.set_ylim(0, 730)
    return fig


reg(codigo="Q01", tipo="multichoice", titulo="¿Clasificación o regresión? Correos de phishing",
    tema="Tipos de problema supervisado", tema_tag="Clasificacion vs Regresion", grafico=g01,
    contexto="<p>El Centro de Operaciones de Seguridad (SOC) de la universidad revisó 800 correos y a cada uno "
             "le puso una <strong>etiqueta</strong>: <em>phishing</em> o <em>legítimo</em>. Ahora quieren un modelo "
             "que, cuando llegue un correo nuevo, diga <strong>a cuál de los dos grupos</strong> pertenece.</p>"
             + nota("si lo que queremos predecir es una <em>categoría</em> (un grupo, una clase) el problema es de "
                    "<strong>clasificación</strong>; si es una <em>cantidad numérica continua</em> (precio, tiempo, "
                    "GB) es de <strong>regresión</strong>. Lo que decide es la columna que se predice, no las "
                    "columnas de entrada."),
    datos=(["correo_id", "num_enlaces", "remitente_externo", "palabras_urgentes", "etiqueta (y)"],
           [["M-001", 7, "sí", 3, "phishing"], ["M-002", 1, "no", 0, "legítimo"],
            ["M-003", 4, "sí", 2, "phishing"], ["M-004", 0, "no", 1, "legítimo"],
            ["M-005", 2, "sí", 0, "legítimo"]]),
    hipotesis="Como casi todas las columnas de entrada son números (enlaces, palabras urgentes), este es un "
              "problema de regresión.",
    pregunta="<p>¿Qué tipo de problema es y por qué?</p>",
    opciones=[(True, "Clasificación, porque la variable que se predice (etiqueta) es una categoría: phishing o legítimo."),
              (False, "Regresión, porque las variables de entrada son numéricas."),
              (False, "Regresión, porque hay 800 correos y eso es una cantidad."),
              (False, "Ninguno: no se puede usar Machine Learning cuando hay columnas de texto como «sí/no».")],
    pista="El recuadro «Recuerda» indica que lo que define el tipo de problema es la columna que se predice.",
    retro="<p>La hipótesis es falsa. La columna objetivo <code>etiqueta</code> toma solo dos valores (phishing / "
          "legítimo), así que es <strong>clasificación binaria</strong>. Que las entradas sean numéricas no cambia "
          "el tipo de problema.</p>")


# ---------------------------------------------------------------------------
def g02():
    x = np.array([50, 80, 120, 150, 200])
    y = np.array([44, 70, 101, 126, 163])
    fig, ax = figura(6.8, 3.5)
    ax.scatter(x, y, s=60, color=AZUL, zorder=3, label="Días observados")
    xs = np.linspace(30, 220, 50)
    ax.plot(xs, 5 + 0.8 * xs, color=NARANJA, lw=2, label="Modelo: tráfico = 5 + 0.8 × usuarios")
    ax.set_xlabel("Usuarios conectados al Wi-Fi")
    ax.set_ylabel("Tráfico total (GB)")
    ax.set_title("Usuarios vs tráfico diario")
    ax.legend(loc="upper left")
    return fig


reg(codigo="Q02", tipo="truefalse", titulo="Pendiente de la regresión lineal del Wi-Fi",
    tema="Regresión lineal", tema_tag="Regresion lineal", grafico=g02,
    contexto="<p>El área de redes registró durante una semana cuántos usuarios se conectaron al Wi-Fi del campus "
             "y el tráfico total del día. Ajustaron una regresión lineal:</p>"
             "<p style='text-align:center'><code>trafico_GB = 5 + 0.8 × usuarios</code></p>"
             + nota("en <code>y = b + m·x</code>, la <strong>pendiente</strong> <code>m</code> dice cuánto cambia "
                    "<code>y</code> cuando <code>x</code> aumenta en <strong>1</strong>. Aquí, cada usuario "
                    "adicional suma 0.8 GB."),
    datos=(["día", "usuarios", "tráfico real (GB)"],
           [["Lun", 50, 44], ["Mar", 80, 70], ["Mié", 120, 101], ["Jue", 150, 126], ["Vie", 200, 163]]),
    hipotesis="Según el modelo, si se conectan 100 usuarios más, el tráfico aumentará aproximadamente 80 GB.",
    pregunta="<p>¿La hipótesis es verdadera o falsa?</p>",
    verdadero=True,
    pista="El recuadro explica que la pendiente 0.8 es el aumento por cada usuario; basta multiplicar por 100.",
    retro="<p><strong>Verdadero.</strong> La pendiente es 0.8 GB por usuario: 100 × 0.8 = 80 GB. El gráfico "
          "muestra la recta subiendo de forma constante (relación positiva).</p>")


# ---------------------------------------------------------------------------
def g03():
    fig, ax = figura(5.2, 3.9)
    matriz_confusion(ax, [[410, 18], [12, 60]], "Antivirus ML - 500 archivos",
                     etq0="Limpio", etq1="Malware", resaltar=(1, 0))
    return fig


reg(codigo="Q03", tipo="shortanswer", titulo="Nombre del error: malware que se deja pasar",
    tema="Matriz de confusión", tema_tag="Matriz de confusion", grafico=g03,
    contexto="<p>Un antivirus basado en Machine Learning analizó 500 archivos. Para el modelo, "
             "<strong>«positivo»</strong> significa <em>«este archivo es malware»</em> y <strong>«negativo»</strong> "
             "significa <em>«este archivo está limpio»</em>.</p>"
             + nota("el nombre de cada celda tiene dos partes: <strong>Verdadero/Falso</strong> (¿el modelo acertó?) "
                    "+ <strong>Positivo/Negativo</strong> (¿qué <em>dijo</em> el modelo?)."),
    datos=(["archivo", "tamaño (KB)", "ejecutable", "predicción", "real"],
           [["factura.pdf", 210, "no", "Limpio", "Limpio"], ["setup_crack.exe", 1840, "sí", "Malware", "Malware"],
            ["foto_viaje.jpg", 3100, "no", "Limpio", "Limpio"], ["invoice.exe", 96, "sí", "Limpio", "Malware"],
            ["update.bat", 4, "sí", "Malware", "Limpio"]]),
    hipotesis="Los 12 archivos marcados en naranja son los errores más peligrosos, porque son malware real que "
              "llegó al usuario.",
    pregunta="<p>Los 12 archivos del recuadro naranja eran <strong>malware real</strong>, pero el modelo dijo "
             "<strong>«Limpio»</strong> (por ejemplo, <code>invoice.exe</code>). ¿Cómo se llama este tipo de error? "
             "<em>(Escribe dos palabras.)</em></p>",
    respuestas=["falso negativo", "falsos negativos", "false negative", "false negatives", "FN"],
    pista="El recuadro explica que el nombre se forma con ¿acertó? (no → Falso) + ¿qué dijo? (Limpio → Negativo).",
    retro="<p><strong>Falso negativo (FN)</strong>: el modelo dijo «negativo» (limpio) y se equivocó. En "
          "ciberseguridad es el error más peligroso, porque el malware entra sin alerta. El caso contrario "
          "(<code>update.bat</code>: limpio marcado como malware) es un falso positivo.</p>")


# ---------------------------------------------------------------------------
def g04():
    fig, ax = figura(7.0, 2.4)
    ax.barh([0], [80], color=AZUL, height=0.5)
    ax.barh([0], [20], left=[80], color=NARANJA, height=0.5)
    ax.text(40, 0, "Entrenamiento (80 %)", ha="center", va="center", color="white", fontweight="bold")
    ax.text(90, 0, "Prueba\n(20 %)", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("% de los 1 000 registros de conexión")
    ax.set_title("División con test_size = 0.2")
    ax.grid(False)
    return fig


reg(codigo="Q04", tipo="multichoice", titulo="¿Cuántos registros van a prueba?",
    tema="División entrenamiento / prueba", tema_tag="Train test split", grafico=g04,
    contexto="<p>Un analista tiene <strong>1 000 registros</strong> de conexiones de red, cada uno etiquetado como "
             "<em>normal</em> o <em>ataque</em>. Antes de entrenar ejecuta:</p>"
             "<pre><code>X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)</code></pre>"
             + nota("<code>test_size</code> es la <em>proporción</em> (no la cantidad) de filas que se guardan para "
                    "<strong>evaluar</strong> el modelo con datos que nunca vio durante el entrenamiento."),
    datos=(["ip_origen", "puerto_destino", "paquetes", "duración (s)", "etiqueta"],
           [["10.0.0.15", 443, 120, 3.2, "normal"], ["185.22.4.9", 22, 950, 0.4, "ataque"],
            ["10.0.0.31", 80, 64, 1.1, "normal"], ["45.13.8.200", 3389, 1200, 0.2, "ataque"]]),
    hipotesis="Con <code>test_size=0.2</code> solo se usan 20 registros para evaluar el modelo.",
    pregunta="<p>¿Cuántos registros quedan en el conjunto de prueba y para qué se usan?</p>",
    opciones=[(True, "200 registros; sirven para evaluar el modelo con datos que no vio al entrenar."),
              (False, "800 registros; sirven para entrenar el modelo."),
              (False, "200 registros; sirven para volver a entrenar el modelo y subir su exactitud."),
              (False, "20 registros; el número 0.2 indica 20 filas.")],
    pista="El recuadro aclara que test_size es una proporción: 0.2 × 1 000.",
    retro="<p>0.2 × 1 000 = <strong>200</strong> registros de prueba (y 800 de entrenamiento). La prueba se usa "
          "<em>solo para evaluar</em>; si se entrenara con ella, ya no mediría el desempeño con datos nuevos.</p>")


# ---------------------------------------------------------------------------
def g05():
    cols = ["usuario", "hora_login", "pais_origen", "dispositivo", "login_exitoso"]
    pct = [0, 0, 38, 2, 0]
    fig, ax = figura(6.8, 3.2)
    b = ax.barh(cols, pct, color=[NARANJA if p > 10 else (AZUL if p else GRIS) for p in pct], height=0.6)
    etiquetas_barras(ax, b, "{:.0f} %", horizontal=True, dx=0.6)
    ax.invert_yaxis()
    ax.set_xlim(0, 45)
    ax.set_xlabel("% de valores nulos (de 2 000 filas)")
    ax.set_title("Valores nulos por columna")
    ax.grid(axis="y", visible=False)
    return fig


reg(codigo="Q05", tipo="truefalse", titulo="¿Eliminar todas las filas con nulos?",
    tema="Limpieza de datos (nulos)", tema_tag="Valores nulos", grafico=g05,
    contexto="<p>El registro de inicios de sesión del sistema académico tiene <strong>2 000 filas</strong>. La "
             "columna <code>pais_origen</code> se obtiene por geolocalización de la IP, que a veces falla y deja la "
             "celda vacía (NaN). El analista piensa usar <code>df.dropna()</code>.</p>"
             + nota("<code>dropna()</code> elimina <strong>toda la fila</strong> si tiene al menos un valor nulo en "
                    "<em>cualquier</em> columna."),
    datos=(["usuario", "hora_login", "pais_origen", "dispositivo", "login_exitoso"],
           [["jperez", "08:12", "Bolivia", "PC", 1], ["mrojas", "23:47", "<em>NaN</em>", "Móvil", 0],
            ["acruz", "10:05", "Bolivia", "PC", 1], ["lquispe", "02:31", "<em>NaN</em>", "<em>NaN</em>", 0]]),
    hipotesis="Aplicar <code>dropna()</code> a todo el dataset es buena idea porque solo se perderán unas pocas filas.",
    pregunta="<p>Observa el gráfico. ¿La hipótesis es verdadera o falsa?</p>",
    verdadero=False,
    pista="El gráfico muestra 38 % de nulos en pais_origen y el recuadro dice que dropna borra la fila completa.",
    retro="<p><strong>Falso.</strong> Al menos el 38 % de las filas (≈ 760 de 2 000) tiene <code>pais_origen</code> "
          "nulo, así que <code>dropna()</code> borraría más de un tercio del dataset, incluyendo información "
          "valiosa de las demás columnas. Es mejor imputar (por ejemplo con la categoría «Desconocido») o "
          "eliminar solo esa columna si no aporta.</p>")


# ---------------------------------------------------------------------------
MB06 = [("E01", "Contabilidad", 120), ("E02", "RRHH", 85), ("E03", "Sistemas", 340), ("E04", "Ventas", 9800),
        ("E05", "Legal", 210), ("E06", "Soporte", 260), ("E07", "Ventas", 150), ("E08", "Sistemas", 390),
        ("E09", "Contabilidad", 95), ("E10", "RRHH", 130)]


def g06():
    fig, ax = figura(7.2, 3.4)
    ax.bar([e for e, _, _ in MB06], [v for _, _, v in MB06], color=AZUL, width=0.6)
    ax.set_ylabel("MB subidos a internet")
    ax.set_title("Datos subidos por empleado (un día)")
    return fig


reg(codigo="Q06", tipo="multichoice", titulo="Valor atípico en datos subidos (DLP)",
    tema="Valores atípicos (outliers)", tema_tag="Outliers", grafico=g06,
    contexto="<p>El sistema de prevención de fuga de datos (DLP) mide cuántos MB sube cada empleado a internet "
             "por día. Normalmente los empleados suben entre 50 y 400 MB (correos, nube, videollamadas).</p>"
             + nota("un <strong>valor atípico (outlier)</strong> es un dato muy alejado del resto. Puede ser un "
                    "error de registro o algo real e importante; por eso primero se <em>investiga</em>."),
    datos=(["empleado", "área", "MB_subidos"], [[e, a, f"{v:,}".replace(",", " ")] for e, a, v in MB06[:6]]),
    hipotesis="Todos los empleados tienen un comportamiento de subida de datos parecido.",
    pregunta="<p>¿Qué empleado presenta un valor atípico y cuál es la acción más razonable?</p>",
    opciones=[(True, "E04: sube cerca de 25 veces más que los demás; hay que investigar si es una fuga de "
                     "información o un error de registro antes de usar o descartar el dato."),
              (False, "E03: porque es del área de Sistemas y ellos siempre son sospechosos."),
              (False, "E02: porque tiene el valor más bajo de la tabla."),
              (False, "Ninguno: todos están dentro de lo normal, la hipótesis es verdadera.")],
    pista="El recuadro da el rango normal (50–400 MB); solo un valor se sale muchísimo.",
    retro="<p>La hipótesis es falsa: E04 sube 9 800 MB, muy lejos del rango normal (50–400). En seguridad un "
          "outlier puede ser justamente el evento que buscamos (exfiltración de datos); no se borra sin "
          "investigarlo.</p>")


# ---------------------------------------------------------------------------
def g07():
    fig, ax = figura(7.6, 2.3)
    ax.axis("off")
    pasos = ["1 000 conexiones\netiquetadas", "Dividir\n80 % / 20 %", "ENTRENAR\ncon el 80 %",
             "PREDECIR\nel 20 % reservado", "Comparar con\nlas etiquetas reales"]
    for i, p in enumerate(pasos):
        x = 0.1 + i * 0.2
        ax.text(x, 0.5, p, ha="center", va="center", fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.5", fc="#eef3fb" if i not in (2, 3) else "#fde6dc",
                          ec=AZUL if i not in (2, 3) else NARANJA))
        if i < 4:
            ax.annotate("", xy=(x + 0.13, 0.5), xytext=(x + 0.07, 0.5),
                        arrowprops=dict(arrowstyle="->", color=TINTA2, lw=1.5))
    ax.set_xlim(0, 1)
    ax.set_title("Flujo de trabajo del detector de intrusiones")
    return fig


reg(codigo="Q07", tipo="ddwtos", titulo="Entrenar y predecir con Random Forest",
    tema="Random Forest con scikit-learn", tema_tag="Random Forest", grafico=g07,
    contexto="<p>Se construye un detector de intrusiones (IDS) con un <strong>Random Forest</strong> (bosque de "
             "árboles de decisión) para clasificar conexiones en <em>normal</em> o <em>ataque</em>. Los datos ya "
             "fueron divididos en <code>X_train, X_test, y_train, y_test</code>.</p>"
             + nota("en scikit-learn: <code>fit</code> = <strong>aprender/entrenar</strong> con datos de "
                    "entrenamiento; <code>predict</code> = <strong>predecir</strong> sobre datos nuevos. Los nombres "
                    "de los clasificadores terminan en <code>Classifier</code>."),
    datos=(["paquetes", "bytes", "puertos_distintos", "duración (s)", "etiqueta"],
           [[120, 54000, 1, 3.2, "normal"], [950, 61000, 45, 0.4, "ataque"], [64, 9800, 1, 1.1, "normal"]]),
    hipotesis="Para medir el desempeño real, el modelo debe predecir sobre los mismos datos con los que fue entrenado.",
    pregunta="<p>Arrastra las opciones para completar el código siguiendo el flujo del gráfico:</p>"
             "<pre><code>from sklearn.ensemble import [[1]]\n\n"
             "modelo = RandomForestClassifier(n_estimators=100, random_state=42)\n"
             "modelo.[[2]](X_train, y_train)\n"
             "y_pred = modelo.[[3]]([[4]])</code></pre>",
    huecos=[("RandomForestClassifier", 1), ("fit", 2), ("predict", 2), ("X_test", 3)],
    distractores=[("LinearRegression", 1), ("transform", 2), ("X_train", 3), ("y_test", 3)],
    pista="El recuadro traduce fit = entrenar y predict = predecir; el gráfico dice que se predice el 20 % reservado.",
    retro="<p>Se importa <code>RandomForestClassifier</code>, se entrena con <code>fit(X_train, y_train)</code> y se "
          "predice con <code>predict(X_test)</code>. La hipótesis es falsa: predecir sobre <code>X_train</code> daría "
          "un resultado optimista porque el modelo ya vio esos datos.</p>")


# ---------------------------------------------------------------------------
def g08():
    rng = np.random.default_rng(3)
    fig, ax = figura(6.4, 4.2)
    nx = np.r_[rng.uniform(0.5, 4, 10), rng.uniform(1, 3, 4)]
    ny = np.r_[rng.uniform(0.5, 3, 10), rng.uniform(5.5, 8, 4)]
    ax.scatter(nx, ny, s=45, color=AZUL, alpha=0.55)
    ax.scatter(rng.uniform(6.5, 8.5, 8), rng.uniform(5.5, 8.5, 8), s=45, color=NARANJA, alpha=0.55)
    vec = {"A": (5.8, 5.0, NARANJA), "B": (5.0, 6.1, NARANJA), "C": (3.7, 5.0, AZUL),
           "D": (5.0, 3.0, AZUL), "E": (6.9, 4.4, AZUL)}
    for k, (x, y, c) in vec.items():
        ax.scatter(x, y, s=90, color=c, edgecolor=TINTA, zorder=3)
        ax.text(x + 0.15, y + 0.15, k, fontsize=11, fontweight="bold", color=TINTA)
        ax.plot([5, x], [5, y], color=GRIS, lw=1, ls="--", zorder=1)
    ax.scatter(5, 5, marker="*", s=380, color="#f5c400", edgecolor=TINTA, zorder=4)
    ax.text(5.1, 4.55, "Nuevo", fontsize=10, color=TINTA)
    ax.scatter([], [], color=AZUL, label="normal")
    ax.scatter([], [], color=NARANJA, label="ataque")
    ax.legend(loc="upper left")
    ax.set_xlabel("intentos fallidos (escalado)")
    ax.set_ylabel("conexiones por minuto (escalado)")
    ax.set_title("Inicios de sesión: normal vs ataque")
    return fig


reg(codigo="Q08", tipo="multichoice", titulo="k-NN con k = 3: votación de vecinos",
    tema="k-Nearest Neighbors", tema_tag="kNN", grafico=g08,
    contexto="<p>Un sistema clasifica cada inicio de sesión como <em>normal</em> o <em>ataque</em> usando "
             "<strong>k-NN con k = 3</strong>. Llega un login nuevo (estrella amarilla). La tabla muestra sus 5 "
             "vecinos más cercanos ordenados por distancia.</p>"
             + nota("k-NN toma <strong>solo los k vecinos con menor distancia</strong> y asigna la clase que más se "
                    "repite entre ellos (votación). Los vecinos más lejanos no votan."),
    datos=(["vecino", "distancia al nuevo", "clase"],
           [["A", 0.8, "ataque"], ["B", 1.1, "ataque"], ["C", 1.3, "normal"], ["D", 2.0, "normal"],
            ["E", 2.2, "normal"]]),
    hipotesis="Como en la tabla hay más vecinos «normal» (3 de 5), el login nuevo será clasificado como normal.",
    pregunta="<p>Con <strong>k = 3</strong>, ¿cómo se clasifica el login nuevo?</p>",
    opciones=[(True, "Ataque: de los 3 vecinos más cercanos (A, B, C), 2 son ataque."),
              (False, "Normal: 3 de los 5 vecinos de la tabla son normal."),
              (False, "Normal: el vecino más lejano (E) decide el desempate."),
              (False, "No se puede decidir: hay un empate entre las clases.")],
    pista="El recuadro dice que solo votan los k = 3 de menor distancia (las tres primeras filas).",
    retro="<p>Los 3 más cercanos son A (ataque), B (ataque) y C (normal) → gana <strong>ataque</strong> 2 a 1. "
          "La hipótesis es falsa porque cuenta los 5 vecinos; con k = 5 sí ganaría normal. El valor de k cambia "
          "el resultado.</p>")


# ---------------------------------------------------------------------------
def g09():
    fig, ax = figura(6.8, 3.2)
    b = ax.bar(["bytes_enviados", "puertos_distintos"], [5_000_000, 20], color=[AZUL, NARANJA], width=0.5)
    ax.text(0, 5_050_000, "hasta 5 000 000", ha="center", va="bottom", fontsize=9.5, color=TINTA)
    ax.text(1, 150_000, "hasta 20\n(¡casi invisible!)", ha="center", va="bottom", fontsize=9.5, color=TINTA)
    ax.set_ylim(0, 5_900_000)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ")))
    ax.set_ylabel("Valor máximo")
    ax.set_title("Rango de cada variable (sin escalar)")
    return fig


reg(codigo="Q09", tipo="truefalse", titulo="k-NN sin escalar: ¿pesan igual las variables?",
    tema="Escalado de variables", tema_tag="Escalado", grafico=g09,
    contexto="<p>Se quiere detectar equipos que hacen <em>escaneo de puertos</em> con k-NN usando dos variables: "
             "<code>bytes_enviados</code> (de 0 a 5 000 000) y <code>puertos_distintos</code> (de 0 a 20).</p>"
             + nota("k-NN usa la <strong>distancia euclidiana</strong>: suma las diferencias al cuadrado de cada "
                    "variable. Una diferencia de 1 000 bytes pesa muchísimo más que una diferencia de 15 puertos si "
                    "no se escalan los datos."),
    datos=(["equipo", "bytes_enviados", "puertos_distintos", "clase"],
           [["PC-01", "1 200 000", 2, "normal"], ["PC-02", "1 201 000", 18, "escaneo"],
            ["PC-03", "4 800 000", 1, "normal"]]),
    hipotesis="Sin escalar, ambas variables influyen por igual en la distancia que calcula k-NN.",
    pregunta="<p>Compara PC-01 y PC-02 en la tabla y observa el gráfico. ¿La hipótesis es verdadera o falsa?</p>",
    verdadero=False,
    pista="El recuadro explica que la diferencia de bytes (miles) domina sobre la de puertos (decenas).",
    retro="<p><strong>Falso.</strong> Entre PC-01 y PC-02 la diferencia de bytes es 1 000 → 1 000² = 1 000 000, "
          "mientras que la de puertos es 16 → 16² = 256. La distancia la decide casi solo "
          "<code>bytes_enviados</code>, aunque <code>puertos_distintos</code> es la que revela el escaneo. Por eso "
          "k-NN necesita <code>StandardScaler</code> o <code>MinMaxScaler</code>.</p>")


# ---------------------------------------------------------------------------
def g10():
    fig, ax = figura(6.4, 3.2)
    b = ax.bar(["TCP", "UDP", "ICMP"], [620, 310, 70], color=AZUL, width=0.55)
    etiquetas_barras(ax, b, "{:.0f}", dx=8)
    ax.set_ylim(0, 700)
    ax.set_ylabel("Cantidad de conexiones")
    ax.set_title("Valores de la columna «protocolo»")
    return fig


reg(codigo="Q10", tipo="shortanswer", titulo="One-Hot Encoding de la columna protocolo",
    tema="Codificación de variables categóricas", tema_tag="One-Hot Encoding", grafico=g10,
    contexto="<p>Un dataset de tráfico de red tiene la columna <code>protocolo</code>. Los modelos de scikit-learn "
             "necesitan números, así que hay que codificarla. Los protocolos <strong>no tienen un orden</strong> "
             "(TCP no es «mayor» que UDP).</p>"
             + nota("<strong>One-Hot Encoding</strong> crea <strong>una columna nueva de 0/1 por cada categoría "
                    "distinta</strong>. Ejemplo: colores {rojo, verde} → <code>color_rojo</code>, "
                    "<code>color_verde</code>."),
    datos=(["conexion", "protocolo", "bytes", "etiqueta"],
           [[1, "TCP", 5400, "normal"], [2, "UDP", 300, "normal"], [3, "ICMP", 64, "ataque"],
            [4, "TCP", 120000, "ataque"]]),
    hipotesis="Basta con reemplazar TCP = 1, UDP = 2, ICMP = 3; así el modelo entenderá que ICMP es «mayor» que TCP.",
    pregunta="<p>La hipótesis es incorrecta porque inventa un orden. Si en su lugar aplicamos One-Hot Encoding "
             "(sin eliminar ninguna columna), <strong>¿cuántas columnas nuevas se crean?</strong> "
             "<em>(Escribe solo el número.)</em></p>",
    respuestas=["3", "tres"],
    pista="El gráfico muestra cuántas categorías distintas hay; el recuadro dice una columna por categoría.",
    retro="<p>Hay 3 categorías (TCP, UDP, ICMP) → <strong>3 columnas</strong>: <code>protocolo_TCP</code>, "
          "<code>protocolo_UDP</code>, <code>protocolo_ICMP</code>. Numerar 1, 2, 3 crea un orden falso que modelos "
          "como k-NN o la regresión logística interpretarían como distancias o magnitudes.</p>")


# ---------------------------------------------------------------------------
def g11():
    z = np.linspace(-6, 6, 200)
    s = 1 / (1 + np.exp(-z))
    fig, ax = figura(6.8, 3.6)
    ax.plot(z, s, color=AZUL, lw=2)
    ax.axhline(0.5, color=NARANJA, ls="--", lw=1.5)
    ax.text(-5.9, 0.53, "umbral = 0.5", color=TINTA, fontsize=9.5)
    pts = {"C1": -2.0, "C2": 0.0, "C3": 1.6, "C4": -0.8}
    for k, zz in pts.items():
        p = 1 / (1 + np.exp(-zz))
        ax.scatter(zz, p, s=70, color=TINTA, zorder=3)
        ax.text(zz + 0.2, p - 0.07, k, fontsize=10.5, fontweight="bold")
    ax.set_xlabel("puntaje z del modelo")
    ax.set_ylabel("P(phishing)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Función sigmoide de la regresión logística")
    return fig


reg(codigo="Q11", tipo="multichoice", titulo="Sigmoide y umbral: ¿cuáles son phishing?",
    tema="Regresión logística", tema_tag="Regresion logistica", grafico=g11,
    contexto="<p>Un filtro de correo usa <strong>regresión logística</strong>. El modelo calcula un puntaje "
             "<code>z</code> y la <strong>función sigmoide</strong> lo convierte en una probabilidad entre 0 y 1.</p>"
             + nota("la regla del filtro es: si <code>P(phishing) ≥ 0.5</code> → <strong>phishing</strong>; si es "
                    "menor → legítimo. Observa que el signo es <em>mayor <u>o igual</u></em>."),
    datos=(["correo", "puntaje z", "P(phishing)"],
           [["C1", -2.0, 0.12], ["C2", 0.0, 0.50], ["C3", 1.6, 0.83], ["C4", -0.8, 0.31]]),
    hipotesis="Solo el correo C3 será marcado como phishing.",
    pregunta="<p>Con umbral 0.5, ¿cuántos correos se marcan como phishing?</p>",
    opciones=[(True, "2 correos: C2 y C3, porque su probabilidad es mayor o igual a 0.5."),
              (False, "1 correo: solo C3, porque es el único con probabilidad alta."),
              (False, "3 correos: C2, C3 y C4, porque sus puntajes z son mayores que el de C1."),
              (False, "Ninguno: para ser phishing la probabilidad debe ser mayor a 0.9.")],
    pista="El recuadro destaca el «mayor o igual»; C2 está exactamente en 0.50.",
    retro="<p>C2 (0.50) y C3 (0.83) cumplen <code>P ≥ 0.5</code> → 2 correos. La hipótesis es falsa porque olvida "
          "el caso límite. En la gráfica: z = 0 corresponde exactamente a P = 0.5.</p>")


# ---------------------------------------------------------------------------
def g12():
    fig, ax = figura(5.2, 3.9)
    matriz_confusion(ax, [[50, 5], [5, 40]], "Filtro de spam - 100 correos", etq0="Normal", etq1="Spam")
    return fig


reg(codigo="Q12", tipo="multichoice", titulo="Exactitud del filtro de spam",
    tema="Métricas: exactitud", tema_tag="Exactitud", grafico=g12,
    contexto="<p>Se evaluó un filtro de spam con <strong>100 correos</strong> que ya tenían etiqueta real. La matriz "
             "de confusión resume los resultados.</p>"
             + nota("<strong>exactitud (accuracy) = aciertos / total</strong>. Los aciertos están en la "
                    "<strong>diagonal</strong> de la matriz (arriba-izquierda y abajo-derecha)."),
    datos=(["correo", "asunto", "predicción", "real"],
           [["#12", "Reunión de área", "Normal", "Normal"], ["#37", "¡Ganaste un iPhone!", "Spam", "Spam"],
            ["#58", "Factura pendiente", "Spam", "Normal"], ["#81", "Oferta exclusiva", "Normal", "Spam"]]),
    hipotesis="El filtro acierta en 9 de cada 10 correos.",
    pregunta="<p>¿Cuál es la exactitud del filtro y se cumple la hipótesis?</p>",
    opciones=[(True, "0.90; sí se cumple: (50 + 40) aciertos de 100."),
              (False, "0.40; no se cumple: solo cuenta los 40 spam detectados."),
              (False, "0.50; no se cumple: solo cuenta los 50 correos normales."),
              (False, "0.95; sí se cumple: solo se resta un tipo de error.")],
    pista="El recuadro dice que los aciertos están en la diagonal (50 y 40).",
    retro="<p>Exactitud = (50 + 40) / 100 = <strong>0.90</strong>. Los 10 errores son 5 falsos positivos y 5 falsos "
          "negativos. La hipótesis se cumple.</p>")


# ---------------------------------------------------------------------------
def g13():
    fig, ax = figura(5.8, 3.4)
    b = ax.bar(["Entrenamiento", "Prueba"], [0.99, 0.62], color=[AZUL, NARANJA], width=0.5)
    etiquetas_barras(ax, b, "{:.0%}")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Exactitud")
    ax.set_title("Detector de bots en el portal web")
    return fig


reg(codigo="Q13", tipo="truefalse", titulo="Detector de bots: ¿sobreajuste?",
    tema="Sobreajuste y subajuste", tema_tag="Overfitting", grafico=g13,
    contexto="<p>Un detector de bots para el portal de inscripciones fue entrenado con un árbol de decisión muy "
             "profundo. Los resultados se muestran en el gráfico.</p>"
             + nota("cuando un modelo <strong>memoriza</strong> los datos de entrenamiento (como un estudiante que "
                    "memoriza el solucionario), obtiene notas altísimas en entrenamiento pero bajas con datos "
                    "nuevos. A esto se le llama <strong>sobreajuste (overfitting)</strong>."),
    datos=(["conjunto", "registros", "exactitud"], [["Entrenamiento", 4000, "99 %"], ["Prueba", 1000, "62 %"]]),
    hipotesis="El modelo presenta sobreajuste (overfitting).",
    pregunta="<p>¿La hipótesis es verdadera o falsa?</p>",
    verdadero=True,
    pista="El recuadro describe exactamente el patrón del gráfico: muy alto en entrenamiento, bajo en prueba.",
    retro="<p><strong>Verdadero.</strong> Hay una brecha de 37 puntos (99 % vs 62 %): el árbol memorizó el "
          "entrenamiento. Se puede corregir limitando <code>max_depth</code>, usando más datos o un Random Forest.</p>")


# ---------------------------------------------------------------------------
def g14():
    fig, ax = figura(6.4, 3.2)
    b = ax.bar(["Benigno", "Malicioso"], [0.3, 4.1], color=[AZUL, NARANJA], width=0.5)
    etiquetas_barras(ax, b, "{:.1f}", dx=0.05)
    ax.set_ylim(0, 4.8)
    ax.set_ylabel("Promedio de archivos_autorun")
    ax.set_title("Archivos autorun según el tipo de USB")
    return fig


reg(codigo="Q14", tipo="matching", titulo="Roles de las columnas en el dataset de USB",
    tema="Conceptos básicos de ML", tema_tag="Conceptos basicos", grafico=g14,
    contexto="<p>Seguridad informática quiere predecir si un dispositivo USB conectado a los equipos del laboratorio "
             "es <strong>malicioso</strong>. Tienen 500 dispositivos analizados: usan el 80 % para entrenar y "
             "guardan el 20 % para evaluar.</p>"
             + nota("la columna que queremos <strong>adivinar</strong> es la <em>etiqueta</em> (y); las columnas que "
                    "<strong>usamos para adivinar</strong> son las <em>variables predictoras</em> (X). Un código único "
                    "por fila no describe al dispositivo."),
    datos=(["id_dispositivo", "fabricante", "archivos_autorun", "tamaño_GB", "es_malicioso"],
           [["USB-0001", "Kingston", 0, 16, 0], ["USB-0002", "Genérico", 5, 2, 1], ["USB-0003", "SanDisk", 0, 64, 0],
            ["USB-0004", "Genérico", 3, 4, 1]]),
    hipotesis="La columna <code>id_dispositivo</code> ayuda al modelo porque es diferente en cada fila.",
    pregunta="<p>Empareja cada elemento con su rol en el proyecto (sobra una opción):</p>",
    pares=[("<code>es_malicioso</code>", "Variable objetivo (etiqueta, y)"),
           ("<code>archivos_autorun</code>", "Variable predictora (feature, X)"),
           ("<code>id_dispositivo</code>", "Identificador: no se usa para predecir"),
           ("El 80 % de los dispositivos con los que se hace fit", "Conjunto de entrenamiento"),
           ("El 20 % reservado para medir el desempeño", "Conjunto de prueba")],
    distractores=["Hiperparámetro del modelo"],
    pista="El recuadro define etiqueta (lo que se adivina), predictoras (lo que se usa) y advierte sobre los códigos únicos.",
    retro="<p><code>es_malicioso</code> es la etiqueta; <code>archivos_autorun</code> es una buena predictora "
          "(el gráfico muestra 4.1 vs 0.3 en promedio). La hipótesis es falsa: <code>id_dispositivo</code> es "
          "distinto en cada fila, no se repite en dispositivos nuevos y solo invita a memorizar.</p>")


# ---------------------------------------------------------------------------
def g15():
    fig, ax = figura(7.6, 3.8)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    nodos = {"r": (5, 5.2, "¿intentos_fallidos > 5?", "#eef3fb", AZUL),
             "a": (2.6, 3.2, "¿hora entre 00:00 y 05:00?", "#eef3fb", AZUL),
             "b": (7.4, 3.2, "¿país nuevo para el usuario?", "#eef3fb", AZUL),
             "a1": (1.2, 0.9, "BLOQUEAR", "#fde6dc", NARANJA), "a2": (3.9, 0.9, "PEDIR 2FA", "#fff4d6", "#c98500"),
             "b1": (6.1, 0.9, "PEDIR 2FA", "#fff4d6", "#c98500"), "b2": (8.8, 0.9, "PERMITIR", "#e3f5ea", VERDE)}
    aristas = [("r", "a", "Sí"), ("r", "b", "No"), ("a", "a1", "Sí"), ("a", "a2", "No"), ("b", "b1", "Sí"),
               ("b", "b2", "No")]
    for p, h, t in aristas:
        x1, y1 = nodos[p][:2]
        x2, y2 = nodos[h][:2]
        ax.annotate("", xy=(x2, y2 + 0.35), xytext=(x1, y1 - 0.35),
                    arrowprops=dict(arrowstyle="->", color=TINTA2, lw=1.4))
        ax.text((x1 + x2) / 2 + (-0.35 if x2 < x1 else 0.15), (y1 + y2) / 2, t, fontsize=10, color=TINTA,
                fontweight="bold")
    for x, y, t, fc, ec in nodos.values():
        ax.text(x, y, t, ha="center", va="center", fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.45", fc=fc, ec=ec, lw=1.5))
    ax.set_title("Árbol de decisión para inicios de sesión")
    return fig


reg(codigo="Q15", tipo="multichoice", titulo="Leer un árbol de decisión de logins",
    tema="Árboles de decisión", tema_tag="Arboles de decision", grafico=g15,
    contexto="<p>El sistema de autenticación usa un <strong>árbol de decisión</strong> para decidir qué hacer con "
             "cada inicio de sesión: permitirlo, pedir un segundo factor (2FA) o bloquearlo.</p>"
             + nota("un árbol se lee <strong>de arriba hacia abajo</strong>: respondes la pregunta del nodo, sigues "
                    "la flecha «Sí» o «No» y repites hasta llegar a una hoja (decisión final)."),
    datos=(["login", "intentos_fallidos", "hora", "país nuevo"],
           [["L1", 8, "03:10", "no"], ["L2", 1, "14:25", "sí"], ["L3", 7, "10:40", "no"]]),
    hipotesis="Un login con muchos intentos fallidos siempre será bloqueado.",
    pregunta="<p>¿Qué decisión toma el árbol para L1, L2 y L3?</p>",
    opciones=[(True, "L1: Bloquear · L2: Pedir 2FA · L3: Pedir 2FA"),
              (False, "L1: Bloquear · L2: Permitir · L3: Bloquear"),
              (False, "L1: Pedir 2FA · L2: Pedir 2FA · L3: Bloquear"),
              (False, "L1: Bloquear · L2: Bloquear · L3: Bloquear")],
    pista="El recuadro explica cómo recorrer el árbol; L3 tiene muchos intentos pero su hora no es nocturna.",
    retro="<p>L1: 8 > 5 → Sí; 03:10 es nocturna → <strong>Bloquear</strong>. L2: 1 > 5 → No; país nuevo → "
          "<strong>Pedir 2FA</strong>. L3: 7 > 5 → Sí; 10:40 no es nocturna → <strong>Pedir 2FA</strong>. "
          "La hipótesis es falsa: L3 tiene muchos intentos y no se bloquea.</p>")


# ---------------------------------------------------------------------------
def g16():
    fig, ax = figura(6.2, 3.2)
    b = ax.bar(["ataque", "normal"], [73, 27], color=[NARANJA, AZUL], width=0.5)
    etiquetas_barras(ax, b, "{:.0f} votos", dx=1)
    ax.set_ylim(0, 85)
    ax.set_ylabel("Votos de los árboles")
    ax.set_title("Votación de 100 árboles para la conexión #4512")
    return fig


reg(codigo="Q16", tipo="shortanswer", titulo="El modelo que vota con muchos árboles",
    tema="Random Forest", tema_tag="Random Forest", grafico=g16,
    contexto="<p>En vez de un solo árbol de decisión, el equipo entrenó <strong>100 árboles</strong>. Cada árbol "
             "aprendió con una muestra <strong>elegida al azar</strong> de los datos y con variables elegidas al "
             "azar. Para clasificar una conexión, <strong>cada árbol vota</strong> y gana la mayoría.</p>"
             + nota("muchos árboles juntos forman un <em>bosque</em>; y como cada árbol usa datos tomados al azar, "
                    "se dice que es un bosque <em>aleatorio</em>."),
    datos=(["árbol", "voto para la conexión #4512"],
           [["Árbol 1", "ataque"], ["Árbol 2", "ataque"], ["Árbol 3", "normal"], ["Árbol 4", "ataque"],
            ["…", "…"], ["Árbol 100", "ataque"]]),
    hipotesis="La decisión final del conjunto es «ataque», porque la mayoría de los árboles votó así.",
    pregunta="<p>La hipótesis es correcta (73 vs 27 votos). <strong>¿Cómo se llama este modelo?</strong> "
             "<em>(Puedes escribirlo en español o en inglés.)</em></p>",
    respuestas=["random forest", "bosque aleatorio", "bosques aleatorios", "random forests", "randomforest",
                "RandomForestClassifier", "bosque aleatorio (random forest)", "random forest classifier"],
    pista="El recuadro casi deletrea el nombre: bosque + aleatorio.",
    retro="<p><strong>Random Forest (bosque aleatorio)</strong>. Combinar muchos árboles distintos reduce el "
          "sobreajuste de un solo árbol: los errores de algunos árboles se compensan con los aciertos de otros.</p>")


# ---------------------------------------------------------------------------
SEM17 = [(1, 410, 38, 55), (2, 460, 44, 54), (3, 520, 51, 70), (4, 600, 63, 72), (5, 650, 70, 86),
         (6, 720, 79, 84), (7, 800, 88, 99), (8, 880, 95, 104)]


def g17():
    caf = np.array([s[3] for s in SEM17])
    ale = np.array([s[2] for s in SEM17])
    fig, ax = figura(6.6, 3.6)
    ax.scatter(caf, ale, s=60, color=AZUL, zorder=3)
    m, b = np.polyfit(caf, ale, 1)
    ax.plot(caf, m * caf + b, color=NARANJA, lw=2)
    r = np.corrcoef(caf, ale)[0, 1]
    ax.text(54, 88, f"correlación r = {r:.2f}", fontsize=10, color=TINTA)
    ax.set_xlabel("Tazas de café en el SOC (semana)")
    ax.set_ylabel("Alertas de seguridad (semana)")
    ax.set_title("Café vs alertas de seguridad")
    return fig


reg(codigo="Q17", tipo="truefalse", titulo="Café y alertas: ¿correlación o causa?",
    tema="Correlación vs causalidad", tema_tag="Correlacion", grafico=g17,
    contexto="<p>Durante el cierre de gestión, el SOC registró por semana las <strong>alertas de seguridad</strong> y "
             "las <strong>tazas de café</strong> que tomaron los analistas. En esas semanas también aumentó mucho "
             "la cantidad de <strong>usuarios activos</strong> en los sistemas.</p>"
             + nota("que dos variables suban juntas (<strong>correlación</strong>) no prueba que una <em>cause</em> "
                    "a la otra. Puede existir una <strong>tercera variable</strong> que mueve a las dos."),
    datos=(["semana", "usuarios_activos", "alertas", "tazas_café"], [list(s) for s in SEM17[::2]]),
    hipotesis="Si prohibimos el café en el SOC, las alertas de seguridad disminuirán.",
    pregunta="<p>¿La hipótesis es verdadera o falsa?</p>",
    verdadero=False,
    pista="El contexto menciona una tercera variable (usuarios activos) que sube junto con las otras dos.",
    retro="<p><strong>Falso.</strong> Café y alertas están muy correlacionados, pero ambos aumentan por una tercera "
          "variable: más usuarios activos → más alertas y más trabajo (más café). Quitar el café no reduce las "
          "alertas. Correlación ≠ causalidad.</p>")


# ---------------------------------------------------------------------------
def g18():
    fig, ax = figura(6.2, 3.3)
    b = ax.bar(["normal", "ataque"], [990, 10], color=[AZUL, NARANJA], width=0.5)
    etiquetas_barras(ax, b, "{:.0f}", dx=10)
    ax.set_ylim(0, 1100)
    ax.set_ylabel("Conexiones")
    ax.set_title("Clases en el conjunto de prueba (1 000)")
    return fig


reg(codigo="Q18", tipo="multichoice", titulo="El modelo «perezoso» con 99 % de exactitud",
    tema="Clases desbalanceadas", tema_tag="Desbalance de clases", grafico=g18,
    contexto="<p>En una red, de 1 000 conexiones solo <strong>10 son ataques</strong>. Un practicante entrega un "
             "modelo que <strong>siempre responde «normal»</strong>, sin importar los datos de entrada.</p>"
             + nota("<strong>recall de ataques</strong> = ataques detectados / ataques reales. Mide qué parte de los "
                    "ataques logramos atrapar."),
    datos=(["conexión", "real", "predicción del modelo"],
           [[1, "normal", "normal"], [2, "normal", "normal"], [3, "ataque", "normal"], [4, "normal", "normal"],
            [5, "ataque", "normal"]]),
    hipotesis="Un modelo con 99 % de exactitud es excelente para detectar ataques.",
    pregunta="<p>El modelo obtiene 990/1 000 = 99 % de exactitud. ¿Qué conclusión es correcta?</p>",
    opciones=[(True, "La exactitud engaña: el modelo detecta 0 de 10 ataques (recall de ataques = 0), así que no sirve."),
              (False, "El modelo es excelente: 99 % es casi perfecto."),
              (False, "El problema es que hay muy pocas conexiones normales en los datos."),
              (False, "Si la exactitud es 99 %, el recall también es 99 %.")],
    pista="El recuadro da la fórmula del recall; en la tabla, los ataques reales siempre se predicen como normal.",
    retro="<p>Con clases desbalanceadas (99 % normal) la exactitud puede ser alta sin detectar nada. Recall de "
          "ataques = 0/10 = 0. Hay que mirar recall, precisión y la matriz de confusión.</p>")


# ---------------------------------------------------------------------------
def g19():
    rng = np.random.default_rng(5)
    t = np.r_[rng.normal(150, 35, 300), rng.uniform(900, 2500, 12)]
    fig, ax = figura(7.0, 3.4)
    ax.hist(t, bins=np.arange(0, 2600, 50), color=AZUL, edgecolor="#fcfcfb")
    ax.annotate("12 solicitudes extremas\n(900 – 2 500 ms)", xy=(1700, 2), xytext=(1150, 70), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color=TINTA2))
    ax.axvline(np.median(t), color=TINTA, lw=2, label=f"Mediana ≈ {np.median(t):.0f} ms")
    ax.axvline(t.mean(), color=NARANJA, lw=2, ls="--", label=f"Media ≈ {t.mean():.0f} ms")
    ax.legend(loc="upper right")
    ax.set_xlabel("tiempo_respuesta_ms")
    ax.set_ylabel("Cantidad de solicitudes")
    ax.set_title("Tiempo de respuesta del servidor web")
    return fig


reg(codigo="Q19", tipo="ddwtos", titulo="Código de preprocesamiento para k-NN",
    tema="Preprocesamiento (imputación, codificación, escalado)", tema_tag="Preprocesamiento", grafico=g19,
    contexto="<p>Se preparan datos de un servidor web para un modelo k-NN que detecta solicitudes anómalas:</p>"
             "<ul><li><code>tiempo_respuesta_ms</code> tiene nulos y algunos valores extremos → rellenar con el "
             "<strong>valor del medio</strong> (robusto a extremos).</li>"
             "<li><code>sistema_operativo</code> (Windows, Linux, macOS) no tiene orden → crear "
             "<strong>una columna 0/1 por categoría</strong>.</li>"
             "<li>k-NN usa distancias → dejar todas las variables con <strong>media 0 y desviación 1</strong>.</li></ul>",
    datos=(["solicitud", "tiempo_respuesta_ms", "sistema_operativo", "bytes"],
           [[1, 142, "Windows", 5300], [2, "<em>NaN</em>", "Linux", 880], [3, 2310, "macOS", 120],
            [4, 161, "Windows", 4100]]),
    hipotesis="La media es la mejor opción para rellenar los nulos de <code>tiempo_respuesta_ms</code>.",
    pregunta="<p>Arrastra las opciones para completar el código:</p>"
             "<pre><code>from sklearn.impute import SimpleImputer\n"
             "from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler\n\n"
             "imputador   = SimpleImputer(strategy=\"[[1]]\")\n"
             "codificador = [[2]](handle_unknown=\"ignore\")\n"
             "escalador   = [[3]]()</code></pre>",
    huecos=[("median", 1), ("OneHotEncoder", 2), ("StandardScaler", 3)],
    distractores=[("mean", 1), ("OrdinalEncoder", 2), ("RandomForestClassifier", 3)],
    pista="Cada viñeta del contexto describe con palabras el paso: valor del medio, columna 0/1 por categoría, media 0 y desviación 1.",
    retro="<p><code>median</code>: el histograma muestra valores extremos que inflan la media, así que la hipótesis "
          "es falsa. <code>OneHotEncoder</code>: categorías sin orden. <code>StandardScaler</code>: media 0 y "
          "desviación 1 para que ninguna variable domine la distancia de k-NN.</p>")


# ---------------------------------------------------------------------------
AREAS20 = [("Contabilidad", 4, 25), ("Ventas", 10, 41), ("Sistemas", 2, 17), ("Biblioteca", 15, 58),
           ("RRHH", 7, 32)]


def g20():
    x = np.array([a[1] for a in AREAS20])
    y = np.array([a[2] for a in AREAS20])
    fig, ax = figura(6.8, 3.6)
    ax.scatter(x, y, s=60, color=AZUL, zorder=3, label="Áreas observadas")
    xs = np.linspace(0, 22, 50)
    ax.plot(xs, 12 + 3 * xs, color=NARANJA, lw=2, label="incidentes = 12 + 3 × equipos")
    ax.axvline(20, color=GRIS, ls=":", lw=1.5)
    ax.text(19.6, 22, "x = 20", ha="right", fontsize=9.5, color=TINTA2)
    ax.set_xlabel("Equipos sin parche de seguridad")
    ax.set_ylabel("Incidentes por mes")
    ax.set_title("Equipos sin parche vs incidentes")
    ax.legend(loc="upper left")
    return fig


reg(codigo="Q20", tipo="multichoice", titulo="Predecir incidentes con regresión lineal",
    tema="Regresión lineal", tema_tag="Regresion lineal", grafico=g20,
    contexto="<p>La Dirección de TI ajustó una regresión lineal para estimar los <strong>incidentes de seguridad "
             "por mes</strong> de cada área según sus <strong>equipos sin parche</strong>:</p>"
             "<p style='text-align:center'><code>incidentes = 12 + 3 × equipos_sin_parche</code></p>"
             + nota("para predecir, <strong>reemplaza x</strong> en la ecuación por el valor que te dan y resuelve "
                    "(primero la multiplicación, luego la suma)."),
    datos=(["área", "equipos_sin_parche", "incidentes reales"], [list(a) for a in AREAS20]),
    hipotesis="Si un área tiene 20 equipos sin parche, el modelo predice más de 70 incidentes al mes.",
    pregunta="<p>¿Cuántos incidentes predice el modelo para 20 equipos y se cumple la hipótesis?</p>",
    opciones=[(True, "72 incidentes; sí se cumple."), (False, "60 incidentes; no se cumple."),
              (False, "35 incidentes; no se cumple."), (False, "240 incidentes; sí se cumple.")],
    pista="El recuadro indica reemplazar x = 20 y multiplicar antes de sumar.",
    retro="<p>12 + 3 × 20 = 12 + 60 = <strong>72</strong> &gt; 70 → la hipótesis se cumple. Error común: "
          "3 × 20 = 60 (olvidar el intercepto) o 12 × 20 = 240 (multiplicar el intercepto en lugar de la pendiente).</p>")
