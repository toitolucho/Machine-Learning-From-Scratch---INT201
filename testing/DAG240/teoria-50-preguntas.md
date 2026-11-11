# DAG240 — Scripting en Blender con Python
## Examen Teórico: 50 Preguntas de Opción Múltiple

> **Instrucciones:** Selecciona la única respuesta correcta para cada pregunta. Se permite el uso de IA para generar código, pero estas preguntas evalúan tu comprensión de los fundamentos del scripting en Blender.

---

## Q1. ¿Qué es `bpy`? — Fácil

¿Qué es el módulo `bpy` en Blender?

A) Una librería externa de Python que se instala con `pip install bpy`  
B) El módulo principal de Python que da acceso a la API interna de Blender desde scripts  
C) Un editor de texto integrado en Blender para escribir código HTML  
D) Un comando de la terminal para abrir archivos `.blend`

**Respuesta correcta: B**

**Explicación:** `bpy` (Blender Python) es el módulo que expone la API interna de Blender al intérprete de Python. No se instala con pip; ya viene incluido dentro del entorno Python de Blender. Permite manipular objetos, escenas, materiales y prácticamente todo lo que Blender gestiona internamente.

---

## Q2. Crear un cubo con código — Fácil

¿Cuál de las siguientes instrucciones crea un cubo en Blender mediante scripting?

A) `bpy.data.meshes.new("Cube")`  
B) `bpy.ops.mesh.primitive_cube_add()`  
C) `bpy.context.scene.add_cube()`  
D) `bpy.types.Mesh.cube()`

**Respuesta correcta: B**

**Explicación:** `bpy.ops.mesh.primitive_cube_add()` es el operador que agrega un cubo primitivo a la escena, equivalente a usar el menú Agregar → Malla → Cubo. `bpy.data.meshes.new()` crea únicamente los datos de malla sin añadir ningún objeto a la escena. Las otras opciones no existen en la API de Blender.

---

## Q3. Crear una esfera con código — Fácil

¿Qué operador se utiliza para agregar una esfera UV a la escena desde un script de Python?

A) `bpy.ops.mesh.primitive_sphere_add()`  
B) `bpy.ops.mesh.primitive_uv_sphere_add()`  
C) `bpy.ops.object.add_sphere()`  
D) `bpy.data.objects.new("Sphere")`

**Respuesta correcta: B**

**Explicación:** El operador correcto es `bpy.ops.mesh.primitive_uv_sphere_add()`. En Blender existen dos tipos de esferas: UV Sphere e Ico Sphere, y cada una tiene su propio operador. La opción A no existe. La opción D crea un objeto vacío sin geometría de esfera.

---

## Q4. La malla Suzanne — Fácil

¿Qué primitiva de malla representa "Suzanne" en Blender?

A) Una esfera de baja resolución  
B) Un toroide retorcido  
C) La cabeza de un mono, mascota oficial de Blender  
D) Un cilindro con tapa superior

**Respuesta correcta: C**

**Explicación:** Suzanne es la famosa cabeza de mono que sirve como mascota no oficial de Blender. Se usa frecuentemente como malla de prueba. Se crea con `bpy.ops.mesh.primitive_monkey_add()`. No es una esfera, ni un toroide, ni un cilindro.

---

## Q5. Agregar un cilindro — Fácil

¿Cómo se agrega un cilindro a la escena desde un script de Blender?

A) `bpy.ops.mesh.primitive_cylinder_add()`  
B) `bpy.ops.mesh.add(type='CYLINDER')`  
C) `bpy.data.meshes.cylinder_add()`  
D) `bpy.context.scene.objects.cylinder()`

**Respuesta correcta: A**

**Explicación:** Cada primitiva de malla en Blender tiene su propio operador con el patrón `bpy.ops.mesh.primitive_<nombre>_add()`. La opción B tiene una sintaxis inventada que no existe en la API. Las opciones C y D también son inexistentes en Blender.

---

## Q6. Propiedad de ubicación (location) — Fácil

Dado el siguiente código, ¿qué hace la línea resaltada?

```python
obj = bpy.context.active_object
obj.location = (3, 0, 0)
```

A) Mueve el origen del mundo al objeto  
B) Coloca el objeto en la posición X=3, Y=0, Z=0 en coordenadas globales  
C) Escala el objeto a lo largo del eje X por un factor de 3  
D) Rota el objeto 3 grados sobre el eje X

**Respuesta correcta: B**

**Explicación:** La propiedad `location` de un objeto en Blender es una tupla de tres valores (X, Y, Z) que define su posición en el espacio 3D. Asignar `(3, 0, 0)` ubica el objeto en X=3, Y=0, Z=0. No tiene relación con escala ni rotación, que tienen sus propias propiedades.

---

## Q7. Propiedad de escala — Fácil

¿Cuál de los siguientes códigos duplica el tamaño de un objeto en todos sus ejes?

A) `obj.scale = (2, 2, 2)`  
B) `obj.location = (2, 2, 2)`  
C) `obj.size = 2`  
D) `obj.dimensions = (2, 2, 2)`

**Respuesta correcta: A**

**Explicación:** La propiedad `scale` controla el factor de escala del objeto en cada eje (X, Y, Z). Un valor de `(2, 2, 2)` duplica el tamaño uniformemente. `location` controla la posición. `obj.size` no es una propiedad válida. `dimensions` existe pero devuelve dimensiones absolutas y no se usa para escalar directamente.

---

## Q8. Unidades de rotación en Blender — Fácil

Blender utiliza internamente ________ para representar los valores de rotación en scripts de Python.

A) Grados (°)  
B) Radianes (rad)  
C) Gradianes (grad)  
D) Revoluciones por minuto (RPM)

**Respuesta correcta: B**

**Explicación:** Aunque la interfaz de Blender puede mostrar grados al usuario, internamente la API de Python utiliza **radianes**. Esto significa que para rotar 90° debes usar `math.radians(90)` o el valor equivalente `1.5708`. Un error común es pasar grados directamente, lo que produce rotaciones incorrectas.

---

## Q9. Rotación con radianes — Fácil

¿Qué importación necesitas para convertir grados a radianes en Python?

A) `import bpy`  
B) `import degrees`  
C) `import math` y luego usar `math.radians()`  
D) No es necesario importar nada; Blender convierte automáticamente

**Respuesta correcta: C**

**Explicación:** La función `math.radians()` del módulo estándar de Python convierte grados a radianes. Se debe importar `math` explícitamente con `import math`. Blender **no** convierte automáticamente: si pasas grados sin convertir, la rotación será completamente diferente a la esperada.

---

## Q10. Referenciar un objeto por nombre — Fácil

¿Cómo se obtiene una referencia a un objeto llamado "Ficha" que ya existe en la escena?

A) `obj = bpy.context.scene.find("Ficha")`  
B) `obj = bpy.ops.object.get("Ficha")`  
C) `obj = bpy.data.objects["Ficha"]`  
D) `obj = bpy.context.active_object("Ficha")`

**Respuesta correcta: C**

**Explicación:** `bpy.data.objects` es un diccionario que contiene todos los objetos del archivo `.blend` y se accede por nombre con corchetes. Las opciones A y B usan métodos inexistentes. La opción D es incorrecta porque `active_object` es una propiedad, no una función.

---

## Q11. `bpy.ops` vs `bpy.data` — Fácil

¿Cuál es la diferencia principal entre `bpy.ops` y `bpy.data`?

A) `bpy.ops` es más rápido que `bpy.data` para leer propiedades  
B) `bpy.ops` ejecuta operadores (acciones), mientras que `bpy.data` accede directamente a los datos del archivo  
C) `bpy.data` solo funciona en modo Edición, `bpy.ops` solo en modo Objeto  
D) Son sinónimos; ambos hacen exactamente lo mismo

**Respuesta correcta: B**

**Explicación:** `bpy.ops` contiene operadores que simulan las acciones del usuario (como agregar objetos, aplicar modificadores). `bpy.data` permite acceso directo a los datos del archivo blend (objetos, mallas, materiales, etc.). Son complementarios y no sinónimos; cada uno tiene su uso apropiado.

---

## Q12. Seleccionar un objeto por código — Fácil

¿Qué propiedad de un objeto se establece en `True` para seleccionarlo desde un script?

A) `obj.active = True`  
B) `obj.select = True`  
C) `obj.select_set(True)`  
D) `bpy.ops.object.select(obj)`

**Respuesta correcta: C**

**Explicación:** En versiones modernas de Blender (2.80+), la selección se hace con el método `obj.select_set(True)`. La propiedad directa `obj.select` fue eliminada en Blender 2.80. `obj.active` no existe como propiedad booleana de selección. La opción D no es un operador válido.

---

## Q13. Objeto activo — Fácil

¿Cómo se establece un objeto como el **objeto activo** de la escena desde un script?

A) `bpy.context.active_object = obj`  
B) `bpy.context.view_layer.objects.active = obj`  
C) `obj.set_active(True)`  
D) `bpy.ops.object.set_active(obj)`

**Respuesta correcta: B**

**Explicación:** El objeto activo se establece asignando directamente a `bpy.context.view_layer.objects.active`. Esta es la forma correcta en Blender 2.80 y versiones posteriores. `bpy.context.active_object` es de solo lectura. Las otras opciones usan métodos o propiedades inexistentes.

---

## Q14. Nombrar objetos con código — Fácil

¿Cómo se le asigna el nombre "PiezaDomino" a un objeto en Blender mediante Python?

A) `bpy.data.objects.rename("PiezaDomino")`  
B) `obj.label = "PiezaDomino"`  
C) `obj.name = "PiezaDomino"`  
D) `bpy.context.scene.set_name(obj, "PiezaDomino")`

**Respuesta correcta: C**

**Explicación:** La propiedad `name` del objeto se puede asignar directamente como una cadena de texto. Es importante notar que si ya existe un objeto con ese nombre, Blender agregará automáticamente un sufijo numérico (ej. "PiezaDomino.001"). Las opciones A, B y D no existen en la API de Blender.

---

## Q15. Eliminar un objeto — Fácil

¿Qué operador se usa para eliminar el objeto activo seleccionado desde un script?

A) `bpy.data.objects.remove(obj)`  
B) `bpy.ops.object.delete()`  
C) `del bpy.context.active_object`  
D) `bpy.context.scene.objects.pop(obj)`

**Respuesta correcta: B**

**Explicación:** `bpy.ops.object.delete()` elimina los objetos actualmente seleccionados, igual que presionar la tecla Suprimir en la interfaz. También es válido `bpy.data.objects.remove(obj)` para un enfoque más directo, pero entre las opciones dadas, B es la correcta. La opción C con `del` no funciona para eliminar objetos de la escena.

---

## Q16. Qué es el pseudocódigo — Fácil

¿Qué es el pseudocódigo en programación?

A) Código Python que tiene errores de sintaxis  
B) Una descripción informal, en lenguaje natural estructurado, de los pasos de un algoritmo, sin seguir la sintaxis de ningún lenguaje  
C) Comentarios dentro de un script de Python precedidos por `#`  
D) Código que solo funciona dentro de Blender y no en otros entornos

**Respuesta correcta: B**

**Explicación:** El pseudocódigo es una representación de alto nivel de un algoritmo, escrita en lenguaje natural estructurado, que no sigue las reglas sintácticas de ningún lenguaje de programación específico. Sirve para planificar la lógica antes de escribir el código real. No es código con errores, ni comentarios de Python, ni código específico de Blender.

---

## Q17. Tuplas para propiedades — Fácil

¿Por qué se usan **tuplas** (y no listas) para asignar valores como `location`, `rotation` y `scale`?

A) Porque las listas no son compatibles con la API de Blender  
B) Las tuplas son más rápidas de escribir y ocupan menos memoria  
C) La API de Blender espera secuencias de longitud fija para estas propiedades; las tuplas comunican que son valores agrupados e inmutables  
D) Blender convierte internamente todo a enteros, y las tuplas lo permiten

**Respuesta correcta: C**

**Explicación:** Propiedades como `location`, `rotation_euler` y `scale` son vectores de longitud fija (3 componentes). Las tuplas son la forma idiomática de representar conjuntos de valores relacionados e inmutables en Python. Aunque Blender también acepta listas en la mayoría de los casos, las tuplas son la convención correcta. Las otras opciones contienen afirmaciones falsas.

---

## Q18. El cursor 3D y la ubicación de objetos — Fácil

¿Dónde aparece un nuevo objeto cuando se agrega con `bpy.ops.mesh.primitive_cube_add()` sin especificar `location`?

A) Siempre en el origen del mundo (0, 0, 0)  
B) En la posición actual del cursor 3D  
C) En la posición del objeto activo  
D) En el centro de la cámara activa

**Respuesta correcta: B**

**Explicación:** Por defecto, los operadores `primitive_*_add()` colocan el nuevo objeto en la posición del cursor 3D. Si el cursor está en el origen, el objeto aparece en (0, 0, 0). Para forzar una posición específica, se pasa el parámetro `location`, por ejemplo: `bpy.ops.mesh.primitive_cube_add(location=(1, 2, 3))`.

---

## Q19. For loop para crear objetos — Fácil

¿Qué hace el siguiente fragmento de código?

```python
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(location=(i * 2, 0, 0))
```

A) Crea 5 cubos en la misma posición (0, 0, 0)  
B) Crea 1 cubo y lo mueve 5 veces  
C) Crea 5 cubos separados cada 2 unidades sobre el eje X  
D) Genera un error porque `range` no es compatible con `bpy`

**Respuesta correcta: C**

**Explicación:** El bucle `for` itera con `i` tomando valores 0, 1, 2, 3, 4. En cada iteración se crea un nuevo cubo en la posición `(i*2, 0, 0)`, es decir, en X=0, X=2, X=4, X=6 y X=8. El módulo `range` es estándar de Python y funciona perfectamente dentro de scripts de Blender.

---

## Q20. Módulo random — Fácil

¿Para qué se utiliza el módulo `random` en scripts de Blender?

A) Para generar colores aleatorios directamente en materiales  
B) Para generar números o valores aleatorios, útiles para variar posiciones, escalas o rotaciones de objetos  
C) Para seleccionar objetos al azar de la escena automáticamente  
D) Es un módulo exclusivo de Blender para movimientos procedurales

**Respuesta correcta: B**

**Explicación:** `random` es un módulo estándar de Python (no exclusivo de Blender) que genera números aleatorios. En scripting de Blender se usa para variar propiedades como posición, escala o rotación, dando resultados procedurales interesantes. No genera colores directamente ni selecciona objetos; esas funciones serían escritas manualmente usando los valores que `random` produce.

---

## Q21. `random.randrange` vs `random.uniform` — Intermedio

¿Cuál es la diferencia entre `random.randrange(1, 10)` y `random.uniform(1.0, 10.0)`?

A) Son idénticos; ambos generan números decimales entre 1 y 10  
B) `randrange` genera un entero dentro del rango, `uniform` genera un número decimal (float) dentro del rango  
C) `randrange` es más preciso que `uniform` para valores pequeños  
D) `uniform` solo funciona con números negativos

**Respuesta correcta: B**

**Explicación:** `random.randrange(1, 10)` devuelve un número entero (ej: 3, 7, 9). `random.uniform(1.0, 10.0)` devuelve un número de punto flotante (ej: 3.47, 7.812). En Blender, para posiciones con precisión decimal se usa `uniform`, mientras que para índices o contadores se usa `randrange`. Las demás opciones son falsas.

---

## Q22. Duplicar un objeto — Intermedio

¿Cuál es la diferencia entre una **copia vinculada** (linked duplicate) y una **copia completa** (full copy) en Blender?

A) No hay diferencia; ambas crean objetos completamente independientes  
B) Una copia vinculada comparte los datos de malla con el original; cambiar la malla de uno afecta al otro. Una copia completa tiene datos independientes  
C) Una copia completa solo copia la posición, no la geometría  
D) La copia vinculada solo funciona con materiales, no con mallas

**Respuesta correcta: B**

**Explicación:** En Blender, una copia vinculada (`Alt+D` o `bpy.ops.object.duplicate(linked=True)`) comparte los mismos datos de malla (mesh data) entre el original y la copia. Si modificas la malla de uno en modo Edición, todos los vinculados cambian. Una copia completa (`Shift+D` o `linked=False`) crea datos de malla independientes. Esto es fundamental para instanciación eficiente.

---

## Q23. Aplicar un material a un objeto — Intermedio

¿Cuál es el proceso correcto para asignar un material existente llamado "Rojo" a un objeto mediante scripting?

A) `obj.material = bpy.data.materials["Rojo"]`  
B) `obj.data.materials.append(bpy.data.materials["Rojo"])`  
C) `bpy.ops.material.assign("Rojo", obj)`  
D) `obj.active_material = "Rojo"`

**Respuesta correcta: B**

**Explicación:** Los materiales de un objeto se gestionan a través de `obj.data.materials`, que es una lista de materiales asignados. Se usa `.append()` para agregar un material existente. La opción A usa una propiedad inexistente. La opción D asignaría una cadena de texto, no un objeto material. La opción C no existe en la API de Blender.

---

## Q24. Creación de un material nuevo — Intermedio

¿Qué hace el siguiente código?

```python
mat = bpy.data.materials.new(name="Azul")
mat.diffuse_color = (0, 0, 1, 1)
```

A) Aplica el material "Azul" al objeto activo automáticamente  
B) Crea un nuevo material llamado "Azul" con color azul y lo almacena en los datos, pero aún no está asignado a ningún objeto  
C) Cambia el color del fondo de la escena a azul  
D) Genera un error porque `diffuse_color` necesita valores entre 0 y 255

**Respuesta correcta: B**

**Explicación:** `bpy.data.materials.new()` crea el material y lo añade a los datos del archivo blend, pero **no** lo asigna automáticamente a ningún objeto. Hay que hacer ese paso por separado. El color `(0, 0, 1, 1)` es RGBA donde el último valor es el alfa (opacidad), y los valores van de 0 a 1, no de 0 a 255. El fondo de la escena no se ve afectado.

---

## Q25. Modificador booleano — concepto — Intermedio

¿Para qué sirve el modificador booleano (Boolean Modifier) en Blender?

A) Para aplicar operaciones lógicas (AND, OR) a las propiedades numéricas de objetos  
B) Para realizar operaciones geométricas entre dos mallas: unión, diferencia o intersección  
C) Para convertir un objeto en una malla booleana que solo tiene valores verdadero/falso  
D) Para activar o desactivar la visibilidad de objetos en la escena

**Respuesta correcta: B**

**Explicación:** El modificador booleano realiza operaciones de geometría computacional entre dos mallas: UNION (une ambas geometrías), DIFFERENCE (resta una malla de la otra) y INTERSECT (conserva solo la parte que se superpone). Es esencial para crear formas complejas, como los huecos (puntos) en una ficha de dominó.

---

## Q26. Boolean DIFFERENCE — Intermedio

En el contexto de crear una ficha de dominó con Python, ¿qué operación booleana se usa para "restar" los cilindros (puntos) del cuerpo de la ficha?

A) UNION  
B) INTERSECT  
C) DIFFERENCE  
D) SUBTRACT (no existe; es DIFFERENCE)

**Respuesta correcta: C**

**Explicación:** La operación DIFFERENCE resta la geometría de un objeto "cortador" del objeto base. Para hacer los huecos circulares (puntos) en una ficha de dominó, se crean cilindros en cada posición de punto y luego se aplica un modificador booleano con tipo DIFFERENCE sobre la ficha, usando cada cilindro como objeto cortador. El resultado es la ficha con los agujeros.

---

## Q27. Agregar un modificador booleano — Intermedio

¿Cuál es la sintaxis correcta para agregar un modificador booleano a un objeto en Blender mediante scripting?

A) `bpy.ops.object.modifier_add(type='BOOLEAN')`  
B) `obj.modifiers.boolean_add()`  
C) `bpy.data.modifiers.new(type='BOOLEAN')`  
D) `bpy.ops.modifier.add_boolean()`

**Respuesta correcta: A**

**Explicación:** `bpy.ops.object.modifier_add(type='BOOLEAN')` agrega el modificador al objeto activo, igual que hacerlo desde el panel de propiedades. Es importante que el objeto receptor sea el activo antes de llamar al operador. Las otras opciones usan sintaxis inventada que no existe en la API de Blender.

---

## Q28. Configurar el modificador booleano — Intermedio

Después de agregar un modificador booleano, ¿cómo se especifica el objeto que actuará como "cortador" (cutter)?

A) `bpy.ops.object.boolean_set_cutter(cutter_obj)`  
B) `mod.object = cutter_obj` donde `mod` es el modificador booleano  
C) `obj.boolean_cutter = cutter_obj`  
D) El cortador se especifica automáticamente como el último objeto creado

**Respuesta correcta: B**

**Explicación:** Después de agregar el modificador, se obtiene su referencia (ej. `mod = obj.modifiers[-1]` o por nombre) y se asigna el objeto cortador mediante `mod.object = cutter_obj`. También hay que configurar `mod.operation = 'DIFFERENCE'` u otro tipo. El cortador nunca se configura automáticamente; debe especificarse explícitamente.

---

## Q29. Acceso al objeto activo — Intermedio

¿Qué devuelve `bpy.context.active_object` si no hay ningún objeto activo en la escena?

A) El primer objeto de la escena  
B) Un objeto vacío (Empty) por defecto  
C) `None`  
D) Lanza una excepción `AttributeError`

**Respuesta correcta: C**

**Explicación:** Cuando no hay objeto activo, `bpy.context.active_object` devuelve `None`. Por eso es buena práctica verificar `if bpy.context.active_object is not None:` antes de acceder a sus propiedades, para evitar errores del tipo `AttributeError: 'NoneType' object has no attribute 'name'`.

---

## Q30. Deseleccionar todos los objetos — Intermedio

¿Cómo se desseleccionan todos los objetos de la escena desde un script?

A) `bpy.ops.object.deselect_all()`  
B) `bpy.context.scene.select_all(action='DESELECT')`  
C) `bpy.ops.object.select_all(action='DESELECT')`  
D) `for obj in bpy.data.objects: obj.selected = False`

**Respuesta correcta: C**

**Explicación:** El operador `bpy.ops.object.select_all(action='DESELECT')` desselecciona todos los objetos. También acepta `action='SELECT'`, `'TOGGLE'` o `'INVERT'`. La opción A usa un operador inexistente. La opción D usa la propiedad `selected` que no existe (es `select_set()`). La opción B tiene una sintaxis incorrecta.

---

## Q31. Posiciones en cuadrícula para dominó — Intermedio

Para colocar los puntos de una ficha de dominó en posiciones específicas, se usa una lista de coordenadas relativas. ¿Qué estructura de datos es más apropiada para almacenar estas posiciones?

A) Una variable entera que cuenta cuántos puntos hay  
B) Una lista de tuplas, donde cada tupla contiene las coordenadas (x, y) de cada punto  
C) Un diccionario con claves numéricas y valores de cadena de texto  
D) Una variable de tipo booleano para cada posición posible

**Respuesta correcta: B**

**Explicación:** Una lista de tuplas como `[(x1, y1), (x2, y2), ...]` es la estructura ideal para almacenar posiciones 2D de los puntos del dominó. Permite iterar fácilmente con un `for` para crear un cilindro en cada posición. Las otras estructuras (entero, diccionario de strings, booleanos) no representan adecuadamente coordenadas espaciales.

---

## Q32. Bucle con lista de posiciones — Intermedio

¿Qué produce el siguiente código en el contexto de una ficha de dominó?

```python
posiciones = [(0.3, 0.3), (-0.3, 0.3), (0, 0), (0.3, -0.3), (-0.3, -0.3)]
for x, y in posiciones:
    bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0.1))
```

A) Crea 5 fichas de dominó en posiciones diferentes  
B) Crea un solo cilindro y lo mueve 5 veces a la última posición  
C) Crea 5 cilindros, uno en cada posición definida en la lista  
D) Genera un error porque no se pueden desempaquetar tuplas en un `for`

**Respuesta correcta: C**

**Explicación:** El bucle `for x, y in posiciones` desempaqueta cada tupla de la lista en las variables `x` e `y`. En cada iteración se crea un nuevo cilindro en la posición correspondiente. Esta técnica de desempaquetado de tuplas en Python es completamente válida y muy usada en Blender scripting.

---

## Q33. Escala del cilindro para puntos de dominó — Intermedio

Al crear los cilindros que representan los puntos de una ficha de dominó, ¿por qué es importante ajustar su escala?

A) Porque por defecto los cilindros son invisibles y necesitan escala mayor a 0  
B) Para que el cilindro tenga el diámetro adecuado como punto del dominó y sea más profundo que la ficha para garantizar una buena operación booleana  
C) Porque la operación booleana solo funciona con objetos escalados uniformemente  
D) La escala no importa para operaciones booleanas; solo importa la posición

**Respuesta correcta: B**

**Explicación:** El tamaño del cilindro determina el tamaño del punto en la ficha. Además, para que la operación DIFFERENCE funcione correctamente, el cilindro debe penetrar completamente el cuerpo de la ficha (ser más profundo), de lo contrario el agujero puede quedar incompleto o no aplicarse. La opción C es falsa; los booleanos funcionan con cualquier escala.

---

## Q34. `bpy.ops` requiere contexto correcto — Intermedio

¿Por qué a veces `bpy.ops.object.modifier_apply()` lanza un error al ejecutarse en un script?

A) Porque los modificadores no se pueden aplicar desde Python, solo manualmente  
B) Porque el operador requiere que haya un objeto activo en modo Objeto, y el contexto puede no ser el correcto al ejecutar el script  
C) Porque `modifier_apply` fue eliminado en Blender 3.0  
D) Porque Python no puede comunicarse con el motor de modificadores de Blender

**Respuesta correcta: B**

**Explicación:** Los operadores de `bpy.ops` requieren un contexto válido (el modo correcto, un objeto activo seleccionado, etc.). Si el script no ha establecido correctamente el objeto activo o no está en Modo Objeto, el operador puede fallar con un error de contexto. Es una fuente común de errores en Blender scripting. Los modificadores sí se pueden aplicar desde Python.

---

## Q35. Pseudocódigo y código real — Intermedio

¿Cuál de los siguientes es un ejemplo correcto de **pseudocódigo** para colocar puntos en una ficha de dominó?

A) `for pos in positions: bpy.ops.mesh.primitive_cylinder_add(location=pos)`  
B) `PARA CADA posición EN lista_de_posiciones: Crear cilindro en esa posición`  
C) `# crear cilindros aquí`  
D) `import random; random.choice(positions)`

**Respuesta correcta: B**

**Explicación:** El pseudocódigo usa lenguaje natural estructurado, no sintaxis de ningún lenguaje. La opción B es pseudocódigo legible en español. La opción A es código Python real. La opción C es un comentario de Python, no pseudocódigo. La opción D es también código Python real, aunque fragmentado.

---

## Q36. Propiedad rotation_euler — Intermedio

¿Cuál es la diferencia entre `obj.rotation_euler` y `obj.rotation_quaternion`?

A) `rotation_euler` usa ángulos en grados; `rotation_quaternion` usa radianes  
B) `rotation_euler` representa la rotación como tres ángulos (X, Y, Z); `rotation_quaternion` usa cuatro componentes (w, x, y, z)  
C) `rotation_quaternion` es obsoleto y fue eliminado en Blender 2.8  
D) Son equivalentes; solo cambia el nombre de la propiedad

**Respuesta correcta: B**

**Explicación:** `rotation_euler` utiliza ángulos de Euler (tres valores en radianes: X, Y, Z), que son intuitivos pero pueden sufrir bloqueo de cardán (gimbal lock). `rotation_quaternion` usa cuatro componentes matemáticos que evitan ese problema. Para scripting básico se usa `rotation_euler`. El modo debe coincidir con `obj.rotation_mode`.

---

## Q37. Indexar `bpy.data.objects` — Intermedio

Si en la escena hay dos objetos llamados "Cubo" y se intenta crear un tercero con `obj.name = "Cubo"`, ¿qué ocurre?

A) Se genera un error y el script se detiene  
B) El tercer objeto reemplaza al primero llamado "Cubo"  
C) Blender asigna automáticamente el nombre "Cubo.002" al nuevo objeto  
D) Los tres objetos quedan con el mismo nombre "Cubo"

**Respuesta correcta: C**

**Explicación:** Blender garantiza nombres únicos para los objetos. Si ya existe "Cubo" y "Cubo.001", al intentar nombrar otro objeto "Cubo", Blender le asigna automáticamente "Cubo.002". Esto es importante saberlo al referenciar objetos por nombre, ya que el nombre que esperas puede no ser el que Blender asignó.

---

## Q38. Escala no uniforme — Intermedio

¿Qué produce el siguiente código?

```python
obj = bpy.context.active_object
obj.scale = (1, 1, 0.1)
```

A) Aplana el objeto a lo largo del eje Z, haciéndolo muy delgado  
B) Escala el objeto uniformemente a un 10% de su tamaño  
C) Genera un error porque la escala debe ser uniforme  
D) Mueve el objeto 0.1 unidades hacia abajo en Z

**Respuesta correcta: A**

**Explicación:** `scale = (1, 1, 0.1)` mantiene la escala original en X e Y (factor 1), pero comprime el objeto a solo el 10% de su altura original en Z. Esta es una escala no uniforme, perfectamente válida. El resultado visual es un objeto "aplanado", ideal para hacer fichas de dominó delgadas. No hay ningún error; Blender admite escalas no uniformes.

---

## Q39. Parámetro `location` en primitivos — Intermedio

¿Cuál es la ventaja de pasar el parámetro `location` directamente al operador vs. moverlo después?

```python
# Opción A
bpy.ops.mesh.primitive_cube_add(location=(3, 0, 0))

# Opción B
bpy.ops.mesh.primitive_cube_add()
bpy.context.active_object.location = (3, 0, 0)
```

A) La Opción A es incorrecta; `location` no es un parámetro válido del operador  
B) Ambas producen el mismo resultado; la Opción A es simplemente más concisa  
C) La Opción B es más rápida porque evita calcular la posición durante la creación  
D) La Opción A crea el objeto en el origen y luego lo teletransporta; la B no

**Respuesta correcta: B**

**Explicación:** Ambas opciones producen exactamente el mismo resultado: un cubo en la posición (3, 0, 0). La Opción A es simplemente más concisa y legible. La Opción B requiere dos líneas y una referencia adicional. `location` sí es un parámetro válido del operador. No hay diferencia de rendimiento significativa en scripts simples.

---

## Q40. Visibilidad de objetos cortadores en dominó — Intermedio

Al crear una ficha de dominó con booleanos, los cilindros cortadores generalmente se ocultan al final. ¿Cuál es la forma correcta de ocultar un objeto en la vista desde Python?

A) `obj.hide = True`  
B) `obj.visible = False`  
C) `obj.hide_viewport = True`  
D) `bpy.ops.object.hide(obj)`

**Respuesta correcta: C**

**Explicación:** En Blender 2.80 y versiones posteriores, `obj.hide_viewport = True` oculta el objeto en la vista 3D (equivalente al ícono del ojo en el Outliner). La propiedad `obj.hide` existía en versiones antiguas de Blender (pre-2.80) pero fue reemplazada. Las otras opciones son incorrectas o inexistentes.

---

## Q41. Profundidad de la operación booleana — Difícil

Al aplicar un modificador DIFFERENCE con un cilindro como cortador sobre una ficha de dominó, el agujero no aparece correctamente. ¿Cuál es la causa más probable?

A) El modificador booleano no funciona con cilindros, solo con cubos  
B) El cilindro cortador no penetra completamente la geometría de la ficha (no sobresale por ambas caras)  
C) Se debe usar UNION en lugar de DIFFERENCE para hacer agujeros  
D) La ficha debe estar en Modo Edición para que el booleano funcione

**Respuesta correcta: B**

**Explicación:** Para que una operación DIFFERENCE funcione correctamente, el objeto cortador debe penetrar completamente el volumen del objeto base, sobresaliendo por ambas caras. Si el cilindro no es suficientemente profundo (en Z) o no está posicionado para atravesar toda la ficha, el resultado puede ser incompleto o incorrecto. La solución es hacer el cilindro más alto que el grosor de la ficha.

---

## Q42. `bpy.ops` vs `bpy.data` — cuándo usar cada uno — Difícil

Un estudiante quiere cambiar el nombre de un material de "Material" a "FichaDomino_Material". ¿Cuál es el enfoque **más directo** y eficiente?

A) `bpy.ops.material.rename(name="FichaDomino_Material")`  
B) `bpy.data.materials["Material"].name = "FichaDomino_Material"`  
C) `bpy.context.active_object.active_material.rename("FichaDomino_Material")`  
D) `bpy.ops.object.material_slot_move(direction='DOWN')`

**Respuesta correcta: B**

**Explicación:** Acceder directamente a través de `bpy.data` y modificar la propiedad `name` es la forma más directa y eficiente. No existe `bpy.ops.material.rename()`. La opción C usa un método inexistente. La opción D mueve slots de material, no renombra. Esta es una situación donde `bpy.data` es preferible a `bpy.ops`.

---

## Q43. Limpiar la escena antes de script — Difícil

Un estudiante escribe el siguiente código para limpiar la escena antes de crear su dominó, pero no funciona como espera:

```python
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
```

¿Cuál podría ser un problema con este enfoque?

A) `select_all` no acepta el argumento `action`; se debe usar `action_type`  
B) Si hay objetos en modos diferentes al Modo Objeto (por ejemplo en Modo Edición), el operador puede fallar o comportarse inesperadamente  
C) `delete()` requiere confirmar manualmente; en scripts no funciona  
D) No hay ningún problema; el código es perfectamente correcto en todos los casos

**Respuesta correcta: B**

**Explicación:** Los operadores de `bpy.ops` son sensibles al contexto. Si algún objeto está en Modo Edición, el operador de selección y eliminación puede no funcionar como se espera, o puede producir errores de contexto. Es una buena práctica asegurarse de estar en Modo Objeto antes de ejecutar estas operaciones, con `bpy.ops.object.mode_set(mode='OBJECT')`.

---

## Q44. Copia vinculada para múltiples fichas — Difícil

Al crear 28 fichas de dominó (el juego completo), un estudiante usa copias vinculadas para eficiencia. Si luego necesita que **solo** la ficha (6-6) tenga una escala diferente en Z, ¿cuál es el problema?

A) No es posible; las copias vinculadas no permiten cambiar ninguna propiedad  
B) La escala, posición y rotación del objeto sí son independientes, pero la geometría de la malla (y los modificadores) son compartidos  
C) Blender bloqueará la operación y mostrará un error  
D) Cambiar la escala de una copia afecta la escala de todas las copias vinculadas

**Respuesta correcta: B**

**Explicación:** En copias vinculadas, las transformaciones del **objeto** (location, scale, rotation) son independientes, pero los **datos de malla** (geometría, modificadores aplicados, formas base) son compartidos. Cambiar la escala del objeto individualmente sí es posible, pero modificar la geometría en Modo Edición o los modificadores afectará a todas las fichas vinculadas. Esto es clave para decidir cuándo usar linked vs. full copy.

---

## Q45. Orden de operaciones — Difícil

Un estudiante escribe este código para hacer un agujero en una ficha de dominó:

```python
# 1. Crear la ficha
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
ficha = bpy.context.active_object

# 2. Crear el cilindro cortador
bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0.1))
cortador = bpy.context.active_object

# 3. Seleccionar la ficha y agregar el booleano
bpy.ops.object.select_all(action='DESELECT')
ficha.select_set(True)
bpy.context.view_layer.objects.active = ficha
bpy.ops.object.modifier_add(type='BOOLEAN')
mod = ficha.modifiers[-1]
mod.object = cortador
mod.operation = 'DIFFERENCE'
```

¿Qué paso crítico falta para que el agujero sea visible en el render final?

A) Cambiar `mod.operation` a `'UNION'`  
B) Aplicar el modificador con `bpy.ops.object.modifier_apply(modifier=mod.name)`  
C) Eliminar el cilindro cortador antes de aplicar el booleano  
D) Nada falta; el código está completo y el agujero será visible

**Respuesta correcta: B**

**Explicación:** Agregar el modificador y configurarlo no es suficiente; el modificador existe pero no ha sido "aplicado" (convertido permanentemente a geometría). Se debe llamar a `bpy.ops.object.modifier_apply()` para que los cambios sean definitivos. Sin aplicarlo, el modificador solo existe como pila de modificadores. También hay que asegurarse de ocultar el cortador después.

---

## Q46. Nombres de objetos duplicados en bucle — Difícil

El siguiente script crea 7 fichas y les asigna nombres, pero al terminar, `bpy.data.objects["Ficha_3"]` lanza `KeyError`. ¿Cuál es la causa más probable?

```python
for i in range(7):
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.name = f"Ficha_{i}"
```

A) `f-strings` no son compatibles con la API de Blender  
B) `range(7)` produce valores del 0 al 6, así que "Ficha_3" sí existe; el error proviene de otra parte  
C) Blender puede haber renombrado automáticamente algún objeto si hubo colisión de nombres, cambiando el nombre esperado  
D) `bpy.context.active_object` no devuelve el último objeto creado después de un `primitive_add`

**Respuesta correcta: C**

**Explicación:** Si ya existía un objeto llamado "Ficha_3" en la escena de una ejecución anterior del script (sin limpiar la escena), Blender renombrará el nuevo como "Ficha_3.001" y el `KeyError` ocurrirá al buscar "Ficha_3". La solución es limpiar la escena antes de ejecutar el script, o verificar el nombre real asignado con `print(obj.name)`. La opción B es parcialmente correcta pero no explica el error.

---

## Q47. Modificador booleano y manifold — Difícil

La operación booleana DIFFERENCE falla y produce geometría incorrecta. El mensaje de error sugiere problemas con la malla. ¿Cuál es la causa más común en mallas básicas?

A) El objeto cortador debe ser de color rojo para que Blender lo reconozca como cortador  
B) La malla no es "manifold" (hermética/cerrada): tiene caras abiertas, normales invertidas o aristas sin cara que impiden el cálculo booleano correcto  
C) Los booleanos solo funcionan con esferas y cubos perfectos, no con cilindros  
D) El modificador booleano requiere una licencia especial de Blender

**Respuesta correcta: B**

**Explicación:** Los modificadores booleanos requieren mallas **manifold** (también llamadas "watertight" o herméticas): sin agujeros, sin caras solapadas, con normales consistentes. Los cilindros primitivos de Blender son manifold por defecto, pero si han sido editados (caras eliminadas, normales invertidas), pueden fallar. Este es un concepto fundamental de geometría 3D para scripting avanzado.

---

## Q48. Eficiencia de scripts — Difícil

¿Por qué es generalmente **menos eficiente** crear 100 objetos usando 100 llamadas a `bpy.ops.mesh.primitive_cube_add()` en comparación con crear la malla programáticamente con `bpy.data.meshes.new()` y `bpy.data.objects.new()`?

A) `bpy.ops` está desactivado para más de 50 llamadas consecutivas  
B) `bpy.ops` ejecuta operadores completos que actualizan la interfaz, el contexto y la escena en cada llamada, generando overhead; `bpy.data` manipula los datos directamente sin esa sobrecarga  
C) `bpy.data.meshes.new()` crea objetos en paralelo, acelerando la creación  
D) No hay diferencia de rendimiento; ambos métodos son igualmente eficientes

**Respuesta correcta: B**

**Explicación:** Cada llamada a `bpy.ops` simula una acción del usuario y actualiza el estado completo de Blender (UI, contexto, historial de deshacer, etc.), lo que implica mucho overhead. Manipular datos directamente con `bpy.data` evita estas actualizaciones innecesarias y es significativamente más rápido para crear muchos objetos. Para scripts de producción con muchos objetos, se prefiere `bpy.data`.

---

## Q49. Coordenadas relativas en dominó — Difícil

Al crear los puntos (cilindros) de una ficha de dominó, las posiciones se definen de forma **relativa** al centro de la ficha. Si la ficha está en la posición `(5, 3, 0)` y un punto debe estar en `(0.3, 0.3)` relativo a la ficha, ¿cuál es la posición **absoluta** del cilindro cortador?

A) `(0.3, 0.3, 0)`  
B) `(5.3, 3.3, 0.1)` asumiendo que Z=0.1 para penetrar la cara superior  
C) `(5, 3, 0.3)`  
D) `(4.7, 2.7, 0)`

**Respuesta correcta: B**

**Explicación:** La posición absoluta se calcula sumando la posición de la ficha más el desplazamiento relativo del punto: X = 5 + 0.3 = 5.3, Y = 3 + 0.3 = 3.3. Z = 0.1 (o el valor apropiado para que el cilindro penetre la cara superior de la ficha). Este concepto de transformar coordenadas locales a globales es fundamental para posicionar elementos correctamente en escenas 3D.

---

## Q50. Comprensión integral del flujo de trabajo — Difícil

Un estudiante quiere crear una ficha de dominó (3-5) completamente desde Python. Ordena los pasos del pseudocódigo correctamente:

```
I.   Aplicar el modificador DIFFERENCE a la ficha para cada cilindro
II.  Crear la ficha (cubo aplanado)
III. Para cada posición en la lista de puntos del 3 y del 5: crear un cilindro cortador
IV.  Limpiar la escena (eliminar objetos previos)
V.   Para cada cilindro: agregar modificador BOOLEAN tipo DIFFERENCE a la ficha
VI.  Ocultar o eliminar los cilindros cortadores
```

¿Cuál es el orden correcto?

A) II → III → V → I → IV → VI  
B) IV → II → III → V → I → VI  
C) IV → III → II → I → V → VI  
D) II → IV → V → III → I → VI

**Respuesta correcta: B**

**Explicación:** El orden lógico es: **IV** (limpiar la escena para empezar limpio) → **II** (crear la ficha base) → **III** (crear todos los cilindros cortadores en sus posiciones) → **V** (agregar el modificador booleano para cada cilindro) → **I** (aplicar los modificadores para hacer permanentes los agujeros) → **VI** (ocultar/eliminar los cortadores que ya no se necesitan). Este flujo garantiza que cada paso tenga los objetos necesarios disponibles.

---

*Fin del examen — DAG240 Scripting en Blender con Python*  
*Total: 50 preguntas | Fácil: 20 | Intermedio: 20 | Difícil: 10*
