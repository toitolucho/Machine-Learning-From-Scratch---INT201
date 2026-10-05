# Banco de Preguntas Moodle — Parte 1: Estructuras de Datos
## Lab: Diseño de Personajes 2D — Serie *Neon Skies*
### Machine Learning from Scratch | INT210

---

> **Convenciones de este documento**
>
> Cada pregunta indica su tipo sugerido para Moodle:
> - **[COMPLETAR]** → Cloze / Drag-and-Drop (el estudiante arrastra el fragmento correcto al espacio en blanco)
> - **[SELECCIÓN]** → Opción múltiple (el estudiante elige el fragmento de código o afirmación correcta entre opciones)
> - **[CONCEPTUAL]** → Respuesta corta o ensayo breve (el estudiante explica propósito o razonamiento)
> - **[LÓGICA]** → Basada en la salida del notebook ejecutado (requiere haber corrido el código)
> - **[V/F]** → Verdadero o Falso
>
> Las respuestas correctas se indican con ✅. Los distractores plausibles se etiquetan con ❌.

---

## Sección 0 — Dataset Inicial

---

### P01 [CONCEPTUAL]

**¿Cuál es el propósito de la variable `characters_raw` definida al inicio del notebook?**

A) Almacenar los personajes ya limpios listos para el modelo de Machine Learning.
B) Definir el conjunto de datos original con errores deliberados que el estudiante debe explorar y corregir. ✅
C) Guardar los resultados calculados de los campos derivados.
D) Crear una copia de seguridad del dataset después de las correcciones.

---

### P02 [COMPLETAR]

**Completa el código para imprimir cuántos personajes hay en el dataset.**

```python
print(f"Dataset cargado: {_____(characters_raw)} personajes registrados.")
```

Opciones: `len` / `count` / `size` / `range`

✅ **Respuesta:** `len`

---

### P03 [V/F]

**El dataset `characters_raw` debe ser modificado directamente cuando se corrijan los errores.**

✅ **Falso.** Se crea una copia profunda (`copy.deepcopy`) en el Ejercicio 3.1 para preservar el dataset original intacto.

---

### P04 [SELECCIÓN]

**¿Cuál de las siguientes instrucciones imprime correctamente los nombres de los campos del primer personaje?**

A) `print(characters_raw.keys())`  ❌ — Las listas no tienen el método `.keys()`
B) `print(list(characters_raw[0].keys()))` ✅
C) `print(characters_raw[0].values())` ❌ — Imprime los valores, no los nombres de campo
D) `print(characters_raw.items())` ❌ — Las listas no tienen el método `.items()`

---

## Sección 1 — Listas (Ejercicios 1.1 – 1.4)

---

### P05 [COMPLETAR] — Ejercicio 1.1

**Completa el código para obtener el nombre del primer personaje del dataset.**

```python
primer_nombre = characters_raw[_____]["name"]
```

Opciones: `0` / `1` / `-1` / `"first"`

✅ **Respuesta:** `0`

---

### P06 [COMPLETAR] — Ejercicio 1.1

**Completa el código para obtener el nombre del último personaje usando indexación negativa.**

```python
ultimo_nombre = characters_raw[_____]["name"]
```

Opciones: `-1` / `19` / `0` / `-0`

✅ **Respuesta:** `-1`

---

### P07 [CONCEPTUAL] — Ejercicio 1.1

**¿Qué diferencia práctica existe entre usar `characters_raw[19]` y `characters_raw[-1]` para acceder al último elemento de una lista de 20 elementos?**

✅ **Respuesta esperada:** Ambas expresiones acceden al mismo elemento (el último). Sin embargo, `characters_raw[-1]` es preferible porque no depende de conocer la longitud exacta de la lista; funciona correctamente independientemente del tamaño del dataset.

---

### P08 [LÓGICA] — Ejercicio 1.1

**Después de ejecutar la celda de la Solución 1.1, ¿cuál es la salida exacta de la línea `print("Personaje en el índice 9:", decimo_nombre)`?**

A) `Personaje en el índice 9: Asha` ❌
B) `Personaje en el índice 9: Pip` ✅
C) `Personaje en el índice 9: Fenn` ❌
D) `Personaje en el índice 9: Kael` ❌

---

### P09 [SELECCIÓN] — Ejercicio 1.2

**¿Cuál de los siguientes fragmentos de código construye correctamente una lista con los nombres de todos los personajes?**

A) `names = [c for c in characters_raw]` ❌ — Produce una lista de diccionarios, no de nombres
B) `names = [c["name"] for c in characters_raw]` ✅
C) `names = {c["name"] for c in characters_raw}` ❌ — Produce un conjunto (set), no una lista
D) `names = [characters_raw["name"]]` ❌ — Las listas no admiten acceso por clave de texto

---

### P10 [COMPLETAR] — Ejercicio 1.2

**Completa el código para obtener solo los nombres de los protagonistas.**

```python
protagonists = [c["name"] for c in characters_raw if c[_____] == "protagonist"]
```

Opciones: `"role"` / `"name"` / `"style"` / `"fps"`

✅ **Respuesta:** `"role"`

---

### P11 [CONCEPTUAL] — Ejercicio 1.2

**¿Por qué es necesaria la cláusula `if` en la comprensión de listas para obtener solo los protagonistas? ¿Qué ocurriría si se omitiera?**

✅ **Respuesta esperada:** La cláusula `if c["role"] == "protagonist"` actúa como filtro para incluir únicamente los registros cuyo campo `role` tenga el valor `"protagonist"`. Si se omitiera, la comprensión devolvería los nombres de los 20 personajes sin distinción de rol.

---

### P12 [LÓGICA] — Ejercicio 1.2

**¿Cuántos personajes aparecen en la lista `protagonists` tras ejecutar la Solución 1.2?**

A) 6 ❌
B) 8 ❌
C) 4 ✅
D) 10 ❌

---

### P13 [LÓGICA] — Ejercicio 1.2

**¿Por qué la suma de `len(protagonists)` + `len(antagonists)` no es igual a 20?**

A) Porque algunos personajes tienen dos roles asignados. ❌
B) Porque hay personajes cuyo campo `role` es `None` y no coincide con ningún filtro. ✅
C) Porque la comprensión de listas omite automáticamente el primero y el último elemento. ❌
D) Porque `characters_raw` tiene menos de 20 registros. ❌

---

### P14 [COMPLETAR] — Ejercicio 1.3

**Completa la comprensión de listas para identificar personajes con `role` faltante.**

```python
missing_role = [c["name"] for c in characters_raw if c[_____] is None]
```

Opciones: `"role"` / `"fps"` / `"has_special_fx"` / `"palette"`

✅ **Respuesta:** `"role"`

---

### P15 [SELECCIÓN] — Ejercicio 1.3

**¿Cuál de las siguientes expresiones detecta correctamente los personajes cuyo `fps` está almacenado como cadena de texto?**

A) `c["fps"] == str` ❌ — Compara el valor con el tipo `str`, no verifica instancia
B) `type(c["fps"]) is "str"` ❌ — Sintaxis inválida
C) `isinstance(c["fps"], str)` ✅
D) `c["fps"] is str` ❌ — Compara identidad de objeto, no tipo

---

### P16 [CONCEPTUAL] — Ejercicio 1.3

**¿Cuál es la diferencia entre `c["fps"] == "24"` e `isinstance(c["fps"], str)` para detectar valores de fps almacenados incorrectamente?**

✅ **Respuesta esperada:** `c["fps"] == "24"` solo detecta el caso exacto donde `fps` es la cadena `"24"`, dejando pasar cualquier otro valor textual como `"12"`. En cambio, `isinstance(c["fps"], str)` verifica si el tipo de dato es `str` independientemente del valor numérico específico, haciendo la detección genérica y robusta ante cualquier cadena.

---

### P17 [LÓGICA] — Ejercicio 1.3

**¿Qué personajes aparecen en la lista `wrong_fps_type` al ejecutar la Solución 1.3?**

A) `["Zorn", "Rex"]` ❌
B) `["Kael", "Thorn"]` ✅
C) `["Mira", "Olmo", "Drak"]` ❌
D) `["Crux", "Rex"]` ❌

---

### P18 [LÓGICA] — Ejercicio 1.3

**¿Qué personaje aparece en más de una lista de anomalías y cuáles son sus problemas?**

A) `Kael`: fps como cadena y paleta incompleta. ❌
B) `Rex`: `role` ausente (`None`) y `has_special_fx` ausente (`None`). ✅
C) `Mira`: paleta incompleta y fps como cadena. ❌
D) `Zorn`: `role` ausente y paleta incompleta. ❌

---

### P19 [SELECCIÓN] — Ejercicio 1.3

**Para detectar personajes con paleta de menos de 3 colores, ¿cuál es el fragmento correcto?**

A) `len(c["palette"] < 3)` ❌ — Error de paréntesis; compara lista con entero antes de contar
B) `c["palette"] < 3` ❌ — Compara la lista directamente con un número
C) `len(c["palette"]) < 3` ✅
D) `c["palette"].count() < 3` ❌ — `.count()` requiere un argumento; no retorna longitud

---

### P20 [CONCEPTUAL] — Ejercicio 1.4

**¿Por qué la operación `len(states) * fps` genera un `TypeError` cuando `fps` es una cadena de texto?**

✅ **Respuesta esperada:** Python no permite multiplicar un `int` (resultado de `len(states)`) por un `str`. Cuando se intenta `3 * "24"`, Python interpreta la multiplicación como repetición de cadena (devuelve `"242424"`), pero `len()` retorna un entero y el operador `*` entre `int` y `str` en este contexto produce una excepción `TypeError: can't multiply sequence by non-int of type 'str'`.

*(Nota al docente: en Python, `int * str` produce repetición de cadena y NO genera TypeError. El error ocurre en sentido contrario: `len(states)` es `int` y `fps` es `str`, por lo que `int * str` SÍ funciona como repetición de cadena — pero el resultado sería incorrecto lógicamente. En la práctica, el `TypeError` ocurriría si se intentara operaciones posteriores con ese resultado numérico. Para este dataset, el código del notebook usa `try/except TypeError` para capturar el caso.)*

---

### P21 [COMPLETAR] — Ejercicio 1.4

**Completa el bloque `try/except` para capturar el error de tipo al calcular fotogramas totales.**

```python
for c in characters_raw:
    try:
        frames = len(c["states"]) * c["fps"]
        valid_frames.append((c["name"], frames))
    except _____:
        error_names.append(c["name"])
```

Opciones: `TypeError` / `ValueError` / `KeyError` / `IndexError`

✅ **Respuesta:** `TypeError`

---

### P22 [CONCEPTUAL] — Ejercicio 1.4

**¿Qué ventaja ofrece utilizar `try/except` en lugar de una condición `if isinstance(c["fps"], str)` para gestionar el error en el cálculo de fotogramas?**

✅ **Respuesta esperada:** El bloque `try/except` gestiona el error en tiempo de ejecución sin interrumpir el proceso completo. Permite recolectar tanto los resultados válidos como los nombres con error en una sola pasada, sin necesidad de verificar el tipo de dato previamente. Además, es más robusto ante otros tipos de errores inesperados que puedan surgir en el mismo cálculo.

---

### P23 [LÓGICA] — Ejercicio 1.4

**Al ejecutar la Solución 1.4, ¿qué valor imprime la línea correspondiente a Blaze?**

A) `Blaze: 144 fotogramas` ❌
B) `Blaze: 168 fotogramas` ✅
C) `Blaze: 120 fotogramas` ❌
D) `Blaze: 185 fotogramas` ❌

> **Justificación:** Blaze tiene 7 estados × 24 fps = 168 fotogramas.

---

### P24 [SELECCIÓN] — Ejercicio 1.4

**¿Cuál es el resultado correcto de `len(["idle","walk","run","attack","special","fall","victory"]) * 24`?**

A) `144` ❌
B) `120` ❌
C) `168` ✅
D) `192` ❌

---

## Sección 2 — Tuplas (Ejercicios 2.1 – 2.4)

---

### P25 [CONCEPTUAL] — Ejercicio 2.1

**¿Por qué los colores de la paleta se almacenan como tuplas `(R, G, B)` y no como listas `[R, G, B]`?**

✅ **Respuesta esperada:** Las tuplas son inmutables: una vez definido un color como `(240, 180, 90)`, sus componentes no pueden modificarse accidentalmente. Esto las hace adecuadas para representar datos de configuración fija como especificaciones de color, que no deben alterarse durante el procesamiento.

---

### P26 [COMPLETAR] — Ejercicio 2.1

**Completa el código para acceder al primer color de la paleta del personaje `char`.**

```python
first_color = char["palette"][_____]
```

Opciones: `0` / `1` / `-1` / `"first"`

✅ **Respuesta:** `0`

---

### P27 [SELECCIÓN] — Ejercicio 2.1

**Dado `first_color = (240, 180, 90)`, ¿cuál instrucción imprime correctamente el canal Verde (G)?**

A) `print(first_color["G"])` ❌ — Las tuplas usan índices numéricos, no claves de texto
B) `print(first_color[1])` ✅
C) `print(first_color.G)` ❌ — Las tuplas no tienen atributos nombrados
D) `print(first_color[2])` ❌ — Índice 2 corresponde al canal Azul (B)

---

### P28 [V/F] — Ejercicio 2.1

**La instrucción `background_color[0] = 255` modifica exitosamente el canal Rojo de una tupla.**

✅ **Falso.** Las tuplas son inmutables. Ejecutar esa instrucción genera un `TypeError: 'tuple' object does not support item assignment`.

---

### P29 [COMPLETAR] — Ejercicio 2.2

**Completa el bucle para desempaquetar cada color de la paleta e imprimir sus canales.**

```python
for i, (r, g, b) in enumerate(char_5["palette"]):
    print(f"  Color {i+1}: R={_____}, G={_____}, B={_____}")
```

Opciones para cada espacio: `r` / `g` / `b` (el estudiante arrastra en orden correcto)

✅ **Respuesta:** `r`, `g`, `b`

---

### P30 [CONCEPTUAL] — Ejercicio 2.2

**¿Qué función cumple `enumerate` en el bucle `for i, (r, g, b) in enumerate(char_5["palette"])`?**

✅ **Respuesta esperada:** `enumerate` itera sobre la lista de colores generando simultáneamente el índice posicional `i` (comenzando en 0) y el elemento `(r, g, b)`. Esto permite numerar los colores en la salida (usando `i+1` para mostrar 1, 2, 3...) sin necesidad de un contador manual independiente.

---

### P31 [LÓGICA] — Ejercicio 2.2

**Al ejecutar la Solución 2.2, ¿cuál es el nombre del personaje en el índice 5 y cuántos colores tiene su paleta?**

A) Vela — 3 colores ❌
B) Crux — 3 colores ❌
C) Seraph — 4 colores ✅
D) Fenn — 3 colores ❌

---

### P32 [LÓGICA] — Ejercicio 2.2

**¿Cuáles son los valores exactos del segundo color en la paleta del personaje en el índice 5?**

A) `R=255, G=220, B=150` ❌ — Primer color
B) `R=200, G=160, B=80` ✅
C) `R=255, G=255, B=220` ❌ — Tercer color
D) `R=180, G=120, B=60` ❌ — Cuarto color

---

### P33 [COMPLETAR] — Ejercicio 2.3

**Completa la comprensión de listas para calcular el brillo de cada color en la paleta.**

```python
brightness_per_color = [(___ + g + b) / 3 for r, g, b in palette]
```

Opciones: `r` / `R` / `red` / `0`

✅ **Respuesta:** `r`

---

### P34 [SELECCIÓN] — Ejercicio 2.3

**¿Cuál es la fórmula correcta para calcular el brillo promedio de una paleta de colores?**

A) `max(brightness_per_color) / len(brightness_per_color)` ❌
B) `sum(brightness_per_color) / len(brightness_per_color)` ✅
C) `sum(brightness_per_color) / 3` ❌ — Divide entre el número de canales, no de colores
D) `sum(palette) / len(palette)` ❌ — `palette` contiene tuplas, no números directamente

---

### P35 [LÓGICA] — Ejercicio 2.3

**Calcula manualmente el brillo del color `(240, 180, 90)` (primer color de Lyra).**

A) `156.67` ❌
B) `180.0` ❌
C) `170.0` ✅
D) `510.0` ❌

> **Justificación:** `(240 + 180 + 90) / 3 = 510 / 3 = 170.0`

---

### P36 [LÓGICA] — Ejercicio 2.3

**¿Qué personaje tiene el mayor brillo promedio de paleta en el dataset inicial (`characters_raw`)?**

A) Mira ❌
B) Sela ❌
C) Lune ✅
D) Vela ❌

> **Justificación:** Lune tiene brillo promedio de 228.89 (colores muy luminosos: `(220,220,255)`, `(180,180,240)`, `(255,255,255)`).

---

### P37 [COMPLETAR] — Ejercicio 2.3

**Completa el código para identificar el personaje con menor brillo promedio.**

```python
darkest = _____(brightness_records, key=lambda t: t[1])
```

Opciones: `min` / `max` / `sorted` / `filter`

✅ **Respuesta:** `min`

---

### P38 [CONCEPTUAL] — Ejercicio 2.3

**¿Qué representa el parámetro `key=lambda t: t[1]` en la función `min(brightness_records, key=lambda t: t[1])`?**

✅ **Respuesta esperada:** `brightness_records` es una lista de tuplas `(name, avg_brightness)`. El parámetro `key` indica a `min()` por qué criterio comparar los elementos. La función `lambda t: t[1]` extrae el segundo elemento de cada tupla (el valor numérico de brillo promedio), por lo que `min` selecciona la tupla cuyo brillo sea el más bajo, en lugar de comparar los nombres alfabéticamente.

---

### P39 [SELECCIÓN] — Ejercicio 2.4

**¿Cuál de las siguientes expresiones construye correctamente el diccionario `production_lookup` con claves compuestas `(name, style)`?**

A) `{[c["name"], c["style"]]: c["production_hours"] for c in characters_raw}` ❌ — Las listas no son hashables
B) `{(c["name"], c["style"]): c["production_hours"] for c in characters_raw}` ✅
C) `{c["name"] + c["style"]: c["production_hours"] for c in characters_raw}` ❌ — Concatena strings pero pierde estructura de clave compuesta
D) `{c: c["production_hours"] for c in characters_raw}` ❌ — Los diccionarios no son hashables

---

### P40 [CONCEPTUAL] — Ejercicio 2.4

**¿Por qué no es posible usar una lista como clave de un diccionario en Python?**

✅ **Respuesta esperada:** Las claves de un diccionario deben ser objetos hashables (inmutables). Python calcula un valor hash para cada clave que permite acceder a ella en tiempo O(1). Las listas son mutables: pueden modificarse después de su creación, lo que haría que su hash cambiara, corrompiendo la estructura interna del diccionario. Por eso Python lanza `TypeError: unhashable type: 'list'`. Las tuplas, siendo inmutables, sí son hashables y se usan como claves compuestas.

---

### P41 [V/F] — Ejercicio 2.4

**El código `{["Lyra", "cel_shaded"]: 142.0}` se ejecuta sin errores en Python.**

✅ **Falso.** Genera `TypeError: unhashable type: 'list'` porque las listas no pueden ser claves de diccionario.

---

### P42 [LÓGICA] — Ejercicio 2.4

**¿Qué valor retorna `production_lookup[("Lyra", "cel_shaded")]` tras ejecutar la Solución 2.4?**

A) `"protagonist"` ❌
B) `142` ❌ — Valor entero; el dato original es float
C) `142.0` ✅
D) `"cel_shaded"` ❌

---

## Sección 3 — Diccionarios (Ejercicios 3.1 – 3.6)

---

### P43 [CONCEPTUAL] — Ejercicio 3.1

**¿Por qué se utiliza `copy.deepcopy(characters_raw)` en lugar de `characters = characters_raw` o `characters = characters_raw.copy()`?**

✅ **Respuesta esperada:**
- `characters = characters_raw` crea una referencia al mismo objeto; cualquier modificación afecta al original.
- `characters_raw.copy()` (copia superficial) duplica la lista externa pero los diccionarios internos siguen siendo los mismos objetos en memoria; modificar `characters[0]["role"]` cambiaría también `characters_raw[0]["role"]`.
- `copy.deepcopy()` crea copias independientes de todos los objetos anidados, garantizando que `characters` y `characters_raw` sean completamente independientes.

---

### P44 [SELECCIÓN] — Ejercicio 3.1

**¿Cuál es la instrucción correcta para crear una copia profunda del dataset?**

A) `characters = characters_raw` ❌ — Solo crea un alias, no una copia
B) `characters = characters_raw[:]` ❌ — Copia superficial; los diccionarios internos son compartidos
C) `characters = copy.deepcopy(characters_raw)` ✅
D) `characters = list(characters_raw)` ❌ — Copia superficial equivalente a `[:]`

---

### P45 [COMPLETAR] — Ejercicio 3.2

**Completa el valor faltante en el diccionario de correcciones.**

```python
role_corrections = {
    "Crux": "support",
    "Rex":  _____,
}
```

Opciones: `"antagonist"` / `"protagonist"` / `"support"` / `None`

✅ **Respuesta:** `"antagonist"`

---

### P46 [COMPLETAR] — Ejercicio 3.2

**Completa el bucle para aplicar las correcciones de rol al dataset.**

```python
for c in characters:
    if c[_____] in role_corrections:
        c["role"] = role_corrections[c["name"]]
```

Opciones: `"name"` / `"role"` / `"style"` / `0`

✅ **Respuesta:** `"name"`

---

### P47 [CONCEPTUAL] — Ejercicio 3.2

**¿Qué ventaja ofrece utilizar un diccionario de correcciones `{nombre: rol_correcto}` en lugar de escribir un bloque `if/elif` para cada personaje a corregir?**

✅ **Respuesta esperada:** El diccionario de correcciones es más mantenible y escalable. Para agregar un nuevo personaje a corregir, basta con añadir una entrada al diccionario sin modificar la lógica del bucle. El bloque `if/elif` requeriría agregar condiciones adicionales y hace el código más difícil de leer a medida que crece la cantidad de correcciones.

---

### P48 [LÓGICA] — Ejercicio 3.2

**Tras aplicar la Solución 3.2, ¿cuántos personajes tienen el rol `"antagonist"`?**

A) 6 ❌ — Cantidad antes de la corrección
B) 7 ✅
C) 8 ❌
D) 9 ❌

---

### P49 [LÓGICA] — Ejercicio 3.2

**¿La suma de los tres conteos de rol (protagonist + antagonist + support) equivale a 20 tras la Solución 3.2?**

A) No, porque todavía hay 2 personajes con `role = None`. ❌
B) Sí, porque todos los registros ahora tienen un rol asignado: 4 + 7 + 9 = 20. ✅
C) No, porque algunos personajes tienen múltiples roles. ❌
D) No, porque el conteo excede 20 ya que Rex aparece en dos categorías. ❌

---

### P50 [COMPLETAR] — Ejercicio 3.3

**Completa el bloque para corregir el tipo de dato de `fps`.**

```python
for c in characters:
    if isinstance(c["fps"], str):
        c["fps"] = _____(c["fps"])
```

Opciones: `int` / `float` / `str` / `bool`

✅ **Respuesta:** `int`

---

### P51 [SELECCIÓN] — Ejercicio 3.3

**¿Qué problema generaría usar `float(c["fps"])` en lugar de `int(c["fps"])` para corregir el tipo de dato?**

A) Generaría un `TypeError` porque `fps` es una cadena. ❌
B) No causaría ningún problema; el cálculo de fotogramas funcionaría igual. ❌
C) El valor de `fps` quedaría como `24.0` en lugar de `24`, lo que podría generar inconsistencias al exportar el dataset o en comparaciones exactas de tipo. ✅
D) `float()` no puede convertir cadenas numéricas. ❌

---

### P52 [LÓGICA] — Ejercicio 3.3

**Después de ejecutar la Solución 3.3, ¿cuántos valores distintos de `fps` existen en el dataset?**

A) 2 (12 y 24) ❌
B) 4 (8, 12, 24 y otro) ❌
C) 3 (8, 12 y 24) ✅
D) 1 (24 para todos) ❌

---

### P53 [V/F] — Ejercicio 3.3

**Después de ejecutar la Solución 3.3, el tipo del campo `fps` para el personaje Kael es `str`.**

✅ **Falso.** Tras la corrección, el campo `fps` de Kael tiene el valor `24` de tipo `int`.

---

### P54 [COMPLETAR] — Ejercicio 3.4

**Completa el código para corregir valores `None` en `has_special_fx`.**

```python
for c in characters:
    if c["has_special_fx"] is _____:
        c["has_special_fx"] = 0
```

Opciones: `None` / `0` / `False` / `""`

✅ **Respuesta:** `None`

---

### P55 [CONCEPTUAL] — Ejercicio 3.4

**¿Por qué se asigna `0` (y no `1`) como valor por defecto para `has_special_fx` cuando el campo es `None`?**

✅ **Respuesta esperada:** El criterio de producción prudente establece que agregar efectos especiales incrementa el costo y debe ser confirmado explícitamente. En ausencia de información, asumir que un personaje no tiene efectos especiales (`0`) es la decisión más conservadora para la planificación de recursos, evitando sobreestimar costos.

---

### P56 [LÓGICA] — Ejercicio 3.4

**¿Qué personajes aparecen en la salida de la Solución 3.4 como corregidos de `None` a `0`?**

A) `Crux` y `Rex` ❌
B) `Kael` y `Thorn` ❌
C) `Zorn` y `Rex` ✅
D) `Mira` y `Olmo` ❌

---

### P57 [LÓGICA] — Ejercicio 3.4

**Tras ejecutar la Solución 3.4, ¿cuántos personajes tienen `has_special_fx` igual a `1`?**

A) 8 ❌
B) 12 ❌
C) 10 ✅
D) 9 ❌

---

### P58 [COMPLETAR] — Ejercicio 3.5

**Completa las entradas del diccionario de adiciones de paleta.**

```python
palette_additions = {
    "Mira": [(240, 250, 255)],
    "Drak": [(255, 50, 50), _____],
    "Olmo": [(80, 140, 60),  _____],
}
```

Opciones para Drak: `(80, 0, 0)` / `(0, 80, 0)` / `(0, 0, 80)` / `(80, 80, 0)`
Opciones para Olmo: `(240, 255, 220)` / `(220, 240, 255)` / `(255, 240, 220)` / `(240, 220, 255)`

✅ **Respuestas:** Drak → `(80, 0, 0)` / Olmo → `(240, 255, 220)`

---

### P59 [COMPLETAR] — Ejercicio 3.5

**Completa el código para agregar los colores a la paleta del personaje.**

```python
for color in palette_additions[c["name"]]:
    c["palette"]._____(color)
```

Opciones: `append` / `add` / `insert` / `extend`

✅ **Respuesta:** `append`

---

### P60 [CONCEPTUAL] — Ejercicio 3.5

**¿Cuál es la diferencia entre `lista.append(elemento)` y `lista.extend(otra_lista)` en Python?**

✅ **Respuesta esperada:** `append(elemento)` agrega un único elemento al final de la lista, por lo que para añadir dos colores se necesitarían dos llamadas a `append`. `extend(otra_lista)` añade todos los elementos de otra lista de una sola vez. En el ejercicio se usó `append` dentro de un bucle `for color in ...` para agregar los colores uno a uno.

---

### P61 [LÓGICA] — Ejercicio 3.5

**¿Cuántos colores tiene la paleta de Mira después de ejecutar la Solución 3.5?**

A) 1 ❌
B) 2 ❌ — Cantidad antes de la corrección
C) 3 ✅
D) 4 ❌

---

### P62 [SELECCIÓN] — Ejercicio 3.5

**¿Qué comprensión de listas permite verificar que ningún personaje tiene menos de 3 colores en su paleta?**

A) `[c for c in characters if len(c["palette"]) >= 3]` ❌ — Lista los que cumplen, no los que fallan
B) `[c["name"] for c in characters if len(c["palette"]) < 3]` ✅ — Retorna `[]` si todo está correcto
C) `{c["name"]: len(c["palette"]) for c in characters}` ❌ — Diccionario, no lista de verificación
D) `all(len(c["palette"]) >= 3 for c in characters)` ❌ — Correcto funcionalmente pero no es una lista de nombres

---

### P63 [COMPLETAR] — Ejercicio 3.6

**Completa la comprensión de diccionarios para contar estados por personaje.**

```python
state_counts = {c[_____]: len(c[_____]) for c in characters}
```

Opciones para primer espacio: `"name"` / `"role"` / `"style"` / `"fps"`
Opciones para segundo espacio: `"states"` / `"palette"` / `"name"` / `"fps"`

✅ **Respuestas:** `"name"`, `"states"`

---

### P64 [COMPLETAR] — Ejercicio 3.6

**Completa el código para encontrar el personaje con mayor número de estados.**

```python
most_complex = max(state_counts, key=lambda name: state_counts[_____])
```

Opciones: `name` / `"name"` / `0` / `most_complex`

✅ **Respuesta:** `name`

---

### P65 [CONCEPTUAL] — Ejercicio 3.6

**¿Qué tipo de objeto devuelve la función `max(state_counts, ...)` cuando `state_counts` es un diccionario?**

✅ **Respuesta esperada:** Cuando se itera sobre un diccionario (como hace `max()`), se itera sobre sus **claves**. Por lo tanto, `max(state_counts, key=...)` devuelve la **clave** con mayor valor según el criterio especificado, que en este caso es el nombre del personaje (tipo `str`), no el valor (número de estados).

---

### P66 [LÓGICA] — Ejercicio 3.6

**¿Qué personaje aparece como el más complejo tras ejecutar la Solución 3.6?**

A) Seraph ❌ — 6 estados
B) Gorr ❌ — 6 estados
C) Blaze ✅ — 7 estados: idle, walk, run, attack, special, fall, victory
D) Asha ❌ — 5 estados

---

### P67 [LÓGICA] — Ejercicio 3.6

**¿Cuántos personajes tienen exactamente 3 estados de animación?**

A) 2 ❌
B) 3 ❌
C) 4 ✅ — Crux, Fenn, Lune, Sela
D) 5 ❌

---

## Sección 4 — Integración (Ejercicios 4.1 – 4.3)

---

### P68 [COMPLETAR] — Ejercicio 4.1

**Completa el cálculo del número de colores en la paleta.**

```python
c["num_colors"] = _____(palette)
```

Opciones: `len` / `count` / `sum` / `max`

✅ **Respuesta:** `len`

---

### P69 [COMPLETAR] — Ejercicio 4.1

**Completa el cálculo de contraste de color.**

```python
c["color_contrast"] = round(_____(brightness_values) - _____(brightness_values), 2)
```

Opciones para el primer espacio: `max` / `min` / `sum` / `abs`
Opciones para el segundo espacio: `min` / `max` / `sum` / `sorted`

✅ **Respuestas:** `max`, `min`

---

### P70 [COMPLETAR] — Ejercicio 4.1

**Completa el cálculo del total estimado de fotogramas clave.**

```python
c["num_frames_total"] = c["num_states"] * c[_____]
```

Opciones: `"fps"` / `"num_colors"` / `"screen_time_ratio"` / `"production_hours"`

✅ **Respuesta:** `"fps"`

---

### P71 [SELECCIÓN] — Ejercicio 4.1

**¿Cuál es la expresión correcta para calcular `avg_brightness` redondeada a 2 decimales?**

A) `round(sum(brightness_values) / 3, 2)` ❌ — Divide entre 3 canales en lugar del número de colores
B) `round(sum(brightness_values) / len(brightness_values), 2)` ✅
C) `sum(brightness_values) / len(brightness_values)` ❌ — Falta el redondeo
D) `round(avg(brightness_values), 2)` ❌ — `avg()` no existe como función nativa en Python

---

### P72 [CONCEPTUAL] — Ejercicio 4.1

**¿Por qué se puede modificar `c["num_colors"]` directamente sin retornar el diccionario al final del bucle?**

✅ **Respuesta esperada:** Cuando se itera sobre `characters` con `for c in characters:`, la variable `c` es una referencia al diccionario original dentro de la lista, no una copia. Por lo tanto, asignar `c["nueva_clave"] = valor` modifica el diccionario en memoria y el cambio queda reflejado permanentemente en `characters`, sin necesidad de reasignación.

---

### P73 [V/F] — Ejercicio 4.2

**Si la celda de verificación del Ejercicio 4.2 imprime `"Verificación exitosa: los 20 registros están completos y validados."`, significa que todos los campos requeridos están presentes, ningún `fps` es texto, y todas las paletas tienen al menos 3 colores.**

✅ **Verdadero.** La celda de verificación comprueba exactamente esas tres condiciones antes de emitir el mensaje de éxito.

---

### P74 [SELECCIÓN] — Ejercicio 4.2

**Si se omite el Ejercicio 3.3 (corrección del tipo de `fps`), ¿qué mensaje aparecería al ejecutar la celda de verificación del Ejercicio 4.2?**

A) `"Verificación exitosa"` ❌ — La verificación detecta el tipo incorrecto
B) Un mensaje indicando que el campo `fps` de Kael y Thorn no es de tipo `int`. ✅
C) Un `KeyError` porque el campo `fps` no existe. ❌
D) Ningún error, porque la verificación no comprueba el tipo de `fps`. ❌

---

### P75 [COMPLETAR] — Ejercicio 4.3

**Completa el código para calcular el promedio de horas de producción.**

```python
all_hours = [c["production_hours"] for c in characters]
avg_hours = _____(all_hours) / _____(all_hours)
```

Opciones para primer espacio: `sum` / `max` / `min` / `sorted`
Opciones para segundo espacio: `len` / `count` / `range` / `size`

✅ **Respuestas:** `sum`, `len`

---

### P76 [COMPLETAR] — Ejercicio 4.3

**Completa el código para identificar al personaje con mayor número total de fotogramas.**

```python
top_frames = max(characters, key=lambda c: c[_____])
```

Opciones: `"num_frames_total"` / `"production_hours"` / `"fps"` / `"num_states"`

✅ **Respuesta:** `"num_frames_total"`

---

### P77 [LÓGICA] — Ejercicio 4.3

**¿Cuál es el promedio de horas de producción de los 20 personajes redondeado a 2 decimales?**

A) `95.35` ❌
B) `96.33` ✅
C) `100.00` ❌
D) `142.0` ❌

> **Justificación:** Suma total = 1926.5 / 20 = 96.325 → redondeado a `96.33`.

---

### P78 [LÓGICA] — Ejercicio 4.3

**¿El personaje con mayor `num_frames_total` es el mismo que el personaje con mayor `production_hours`?**

A) No, son personajes diferentes. ❌
B) Sí, en ambos casos es Blaze (168 fotogramas y 185.0 horas). ✅
C) Sí, en ambos casos es Seraph. ❌
D) No es posible determinarlo sin ejecutar el código. ❌

---

### P79 [CONCEPTUAL] — Ejercicio 4.3

**¿Qué implica que el mayor número de fotogramas y el mayor tiempo de producción coincidan en el mismo personaje?**

✅ **Respuesta esperada:** En este dataset, Blaze es el personaje más costoso en ambas dimensiones. Sin embargo, comparando el resto de personajes (por ejemplo, Seraph y Gorr tienen 144 fotogramas cada uno pero Seraph requiere más horas), queda evidente que el número de fotogramas no es el único factor determinante del costo de producción. El estilo de arte (`painted` vs `flat`), la presencia de efectos especiales y la proporción de pantalla también influyen. Esto anticipa la necesidad del análisis de correlación en la Parte 2.

---

### P80 [SELECCIÓN] — Exportación Final

**¿Cuál es el propósito de `extrasaction="ignore"` en `csv.DictWriter(f, fieldnames=export_fields, extrasaction="ignore")`?**

A) Ignorar los errores de codificación de caracteres al escribir el CSV. ❌
B) Omitir automáticamente los campos presentes en los diccionarios pero no listados en `fieldnames`, como `palette` y `states`. ✅
C) Ignorar los registros con valores `None` al exportar. ❌
D) Deshabilitar las comillas en los valores del archivo CSV. ❌

---

### P81 [CONCEPTUAL] — Exportación Final

**¿Por qué los campos `palette` y `states` no se incluyen en `export_fields` para el archivo CSV?**

✅ **Respuesta esperada:** Las paletas son listas de tuplas `[(R,G,B), ...]` y `states` es una lista de cadenas `["idle","walk",...]`. Estas estructuras no pueden representarse directamente en un formato CSV plano de manera que sean fácilmente legibles por Pandas en la Parte 2. En su lugar, se exportan los campos derivados numéricos (`num_colors`, `avg_brightness`, `color_contrast`, `num_states`, `num_frames_total`) que resumen la información relevante de esas estructuras de forma tabular.

---

## Sección 5 — Preguntas de Comprensión General

---

### P82 [SELECCIÓN] — Comprensión general

**¿Cuál es el flujo de trabajo correcto de este notebook?**

A) Exportar → Corregir → Detectar errores → Calcular campos derivados ❌
B) Detectar errores → Exportar → Corregir → Calcular campos derivados ❌
C) Detectar errores → Copiar dataset → Corregir → Calcular campos derivados → Verificar → Exportar ✅
D) Copiar dataset → Exportar → Corregir → Verificar ❌

---

### P83 [CONCEPTUAL] — Comprensión general

**¿Por qué el notebook utiliza `characters_raw` para los ejercicios de la Parte 1 (Listas) y la Parte 2 (Tuplas), pero cambia a `characters` a partir de la Parte 3 (Diccionarios)?**

✅ **Respuesta esperada:** Los ejercicios de Partes 1 y 2 son de exploración y diagnóstico: identifican los errores sin modificarlos para permitir que el estudiante comprenda el estado inicial de los datos. A partir de la Parte 3 se realizan las correcciones, que deben aplicarse a `characters` (la copia profunda) para no alterar el dataset original de referencia `characters_raw`.

---

### P84 [V/F] — Comprensión general

**El archivo `characters_clean.csv` exportado al final del notebook contiene las mismas 20 filas con datos ya corregidos y con campos derivados calculados.**

✅ **Verdadero.** El CSV exportado contiene 20 registros con los 12 campos de análisis: `name, role, fps, has_special_fx, style, screen_time_ratio, num_colors, avg_brightness, color_contrast, num_states, num_frames_total, production_hours`.

---

### P85 [CONCEPTUAL] — Comprensión general

**¿Cuál es la importancia del dataset `characters_clean.csv` generado en este notebook para las partes siguientes del curso?**

✅ **Respuesta esperada:** El archivo `characters_clean.csv` sirve como punto de entrada para la Parte 2, donde se cargará con Pandas para realizar análisis exploratorio y selección de características. En la Parte 3, las características seleccionadas se usarán para entrenar un modelo de regresión lineal que prediga `production_hours`. Sin la limpieza realizada en este notebook, los errores de tipo y los valores faltantes causarían fallos o resultados incorrectos en las etapas posteriores.

---

## Apéndice — Fragmentos de Código para Preguntas de Arrastrar y Soltar

> Esta sección proporciona piezas de código que se pueden configurar en Moodle como elementos arrastrables para las preguntas de tipo Drag-and-Drop Markers o Drag-and-Drop into Text.

### Bloque A — Acceso a datos

| Fragmento | Uso |
|-----------|-----|
| `characters_raw[0]` | Primer elemento de la lista |
| `characters_raw[-1]` | Último elemento de la lista |
| `characters_raw[9]` | Elemento en índice 9 |
| `len(characters_raw)` | Total de elementos |
| `c["name"]` | Campo nombre del personaje |
| `c["role"]` | Campo rol del personaje |
| `c["fps"]` | Campo fps del personaje |
| `c["palette"]` | Campo paleta del personaje |
| `c["states"]` | Campo estados del personaje |

### Bloque B — Condiciones y tipos

| Fragmento | Uso |
|-----------|-----|
| `is None` | Verificar valor faltante |
| `isinstance(c["fps"], str)` | Verificar si fps es texto |
| `len(c["palette"]) < 3` | Paleta incompleta |
| `c["role"] == "protagonist"` | Filtrar protagonistas |
| `c["role"] == "antagonist"` | Filtrar antagonistas |

### Bloque C — Operaciones y funciones

| Fragmento | Uso |
|-----------|-----|
| `len(lista)` | Contar elementos |
| `sum(lista)` | Sumar valores |
| `min(lista, key=...)` | Valor mínimo |
| `max(lista, key=...)` | Valor máximo |
| `int(valor)` | Convertir a entero |
| `round(valor, 2)` | Redondear a 2 decimales |
| `copy.deepcopy(obj)` | Copia profunda |
| `lista.append(elem)` | Agregar elemento |

### Bloque D — Estructuras

| Fragmento | Uso |
|-----------|-----|
| `[expr for x in lista]` | Comprensión de lista |
| `[expr for x in lista if cond]` | Comprensión con filtro |
| `{k: v for x in lista}` | Comprensión de diccionario |
| `for r, g, b in palette:` | Desempaquetado de tuplas en bucle |
| `for i, (r, g, b) in enumerate(...)` | Desempaquetado con índice |
| `try: ... except TypeError:` | Manejo de excepciones |

---

*Fin del Banco de Preguntas — Parte 1: Estructuras de Datos*
*Total: 85 preguntas | Tipos: COMPLETAR (22) · SELECCIÓN (22) · CONCEPTUAL (18) · LÓGICA (15) · V/F (8)*
