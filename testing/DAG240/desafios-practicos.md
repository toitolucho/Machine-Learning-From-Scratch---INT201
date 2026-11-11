# Desafíos Prácticos — Python en Blender
## DAG240 — Scripting con Python

> **Instrucciones generales:** Tienes permiso de usar IA en la Fase 2. La Fase 1 debe completarse con tu propio código o adaptando código visto en clase. Demuestra que entiendes lo que tu código hace.

---

## Desafío 1: La Fila de Dados

### Contexto
Una fábrica de juegos de mesa te contrató para automatizar la creación de piezas de dominó en 3D. El primer prototipo es simple: una fila de cubos que representan los cuerpos de los dados. Si logras ese paso, el siguiente reto es construir piezas de dominó completas con sus puntos grabados. El cliente quiere ver el potencial de Blender como herramienta de producción automatizada.

---

### Fase 1 — Código Propio (≈10 minutos)

**Objetivo:** Crear una fila de 5 cubos de tamaño 1×1×1 unidades, distribuidos uniformemente a lo largo del eje X, usando un bucle `for`.

**Requisitos:**
- Deben existir exactamente 5 cubos en la escena después de ejecutar el script.
- Cada cubo debe medir 1×1×1 unidades (escala unitaria).
- El primer cubo se ubica en el origen `(0, 0, 0)`.
- Cada cubo siguiente se separa **2 unidades** del anterior en el eje X (separación entre centros).
- El cubo base "Cube" que ya existe en la escena puede usarse como punto de partida o eliminarse/ignorarse según tu criterio.
- Los cubos deben nombrarse automáticamente: `Dado_1`, `Dado_2`, ..., `Dado_5`.

**Punto de partida:**
La escena tiene el cubo predeterminado de Blender (`Cube`) en el origen. Puedes conservarlo o borrarlo antes de crear los tuyos. Usa `bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))` para agregar cubos. Para renombrar el objeto activo, accede a `bpy.context.active_object.name`.

**Pseudocódigo sugerido:**
```
importar bpy

Para cada número i del 0 al 4:
    calcular posición_x = i * 2
    agregar cubo en (posición_x, 0, 0) con tamaño 1
    renombrar el objeto activo como "Dado_" + (i + 1)
```

**Criterio de evaluación:**
- El script se ejecuta sin errores en la Consola de Python de Blender.
- Se crean exactamente 5 cubos en la vista 3D.
- La separación entre cubos es visualmente uniforme (2 u entre centros).
- Cada cubo tiene el nombre correcto visible en el Outliner.

**Pista:** Después de `primitive_cube_add`, el nuevo objeto queda seleccionado y activo automáticamente. Puedes acceder a él con `bpy.context.active_object`.

---

### Fase 2 — Con Asistencia de IA

**Descripción del reto extendido:**

Ahora debes crear un **juego completo de dominó** en 3D de forma procedural. Cada pieza de dominó tiene dos mitades rectangulares unidas, y cada mitad debe mostrar una cantidad de puntos (entre 0 y 6) representados como pequeñas esferas hundidas usando el modificador Boolean de Blender. Las combinaciones de puntos deben generarse aleatoriamente (o siguiendo el conjunto estándar de dominó del [0|0] al [6|6]).

Para describirle bien el problema a una IA necesitarás entender: cómo se estructura una pieza de dominó geométricamente, cómo se posicionan los puntos según el número (patrón de cara de dado), cómo funciona el modificador Boolean en `bpy`, y cómo se recorre y aplica sobre un objeto base.

**Lo que debes lograr:**
- Generar al menos 5 piezas de dominó con combinaciones distintas de puntos (puede ser aleatorio con `random`).
- Cada pieza debe ser un objeto único compuesto por dos mitades rectangulares fusionadas (o agrupadas lógicamente).
- Los puntos (hoyos) de cada mitad deben corresponder al número asignado (0 a 6), posicionados de forma reconocible como en un dado real.
- Las piezas deben estar separadas y visibles en la vista 3D, no superpuestas.
- Aplica el modificador Boolean para que los puntos aparezcan como depresiones en la superficie del dominó.

**Criterio de evaluación de la Fase 2:**
- El código generado por IA funciona sin errores en Blender (versión 3.x o 4.x).
- El estudiante puede explicar qué hace cada bloque del código: creación de la pieza, posicionado de puntos, aplicación del Boolean.
- El estudiante puede modificar el número de piezas generadas o el tamaño de los puntos cambiando un solo parámetro.
- Los puntos están correctamente distribuidos según el patrón estándar de cada número (1 al 6).
- El estudiante puede defender por qué eligió el prompt que usó y qué ajustes tuvo que hacer al código de la IA.

**Reflexión (entregar junto al código):**
1. ¿Qué tan preciso tuviste que ser en tu prompt para que la IA generara un código útil? ¿Qué información fue indispensable incluir y qué ocurrió cuando la omitiste?
2. ¿El código de la IA funcionó a la primera? Si no, ¿qué tuviste que corregir y por qué crees que la IA cometió ese error?

---

## Desafío 2: El Árbol de Esferas

### Contexto
Eres el artista técnico de un estudio de animación que produce una serie navideña. El director quiere un árbol de Navidad minimalista hecho enteramente de esferas, generado por script para poder cambiar fácilmente su tamaño y densidad sin rehacer el modelo. La primera versión es un árbol simple de tres niveles. Si convences al director, te pedirá una versión fractal completa con materiales por nivel.

---

### Fase 1 — Código Propio (≈10 minutos)

**Objetivo:** Crear un árbol de tres niveles con esferas usando `primitive_uv_sphere_add`, posicionando cada nivel con cálculos trigonométricos básicos.

**Requisitos:**
- **Nivel 0 (base / tronco superior):** 1 esfera grande de radio `1.0` ubicada en `(0, 0, 0)`.
- **Nivel 1 (medio):** 3 esferas medianas de radio `0.6`, distribuidas en un anillo circular alrededor del centro a un radio de `1.8` unidades, elevadas en `Z = 1.5`.
- **Nivel 2 (cima):** 5 esferas pequeñas de radio `0.35`, distribuidas en un anillo circular a radio `1.2` unidades, elevadas en `Z = 3.0`.
- Usar `import math` y las funciones `math.cos()` y `math.sin()` para calcular las posiciones X e Y de cada esfera en el anillo.
- Cada esfera debe nombrarse según su nivel: `Nivel0_0`, `Nivel1_0`, `Nivel1_1`, etc.

**Punto de partida:**
Escena vacía (o con el cubo predeterminado que puedes ignorar/borrar). Usa `bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, z))` para crear cada esfera.

**Pseudocódigo sugerido:**
```
importar bpy, math

# Nivel 0
agregar esfera en (0, 0, 0) con radio 1.0
renombrar como "Nivel0_0"

# Nivel 1 — 3 esferas en anillo
Para i del 0 al 2:
    ángulo = (2 * PI / 3) * i        # dividir el círculo en 3 partes iguales
    x = cos(ángulo) * 1.8
    y = sin(ángulo) * 1.8
    z = 1.5
    agregar esfera en (x, y, z) con radio 0.6
    renombrar como "Nivel1_" + i

# Nivel 2 — 5 esferas en anillo
Para i del 0 al 4:
    ángulo = (2 * PI / 5) * i
    x = cos(ángulo) * 1.2
    y = sin(ángulo) * 1.2
    z = 3.0
    agregar esfera en (x, y, z) con radio 0.35
    renombrar como "Nivel2_" + i
```

**Criterio de evaluación:**
- El script crea exactamente 9 esferas (1 + 3 + 5) sin errores.
- Las esferas de cada nivel están visiblemente en anillo, con separación uniforme.
- Los tamaños decrecen correctamente de nivel en nivel.
- El árbol se "ve" como un árbol cuando se observa desde una vista lateral.
- Los nombres son correctos en el Outliner.

**Pista:** El ángulo total de un círculo completo es `2 * math.pi` radianes. Para dividirlo en `n` partes iguales, el ángulo de cada parte es `(2 * math.pi / n) * i` para el elemento `i`.

---

### Fase 2 — Con Asistencia de IA

**Descripción del reto extendido:**

Ahora debes construir un **árbol fractal de esferas con N niveles** configurable, donde cada nivel tenga más esferas que el anterior, radio y tamaño de esfera progresivamente menores, y altura creciente. Adicionalmente, cada nivel debe tener un **material propio con un color distinto** asignado proceduralmente (por ejemplo, del verde oscuro en la base al verde claro o dorado en la cima). El número total de niveles `N` debe ser un parámetro fácil de cambiar al inicio del script.

Para describir esto bien a una IA necesitarás comprender: cómo crear y asignar materiales en `bpy`, cómo usar `bpy.data.materials.new()` y el nodo `Principled BSDF`, y cómo estructurar un bucle anidado para niveles y esferas dentro de cada nivel.

**Lo que debes lograr:**
- El script acepta un parámetro `N_NIVELES` (mínimo 4, prueba con 6).
- Cada nivel `i` tiene `2*i + 1` esferas (nivel 0 tiene 1, nivel 1 tiene 3, nivel 2 tiene 5...).
- El radio de las esferas disminuye con cada nivel (ej. `radio = 1.0 - i * 0.15`).
- El radio del anillo también disminuye hacia arriba (ej. `radio_anillo = 2.0 - i * 0.3`).
- La altura Z aumenta uniformemente por nivel.
- Cada nivel tiene un material único con un color RGBA distinto interpolado entre dos colores definidos por el usuario.
- Todos los objetos están correctamente nombrados con su nivel e índice.

**Criterio de evaluación de la Fase 2:**
- El árbol fractal se genera correctamente para `N_NIVELES = 5` y `N_NIVELES = 7` sin errores.
- Los materiales son visibles en el modo de previsualización de material (Material Preview).
- El estudiante puede cambiar los colores del gradiente modificando solo dos variables al inicio del script.
- El estudiante puede explicar cómo se interpolan los colores entre niveles.
- El resultado es visualmente reconocible como un árbol.

**Reflexión (entregar junto al código):**
1. ¿Qué conceptos de matemática (trigonometría, interpolación) tuviste que explicarle a la IA para que el código fuera correcto? ¿Cómo los explicaste?
2. Observa el árbol generado: ¿qué cambiarías para hacerlo más realista o más interesante visualmente? ¿Puedes implementar ese cambio tú mismo sin ayuda de la IA?

---

## Desafío 3: La Galería de Clones

### Contexto
Eres el asistente técnico de un artista que modeló manualmente un personaje llamado "Personaje" en Blender. El artista quiere mostrar su creación en una galería virtual donde aparecen múltiples versiones del mismo personaje en diferentes tamaños, como si fuera una instalación de arte contemporáneo. Tu trabajo es automatizar la clonación y disposición de los personajes con un script de Python, ahorrando horas de trabajo manual.

---

### Fase 1 — Código Propio (≈10 minutos)

**Objetivo:** Crear 3 clones del objeto `"Personaje"` de la escena, dispuestos en fila, cada uno con una escala diferente y conservando el material del original.

**Requisitos:**
- El objeto original llamado `"Personaje"` ya existe en la escena (si no existe, créate un cubo simple con ese nombre como sustituto).
- Crear **3 clones** usando `bpy.ops.object.duplicate(linked=False)`.
- Separar los clones **3 unidades** entre sí en el eje X (el primero en X=3, el segundo en X=6, el tercero en X=9; el original permanece en su posición).
- Aplicar escalas: primer clon `0.8`, segundo clon `1.0`, tercer clon `1.2` (escala uniforme en XYZ).
- Nombrar los clones: `Personaje_Clon_1`, `Personaje_Clon_2`, `Personaje_Clon_3`.
- El material del original debe mantenerse en cada clon (con `linked=False`, el material se hereda automáticamente; verifica que así sea).

**Punto de partida:**
Escena con un objeto llamado `"Personaje"` (puede ser un cubo renombrado). Para seleccionar y duplicar un objeto específico por nombre:
```python
# Deseleccionar todo
bpy.ops.object.select_all(action='DESELECT')
# Seleccionar el objeto por nombre
bpy.data.objects["Personaje"].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects["Personaje"]
# Duplicar
bpy.ops.object.duplicate(linked=False)
# El clon ahora es el objeto activo
clon = bpy.context.active_object
```

**Pseudocódigo sugerido:**
```
importar bpy

escalas = [0.8, 1.0, 1.2]
posiciones_x = [3, 6, 9]

Para cada i del 0 al 2:
    deseleccionar todos los objetos
    seleccionar "Personaje" y hacerlo activo
    duplicar (linked=False)
    el clon = objeto activo
    mover clon a (posiciones_x[i], 0, 0)
    escalar clon uniformemente a escalas[i]
    renombrar clon como "Personaje_Clon_" + (i+1)
```

**Criterio de evaluación:**
- Se generan exactamente 3 clones, el original permanece intacto en su posición.
- Cada clon está en la posición X correcta (3, 6, 9).
- Cada clon tiene la escala correcta y visualmente se nota la diferencia de tamaño.
- Los nombres aparecen correctamente en el Outliner.
- Los clones comparten o heredan el material del original.

**Pista:** Para mover el objeto activo a una posición absoluta, usa `clon.location = (x, y, z)`. Para escalar uniformemente, usa `clon.scale = (s, s, s)`.

---

### Fase 2 — Con Asistencia de IA

**Descripción del reto extendido:**

Ahora debes crear una **galería completa** con `N × M` clones del `"Personaje"` dispuestos en una cuadrícula (grid), donde `N` es el número de filas y `M` el número de columnas. Cada clon debe tener una **variación aleatoria ligera** en su escala, rotación y posición (un pequeño desplazamiento aleatorio respecto a su posición en la cuadrícula), para que la galería se vea orgánica y no robótica. Además, cada clon debe recibir un **nombre único automático** que incluya su fila y columna (ej. `Personaje_F2_C3`), y opcionalmente un color de material único generado aleatoriamente o basado en su posición en la cuadrícula.

Para describir esto a una IA necesitarás saber: cómo funciona el módulo `random` de Python, qué significa "variación" en términos de transformaciones 3D en Blender, cómo estructurar un doble bucle (filas × columnas), y cómo nombrar objetos dinámicamente con `f-strings` o concatenación.

**Lo que debes lograr:**
- Parámetros configurables: `N_FILAS`, `N_COLUMNAS`, `SEPARACION`, `VARIACION_MAX`.
- Cada clon se posiciona en su celda de la cuadrícula más un desplazamiento aleatorio de hasta `±VARIACION_MAX` en X, Y y Z.
- Escala aleatoria por clon en el rango `[0.8, 1.3]`.
- Rotación aleatoria en el eje Z entre `-15°` y `+15°` (en radianes en Blender).
- Nombre único por clon siguiendo el patrón `Personaje_F{fila}_C{col}`.
- Opcional (+puntos): material con color único por clon usando `bpy.data.materials`.
- El objeto original `"Personaje"` no se mueve ni modifica.

**Criterio de evaluación de la Fase 2:**
- El script genera una cuadrícula correcta de `N × M` clones para valores de prueba como `3×4` y `5×5`.
- Las variaciones aleatorias son visibles pero no tan grandes que destruyan la forma de cuadrícula.
- El estudiante puede ajustar `VARIACION_MAX` y `SEPARACION` para cambiar el aspecto de la galería.
- Cada clon tiene un nombre único y correcto en el Outliner.
- El estudiante puede explicar por qué se usa `math.radians()` para convertir los ángulos.
- El estudiante puede describir con sus propias palabras cómo funciona el doble bucle anidado.

**Reflexión (entregar junto al código):**
1. ¿Cómo le explicaste a la IA el concepto de "variación aleatoria" para que generara código útil? ¿Usaste terminología técnica de Blender o de Python? ¿Qué funcionó mejor?
2. Después de ver el resultado, ¿la galería se ve como esperabas? Describe un ajuste que hiciste al código de la IA (o que harías) para mejorar el resultado visual y explica por qué ese ajuste funciona.

---

> **Nota de entrega:** Para cada desafío, entrega: (1) el archivo `.py` con tu código de la Fase 1, (2) el archivo `.py` con el código de la Fase 2 (indicando qué partes generó la IA y qué modificaste tú), (3) una captura de pantalla del resultado en Blender, y (4) las respuestas escritas a las preguntas de reflexión.
