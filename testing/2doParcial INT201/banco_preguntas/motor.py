# -*- coding: utf-8 -*-
"""
Motor del banco de preguntas: estilo de gráficos, plantilla de enunciado,
exportación a Moodle XML y a Markdown (guía docente).

Reglas aplicadas (skill generador_quizzes_moodle):
  * TODO el contenido de <text>/<feedback> va dentro de CDATA.
  * Sin genéricos < > en textos de ddwtos; el código en <pre> usa &lt; &gt;.
  * ddwtos: los <dragbox> 1..K son SIEMPRE las respuestas de [[1]]..[[K]] (en orden),
    los distractores van DESPUÉS. El motor lo construye así automáticamente.
  * Selección múltiple con penalización negativa (fracciones válidas de Moodle).
  * shortanswer con <usecase>0</usecase>.
"""
import base64
import html
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)

# ---------------------------------------------------------------------------
# Estilo de gráficos (paleta validada: azul / naranja como par adyacente)
# ---------------------------------------------------------------------------
AZUL, NARANJA, VERDE, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#b4b2aa"
TINTA, TINTA2, SUP = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({
    "font.size": 10.5, "axes.edgecolor": GRIS, "axes.labelcolor": TINTA2,
    "xtick.color": TINTA2, "ytick.color": TINTA2, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e5e0",
    "grid.linewidth": 0.8, "axes.axisbelow": True, "figure.facecolor": SUP,
    "axes.facecolor": SUP, "axes.titlecolor": TINTA, "axes.titleweight": "bold",
    "axes.titlesize": 11.5, "legend.frameon": False,
})


def figura(w=7.2, h=3.6, ncols=1, **kw):
    fig, ax = plt.subplots(1, ncols, figsize=(w, h), **kw)
    return fig, ax


def etiquetas_barras(ax, barras, fmt="{:.2f}", horizontal=False, dx=None):
    for b in barras:
        if horizontal:
            v = b.get_width()
            ax.text(v + (dx or 0.01), b.get_y() + b.get_height() / 2, fmt.format(v),
                    va="center", fontsize=9.5, color=TINTA)
        else:
            v = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, v + (dx or 0.01), fmt.format(v),
                    ha="center", va="bottom", fontsize=9.5, color=TINTA)


def matriz_confusion(ax, m, titulo, etq0="Normal (0)", etq1="Ataque (1)", resaltar=None, vmax=None):
    """m = [[TN, FP], [FN, TP]]"""
    import numpy as np
    m = np.array(m)
    ax.imshow(m, cmap="Blues", vmin=0, vmax=vmax or m.max() * 1.25)
    ax.grid(False)
    for i in range(2):
        for j in range(2):
            v = m[i, j]
            oscuro = v > (vmax or m.max() * 1.25) * 0.55
            ax.text(j, i, str(v), ha="center", va="center", fontsize=16, fontweight="bold",
                    color="white" if oscuro else TINTA)
    if resaltar is not None:
        i, j = resaltar
        ax.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, fill=False, ec=NARANJA, lw=3))
    ax.set_xticks([0, 1], [f"Pred:\n{etq0}", f"Pred:\n{etq1}"])
    ax.set_yticks([0, 1], [f"Real:\n{etq0}", f"Real:\n{etq1}"])
    ax.set_title(titulo)
    for s in ax.spines.values():
        s.set_visible(False)


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(os.path.join(IMG, nombre), dpi=100)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Plantilla de enunciado (HTML)
# ---------------------------------------------------------------------------
CELDA = 'style="border:1px solid #c9c8c2;padding:3px 9px;text-align:center"'
CAB = 'style="border:1px solid #c9c8c2;padding:3px 9px;background:#eef3fb;text-align:center"'
DIF_COLOR = {"Fácil": "#008300", "Intermedio": "#c98500", "Difícil": "#d03b3b"}
TIPO_TXT = {"multichoice": "Selección única", "multi": "Selección múltiple (varias correctas)",
            "truefalse": "Verdadero / Falso", "shortanswer": "Respuesta corta",
            "ddwtos": "Arrastrar y soltar", "matching": "Emparejamiento", "cloze": "Completar"}


def tabla_html(cab, filas):
    h = "".join(f"<th {CAB}>{c}</th>" for c in cab)
    b = "".join("<tr>" + "".join(f"<td {CELDA}>{v}</td>" for v in f) + "</tr>" for f in filas)
    return (f'<table style="border-collapse:collapse;font-size:0.9em;margin:4px 0 8px 0">'
            f"<thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>")


def seccion(t, c):
    return f'<p style="margin:12px 0 4px 0"><strong>{t}</strong></p>{c}'


def enunciado_html(q, img_src):
    cab = (f'<p><span style="color:{DIF_COLOR[q["dif"]]};font-weight:bold">[{q["dif"]}]</span> '
           f'<strong>{TIPO_TXT[q["tipo"]]} | {q["tema"]}</strong></p>')
    return (cab
            + seccion("1. Contexto", q["contexto"])
            + seccion("2. Datos de muestra", tabla_html(*q["datos"]))
            + seccion("3. Gráfico", f'<p><img src="{img_src}" alt="Gráfico de la pregunta" '
                                    f'style="max-width:100%;height:auto"></p>')
            + seccion("4. Hipótesis", f'<blockquote style="border-left:4px solid {NARANJA};padding:4px 12px;'
                                      f'margin:4px 0;font-style:italic">{q["hipotesis"]}</blockquote>')
            + seccion("5. Pregunta", q["pregunta"])
            + (ALERTA_PENALIZACION if q["tipo"] in ("multichoice", "multi") else ""))


ALERTA_PENALIZACION = (
    '<p style="background:#fdecea;border-left:4px solid #d03b3b;border-radius:6px;padding:6px 10px;margin:10px 0 0 0">'
    "<strong>⚠ Atención:</strong> en esta pregunta las respuestas incorrectas <strong>restan puntos</strong>. "
    "Si no estás seguro de la respuesta, es mejor <strong>dejarla en blanco</strong> para evitar la penalización.</p>")


# ---------------------------------------------------------------------------
# Moodle XML
# ---------------------------------------------------------------------------
NOTA = {"Fácil": 1, "Intermedio": 2, "Difícil": 3}
FRAC = {1: "100", 2: "50", 3: "33.33333", 4: "25", 5: "20", 6: "16.66667"}


def cd(s):
    assert "]]>" not in s
    return f"<![CDATA[{s}]]>"


def b64(nombre):
    with open(os.path.join(IMG, nombre), "rb") as f:
        return base64.b64encode(f.read()).decode()


def sin_tildes(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tags_xml(q, tags_globales):
    # Tags SIN tildes: Moodle (MySQL, collation sin acentos) ya tiene "Facil"/"Dificil" y considera
    # "Fácil" un duplicado -> "Error escribiendo a la base de datos" al importar.
    tags = list(tags_globales) + [sin_tildes(q["dif"]), sin_tildes(q["tema_tag"])]
    for t in tags:
        assert t == sin_tildes(t), t
    return "<tags>" + "".join(f"<tag><text>{html.escape(t)}</text></tag>" for t in tags) + "</tags>"


def pregunta_xml(q, tags_globales):
    img = q["img"]
    nombre = f'{q["codigo"]}. [{q["dif"].upper()}] {q["titulo"]}'
    qt = (f'<questiontext format="html"><text>{cd(enunciado_html(q, "@@PLUGINFILE@@/" + img))}</text>'
          f'<file name="{img}" path="/" encoding="base64">{b64(img)}</file></questiontext>')
    head = (f'<name><text>{cd(nombre)}</text></name>{qt}'
            f'<generalfeedback format="html"><text>{cd(q["retro"])}</text></generalfeedback>'
            f'<defaultgrade>{NOTA[q["dif"]]}</defaultgrade>')
    fb = ('<correctfeedback format="html"><text>' + cd("¡Correcto!") + '</text></correctfeedback>'
          '<partiallycorrectfeedback format="html"><text>' + cd("Parcialmente correcto. Revisa la retroalimentación.")
          + '</text></partiallycorrectfeedback><incorrectfeedback format="html"><text>'
          + cd("Incorrecto. Revisa la retroalimentación.") + '</text></incorrectfeedback>')
    t = q["tipo"]
    tg = tags_xml(q, tags_globales)

    if t in ("multichoice", "multi"):
        ops = q["opciones"]
        nok = sum(1 for ok, _ in ops if ok)
        nbad = len(ops) - nok
        if t == "multichoice":
            assert nok == 1, q["codigo"]
            bien, mal = "100", "-" + FRAC[nbad]
        else:
            assert nok >= 2, q["codigo"]
            bien, mal = FRAC[nok], "-" + FRAC[min(nok, 2)]  # cada incorrecta resta 50 % (o 1/k)
        ans = "".join(
            f'<answer fraction="{bien if ok else mal}" format="html"><text>{cd(txt)}</text>'
            f'<feedback format="html"><text>{cd("")}</text></feedback></answer>' for ok, txt in ops)
        return (f'<question type="multichoice">{head}<penalty>0.3333333</penalty><hidden>0</hidden>'
                f'<single>{"true" if t == "multichoice" else "false"}</single><shuffleanswers>true</shuffleanswers>'
                f'<answernumbering>abc</answernumbering>{fb}<shownumcorrect/>{ans}{tg}</question>')

    if t == "truefalse":
        v = q["verdadero"]
        return (f'<question type="truefalse">{head}<penalty>1</penalty><hidden>0</hidden>'
                f'<answer fraction="{100 if v else 0}" format="moodle_auto_format"><text>true</text>'
                f'<feedback format="html"><text>{cd(q["retro_corta"] if v else "Incorrecto.")}</text></feedback></answer>'
                f'<answer fraction="{0 if v else 100}" format="moodle_auto_format"><text>false</text>'
                f'<feedback format="html"><text>{cd("Incorrecto." if v else q["retro_corta"])}</text></feedback></answer>'
                f'{tg}</question>')

    if t == "shortanswer":
        ans = "".join(f'<answer fraction="100" format="moodle_auto_format"><text>{cd(a)}</text>'
                      f'<feedback format="html"><text>{cd("¡Correcto!")}</text></feedback></answer>'
                      for a in q["respuestas"])
        return (f'<question type="shortanswer">{head}<penalty>0.3333333</penalty><hidden>0</hidden>'
                f'<usecase>0</usecase>{ans}{tg}</question>')

    if t == "ddwtos":
        huecos = q["huecos"]
        nums = sorted(set(int(n) for n in re.findall(r"\[\[(\d+)\]\]", q["pregunta"])))
        assert nums == list(range(1, len(huecos) + 1)), q["codigo"]
        cajas = huecos + q["distractores"]           # 1..K correctas EN ORDEN, luego distractores
        for txt, _ in cajas:
            assert "<" not in txt and ">" not in txt, (q["codigo"], txt)
        dd = "".join(f"<dragbox><text>{cd(txt)}</text><group>{g}</group></dragbox>" for txt, g in cajas)
        return (f'<question type="ddwtos">{head}<penalty>0.3333333</penalty><hidden>0</hidden>'
                f'<shuffleanswers>true</shuffleanswers>{fb}<shownumcorrect/>{dd}{tg}</question>')

    if t == "matching":
        subs = "".join(f'<subquestion format="html"><text>{cd(p)}</text><answer><text>{html.escape(r)}'
                       f'</text></answer></subquestion>' for p, r in q["pares"])
        subs += "".join(f'<subquestion format="html"><text>{cd("")}</text><answer><text>{html.escape(r)}'
                        f'</text></answer></subquestion>' for r in q.get("distractores", []))
        return (f'<question type="matching">{head}<penalty>0.3333333</penalty><hidden>0</hidden>'
                f'<shuffleanswers>true</shuffleanswers>{fb}<shownumcorrect/>{subs}{tg}</question>')

    if t == "cloze":
        codigos = re.findall(r"\{\d+:(NUMERICAL|MULTICHOICE|SHORTANSWER):[^}]*\}", q["pregunta"])
        assert codigos, q["codigo"]
        for c in re.findall(r"\{\d+:MULTICHOICE:([^}]*)\}", q["pregunta"]):
            ops = c.split("~")
            assert sum(o.startswith("=") for o in ops) == 1, (q["codigo"], c)
            assert all("=" not in o.lstrip("=") for o in ops), (q["codigo"], c)
            assert "#" not in c and ":" not in c and "{" not in c, (q["codigo"], c)
        # En cloze la nota la definen los pesos {n:...}; Moodle ignora defaultgrade.
        return f'<question type="cloze">{head}<penalty>0.3333333</penalty><hidden>0</hidden>{tg}</question>'

    raise ValueError(t)


def exportar_xml(preguntas, ruta, raiz_categoria, tags_globales):
    partes = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    actual = None
    for q in preguntas:
        cat = f'{raiz_categoria}/{q["cat"]}'
        if cat != actual:
            partes.append(
                f'<question type="category"><category><text>$course$/{cat}</text></category>'
                f'<info format="html"><text>{cd("Preguntas de nivel " + q["dif"] + " - escenarios de ciberseguridad.")}'
                f"</text></info></question>")
            actual = cat
        partes.append(pregunta_xml(q, tags_globales))
    partes.append("</quiz>\n")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))


# ---------------------------------------------------------------------------
# Markdown (guía docente)
# ---------------------------------------------------------------------------
def html_a_md(s):
    def pre(m):
        cuerpo = re.sub(r"</?code>", "", m.group(1))
        return "\n```python\n" + html.unescape(cuerpo).strip("\n") + "\n```\n"
    s = re.sub(r"<pre>(.*?)</pre>", pre, s, flags=re.S)
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s)
    s = re.sub(r"</?(strong|b)>", "**", s)
    s = re.sub(r"</?(em|i)>", "*", s)
    s = re.sub(r"<br\s*/?>", "  \n", s)
    s = re.sub(r"<li>", "- ", s)
    s = re.sub(r"</li>", "\n", s)
    s = re.sub(r"</p>", "\n\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def cloze_md(s):
    def rep(m):
        tipo, cuerpo = m.group(2), m.group(3)
        if tipo == "NUMERICAL":
            v, tol = cuerpo.lstrip("=").split(":")
            return f"`____` **[{v}{' ± ' + tol if float(tol) else ''}]**"
        ops = cuerpo.split("~")
        ok = next(o.lstrip("=") for o in ops if o.startswith("="))
        return f"`▾ ({' / '.join(o.lstrip('=') for o in ops)})` **[{ok}]**"
    return re.sub(r"\{(\d+):(NUMERICAL|MULTICHOICE):([^}]*)\}", rep, s)


def tabla_md(cab, filas):
    limpiar = lambda v: html_a_md(str(v)).replace("|", "\\|")
    out = "| " + " | ".join(limpiar(c) for c in cab) + " |\n|" + "---|" * len(cab) + "\n"
    out += "".join("| " + " | ".join(limpiar(v) for v in f) + " |\n" for f in filas)
    return out


def pregunta_md(q):
    o = [f'### {q["codigo"]}. {q["titulo"]}\n',
         f'**Nivel:** {q["dif"]} · **Tipo:** {TIPO_TXT[q["tipo"]]} · **Tema:** {q["tema"]} · '
         f'**Puntaje:** {NOTA[q["dif"]] if q["tipo"] != "cloze" else "según huecos"}\n',
         "**1. Contexto**\n", html_a_md(q["contexto"]) + "\n",
         "**2. Datos de muestra**\n", tabla_md(*q["datos"]),
         "**3. Gráfico**\n", f'![{q["codigo"]}](img/{q["img"]})\n',
         "**4. Hipótesis**\n", "> " + html_a_md(q["hipotesis"]) + "\n",
         "**5. Pregunta**\n"]
    preg = q["pregunta"]
    if q["tipo"] == "cloze":
        preg = cloze_md(preg)
    if q["tipo"] == "ddwtos":
        for i, (txt, _) in enumerate(q["huecos"], 1):
            preg = preg.replace(f"[[{i}]]", f"[[{i}→{txt}]]")
    o.append(html_a_md(preg) + "\n")

    o.append("**Respuesta**\n")
    t = q["tipo"]
    if t in ("multichoice", "multi"):
        o += [f'- {"✅" if ok else "❌"} {html_a_md(txt)}' for ok, txt in q["opciones"]]
        o.append("")
    elif t == "truefalse":
        o.append(f'- **{"VERDADERO" if q["verdadero"] else "FALSO"}**\n')
    elif t == "shortanswer":
        o.append("- Respuestas aceptadas (sin distinguir mayúsculas): "
                 + ", ".join(f"`{a}`" for a in q["respuestas"]) + "\n")
    elif t == "ddwtos":
        o += [f"- [[{i}]] → **{txt}** (grupo {g})" for i, (txt, g) in enumerate(q["huecos"], 1)]
        o.append("- Distractores: " + ", ".join(f"`{t_}` (g{g})" for t_, g in q["distractores"]) + "\n")
    elif t == "matching":
        o += [f"- {html_a_md(p)} → **{r}**" for p, r in q["pares"]]
        if q.get("distractores"):
            o.append("- Distractor(es): " + ", ".join(q["distractores"]))
        o.append("")
    elif t == "cloze":
        o.append("- Ver valores entre corchetes en la pregunta.\n")

    o.append("**Pista incluida en el contexto (para el docente):** " + q["pista"] + "\n")
    o.append("**Explicación:** " + html_a_md(q["retro"]) + "\n")
    o.append("---\n")
    return "\n".join(o)
