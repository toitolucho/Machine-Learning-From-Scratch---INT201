# -*- coding: utf-8 -*-
"""
Banco de 50 preguntas - 2do Parcial INT201 (Machine Learning) - 02-2026
Escenarios de ciberseguridad / TI. Estructura de cada pregunta:
    Contexto (con pista de lectura) -> Datos de muestra -> Gráfico -> Hipótesis -> Pregunta

Ejecutar:   python generar_banco.py
Salida:     parcial2_INT201_50preguntas.xml   (importar en Moodle, formato Moodle XML)
            guia_revision_parcial2.md          (preguntas + respuestas + guía docente)
            img/qNN.png                        (gráficos, también embebidos en el XML)
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt  # noqa: E402

import motor  # noqa: E402
import preguntas_faciles  # noqa: E402
import preguntas_intermedias  # noqa: E402
import preguntas_dificiles  # noqa: E402

RAIZ_CATEGORIA = "02-2026 INT201 - P2 Machine Learning"
TAGS = ["02-2026 INT201", "P2"]
XML = os.path.join(motor.BASE, "parcial2_INT201_50preguntas.xml")
MD = os.path.join(motor.BASE, "guia_revision_parcial2.md")
PRUEBA = os.path.join(motor.BASE, "prueba_importacion_7tipos.xml")


def cargar():
    qs = preguntas_faciles.PREGUNTAS + preguntas_intermedias.PREGUNTAS + preguntas_dificiles.PREGUNTAS
    codigos = [q["codigo"] for q in qs]
    assert codigos == [f"Q{i:02d}" for i in range(1, 51)], codigos
    for q in qs:
        q["img"] = f'{q["codigo"].lower()}.png'
        fig = q["grafico"]()
        motor.guardar(fig, q["img"])
        q.setdefault("retro_corta", "¡Correcto! " + motor.html_a_md(q["retro"])[:300])
        for campo in ("contexto", "datos", "hipotesis", "pregunta", "retro", "pista", "tema", "tema_tag"):
            assert q.get(campo), (q["codigo"], campo)
    plt.close("all")
    return qs


def guia(qs):
    por_dif = Counter(q["dif"] for q in qs)
    por_tipo = Counter(motor.TIPO_TXT[q["tipo"]] for q in qs)
    filas = "\n".join(
        f'| {q["codigo"]} | {q["dif"]} | {motor.TIPO_TXT[q["tipo"]]} | {q["tema"]} | {q["titulo"]} |' for q in qs)
    total_pts = sum(motor.NOTA[q["dif"]] for q in qs if q["tipo"] != "cloze")
    return f"""# 2do Parcial INT201 – Machine Learning (02-2026) · Guía de revisión docente

Banco de **50 preguntas** basadas en escenarios de **ciberseguridad / TI**. Cada pregunta tiene la misma estructura:

1. **Contexto**: describe el escenario e incluye un recuadro **«Recuerda»**, una pista de lectura con la definición
   o fórmula necesaria. El estudiante que lee con atención tiene la herramienta, pero **igual debe interpretar los
   datos o el gráfico** para responder.
2. **Datos de muestra**: tabla con filas del escenario.
3. **Gráfico**: generado a partir de los mismos datos, para que sean coherentes.
4. **Hipótesis**: una afirmación que el estudiante debe **validar o refutar** con la evidencia.
5. **Pregunta**: de selección única, selección múltiple, verdadero/falso, respuesta corta, arrastrar y soltar,
   emparejamiento o completar (cloze).

## Archivos

| Archivo | Uso |
|---|---|
| `parcial2_INT201_50preguntas.xml` | Importar en Moodle (las imágenes van embebidas) |
| `guia_revision_parcial2.md` | Esta guía: preguntas, respuestas, pistas y explicaciones |
| `img/qNN.png` | Gráficos (solo para esta guía; el XML no los necesita) |
| `generar_banco.py`, `motor.py`, `preguntas_*.py` | Generador: edita una pregunta y vuelve a ejecutar `python generar_banco.py` |

## Cómo importar en Moodle

1. **Banco de preguntas → Importar → Formato «Moodle XML»**, subir `parcial2_INT201_50preguntas.xml`.
2. Se crean 3 subcategorías bajo **`{RAIZ_CATEGORIA}`**: `1 - Fácil`, `2 - Intermedio`, `3 - Difícil`.
3. Todas las preguntas llevan las etiquetas **`02-2026 INT201`** y **`P2`**, además del nivel (`Facil`,
   `Intermedio`, `Dificil`) y una etiqueta de tema (por ejemplo `kNN`, `Data leakage`). Las etiquetas van
   **sin tildes** a propósito: Moodle ya tiene `Facil`/`Dificil` y una versión con tilde provoca
   «Error escribiendo a la base de datos».
5. Si un import falla, prueba primero `prueba_importacion_7tipos.xml` (una pregunta de cada tipo, en una
   categoría aparte) para identificar qué tipo causa el problema.
4. Para armar el examen se puede usar **«Añadir pregunta aleatoria»** por subcategoría (ej. 8 fáciles + 8
   intermedias + 4 difíciles) o filtrar por etiqueta.

## Puntajes y penalizaciones

| Nivel | Puntaje por pregunta (`defaultgrade`) |
|---|---|
| Fácil | 1 |
| Intermedio | 2 |
| Difícil | 3 |

- Las 24 preguntas de selección única y múltiple muestran al estudiante un **aviso rojo**: las respuestas
  incorrectas restan puntos y, si no está seguro, conviene dejarla en blanco.
- **Selección única**: cada opción incorrecta resta (−33.3 % con 4 opciones).
- **Selección múltiple**: cada correcta suma por igual; cada incorrecta resta (−33.3 % o −50 %). El mínimo de la
  pregunta es 0.
- **Verdadero/Falso**: sin penalización negativa (penalty = 1 solo aplica en modo interactivo).
- **Cloze (completar)**: Moodle calcula el puntaje con los **pesos de cada hueco** (`{{1:...}}`, `{{2:...}}`), no con
  `defaultgrade`. Si quieres que valgan 2 o 3 puntos, ajusta la **nota máxima** en el cuestionario.
- Puntaje total sin cloze: **{total_pts}** puntos (7 preguntas cloze adicionales).

## Distribución

**Por nivel:** {", ".join(f"{k}: {v}" for k, v in por_dif.items())}

**Por tipo:** {", ".join(f"{k}: {v}" for k, v in por_tipo.items())}

| Código | Nivel | Tipo | Tema | Título |
|---|---|---|---|---|
{filas}

## Lista de verificación para revisar

- [ ] ¿La pista del recuadro «Recuerda» ayuda **sin dar** la respuesta directa? (ver «Pista incluida» en cada pregunta)
- [ ] ¿Los números de la tabla, el gráfico y la explicación coinciden?
- [ ] ¿Los distractores son plausibles (errores típicos de los estudiantes) y no ambiguos?
- [ ] ¿El nivel asignado corresponde a lo que vieron en clase?
- [ ] Respuesta corta: ¿faltan variantes aceptables? (agregar en `respuestas=[...]`)
- [ ] Cloze: los estudiantes deben usar **punto decimal**; el aviso está en cada pregunta.
- [ ] Después de importar, **previsualizar 2–3 preguntas de cada tipo** en Moodle (imágenes y arrastrar y soltar).

## Notas técnicas (reglas del generador de quizzes)

- Todo el contenido de `<text>` y `<feedback>` va en `CDATA`.
- Arrastrar y soltar (`ddwtos`): el `<dragbox>` N es **siempre** la respuesta de `[[N]]`, con el mismo grupo; los
  distractores van **al final**. El generador valida esto y que ninguna opción tenga `<` o `>`.
- Cloze: cada `MULTICHOICE` tiene exactamente una opción con `=` y sin `#`, `:` ni `{{`.
- No se usa LaTeX (las fórmulas están en texto plano), así que no hay problemas de renderizado.

---

# Preguntas y respuestas

""" + "\n".join(motor.pregunta_md(q) for q in qs)


def main():
    qs = cargar()
    motor.exportar_xml(qs, XML, RAIZ_CATEGORIA, TAGS)
    # Archivo de prueba: una pregunta de cada tipo, en una categoría aparte (fácil de borrar)
    muestra, vistos = [], set()
    for q in qs:
        if q["tipo"] not in vistos:
            vistos.add(q["tipo"])
            muestra.append(dict(q, cat="PRUEBA importacion (borrar)"))
    motor.exportar_xml(muestra, PRUEBA, RAIZ_CATEGORIA, TAGS)
    with open(MD, "w", encoding="utf-8") as f:
        f.write(guia(qs))
    print(f"OK: {len(qs)} preguntas")
    print("  ", XML)
    print("  ", MD)
    print("   Por nivel:", dict(Counter(q["dif"] for q in qs)))
    print("   Por tipo :", dict(Counter(q["tipo"] for q in qs)))


if __name__ == "__main__":
    main()
