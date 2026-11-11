# DAG240 — Examen: Lectura y Comprensión de Código Python en Blender
**30 Preguntas | Distribución: 10 Fácil · 12 Intermedio · 8 Difícil**

> **Instrucciones:** Lee cada fragmento de código con atención. Las preguntas evalúan tu comprensión de lo que hace el código, no si puedes copiarlo. Algunas preguntas tienen trampas sutiles — ¡analiza bien antes de responder!

---

## Q1. Acceso a un objeto por nombre — Fácil — Tipo: Lectura de Código

¿Qué hace la siguiente línea de código en Blender?

```python
domino = bpy.data.objects["Cube"]
```

A) Crea un nuevo objeto llamado "Cube" en la escena  
B) Busca y obtiene una referencia al objeto llamado "Cube" que ya existe en la escena  
C) Selecciona el objeto "Cube" en la escena  
D) Elimina el objeto "Cube" de la escena  

**Respuesta correcta: B**

**Explicación:** `bpy.data.objects["Cube"]` accede al diccionario de objetos de Blender y retorna una referencia (un puntero) al objeto cuyo nombre es "Cube". No crea, no selecciona ni elimina — simplemente obtiene acceso a ese objeto para poder usarlo después en el código. Si el objeto no existe, Blender lanzará un `KeyError`.

---

## Q2. Cambiar la posición de un objeto — Fácil — Tipo: Lectura de Código

¿Qué efecto tiene este código sobre el objeto `agujereador`?

```python
agujereador.location = (0.3, 0, -1.5)
```

A) Mueve el objeto 0.3 unidades en X, 0 en Y y -1.5 en Z **de forma relativa** a su posición actual  
B) Mueve el objeto a la posición absoluta X=0.3, Y=0, Z=-1.5 en el espacio de la escena  
C) Escala el objeto por los valores dados  
D) Rota el objeto usando los valores dados como ángulos en grados  

**Respuesta correcta: B**

**Explicación:** Asignar directamente a `.location` establece la **posición absoluta** del objeto en el espacio 3D de la escena. No es un desplazamiento relativo — si el objeto estaba en (5, 5, 5), después de esta línea estará exactamente en (0.3, 0, -1.5). Para moverse de forma relativa habría que sumar: `agujereador.location.x += 0.3`.

---

## Q3. Número aleatorio con `random.randrange` — Fácil — Tipo: Predicción

¿Cuáles son los posibles valores que puede generar la siguiente línea?

```python
x = random.randrange(-8, 8)
```

A) Números del -8 al 8, incluyendo ambos extremos  
B) Números del -8 al 7, incluyendo -8 pero **excluyendo** el 8  
C) Números del -7 al 8, excluyendo -8 pero incluyendo el 8  
D) Solo números positivos del 0 al 8  

**Respuesta correcta: B**

**Explicación:** `random.randrange(inicio, fin)` genera un entero desde `inicio` hasta `fin - 1`. El valor final **no está incluido**. Entonces `randrange(-8, 8)` puede generar -8, -7, -6, ..., 6, 7 — pero nunca el 8. Esto es idéntico al comportamiento de `range()` en Python.

---

## Q4. Deseleccionar todos los objetos — Fácil — Tipo: Lectura de Código

¿Cuál es el propósito de esta línea en el contexto del script del dominó?

```python
bpy.ops.object.select_all(action='DESELECT')
```

A) Elimina todos los objetos de la escena  
B) Oculta todos los objetos en el viewport  
C) Quita la selección de todos los objetos, dejando la escena sin nada seleccionado  
D) Selecciona todos los objetos de la escena  

**Respuesta correcta: C**

**Explicación:** `select_all(action='DESELECT')` recorre todos los objetos visibles y les quita el estado de selección. Esto es necesario antes de seleccionar manualmente objetos específicos, para asegurarse de que las operaciones posteriores (como aplicar un modificador) solo afecten al objeto deseado y no a todos los que estuvieran seleccionados previamente.

---

## Q5. Seleccionar y activar un objeto — Fácil — Tipo: Lectura de Código

Observa estas dos líneas:

```python
domino.select_set(True)
bpy.context.view_layer.objects.active = domino
```

¿Cuál es la diferencia entre "seleccionar" y "activar" un objeto?

A) Son exactamente lo mismo; ambas líneas hacen lo mismo  
B) `select_set(True)` lo marca como seleccionado (borde naranja), mientras que `.active` lo convierte en el objeto activo (borde amarillo brillante) sobre el que actúan los operadores  
C) Solo `.active` es necesario; `select_set` es obsoleto en versiones modernas  
D) `select_set` selecciona el objeto en la escena, y `.active` lo selecciona en el outliner  

**Respuesta correcta: B**

**Explicación:** En Blender, puedes tener varios objetos seleccionados, pero solo uno puede ser el **activo**. Los operadores como `modifier_apply` trabajan sobre el objeto activo. `select_set(True)` marca el objeto con el borde de selección, y `objects.active` define cuál es el activo. Muchos operadores requieren ambas condiciones para funcionar correctamente.

---

## Q6. Escala de un objeto — Fácil — Tipo: Lectura de Código

¿Qué hace este código?

```python
obj = bpy.data.objects["Cube"]
obj.scale = (2, 1, 3)
```

A) Mueve el cubo a las coordenadas (2, 1, 3)  
B) Escala el cubo: el doble en X, sin cambio en Y, el triple en Z  
C) Escala el cubo uniformemente por un factor de (2+1+3)/3 = 2  
D) Rota el cubo 2° en X, 1° en Y y 3° en Z  

**Respuesta correcta: B**

**Explicación:** `.scale` acepta una tupla `(x, y, z)` donde cada valor es un multiplicador. `scale = (2, 1, 3)` hace el cubo dos veces más ancho en X, mantiene su tamaño en Y (factor 1 = sin cambio) y lo hace tres veces más alto en Z. No tiene ningún efecto sobre la posición ni la rotación.

---

## Q7. Bucle para crear múltiples cubos — Fácil — Tipo: Predicción

¿Cuántos cubos creará el siguiente bucle?

```python
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(location=(i * 2, 0, 0))
```

A) 4 cubos  
B) 5 cubos  
C) 6 cubos  
D) Ninguno — `primitive_cube_add` necesita un tamaño obligatorio  

**Respuesta correcta: B**

**Explicación:** `range(5)` genera los valores 0, 1, 2, 3, 4 — exactamente 5 iteraciones. En cada iteración se crea un cubo en posiciones X = 0, 2, 4, 6, 8. El parámetro `location` en `primitive_cube_add` es opcional; si no se da, el cubo aparece en el origen. Entonces el resultado son **5 cubos** distribuidos a lo largo del eje X.

---

## Q8. Rotación con radianes — Fácil — Tipo: Lectura de Código

¿Qué hace este fragmento de código? ¿A cuántos grados equivale?

```python
import math
obj.rotation_euler = (0, 0, math.radians(90))
```

A) Rota el objeto 90 radianes en Z, lo cual equivale aproximadamente a 5157°  
B) Rota el objeto 90° en el eje Z usando la representación en radianes (π/2)  
C) Rota el objeto 1.57° en Z, porque `math.radians(90)` retorna aproximadamente 1.57  
D) Establece la rotación en grados directamente, sin conversión  

**Respuesta correcta: B**

**Explicación:** Blender almacena la rotación en **radianes**, no en grados. `math.radians(90)` convierte 90° a su equivalente en radianes, que es π/2 ≈ 1.5708. Entonces el código rota el objeto exactamente 90° alrededor del eje Z. Si escribieras `rotation_euler = (0, 0, 90)` sin convertir, el objeto giraría ~5157°, que es incorrecto.

---

## Q9. Modificador Boolean — tipo de operación — Fácil — Tipo: Verdadero/Falso

**Afirmación:** En el script del dominó, si cambias `'DIFFERENCE'` por `'UNION'`, el cilindro se **restará** del cubo en lugar de unirse a él.

**Respuesta correcta:** Falso

**Explicación:** Es exactamente al revés. La operación `'DIFFERENCE'` **resta** la forma del objeto herramienta (el cilindro) del objeto base (el dominó), creando un hueco. La operación `'UNION'` **combina** ambas formas en una sola malla fusionada. Para hacer agujeros en el dominó, se necesita `'DIFFERENCE'`.

---

## Q10. Referencia al objeto activo — Fácil — Tipo: Lectura de Código

¿Qué objeto modifican estas líneas del script del dominó?

```python
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = agujereador
```

A) Modifican el objeto `agujereador` (el cilindro)  
B) Modifican todos los objetos seleccionados en la escena  
C) Modifican el objeto activo, que en este caso es `domino` (el cubo)  
D) Crean un nuevo objeto vacío con el modificador  

**Respuesta correcta: C**

**Explicación:** `bpy.context.object` siempre hace referencia al **objeto activo** en el momento de la ejecución. En el script del dominó, justo antes de estas líneas se ejecuta `bpy.context.view_layer.objects.active = domino`, así que el objeto activo es `domino`. Por eso el modificador Boolean se agrega y configura sobre el cubo (dominó), no sobre el cilindro.

---

## Q11. Error en el script del dominó — Intermedio — Tipo: Error

El siguiente código intenta hacer un agujero en el dominó, pero tiene un **error en una línea**. ¿Cuál es?

```python
import bpy
import random

domino = bpy.data.objects["Cube"]
agujereador = bpy.data.objects["Cylinder"]

x = random.randrange(-8, 8) / 10
z = random.randrange(-18, 18) / 10

agujereador.location = (x, 0, z)

bpy.ops.object.select_all(action='DESELECT')
domino.select_set(True)
bpy.context.view_layer.objects.active = agujereador   # línea A

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = agujereador
bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
bpy.ops.object.modifier_apply(modifier="Boolean")
```

A) `agujereador.location = (x, 0, z)` — debería ser `(0, x, z)`  
B) `bpy.ops.object.select_all(action='DESELECT')` — debería ser `action='SELECT'`  
C) `bpy.context.view_layer.objects.active = agujereador` — debería ser `= domino`  
D) `operation = 'DIFFERENCE'` — debería ser `operation = 'SUBTRACT'`  

**Respuesta correcta: C**

**Explicación:** El error está en la **línea A**. Se selecciona `domino` con `select_set(True)`, pero luego se establece `agujereador` como el objeto **activo**. Esto es una contradicción: el modificador Boolean se agrega al objeto activo (el cilindro), no al dominó. El modificador debe agregarse al cubo, así que la línea correcta es `bpy.context.view_layer.objects.active = domino`. El valor `'DIFFERENCE'` es correcto y `'SUBTRACT'` no existe como operación válida.

---

## Q12. Bucle anidado — grilla de cubos — Intermedio — Tipo: Predicción

¿Cuántos cubos crea el siguiente código y en qué disposición quedan?

```python
for fila in range(4):
    for columna in range(3):
        bpy.ops.mesh.primitive_cube_add(
            location=(columna * 2, fila * 2, 0)
        )
```

A) 7 cubos en una línea recta  
B) 12 cubos en una grilla de 4 filas × 3 columnas  
C) 12 cubos en una grilla de 3 filas × 4 columnas  
D) 4 cubos en una grilla de 2×2  

**Respuesta correcta: B**

**Explicación:** El bucle externo (`fila`) itera 4 veces (0, 1, 2, 3) y el interno (`columna`) itera 3 veces (0, 1, 2). En total: 4 × 3 = **12 cubos**. La variable `fila` controla la posición en Y y `columna` en X. Resultado: una grilla de **4 filas en Y** y **3 columnas en X**. Si la pregunta dijera "3 filas × 4 columnas", los ejes estarían intercambiados — pero la cantidad de cubos sería la misma.

---

## Q13. Duplicate vs Linked Duplicate — Intermedio — Tipo: Lectura de Código

¿Cuál es la diferencia entre estas dos operaciones?

```python
# Opción A
bpy.ops.object.duplicate(linked=False)

# Opción B
bpy.ops.object.duplicate(linked=True)
```

A) No hay diferencia; ambas crean copias independientes  
B) `linked=False` crea una copia con su propia malla independiente; `linked=True` crea una copia que comparte la misma malla (linked duplicate / instancia)  
C) `linked=True` duplica también los modificadores; `linked=False` no  
D) `linked=True` es para duplicar materiales; `linked=False` es para duplicar geometría  

**Respuesta correcta: B**

**Explicación:** Con `linked=False` (equivalente a Shift+D), cada copia tiene su **propia malla independiente** — editar una no afecta a las demás. Con `linked=True` (equivalente a Alt+D), las copias **comparten datos de malla**: editar la geometría de una afecta a todas. Las linked duplicates son útiles para crear muchas instancias del mismo objeto ahorrando memoria, como piezas de dominó repetidas.

---

## Q14. Modificar solo el eje X de la posición — Intermedio — Tipo: Lectura de Código

¿Cuál es la diferencia entre estas dos formas de mover un objeto?

```python
# Forma 1
obj.location = (5, 0, 0)

# Forma 2
obj.location.x = 5
```

A) Son equivalentes; ambas producen exactamente el mismo resultado  
B) La Forma 1 mueve el objeto a X=5, Y=0, Z=0; la Forma 2 solo cambia X=5, conservando los valores actuales de Y y Z  
C) La Forma 2 es incorrecta; no se puede acceder a `.location.x` directamente  
D) La Forma 1 mueve el objeto de forma relativa; la Forma 2 lo mueve de forma absoluta  

**Respuesta correcta: B**

**Explicación:** Esta es una distinción importante. `obj.location = (5, 0, 0)` **reemplaza** toda la tupla de ubicación, forzando Y=0 y Z=0 sin importar dónde estuviera el objeto. En cambio, `obj.location.x = 5` **solo modifica** la componente X, dejando Y y Z intactos. Si el objeto estaba en (1, 3, 2), después de la Forma 2 estará en (5, 3, 2).

---

## Q15. Aplicar material a un objeto — Intermedio — Tipo: Completar

Completa el código para asignar un material ya existente llamado `"Material.001"` al objeto `cubo`:

```python
cubo = bpy.data.objects["Cube"]
material = bpy.data.materials["Material.001"]

if cubo.data.material_slots:
    cubo.data.material_slots[0].material = material
else:
    _____________________________
```

**Respuesta correcta:** `cubo.data.materials.append(material)`

**Explicación:** Antes de asignar un material, se verifica si el objeto ya tiene slots de material. Si los tiene, se puede asignar directamente al slot 0. Si **no** tiene slots (la condición `else`), se debe usar `.append()` para agregar el material al objeto. Intentar acceder a `material_slots[0]` en un objeto sin slots causaría un `IndexError`.

---

## Q16. Trampa: `select_all` con acción incorrecta — Intermedio — Tipo: Error

Un estudiante quiere eliminar todos los objetos de la escena con este código. ¿Funciona correctamente?

```python
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
```

A) Sí, funciona perfectamente  
B) No, porque `delete()` necesita que el objeto esté activo, no solo seleccionado  
C) Sí funciona, pero también eliminaría la cámara y la luz de la escena  
D) No, porque `action='SELECT'` no existe; debería ser `action='ALL'`  

**Respuesta correcta: C**

**Explicación:** El código **sí funciona** técnicamente — `select_all(action='SELECT')` selecciona **todos** los objetos visibles en la escena, incluyendo la cámara, luces, y cualquier otro objeto auxiliar, y luego `delete()` los elimina todos. La trampa aquí es que el código no produce un error, pero su efecto puede ser no deseado si el estudiante solo quería eliminar los objetos de geometría. La opción D es incorrecta: `action='SELECT'` sí es válido.

---

## Q17. Trampa: Nombre de modificador incorrecto — Intermedio — Tipo: Error

El siguiente código intenta aplicar el modificador Boolean pero falla en la última línea. ¿Por qué?

```python
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = agujereador
bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
bpy.ops.object.modifier_apply(modifier="Booleano")
```

A) `operation = 'DIFFERENCE'` no es válido; debería ser `'SUBTRACT'`  
B) `modifier_apply` recibe el nombre del modificador como aparece en Blender, que es `"Boolean"`, no `"Booleano"`  
C) Falta llamar a `bpy.ops.object.update()` antes de aplicar el modificador  
D) El modificador debe aplicarse con `modifier_apply(type='BOOLEAN')`  

**Respuesta correcta: B**

**Explicación:** Blender nombra el modificador automáticamente como `"Boolean"` (en inglés) cuando se usa `modifier_add(type='BOOLEAN')`. La función `modifier_apply` requiere el **nombre exacto** del modificador tal como aparece en la interfaz/datos. Escribir `"Booleano"` (en español) causará que Blender no encuentre ningún modificador con ese nombre y lanzará un error. Siempre se debe usar el nombre que Blender asignó internamente.

---

## Q18. Rango de posición aleatoria en el dominó — Intermedio — Tipo: Predicción

En el script del dominó, el agujero se posiciona así:

```python
x = random.randrange(-8, 8) / 10
z = random.randrange(-18, 18) / 10
```

¿Cuáles son los valores mínimo y máximo posibles para `x` y `z` respectivamente?

A) x: [-0.8, 0.8], z: [-1.8, 1.8]  
B) x: [-0.8, 0.7], z: [-1.8, 1.7]  
C) x: [-0.7, 0.8], z: [-1.7, 1.8]  
D) x: [-8, 8], z: [-18, 18]  

**Respuesta correcta: B**

**Explicación:** Recordando que `randrange(a, b)` excluye el límite superior: `randrange(-8, 8)` genera de -8 a 7, y al dividir entre 10 da de **-0.8 a 0.7**. De igual forma, `randrange(-18, 18)` genera de -18 a 17, y al dividir da de **-1.8 a 1.7**. La opción A es una trampa común — asume que el 8 y el 18 están incluidos, lo cual es incorrecto.

---

## Q19. Bucle con índice y posición — Intermedio — Tipo: Lectura de Código

¿Qué posiciones en X tendrán los cubos creados por este código?

```python
for i in range(1, 6):
    bpy.ops.mesh.primitive_cube_add(location=(i * 1.5, 0, 0))
```

A) X = 0, 1.5, 3.0, 4.5, 6.0  
B) X = 1.5, 3.0, 4.5, 6.0, 7.5  
C) X = 1, 2, 3, 4, 5  
D) X = 0, 1, 2, 3, 4  

**Respuesta correcta: B**

**Explicación:** `range(1, 6)` genera los valores 1, 2, 3, 4, 5 (empieza en 1, no en 0). Al multiplicar por 1.5: 1×1.5=1.5, 2×1.5=3.0, 3×1.5=4.5, 4×1.5=6.0, 5×1.5=7.5. La trampa es que `range(5)` empieza en 0, pero `range(1, 6)` empieza en 1 — un detalle que cambia todos los valores.

---

## Q20. Verdadero/Falso: Mover el agujereador mueve el agujero — Intermedio — Tipo: Verdadero/Falso

**Afirmación:** En el script del dominó, después de aplicar el modificador Boolean con `modifier_apply`, si mueves el objeto `agujereador` (el cilindro) a otra posición, el agujero en el dominó también se moverá.

**Respuesta correcta:** Falso

**Explicación:** Una vez que se llama a `modifier_apply`, el modificador Boolean se **aplica de forma permanente** a la malla del dominó. El agujero queda "grabado" en la geometría del cubo. Desde ese momento, mover el cilindro no tiene ningún efecto sobre el dominó. Antes de aplicar el modificador (si solo está agregado pero no aplicado), mover el cilindro sí afectaría la forma del agujero en tiempo real.

---

## Q21. Trampa: `bpy.context.object` sin objeto activo — Intermedio — Tipo: Error

¿Qué problema tiene el siguiente código?

```python
import bpy

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.modifier_add(type='BOOLEAN')
```

A) `select_all` y `modifier_add` no pueden usarse en la misma sesión  
B) No hay problema; el código funciona correctamente  
C) Después de deseleccionar todo, no hay objeto activo, por lo que `modifier_add` fallará o actuará sobre un contexto vacío  
D) `modifier_add` requiere que primero se llame a `bpy.ops.object.mode_set(mode='EDIT')`  

**Respuesta correcta: C**

**Explicación:** `bpy.ops.object.select_all(action='DESELECT')` quita la selección de todos los objetos. Dependiendo de la versión de Blender y el contexto, esto puede dejar sin objeto activo (`bpy.context.object` puede ser `None`). Al intentar `modifier_add`, Blender necesita un objeto activo para agregarle el modificador — sin uno, el operador lanzará un error de contexto. Siempre se debe establecer el objeto activo antes de usar operadores que lo requieren.

---

## Q22. Trampa: operación Boolean incorrecta — Intermedio — Tipo: Error

¿Cuál es el error en el siguiente fragmento del script del dominó?

```python
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = agujereador
bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
bpy.ops.object.modifier_apply(modifier="Boolean")
```

A) `'INTERSECT'` no es una operación válida de Boolean en Blender  
B) No hay error técnico, pero si el objetivo es hacer un agujero, se debería usar `'DIFFERENCE'` en lugar de `'INTERSECT'`  
C) Falta la línea `bpy.context.object.modifiers["Boolean"].solver = 'FAST'`  
D) El modificador debería aplicarse antes de configurar su operación  

**Respuesta correcta: B**

**Explicación:** `'INTERSECT'` **es** una operación válida en Blender — no hay error de sintaxis. Pero su efecto es completamente diferente: en lugar de restar el cilindro del cubo, conserva **solo la parte donde ambos objetos se superponen**. Para crear agujeros en el dominó, la operación correcta es `'DIFFERENCE'`. Esta es una trampa conceptual: el código ejecuta sin errores, pero no produce el resultado esperado.

---

## Q23. Escala no uniforme y Boolean — Difícil — Tipo: Lectura de Código

Un estudiante quiere crear agujeros circulares perfectos en el dominó. Tiene este código:

```python
agujereador = bpy.data.objects["Cylinder"]
agujereador.scale = (2, 2, 1)
agujereador.location = (0, 0, 0)

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = agujereador
bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
bpy.ops.object.modifier_apply(modifier="Boolean")
```

¿Qué problema podría ocurrir con esta escala no uniforme al aplicar el Boolean?

A) Ninguno; la escala no afecta a las operaciones Boolean  
B) El Boolean puede fallar o dar resultados incorrectos si la escala del objeto no ha sido aplicada (`Ctrl+A` / Apply Scale), porque Blender opera sobre la geometría real, no sobre la transformación visual  
C) El cilindro se volverá invisible antes del Boolean  
D) El Boolean solo funciona si la escala es `(1, 1, 1)`  

**Respuesta correcta: B**

**Explicación:** Esta es una situación real y común en Blender. Cuando escalas un objeto en Python con `.scale`, estás cambiando la **transformación del objeto**, no la geometría real de la malla. El modificador Boolean opera sobre las mallas reales. Si la escala no está aplicada, el Boolean puede producir resultados inesperados o incorrectos. La solución es aplicar la escala antes del Boolean: `bpy.ops.object.transform_apply(scale=True)`. Esto "hornea" la transformación en la geometría.

---

## Q24. Script completo del dominó — múltiples agujeros — Difícil — Tipo: Completar

Completa el código para hacer **5 agujeros aleatorios** en el dominó usando un bucle:

```python
import bpy
import random

domino = bpy.data.objects["Cube"]
agujereador = bpy.data.objects["Cylinder"]

for _ in range(_____):                          # línea A
    x = random.randrange(-8, 8) / 10
    z = random.randrange(-18, 18) / 10
    agujereador.location = (x, 0, z)

    bpy.ops.object.select_all(action='DESELECT')
    domino.select_set(True)
    bpy.context.view_layer.objects.active = domino

    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = agujereador
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(modifier=_____) # línea B
```

**Respuesta correcta:**  
- Línea A: `5`  
- Línea B: `"Boolean"`

**Explicación:** Para crear 5 agujeros, el bucle debe iterar 5 veces: `range(5)`. Se usa `_` como variable de bucle porque su valor no se utiliza dentro del cuerpo (es una convención en Python). En la línea B, `modifier_apply` necesita el nombre exacto del modificador como string: `"Boolean"` — así es como Blender nombra automáticamente el primer modificador Boolean creado.

---

## Q25. Trampa: Crear objetos fuera del bucle — Difícil — Tipo: Error

El siguiente código intenta crear 4 cubos en diferentes posiciones pero tiene un error lógico. ¿Cuál es?

```python
import bpy

posiciones = [(0,0,0), (3,0,0), (6,0,0), (9,0,0)]

bpy.ops.mesh.primitive_cube_add()
cubo = bpy.context.active_object

for pos in posiciones:
    cubo.location = pos
```

A) `primitive_cube_add` debería estar dentro del bucle para crear 4 cubos distintos  
B) No hay ningún error; el código crea 4 cubos correctamente  
C) `bpy.context.active_object` no funciona para obtener el cubo recién creado  
D) `cubo.location = pos` es incorrecto; debería ser `cubo.location = list(pos)`  

**Respuesta correcta: A**

**Explicación:** El código solo crea **un solo cubo** fuera del bucle, y luego lo mueve 4 veces a diferentes posiciones. Al final, el cubo queda en la última posición `(9, 0, 0)` — no hay 4 cubos. Para crear 4 cubos en 4 posiciones, `primitive_cube_add` debe estar **dentro** del bucle. Esta es una trampa de lógica: el código funciona sin errores, pero el resultado no es el esperado.

---

## Q26. Trampa: `randrange` vs `random.uniform` — Difícil — Tipo: Lectura de Código

¿Cuál es la diferencia entre estas dos versiones del script del dominó?

```python
# Versión A
x = random.randrange(-8, 8) / 10

# Versión B
x = random.uniform(-0.8, 0.8)
```

A) No hay diferencia; ambas generan exactamente los mismos valores  
B) La Versión A genera solo valores enteros divididos entre 10 (como -0.8, -0.7, ..., 0.6, 0.7); la Versión B genera cualquier número decimal entre -0.8 y 0.8  
C) La Versión B es incorrecta; `random.uniform` no existe en Python  
D) La Versión A puede generar valores negativos; la Versión B solo positivos  

**Respuesta correcta: B**

**Explicación:** `random.randrange(-8, 8)` genera **enteros** (-8, -7, ..., 7) y al dividir entre 10 se obtienen múltiplos de 0.1 (valores discretos). `random.uniform(-0.8, 0.8)` genera **cualquier número de punto flotante** entre -0.8 y 0.8, con mucha más precisión y variedad. Para posicionamiento de agujeros, `uniform` da resultados más naturales y menos "cuadriculados". Ambas opciones son válidas, pero producen distribuciones distintas.

---

## Q27. Acceso a objeto inexistente — Difícil — Tipo: Predicción

¿Qué ocurrirá cuando se ejecute este código si no existe ningún objeto llamado "Domino" en la escena?

```python
import bpy

pieza = bpy.data.objects["Domino"]
pieza.location = (0, 0, 5)
print("Objeto movido exitosamente")
```

A) Blender crea automáticamente un objeto vacío llamado "Domino"  
B) El código falla en la primera línea con un `KeyError` y el resto del código nunca se ejecuta  
C) `pieza` se convierte en `None` y la segunda línea lanza un `AttributeError`  
D) El código ejecuta sin errores; Blender simplemente ignora las líneas que no puede completar  

**Respuesta correcta: B**

**Explicación:** Acceder a `bpy.data.objects["Domino"]` cuando ese objeto no existe lanza inmediatamente un `KeyError: 'bpy_prop_collection[key]: key "Domino" not found'`. La ejecución del script se detiene ahí — las líneas 2 y 3 nunca llegan a ejecutarse, y el `print` nunca aparece. Para evitar esto se puede verificar antes: `if "Domino" in bpy.data.objects:` o usar un bloque `try/except KeyError`.

---

## Q28. Script de dominó: orden de operaciones — Difícil — Tipo: Error

El siguiente código tiene el orden de operaciones incorrecto. ¿Qué pasaría al ejecutarlo?

```python
import bpy

domino = bpy.data.objects["Cube"]
agujereador = bpy.data.objects["Cylinder"]

bpy.ops.object.modifier_add(type='BOOLEAN')           # paso 1
bpy.context.object.modifiers["Boolean"].object = agujereador
bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'

bpy.ops.object.select_all(action='DESELECT')           # paso 2
domino.select_set(True)
bpy.context.view_layer.objects.active = domino

bpy.ops.object.modifier_apply(modifier="Boolean")     # paso 3
```

A) Funciona correctamente; el orden de las secciones no importa  
B) El modificador se agrega al objeto activo **antes** de que el dominó sea el objeto activo, por lo que podría agregarse al objeto activo en ese momento (que podría ser cualquier otro objeto) — y luego intentar aplicarlo al dominó que tiene un contexto inconsistente  
C) `modifier_apply` siempre falla si se llama después de `select_all`  
D) El código falla porque `select_all` borra los modificadores recién agregados  

**Respuesta correcta: B**

**Explicación:** El orden importa crucialmente. En el código correcto, primero se establece `domino` como el objeto activo, y **luego** se agrega el modificador (que se agrega al objeto activo). En este código alterado, el modificador se agrega al objeto activo del momento (que puede ser el cilindro u otro objeto). Después se cambia el objeto activo al dominó, pero el modificador ya está en el objeto equivocado. Al aplicar, el resultado es impredecible o erróneo.

---

## Q29. Generación procedural de dominó completo — Difícil — Tipo: Lectura de Código

¿Qué hace el siguiente código completo? Describe el resultado final en la escena.

```python
import bpy
import random
import math

for i in range(7):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * 1.2, 0, 0)
    )
    pieza = bpy.context.active_object
    pieza.scale = (0.4, 0.8, 0.9)
    pieza.rotation_euler = (0, 0, math.radians(random.randrange(0, 360)))
```

A) Crea 7 cilindros en fila, cada uno con una rotación aleatoria en Z  
B) Crea 7 cubos en fila, cada uno escalado como una ficha de dominó rectangular y rotado aleatoriamente en Z  
C) Crea 7 cubos todos en la misma posición con escalas distintas  
D) Crea 1 cubo y lo mueve 7 veces a posiciones distintas  

**Respuesta correcta: B**

**Explicación:** El bucle itera 7 veces. En cada iteración: (1) crea un cubo separado en posición X = i×1.2 (0, 1.2, 2.4, 3.6, 4.8, 6.0, 7.2), (2) lo escala a proporciones rectangulares similares a una ficha de dominó (delgado en X, mediano en Y, alto en Z), y (3) lo rota un ángulo aleatorio en Z. El resultado es una **fila de 7 "fichas de dominó"** mal mezcladas (orientación caótica). `bpy.context.active_object` obtiene el cubo recién creado en cada iteración.

---

## Q30. Trampa maestra: Boolean sin objeto herramienta — Difícil — Tipo: Error

El siguiente código intenta hacer un agujero en el dominó. Parece correcto pero tiene un error muy sutil. ¿Cuál es?

```python
import bpy
import random

domino = bpy.data.objects["Cube"]

x = random.randrange(-8, 8) / 10
z = random.randrange(-18, 18) / 10

bpy.ops.object.select_all(action='DESELECT')
domino.select_set(True)
bpy.context.view_layer.objects.active = domino

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
bpy.ops.object.modifier_apply(modifier="Boolean")
```

A) `random.randrange` debería ser `random.uniform` para valores decimales  
B) El modificador Boolean nunca recibe un objeto herramienta (falta `modifiers["Boolean"].object = ...`), por lo que el Boolean no tiene qué restar  
C) Falta `agujereador.location = (x, 0, z)` después de crear las variables `x` y `z`  
D) Tanto B como C son errores en este código  

**Respuesta correcta: D**

**Explicación:** Este código tiene **dos errores**: (1) Nunca se obtiene ni se referencia el objeto `agujereador` — las variables `x` y `z` se calculan pero nunca se usan. (2) La línea `bpy.context.object.modifiers["Boolean"].object = agujereador` está completamente ausente, así que el Boolean no sabe qué forma usar para restar. Un modificador Boolean sin objeto herramienta asignado no puede aplicarse correctamente. Blender puede lanzar un error o simplemente no hacer ningún cambio visible. Esta pregunta prueba si el estudiante lee el código con atención y nota **lo que falta**, no solo lo que está mal escrito.

---

*Fin del examen — DAG240 | Blender Python Scripting*
