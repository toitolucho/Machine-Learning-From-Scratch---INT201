# Moodle XML Generator Guide — COM200 Data Structures Quizzes

This file tells the XML generator **which Moodle question type to use for each question** in the two COM200 quiz files, how to transform the Markdown content into that type, and which XML template to emit.

| Source file | Prefix | Questions |
|---|---|---|
| `estructuras-datos-50-preguntas.md` (theory) | `T` | T-Q01 … T-Q50 |
| `estructuras-datos-codigo-50-preguntas.md` (code) | `C` | C-Q01 … C-Q50 |

---

## 1. Parsing the source Markdown

Every question in both files follows this structure:

```
## Q<n>. <Title> — <Fácil|Intermedio|Difícil>[ — Tipo: <Type label>]

[**Escenario (<Game>):** ...]          (code file only)
[**Objetivo:** ...]                     (code file only, optional)
<question text, may contain ```csharp fenced blocks with ______ blanks>

A) <option>
B) <option>
C) <option>
D) <option>

**Respuesta correcta: <A|B|C|D>**

**Retroalimentación:** <feedback text>

---
```

Parsing rules:

1. **Question name:** `<Prefix>-Q<nn> <Title>` (zero-padded, e.g. `C-Q07 Leer una celda de matriz escalonada`). Drop the difficulty and the `Tipo:` label from the name.
2. **Difficulty:** taken from the header (`Fácil`, `Intermedio` or `Difícil`) and used for the category (section 4).
3. **Question text:** everything between the header and the line `A)`.
4. **Options:** the lines starting with `A)`–`D)`. Strip the `A) ` prefix and the trailing two spaces (Markdown line break).
5. **Correct option:** the letter in `**Respuesta correcta: X**`.
6. **Feedback:** the text after `**Retroalimentación:**`, which goes into `<generalfeedback>`.
7. **Inline Markdown → HTML:** `` `code` `` → `<code>code</code>`, `**bold**` → `<strong>bold</strong>`, `*italic*` → `<em>italic</em>`.
8. **Fenced code blocks:** ` ```csharp ... ``` ` and ` ``` ... ``` ` → `<pre><code>...</code></pre>`. Inside the block, HTML-escape `<`, `>` and `&` (`List<int>` → `List&lt;int&gt;`) and **preserve indentation and line breaks exactly**.
9. Wrap every HTML `<text>` in `<![CDATA[ ... ]]>`.

---

## 2. Moodle question-type catalogue (when to use each)

| Moodle type (UI name) | XML `type` | Use it when… | Avoid it when… |
|---|---|---|---|
| Multiple choice (single answer) | `multichoice` | The question asks for a **decision or judgement** and the wrong options are meaningful misconceptions (scenario → which structure, debugging "what is the cause", design choices). | The answer is a single token that fits inside the code. |
| True/False | `truefalse` | The whole question reduces to **one clear statement** that is true or false and the common misconception is the opposite. | There are several plausible alternatives (50% guessing is too high). |
| Select missing words | `gapselect` | **Complete-the-code** questions: the `______` blank is replaced by a dropdown inside the code. Works with any option text, including spaces and `<` `>`. | — (it is the safe default for code completion) |
| Drag and drop into text | `ddwtos` | Complete-the-code with **short tokens** (single identifiers such as `Add`, `Count`, `Peek`) and no `<` `>` characters, or when the **same token fills several blanks**. | The options contain spaces, long expressions or generics like `Stack<Sprite>` (ddwtos choices allow only limited HTML and `<...>` can be stripped). |
| Numerical | `numerical` | "Predict the output" questions where the answer is **one number** and every distractor is also a number (so the input box does not give a hint). | A key distractor is non-numeric (e.g. `null`, "throws an exception"). Keep those as `multichoice`. |
| Embedded answers (Cloze) | `cloze` | Output prediction with **several values** (e.g. what `Dequeue()` returns, what `Peek()` returns, and `Count`). Each value becomes its own dropdown or number field with partial credit. | A single value is enough (use `numerical` or `multichoice`). |
| Matching | `matching` | The question pairs **several requirements with several structures**. | There is only one pair. |
| Short answer | `shortanswer` | — Not recommended here: typed C# identifiers fail on case, spaces, `()` and `;` differences. | Always, for this quiz. |
| Ordering | `ordering` | Not used in these files. Check that the type is installed on your Moodle site before adding ordering questions (it is standard only in recent Moodle versions). | — |

### General decision rules

1. `Tipo: Completar Código`:
   - All options are single tokens without spaces and without `<` `>` → `ddwtos`.
   - Otherwise → `gapselect`.
2. `Tipo: Predicción`:
   - One numeric answer and only numeric distractors → `numerical`.
   - Several values to predict → `cloze`.
   - The distractors include an exception, `null` or another non-numeric outcome → `multichoice`.
3. `Tipo: Depuración`, `Tipo: Mejor Enfoque` and all theory scenario questions → `multichoice`.
4. `Tipo: Lectura de Código` reducible to one true/false statement → `truefalse`.
5. Many-to-many requirement mapping → `matching`.

The per-question tables in section 5 are the final word and override these rules.

---

## 3. Global settings and pitfalls

### Multiple choice settings

- `<single>true</single>`
- `<shuffleanswers>false</shuffleanswers>` — **Important:** the feedback text refers to options by letter ("la opción B…"). Shuffling would make those references wrong. The source files already spread the correct answers evenly across A–D (13/13/12–13/11–12).
- `<answernumbering>ABCD</answernumbering>`
- Correct option `fraction="100"`, the others `fraction="0"`.
- `<penalty>0.3333333</penalty>`, `<defaultgrade>1</defaultgrade>`.

### Rewriting letter references (all non-`multichoice` types)

In `gapselect`, `ddwtos`, `numerical`, `cloze`, `matching` and `truefalse`, the options lose their letters. Before writing the feedback, **replace every letter reference with the option's text**:

- "La opción A …" → "La opción `i <= fila.Length` …"
- "Las opciones C y D …" → "Las opciones `(int)tokens[c]` y `row[c] = tokens[c]` …"

### Gap questions (`gapselect` / `ddwtos`)

- Replace `______` in the code with `[[1]]`.
- In Moodle, `[[n]]` means "the correct answer for this gap is **choice number n**". Always write the correct option as **choice 1**, then the three distractors as choices 2–4, all in **group 1**.
- If the same blank appears several times (C-Q05), use `[[1]]` in every position. For `ddwtos`, mark choice 1 as `<infinite/>` so it can be dragged several times.
- `<shuffleanswers>1</shuffleanswers>` is safe here (choices have no letters).
- Choice text is **plain text**. Escape it only at the XML level (`<` → `&lt;`, `&` → `&amp;`), not twice.
- Check that `[[1]]` inside `<pre><code>` renders correctly: import **C-Q01** (gapselect with `Stack<Sprite>`) and **C-Q04** (ddwtos) first, preview them, and only then import everything.

### Numerical

- `<tolerance>0</tolerance>` for integers; `0.001` for decimal answers.
- Append to the question text: *"Escribe solo el número (usa punto como separador decimal)."* Test on your site whether `3,5` is also accepted.

### Cloze

- Syntax: `{1:MULTICHOICE:=correct#feedback~wrong#feedback}` (dropdown) and `{1:NUMERICAL:=7:0#feedback}` (number, tolerance after the `:`).
- Inside embedded answers, escape `}`, `#`, `~`, `/`, `"` and `\` with a backslash.
- Braces that appear in the **C# code outside the embedded answers** do not need escaping.
- Each embedded part is graded separately (partial credit). Put the full Retroalimentación text in `<generalfeedback>`.

### HTML in the question text

- Keep the `**Escenario (...)**` and `**Objetivo:**` lines as `<p><strong>…</strong> …</p>`.
- The code block is the core of most code questions. Never collapse its whitespace.

---

## 4. Categories

Emit a `category` pseudo-question before each group:

```
$course$/top/COM200/Teoria/Facil
$course$/top/COM200/Teoria/Intermedio
$course$/top/COM200/Teoria/Dificil
$course$/top/COM200/Codigo/Facil
$course$/top/COM200/Codigo/Intermedio
$course$/top/COM200/Codigo/Dificil
```

Suggested `defaultgrade`: Fácil 1, Intermedio 1, Difícil 2 (adjust as needed; with random questions per category, the grades within one category must match).

---

## 5. Per-question type assignment

### 5.1 Theory file — `estructuras-datos-50-preguntas.md`

Theory questions test **judgement between plausible alternatives**, so almost all stay `multichoice`. Four are converted because another type measures the skill more precisely.

| ID | Difficulty | Moodle type | Notes |
|---|---|---|---|
| T-Q01 – T-Q20 | Fácil | `multichoice` | Scenario → structure/method decision. |
| T-Q21 | Intermedio | `cloze` | See transformation T-Q21 below. |
| T-Q22 – T-Q31 | Intermedio | `multichoice` | |
| T-Q32 | Intermedio | `cloze` | See transformation T-Q32 below. |
| T-Q33 – T-Q37 | Intermedio | `multichoice` | |
| T-Q38 | Intermedio | `numerical` | Answer `0.6`, tolerance `0.001`. |
| T-Q39 – T-Q40 | Intermedio | `multichoice` | |
| T-Q41 – T-Q49 | Difícil | `multichoice` | Design and debugging decisions. |
| T-Q50 | Difícil | `matching` | See transformation T-Q50 below. |

**Totals (theory):** `multichoice` 46 · `cloze` 2 · `numerical` 1 · `matching` 1.

#### Transformations (theory)

**T-Q21 — Traza de una pila (`cloze`)**
Keep the code block and replace the question line and options with:

```
Valor de x: {1:MULTICHOICE:A~=B~C}
Elementos que quedan en la pila: {1:NUMERICAL:=2:0}
```

**T-Q32 — Posición en el mundo (`cloze`)**
Keep the question text and replace the options with:

```
X = {1:NUMERICAL:=3:0}   Y = {1:NUMERICAL:=-2:0}   Z = 0
```

**T-Q38 — Altura del plato apilado (`numerical`)**
Keep the text and code, delete the options, and add "Escribe solo el número (usa punto como separador decimal)." Answer `0.6`, tolerance `0.001`.

**T-Q50 — Diseño integral (`matching`)**
Question text: the intro plus "Relaciona cada requerimiento con la estructura más adecuada."

| Subquestion (requirement) | Answer |
|---|---|
| I. Un conjunto fijo de 4 sprites de bloques. | `Sprite[]` |
| II. Mapas de nivel en archivos .txt incluidos en la build. | `int[][]` + `TextAsset` |
| III. Tanques enemigos que aparecen en el orden programado. | `Queue<GameObject>` |
| IV. Deshacer la última pared colocada en el editor. | `Stack<Accion>` |
| *(distractor: empty subquestion text)* | `List<GameObject>` |
| *(distractor: empty subquestion text)* | `int[,]` + `System.IO.File` |

`<shuffleanswers>true</shuffleanswers>`. Rewrite the Retroalimentación without letters (it already explains I–IV by number).

---

### 5.2 Code file — `estructuras-datos-codigo-50-preguntas.md`

| ID | Diff. | Source label | Moodle type | Notes |
|---|---|---|---|---|
| C-Q01 | F | Completar | `gapselect` | Options contain `<>` (`Stack<Sprite>`), so not ddwtos. |
| C-Q02 | F | Completar | `gapselect` | Options contain spaces and `<`. |
| C-Q03 | F | Completar | `gapselect` | |
| C-Q04 | F | Completar | `ddwtos` | Tokens: `Add`, `Push`, `Enqueue`, `Insert`. |
| C-Q05 | F | Completar | `ddwtos` | **Three blanks**, all `[[1]]`; choice 1 `Enqueue` marked `<infinite/>`. |
| C-Q06 | F | Completar | `gapselect` | |
| C-Q07 | F | Completar | `gapselect` | |
| C-Q08 | F | Completar | `ddwtos` | |
| C-Q09 | F | Completar | `ddwtos` | |
| C-Q10 | F | Completar | `ddwtos` | |
| C-Q11 | F | Predicción | `multichoice` | Distractors `null` / exception are non-numeric. |
| C-Q12 | F | Predicción | `numerical` | Answer `1400`, tolerance 0. |
| C-Q13 | F | Predicción | `numerical` | Answer `3.5`, tolerance 0.001; add "sin la letra f". |
| C-Q14 | F | Completar | `ddwtos` | |
| C-Q15 | F | Completar | `ddwtos` | |
| C-Q16 | F | Completar | `ddwtos` | |
| C-Q17 | F | Completar | `ddwtos` | |
| C-Q18 | F | Lectura | `truefalse` | See transformation C-Q18 below. |
| C-Q19 | F | Completar | `ddwtos` | |
| C-Q20 | F | Depuración | `multichoice` | |
| C-Q21 | I | Completar | `gapselect` | |
| C-Q22 | I | Completar | `gapselect` | Option `tileType = 1` has spaces. |
| C-Q23 | I | Completar | `gapselect` | |
| C-Q24 | I | Completar | `gapselect` | |
| C-Q25 | I | Completar | `gapselect` | |
| C-Q26 | I | Completar | `gapselect` | |
| C-Q27 | I | Completar | `gapselect` | |
| C-Q28 | I | Predicción | `cloze` | See transformation C-Q28 below. |
| C-Q29 | I | Predicción | `cloze` | See transformation C-Q29 below. |
| C-Q30 | I | Completar | `gapselect` | |
| C-Q31 | I | Completar | `gapselect` | |
| C-Q32 | I | Predicción | `numerical` | Answer `250`, tolerance 0. |
| C-Q33 | I | Completar | `gapselect` | |
| C-Q34 | I | Depuración | `multichoice` | |
| C-Q35 | I | Completar | `gapselect` | |
| C-Q36 | I | Completar | `gapselect` | |
| C-Q37 | I | Predicción | `cloze` | See transformation C-Q37 below. |
| C-Q38 | I | Predicción | `cloze` | See transformation C-Q38 below. |
| C-Q39 | I | Completar | `gapselect` | |
| C-Q40 | I | Completar | `gapselect` | |
| C-Q41 | D | Predicción | `multichoice` | Distractors (exception, ASCII) are the point of the question. |
| C-Q42 | D | Predicción | `cloze` | See transformation C-Q42 below. |
| C-Q43 | D | Depuración | `multichoice` | |
| C-Q44 | D | Completar | `gapselect` | |
| C-Q45 | D | Predicción | `multichoice` | The options explain *why* an element is skipped; keep them. |
| C-Q46 | D | Completar | `gapselect` | |
| C-Q47 | D | Depuración | `multichoice` | |
| C-Q48 | D | Completar | `gapselect` | |
| C-Q49 | D | Mejor Enfoque | `multichoice` | Long conditions; comparing them side by side is the task. |
| C-Q50 | D | Predicción | `cloze` | See transformation C-Q50 below. |

**Totals (code):** `gapselect` 22 · `ddwtos` 10 · `multichoice` 8 · `cloze` 6 · `numerical` 3 · `truefalse` 1.

#### Transformations (code)

**C-Q18 — Reiniciar la partida (`truefalse`)**
Keep the scenario and code. Replace the question line and options with the statement:
"Después de ejecutar `autos.Clear()`, los autos desaparecen de la escena."
Correct answer: **Falso**. Use the existing Retroalimentación as general feedback.

**C-Q28 — Traza de la cola de autos (`cloze`)**
Keep the code. Replace the question line and options with:

```
Valor de a: {1:MULTICHOICE:=Rojo~Azul~Verde~Amarillo}
Valor de b: {1:MULTICHOICE:Rojo~=Azul~Verde~Amarillo}
Valor de cola.Peek(): {1:MULTICHOICE:Rojo~Azul~=Verde~Amarillo}
```

**C-Q29 — Traza de la pila de power-ups (`cloze`)**

```
Valor de usado: {1:MULTICHOICE:Escudo~Estrella~=Granada~Reloj}
Valor de pila.Peek(): {1:MULTICHOICE:Escudo~Estrella~Granada~=Reloj}
Valor de pila.Count: {1:NUMERICAL:=3:0}
```

**C-Q37 — Contar autos por carril (`cloze`)**

```
carriles.Length = {1:NUMERICAL:=3:0}
total = {1:NUMERICAL:=7:0}
```

**C-Q38 — Oleada de tanques enemigos (`cloze`)**

```
tanques.Peek() = {1:MULTICHOICE:Básico~Rápido~=Blindado~Pesado}
tanques.Count = {1:NUMERICAL:=2:0}
```

**C-Q42 — Traza completa del parser (`cloze`)**
Keep the file content and the description of the parser. Replace the question line and options with:

```
Cantidad de filas de la matriz: {1:NUMERICAL:=3:0}
Longitud de la fila 0: {1:NUMERICAL:=3:0}
Longitud de la fila 1: {1:NUMERICAL:=3:0}
Longitud de la fila 2: {1:NUMERICAL:=4:0}
```

Make sure the line that contains only one space is kept in the `<pre>` block (do not trim it).

**C-Q50 — Invertir el orden de una oleada (`cloze`)**

```
cola.Dequeue() = {1:MULTICHOICE:Cactus~Ave~=Roca}
cola.Peek() = {1:MULTICHOICE:Cactus~=Ave~Roca}
cola.Count = {1:NUMERICAL:=2:0}
```

---

## 6. XML templates

All templates go inside `<quiz> ... </quiz>`, after the matching category block.

### 6.1 Category

```xml
<question type="category">
  <category><text>$course$/top/COM200/Codigo/Facil</text></category>
</question>
```

### 6.2 Multiple choice

```xml
<question type="multichoice">
  <name><text>T-Q01 Principio LIFO</text></name>
  <questiontext format="html"><text><![CDATA[<p>...</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Retroalimentación...</p>]]></text></generalfeedback>
  <defaultgrade>1</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <single>true</single>
  <shuffleanswers>false</shuffleanswers>
  <answernumbering>ABCD</answernumbering>
  <answer fraction="0" format="html"><text><![CDATA[<code>Queue&lt;GameObject&gt;</code>]]></text><feedback format="html"><text></text></feedback></answer>
  <answer fraction="0" format="html"><text><![CDATA[<code>List&lt;GameObject&gt;</code>]]></text><feedback format="html"><text></text></feedback></answer>
  <answer fraction="100" format="html"><text><![CDATA[<code>Stack&lt;GameObject&gt;</code>]]></text><feedback format="html"><text></text></feedback></answer>
  <answer fraction="0" format="html"><text><![CDATA[<code>int[,]</code>]]></text><feedback format="html"><text></text></feedback></answer>
</question>
```

Keep the answers in source order A, B, C, D.

### 6.3 True/False

```xml
<question type="truefalse">
  <name><text>C-Q18 Reiniciar la partida</text></name>
  <questiontext format="html"><text><![CDATA[<p><strong>Escenario (Frogger):</strong> ...</p><pre><code>void GameOver()
{
    autos.Clear();
}</code></pre><p>Después de ejecutar <code>autos.Clear()</code>, los autos desaparecen de la escena.</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>...</p>]]></text></generalfeedback>
  <defaultgrade>1</defaultgrade>
  <penalty>1</penalty>
  <answer fraction="0" format="moodle_auto_format"><text>true</text><feedback><text></text></feedback></answer>
  <answer fraction="100" format="moodle_auto_format"><text>false</text><feedback><text></text></feedback></answer>
</question>
```

### 6.4 Select missing words (gapselect)

```xml
<question type="gapselect">
  <name><text>C-Q02 Contar puntos de una fila</text></name>
  <questiontext format="html"><text><![CDATA[<p><strong>Escenario (Pac-Man):</strong> ...</p>
<pre><code>int[] fila = { 1, 5, 5, 0, 5, 1 };
int puntos = 0;

for (int i = 0; [[1]]; i++)
{
    if (fila[i] == 5) puntos++;
}</code></pre>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>... (letters rewritten as option text) ...</p>]]></text></generalfeedback>
  <defaultgrade>1</defaultgrade>
  <penalty>0.3333333</penalty>
  <shuffleanswers>1</shuffleanswers>
  <correctfeedback format="html"><text>Respuesta correcta.</text></correctfeedback>
  <partiallycorrectfeedback format="html"><text>Respuesta parcialmente correcta.</text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text>Respuesta incorrecta.</text></incorrectfeedback>
  <shownumcorrect/>
  <selectoption><text>i &lt; fila.Length</text><group>1</group></selectoption>
  <selectoption><text>i &lt;= fila.Length</text><group>1</group></selectoption>
  <selectoption><text>i &lt; fila.Count</text><group>1</group></selectoption>
  <selectoption><text>i &lt; fila.GetLength(1)</text><group>1</group></selectoption>
</question>
```

The correct option is always the **first** `selectoption`, because `[[1]]` points to choice 1.

### 6.5 Drag and drop into text (ddwtos)

```xml
<question type="ddwtos">
  <name><text>C-Q05 Orden de salida de los autos</text></name>
  <questiontext format="html"><text><![CDATA[<p><strong>Escenario (Carrera de autos):</strong> ...</p>
<pre><code>void Start()
{
    colaAutos.[[1]](autoRojo);
    colaAutos.[[1]](autoAzul);
    colaAutos.[[1]](autoVerde);
}</code></pre>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>...</p>]]></text></generalfeedback>
  <defaultgrade>1</defaultgrade>
  <penalty>0.3333333</penalty>
  <shuffleanswers>1</shuffleanswers>
  <correctfeedback format="html"><text>Respuesta correcta.</text></correctfeedback>
  <partiallycorrectfeedback format="html"><text>Respuesta parcialmente correcta.</text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text>Respuesta incorrecta.</text></incorrectfeedback>
  <shownumcorrect/>
  <dragbox><text>Enqueue</text><group>1</group><infinite/></dragbox>
  <dragbox><text>Push</text><group>1</group></dragbox>
  <dragbox><text>Add</text><group>1</group></dragbox>
  <dragbox><text>Dequeue</text><group>1</group></dragbox>
</question>
```

Use `<infinite/>` only when the same token fills more than one gap (C-Q05).

### 6.6 Numerical

```xml
<question type="numerical">
  <name><text>C-Q12 Sumar puntajes</text></name>
  <questiontext format="html"><text><![CDATA[<p>...</p><pre><code>...</code></pre><p>¿Qué se imprime en consola? Escribe solo el número.</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>...</p>]]></text></generalfeedback>
  <defaultgrade>1</defaultgrade>
  <penalty>0.3333333</penalty>
  <answer fraction="100"><text>1400</text><tolerance>0</tolerance><feedback format="html"><text></text></feedback></answer>
</question>
```

### 6.7 Embedded answers (Cloze)

```xml
<question type="cloze">
  <name><text>C-Q37 Contar autos por carril</text></name>
  <questiontext format="html"><text><![CDATA[<p><strong>Escenario (Frogger):</strong> ...</p>
<pre><code>...</code></pre>
<p>carriles.Length = {1:NUMERICAL:=3:0}</p>
<p>total = {1:NUMERICAL:=7:0}</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>...</p>]]></text></generalfeedback>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
</question>
```

Cloze questions take their grade from the sum of the embedded weights (`{1:...}` = weight 1 each). Do not set `defaultgrade` manually.

### 6.8 Matching

```xml
<question type="matching">
  <name><text>T-Q50 Diseño integral de un juego</text></name>
  <questiontext format="html"><text><![CDATA[<p>Un juego tipo <em>Battle City</em> tiene los siguientes requerimientos. Relaciona cada requerimiento con la estructura más adecuada.</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>...</p>]]></text></generalfeedback>
  <defaultgrade>2</defaultgrade>
  <penalty>0.3333333</penalty>
  <shuffleanswers>true</shuffleanswers>
  <correctfeedback format="html"><text>Respuesta correcta.</text></correctfeedback>
  <partiallycorrectfeedback format="html"><text>Respuesta parcialmente correcta.</text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text>Respuesta incorrecta.</text></incorrectfeedback>
  <shownumcorrect/>
  <subquestion format="html"><text><![CDATA[<p>I. Un conjunto fijo de 4 sprites de bloques.</p>]]></text><answer><text>Sprite[]</text></answer></subquestion>
  <subquestion format="html"><text><![CDATA[<p>II. Mapas de nivel en archivos .txt incluidos en la build.</p>]]></text><answer><text>int[][] + TextAsset</text></answer></subquestion>
  <subquestion format="html"><text><![CDATA[<p>III. Tanques enemigos que aparecen en el orden programado.</p>]]></text><answer><text>Queue&lt;GameObject&gt;</text></answer></subquestion>
  <subquestion format="html"><text><![CDATA[<p>IV. Deshacer la última pared colocada en el editor.</p>]]></text><answer><text>Stack&lt;Accion&gt;</text></answer></subquestion>
  <subquestion format="html"><text></text><answer><text>List&lt;GameObject&gt;</text></answer></subquestion>
  <subquestion format="html"><text></text><answer><text>int[,] + System.IO.File</text></answer></subquestion>
</question>
```

Subquestions with empty text are extra wrong answers in the dropdown.

---

## 7. Validation checklist for the generator

- [ ] 100 questions emitted (50 `T-`, 50 `C-`), plus 6 category blocks.
- [ ] Type totals: theory → multichoice 46, cloze 2, numerical 1, matching 1; code → gapselect 22, ddwtos 10, multichoice 8, cloze 6, numerical 3, truefalse 1.
- [ ] Every `gapselect`/`ddwtos` has exactly one `[[1]]` (three in C-Q05), and its correct option is choice 1.
- [ ] No `______` left in any question text.
- [ ] No feedback in a non-multichoice question still refers to "opción A/B/C/D".
- [ ] All code blocks are inside `<pre><code>`, with `<` `>` `&` escaped and indentation preserved.
- [ ] Every cloze question parses: no unescaped `}` `#` `~` inside embedded answers.
- [ ] Test-import C-Q01, C-Q04, C-Q18, C-Q28, C-Q12 and T-Q50 into a sandbox course and preview them before importing the full file.
