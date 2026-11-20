# COM200 — Programación Avanzada
## Examen Teórico: Estructuras de Datos en C# para Unity (Arreglos, Matrices, List, Queue, Stack)
## 50 Preguntas de Opción Múltiple

> **Instrucciones:** Selecciona la única respuesta correcta para cada pregunta. Las preguntas evalúan tu criterio para decidir qué estructura de datos u operación es la más adecuada en distintos escenarios de un videojuego.

---

## Q1. Principio LIFO — Fácil

En un juego de cocina, el jugador apila platos sucios uno encima de otro y siempre debe entregar primero el plato que está arriba (el último que recogió). ¿Qué estructura modela exactamente este comportamiento?

A) `Queue<GameObject>`  
B) `List<GameObject>`  
C) `Stack<GameObject>`  
D) `int[,]`

**Respuesta correcta: C**

**Retroalimentación:** El `Stack` (pila) sigue el principio LIFO (*Last In, First Out*): el último elemento en entrar es el primero en salir, igual que una torre de platos. La `Queue` es FIFO (sale primero el que llegó primero), la `List` permite acceso libre por índice sin imponer un orden de salida, y `int[,]` es una matriz rectangular de tamaño fijo.

---

## Q2. Principio FIFO — Fácil

En un juego de tienda, los clientes llegan al mostrador y deben ser atendidos estrictamente en el orden en que llegaron. ¿Qué estructura es la más adecuada?

A) `Queue<Cliente>`  
B) `Stack<Cliente>`  
C) `Cliente[]` de tamaño fijo  
D) `int[][]`

**Respuesta correcta: A**

**Retroalimentación:** La `Queue` (cola) es FIFO (*First In, First Out*): el primero en llegar es el primero en ser atendido. Un `Stack` atendería primero al último cliente en llegar, lo cual es injusto en este escenario. Un arreglo de tamaño fijo no se adapta a una cantidad variable de clientes, y `int[][]` es una matriz escalonada de números, no una fila de espera.

---

## Q3. Tamaño de un arreglo — Fácil

Se declara `int[] puntos = new int[5];` y, durante el juego, se descubre que se necesita guardar un sexto puntaje. ¿Qué afirmación es correcta?

A) El arreglo crece automáticamente a 6 posiciones al asignar `puntos[5]`.  
B) Se puede usar `puntos.Add(valor)` para agregar el sexto elemento.  
C) El sexto valor sobrescribe automáticamente la posición 0.  
D) El tamaño de un arreglo es fijo; habría que crear un arreglo nuevo o usar una estructura dinámica como `List<int>`.

**Respuesta correcta: D**

**Retroalimentación:** Una vez instanciado, un arreglo tiene **tamaño estático**: su capacidad no puede alterarse. Asignar `puntos[5]` lanza `IndexOutOfRangeException`, y los arreglos no tienen método `Add()`. Cuando la cantidad de elementos varía en tiempo de ejecución, la estructura adecuada es `List<T>`, cuya capacidad crece y se reduce dinámicamente.

---

## Q4. Valores por defecto — Fácil

Se crea `GameObject[] enemigos = new GameObject[3];` y no se asigna nada más. ¿Qué contiene cada posición del arreglo?

A) `null`  
B) Tres `GameObject` vacíos ya creados en la escena  
C) El valor `0`  
D) Nada; acceder a `enemigos[0]` lanza `IndexOutOfRangeException`

**Respuesta correcta: A**

**Retroalimentación:** Al crear un arreglo con `new T[N]`, cada elemento toma el valor por defecto de su tipo: `0` para números y `null` para objetos (como `GameObject`). No se crean objetos en la escena; eso requeriría `Instantiate`. El índice 0 es válido porque el arreglo tiene `Length` 3, así que no se lanza excepción: simplemente se obtiene `null`.

---

## Q5. Límites de un arreglo — Fácil

Dado `int[] scores = { 10, 20, 30, 40 };`, ¿cuál de los siguientes accesos provoca una `IndexOutOfRangeException`?

A) `scores[0]`  
B) `scores[3]`  
C) `scores[4]`  
D) `scores[scores.Length - 1]`

**Respuesta correcta: C**

**Retroalimentación:** La indexación es en base cero: los índices válidos van de `0` a `Length - 1`, es decir, de 0 a 3. `scores[4]` está fuera del rango. La regla a verificar siempre es `0 <= i < array.Length`. La opción D es exactamente `scores[3]`, el último elemento válido.

---

## Q6. Mostrar el siguiente sin retirarlo — Fácil

La interfaz de usuario debe mostrar "Próximo enemigo: Orco" mientras el orco sigue esperando en la `Queue` de oleadas. ¿Qué método se debe usar?

A) `Dequeue()`  
B) `Peek()`  
C) `Enqueue()`  
D) `Clear()`

**Respuesta correcta: B**

**Retroalimentación:** `Peek()` devuelve el primer elemento **sin retirarlo** de la cola, ideal para mostrar información en la UI. `Dequeue()` lo devolvería pero también lo eliminaría, alterando la oleada. `Enqueue()` agrega al final y `Clear()` vacía toda la cola.

---

## Q7. Naturaleza de `Count` — Fácil

En `List`, `Stack` y `Queue`, ¿qué es `Count`?

A) Un método que se invoca como `Count()` para contar elementos uno a uno  
B) La capacidad máxima que la estructura puede almacenar  
C) El índice del último elemento  
D) Una propiedad que devuelve la cantidad actual de elementos

**Respuesta correcta: D**

**Retroalimentación:** `Count` es una **propiedad** (no un método), por eso se usa sin paréntesis: `inventario.Count`. Indica cuántos elementos hay actualmente, no la capacidad máxima. El índice del último elemento de una lista sería `Count - 1`. En los arreglos, el equivalente es la propiedad `Length`.

---

## Q8. Eliminar por valor — Fácil

El jugador descarta su "espada rota", pero no sabes en qué posición del inventario (`List<GameObject>`) se encuentra. ¿Qué operación es la más apropiada?

A) `inventario.Remove(espadaRota)`  
B) `inventario.RemoveAt(0)`  
C) `inventario.Clear()`  
D) `inventario.Pop()`

**Respuesta correcta: A**

**Retroalimentación:** `Remove(elemento)` busca el elemento y elimina su primera aparición, sin que tengas que conocer su índice; además devuelve `true` si lo encontró. `RemoveAt(0)` elimina lo que haya en la posición 0, que podría ser otro objeto. `Clear()` vaciaría todo el inventario y `Pop()` no existe en `List` (es un método de `Stack`).

---

## Q9. Espacio de nombres requerido — Fácil

Para usar `List<T>`, `Queue<T>` y `Stack<T>` en un script de Unity, ¿qué directiva `using` se necesita?

A) `using UnityEngine.UI;`  
B) `using System.IO;`  
C) `using System.Collections.Generic;`  
D) `using System.Text;`

**Respuesta correcta: C**

**Retroalimentación:** Las colecciones genéricas (`List<T>`, `Queue<T>`, `Stack<T>`) pertenecen al espacio de nombres `System.Collections.Generic`. `System.IO` se usa para leer archivos (`File.ReadAllLines`), `UnityEngine.UI` para componentes de interfaz y `System.Text` para manipulación avanzada de texto.

---

## Q10. Acceso directo por índice — Fácil

¿Cuál de estas estructuras permite leer directamente el tercer elemento con la sintaxis `coleccion[2]`?

A) `Stack<T>`  
B) `List<T>`  
C) `Queue<T>`  
D) Ninguna de las tres

**Respuesta correcta: B**

**Retroalimentación:** `List<T>` ofrece **acceso aleatorio** por índice en base cero con corchetes `[]`, igual que un arreglo. `Stack` y `Queue` restringen el acceso: solo permiten trabajar con el elemento superior (pila) o con el primero (cola), mediante `Pop/Peek` o `Dequeue/Peek`.

---

## Q11. Dónde agrega `Push()` — Fácil

Al ejecutar `pilaDePlatos.Push(plato)`, ¿dónde queda ubicado el nuevo plato?

A) En la parte superior de la pila; será el próximo en salir con `Pop()`  
B) En la base de la pila; será el último en salir  
C) En la posición indicada por un índice  
D) Al final de la fila; saldrá después de todos los demás

**Respuesta correcta: A**

**Retroalimentación:** `Push()` coloca el elemento en la **cima** de la pila. Por el principio LIFO, ese mismo elemento será el primero en ser devuelto por `Pop()` o consultado por `Peek()`. La pila no admite inserción por índice, y la descripción de la opción D corresponde al comportamiento de `Enqueue()` en una cola.

---

## Q12. Función "Deshacer" — Fácil

En un editor de niveles dentro del juego, el diseñador coloca bloques y quiere un botón "Deshacer" que revierta **la última acción realizada**. ¿Qué estructura conviene para guardar el historial de acciones?

A) `Queue<Accion>`  
B) `int[,]`  
C) `Accion[]` de tamaño fijo  
D) `Stack<Accion>`

**Respuesta correcta: D**

**Retroalimentación:** "Deshacer" siempre revierte la acción **más reciente**, que es exactamente lo que entrega `Pop()` en una pila (LIFO). Una `Queue` devolvería la acción más antigua, lo cual es incorrecto. Un arreglo de tamaño fijo limitaría el historial, y `int[,]` es una matriz numérica sin relación con el problema.

---

## Q13. Sintaxis de acceso en matrices — Fácil

¿A qué tipo de matriz corresponde la sintaxis de acceso `mapa[r, c]`?

A) Matriz escalonada `int[][]`  
B) Matriz rectangular `int[,]`  
C) `List<int[]>`  
D) Arreglo unidimensional `int[]`

**Respuesta correcta: B**

**Retroalimentación:** La matriz rectangular `int[,]` usa una sola pareja de corchetes con coma: `mapa[r, c]`. La matriz escalonada (*jagged*) `int[][]` es un arreglo de arreglos y se accede con corchetes dobles: `mapa[r][c]`. Un arreglo unidimensional usa un solo índice.

---

## Q14. Tablero de ajedrez — Fácil

Se programa un juego de ajedrez con un tablero de 8×8 casillas que nunca cambia de forma. ¿Qué estructura es la más natural para representar el tablero?

A) `int[,]` (matriz rectangular)  
B) `Queue<int>`  
C) `Stack<int>`  
D) `int[][]` leído línea por línea desde un archivo `.txt`

**Respuesta correcta: A**

**Retroalimentación:** Cuando la cuadrícula tiene dimensiones **uniformes y conocidas de antemano**, la matriz rectangular `int[,]` es la elección natural: todas las filas tienen la misma cantidad de columnas y se accede como `tablero[fila, columna]`. Las colas y pilas no permiten acceso por posición. La matriz escalonada es más útil cuando el mapa se construye dinámicamente desde texto o cuando las filas pueden variar de longitud.

---

## Q15. Contenido de `TextAsset.text` — Fácil

Si se asigna un archivo `nivel1.txt` a un campo `TextAsset mapFile` en el Inspector, ¿qué devuelve `mapFile.text`?

A) Un arreglo `string[]` con una línea por posición  
B) Una matriz `int[][]` ya convertida a números  
C) Un único `string` con todo el contenido del archivo  
D) La ruta del archivo en el disco

**Respuesta correcta: C**

**Retroalimentación:** La propiedad `.text` de un `TextAsset` entrega el **contenido completo** del archivo como un solo `string`. Dividirlo en líneas, separar las celdas y convertirlas a números es responsabilidad del *pipeline* de parseo (por ejemplo, `MapParser.ParseTextToMatrix`). Quien devuelve un `string[]` por líneas es `File.ReadAllLines`.

---

## Q16. Niveles incluidos en el juego — Fácil

Un juego tendrá 10 niveles diseñados por el equipo, y debe publicarse en Windows, Android y WebGL. ¿Qué método de carga de archivos es el más recomendable?

A) `System.IO.File.ReadAllLines` con rutas absolutas como `C:/Niveles/nivel1.txt`  
B) `UnityEngine.TextAsset` asignado desde el Inspector  
C) Escribir los mapas a mano en un `Stack<string>`  
D) `System.IO.File` leyendo desde el escritorio del usuario

**Respuesta correcta: B**

**Retroalimentación:** `TextAsset` se empaqueta dentro de la *build* final, es multiplataforma de forma nativa y evita rutas fijas (*hardcoded paths*). Las rutas absolutas del disco no existen en otros dispositivos, y en Android/WebGL el acceso directo con `System.IO.File` requiere consideraciones adicionales.

---

## Q17. Niveles creados por jugadores (modding) — Fácil

Se desea que los jugadores puedan crear o modificar sus propios niveles en archivos de texto **sin recompilar el juego**. ¿Qué enfoque se ajusta mejor?

A) `TextAsset` asignado en el Inspector  
B) Una matriz `int[,]` escrita directamente en el código  
C) Un arreglo `int[]` declarado con valores explícitos  
D) `System.IO.File` leyendo desde `Application.streamingAssetsPath`

**Respuesta correcta: D**

**Retroalimentación:** `System.IO.File` lee archivos directamente del disco (por ejemplo, desde `StreamingAssets`), lo que permite a los jugadores agregar o editar niveles sin recompilar. Un `TextAsset` queda empaquetado en la *build* y no puede ser modificado por el jugador. Escribir el mapa en el código (opciones B y C) obliga a recompilar ante cualquier cambio.

---

## Q18. ¿`for` o `foreach`? — Fácil

Necesitas imprimir en consola el mensaje `"Elemento en índice 2: 30"` para cada elemento de un arreglo, es decir, mostrar **la posición y el valor**. ¿Qué bucle es el más apropiado?

A) `for`, porque da acceso directo al índice actual  
B) `foreach`, porque es el único que puede leer el valor  
C) `foreach`, porque permite consultar el índice con `.Index`  
D) Ninguno; se debe usar `Peek()`

**Respuesta correcta: A**

**Retroalimentación:** El bucle `for` maneja explícitamente la variable de índice (`i`), por lo que puede mostrar la posición y el valor (`scores[i]`). `foreach` tiene una sintaxis más limpia, pero no expone el índice; es ideal cuando solo se necesita leer los valores. `Peek()` pertenece a `Stack`/`Queue`, no a un recorrido.

---

## Q19. Reiniciar una oleada — Fácil

El jugador pierde y la oleada actual debe cancelarse por completo, eliminando todos los enemigos pendientes de la `Queue`. ¿Qué operación es la más directa?

A) Llamar a `Peek()` repetidamente  
B) `colaDeEnemigos.Clear()`  
C) `colaDeEnemigos.Enqueue(null)`  
D) `colaDeEnemigos.Count = 0`

**Respuesta correcta: B**

**Retroalimentación:** `Clear()` vacía la cola completa en una sola operación. `Peek()` solo consulta el primer elemento sin retirarlo, así que repetirlo no cambia nada. Encolar `null` agrega un elemento inválido, y `Count` es una propiedad de solo lectura: no se le puede asignar un valor.

---

## Q20. Conjunto fijo de sprites — Fácil

Un juego tipo laberinto usa exactamente 4 sprites de bloques (ladrillo, acero, pasto y agua) que nunca cambian durante la partida. ¿Qué estructura es la más simple y adecuada para guardarlos?

A) `Queue<Sprite>`  
B) `Stack<Sprite>`  
C) `Sprite[]` (arreglo unidimensional)  
D) `int[,]`

**Respuesta correcta: C**

**Retroalimentación:** Para una colección **de tamaño fijo y conocido** que se consulta por posición, el arreglo unidimensional `T[]` es ideal: acceso en O(1) mediante índice (`wallSprites[i]`) y sin sobrecarga. Una cola o una pila obligarían a sacar elementos para acceder a ellos, y `int[,]` almacena números, no sprites.

---

## Q21. Traza de una pila — Intermedio

Analiza la siguiente secuencia de operaciones:

```
Stack<string> pila = new Stack<string>();
pila.Push("A");
pila.Push("B");
pila.Push("C");
pila.Pop();
string x = pila.Peek();
```

¿Cuál es el valor de `x` y cuántos elementos quedan en la pila?

A) `x = "A"`, quedan 2 elementos  
B) `x = "C"`, quedan 3 elementos  
C) `x = "B"`, quedan 1 elemento  
D) `x = "B"`, quedan 2 elementos

**Respuesta correcta: D**

**Retroalimentación:** Tras los tres `Push`, la cima es `"C"`. `Pop()` retira `"C"`, dejando `"B"` en la cima y `"A"` en la base. `Peek()` devuelve `"B"` **sin eliminarlo**, por lo que la pila conserva 2 elementos (`"A"` y `"B"`).

---

## Q22. Traza de una cola — Intermedio

Analiza la siguiente secuencia:

```
Queue<string> cola = new Queue<string>();
cola.Enqueue("goblin");
cola.Enqueue("orco");
cola.Enqueue("dragon");
cola.Dequeue();
cola.Enqueue("troll");
string siguiente = cola.Peek();
```

¿Cuál es el valor de `siguiente`?

A) `"orco"`  
B) `"goblin"`  
C) `"troll"`  
D) `"dragon"`

**Respuesta correcta: A**

**Retroalimentación:** La cola es FIFO. `Dequeue()` retira `"goblin"` (el primero en entrar). Luego `"troll"` se agrega **al final**. La cola queda: `orco → dragon → troll`, por lo que `Peek()` devuelve `"orco"`. El troll, aunque fue el último en llegar, debe esperar su turno.

---

## Q23. Validar antes de retirar — Intermedio

En los ejemplos se recomienda escribir `if (colaDeEnemigos.Count > 0)` antes de llamar a `Dequeue()`. ¿Cuál es la razón principal?

A) Porque `Dequeue()` es más rápido cuando hay elementos  
B) Porque llamar a `Dequeue()` (o `Peek()`) sobre una cola vacía lanza una excepción y detiene la ejecución del script  
C) Porque `Dequeue()` sobre una cola vacía devuelve `0` y genera un enemigo invisible  
D) Porque `Count` reinicia la cola si es cero

**Respuesta correcta: B**

**Retroalimentación:** Retirar o consultar un elemento de una `Queue` (o una `Stack` con `Pop()`/`Peek()`) vacía lanza una `InvalidOperationException`. Verificar `Count > 0` previene el error. No devuelve un valor por defecto, y `Count` es solo una propiedad de consulta: no modifica la estructura.

---

## Q24. Efecto de `Insert()` — Intermedio

El inventario contiene `[espada, escudo, arco]`. Se ejecuta `inventario.Insert(0, pocion);`. ¿Qué devuelve ahora `inventario[1]`?

A) `pocion`  
B) `escudo`  
C) `espada`  
D) `arco`

**Respuesta correcta: C**

**Retroalimentación:** `Insert(0, pocion)` coloca la poción en la posición 0 y **desplaza** todos los elementos siguientes una posición hacia adelante. El inventario queda `[pocion, espada, escudo, arco]`, por lo que el índice 1 contiene `espada`. Este desplazamiento es importante: cualquier índice guardado previamente deja de apuntar al mismo objeto.

---

## Q25. Comportamiento de `Remove()` con duplicados — Intermedio

Una `List<string>` contiene `["pocion", "espada", "pocion"]`. Se ejecuta `bool ok = lista.Remove("pocion");`. ¿Cuál es el resultado?

A) La lista queda `["espada"]` y `ok` es `true`  
B) La lista queda `["pocion", "espada"]` y `ok` es `true`  
C) La lista no cambia y `ok` es `false`, porque hay duplicados  
D) La lista queda `["espada", "pocion"]` y `ok` es `true`

**Respuesta correcta: D**

**Retroalimentación:** `Remove()` elimina únicamente la **primera aparición** del elemento y devuelve `true` si tuvo éxito. Se elimina la poción del índice 0 y la lista queda `["espada", "pocion"]`. Para eliminar todas las apariciones habría que repetir la operación o usar otro enfoque.

---

## Q26. Dimensiones de una matriz rectangular — Intermedio

Se tiene la matriz rectangular `int[,] mapa = new int[3, 5];` (3 filas y 5 columnas). ¿Qué devuelve `mapa.GetLength(1)` y para qué se usa normalmente?

A) Devuelve 5; se usa como límite del bucle de columnas  
B) Devuelve 3; se usa como límite del bucle de filas  
C) Devuelve 15; es el total de celdas  
D) Devuelve 1; es la cantidad de dimensiones

**Respuesta correcta: A**

**Retroalimentación:** En una matriz rectangular, `GetLength(0)` devuelve la cantidad de filas (3) y `GetLength(1)` la cantidad de columnas (5). Por eso, en un doble bucle se usa `GetLength(0)` para las filas y `GetLength(1)` para las columnas. Confundir estas dimensiones es una fuente común de `IndexOutOfRangeException`.

---

## Q27. Recorrido de una matriz escalonada — Intermedio

Al recorrer una matriz escalonada `int[][] matriz` con un doble bucle `for`, ¿cuál debe ser la condición del bucle interno (columnas)?

A) `c < matriz.Length`  
B) `c < matriz.GetLength(1)`  
C) `c < matriz[r].Length`  
D) `c < matriz[0].Length` para todas las filas

**Respuesta correcta: C**

**Retroalimentación:** En una matriz escalonada, **cada fila es un arreglo independiente** que puede tener su propia longitud, por lo que el bucle interno debe consultar `matriz[r].Length`. `matriz.Length` es la cantidad de filas, `GetLength(1)` no aplica a un arreglo de arreglos, y usar `matriz[0].Length` asume que todas las filas miden lo mismo, lo cual puede fallar.

---

## Q28. Por qué *jagged* para leer archivos — Intermedio

¿Por qué se recomienda `int[][]` (escalonada) en lugar de `int[,]` (rectangular) para construir un mapa leído desde un archivo `.txt`?

A) Porque `int[][]` ocupa siempre menos memoria  
B) Porque permite construir la matriz línea por línea, sin conocer de antemano las dimensiones, y tolera filas de distinta longitud  
C) Porque `int[,]` no puede almacenar números enteros  
D) Porque `int[][]` se ordena automáticamente al leer el archivo

**Respuesta correcta: B**

**Retroalimentación:** Una matriz rectangular exige conocer filas y columnas **antes** de crearla, lo que es rígido cuando los datos vienen de un archivo. La matriz escalonada permite convertir cada línea del archivo en una fila independiente (`int[]`) y agregarla a medida que se lee, sin importar cuántas líneas haya ni si alguna tiene longitud distinta.

---

## Q29. `List<int[]>` dentro del parser — Intermedio

En `MapParser.ParseTextToMatrix`, las filas se guardan primero en una `List<int[]>` y al final se convierten con `ToArray()`. ¿Por qué no se crea directamente un `int[][]` con el tamaño de `rawLines.Length`?

A) Porque `int[][]` no puede contener arreglos  
B) Porque `List` convierte automáticamente el texto a números  
C) Porque `ToArray()` ordena las filas del mapa  
D) Porque no se sabe de antemano cuántas filas serán válidas: las líneas vacías y los comentarios se descartan, y la `List` crece dinámicamente

**Respuesta correcta: D**

**Retroalimentación:** El parser **filtra** líneas vacías y comentarios (`#`, `//`), así que la cantidad final de filas puede ser menor que `rawLines.Length`. Si se creara un arreglo de ese tamaño quedarían posiciones `null` al final. La `List` crece solo con las filas válidas y, una vez completa, `ToArray()` produce un `int[][]` del tamaño exacto.

---

## Q30. `int.TryParse` frente a `int.Parse` — Intermedio

¿Por qué el *pipeline* de parseo utiliza `int.TryParse()` para convertir cada celda del mapa?

A) Porque es la única forma de convertir texto a número en C#  
B) Porque convierte automáticamente letras en su código ASCII  
C) Porque no lanza excepción ante un valor inválido: devuelve `false` y permite que el juego continúe  
D) Porque elimina las líneas de comentario del archivo

**Respuesta correcta: C**

**Retroalimentación:** `int.Parse()` lanza una excepción si el texto no es un número válido, lo que podría cerrar o bloquear la carga del nivel. `int.TryParse()` devuelve un `bool` indicando el éxito de la conversión y nunca lanza excepción por formato inválido, haciendo que la carga sea robusta frente a caracteres inesperados en archivos editados a mano.

---

## Q31. Saltos de línea de Windows — Intermedio

Un archivo de mapa creado en Windows separa las líneas con `\r\n`. ¿Por qué el parser divide el texto con `Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries)`?

A) Para que se descarten tanto el `\r` sobrante como las cadenas vacías que aparecen entre `\r` y `\n`, evitando filas fantasma  
B) Para convertir el archivo al formato de Linux antes de guardarlo  
C) Para separar cada número de la fila  
D) Para ordenar las líneas alfabéticamente

**Respuesta correcta: A**

**Retroalimentación:** Si solo se dividiera por `\n`, cada línea conservaría un `\r` al final; si se divide por ambos caracteres, entre `\r` y `\n` aparece una cadena vacía. `RemoveEmptyEntries` descarta esas cadenas vacías, de modo que solo quedan las líneas con contenido real. La separación de cada número se hace en un paso posterior, usando comas, espacios o tabuladores.

---

## Q32. Posición en el mundo — Intermedio

Usando la fórmula de la cuadrícula, con origen en `(0, 0)`, `cellWidth = 1` y `cellHeight = 1`, ¿en qué posición del mundo se instancia el bloque de la fila `r = 2`, columna `c = 3`?

A) `(2, -3, 0)`  
B) `(3, 2, 0)`  
C) `(-3, 2, 0)`  
D) `(3, -2, 0)`

**Respuesta correcta: D**

**Retroalimentación:** La fórmula es `X = Xorigen + c × cellWidth` y `Y = Yorigen − r × cellHeight`. Las **columnas** controlan el eje X (`0 + 3 × 1 = 3`) y las **filas** el eje Y en sentido negativo (`0 − 2 × 1 = −2`). Es un error frecuente intercambiar fila y columna con X e Y.

---

## Q33. El signo negativo en Y — Intermedio

En la fórmula `Y = Yorigen − r × cellHeight`, ¿qué ocurriría si se usara `+` en lugar de `−`?

A) El mapa se dibujaría con las columnas invertidas de derecha a izquierda  
B) El mapa aparecería invertido verticalmente: la fila 0 del archivo quedaría abajo en lugar de arriba  
C) No cambiaría nada, porque Unity corrige el signo automáticamente  
D) Se lanzaría una `IndexOutOfRangeException`

**Respuesta correcta: B**

**Retroalimentación:** En el archivo, las filas avanzan de arriba hacia abajo (`+r`), pero en Unity el eje Y positivo apunta hacia arriba. El signo negativo hace que la fila 0 quede en la parte superior, tal como se ve en el archivo. Con `+`, cada fila nueva se dibujaría más arriba y el nivel aparecería volteado verticalmente. No afecta a las columnas ni genera excepciones.

---

## Q34. Del número al sprite — Intermedio

Según la tabla de tipos de bloque (`0` vacío, `1` ladrillo, `2` acero, `3` pasto, `4` agua) y la fórmula `spriteIndex = tileType − 1`, ¿qué sprite se asigna a una celda con valor `3`?

A) `wallSprites[2]`, el pasto, que oculta a los tanques  
B) `wallSprites[3]`, el agua  
C) `wallSprites[3]`, el pasto  
D) Ninguno, porque 3 es un bloque vacío

**Respuesta correcta: A**

**Retroalimentación:** `spriteIndex = 3 − 1 = 2`, por lo que se usa `wallSprites[2]`, el pasto o arbusto. Se resta 1 porque el valor `0` representa una celda vacía que no se instancia; así el tipo `1` corresponde al índice 0 del arreglo de sprites.

---

## Q35. Turnos cíclicos — Intermedio

En un combate por turnos, cada personaje actúa en orden y, después de actuar, **vuelve al final de la fila** para esperar su próximo turno. ¿Qué combinación de estructura y operaciones modela mejor esto?

A) `Stack` con `Pop()` seguido de `Push()`  
B) `int[,]` recorrida con `foreach`  
C) `Queue` con `Dequeue()` para obtener al personaje y luego `Enqueue()` para devolverlo al final  
D) `List` con `Clear()` al terminar cada turno

**Respuesta correcta: C**

**Retroalimentación:** La cola (FIFO) garantiza el orden de turnos: `Dequeue()` obtiene al personaje que lleva más tiempo esperando y `Enqueue()` lo coloca al final para el siguiente ciclo. Con un `Stack`, el personaje que acaba de actuar volvería a la cima y actuaría de nuevo inmediatamente. Vaciar la lista con `Clear()` perdería a todos los personajes.

---

## Q36. Inventario con ranuras seleccionables — Intermedio

El jugador tiene un inventario en el que puede **seleccionar cualquier ranura** con las teclas 1–9, usar objetos en cualquier orden y recoger objetos nuevos durante la partida. ¿Qué estructura es la más adecuada?

A) `Stack<Item>`, porque los objetos se apilan  
B) `List<Item>`, porque permite acceso directo por índice y crecer dinámicamente  
C) `Queue<Item>`, porque los objetos se recogen en orden  
D) `Item[,]`, porque el inventario es una cuadrícula fija

**Respuesta correcta: B**

**Retroalimentación:** Elegir la ranura 5 equivale a acceder a `inventario[4]`: se necesita **acceso aleatorio** y además **tamaño dinámico** para agregar y quitar objetos. `List<T>` reúne ambas características. `Stack` y `Queue` solo permiten acceder a un extremo, y una matriz de tamaño fijo no puede crecer.

---

## Q37. Enemigos activos en escena — Intermedio

Los enemigos aparecen en momentos distintos y mueren en **cualquier orden** según dónde dispare el jugador. Se necesita una colección de enemigos activos para recorrerlos cada frame y quitar a los que mueren. ¿Qué opción es la más apropiada?

A) `List<GameObject>` con `Add()` al aparecer y `Remove()` al morir  
B) `Queue<GameObject>`, porque los enemigos llegan en orden  
C) `Stack<GameObject>`, porque el último enemigo en aparecer es el que muere  
D) `GameObject[]` con tamaño fijo igual al número inicial de enemigos

**Respuesta correcta: A**

**Retroalimentación:** Como los enemigos mueren en cualquier orden, se necesita poder **eliminar un elemento específico** sin importar su posición. `List.Remove()` lo permite. `Queue` y `Stack` solo permiten retirar un extremo, y suponer que el primero (o el último) en aparecer es el que muere no se cumple. Un arreglo fijo no puede crecer si aparecen más enemigos.

---

## Q38. Altura del plato apilado — Intermedio

En el `RecolectorDePlatos`, la posición del nuevo plato se calcula **antes** del `Push()` así:

```
nuevaPos = puntoDeApilado.position + Vector3.up * (pilaDePlatos.Count * alturaEntrePlatos);
```

Si `alturaEntrePlatos = 0.2` y ya hay 3 platos en la pila, ¿a qué altura sobre `puntoDeApilado` aparece el nuevo plato?

A) 0.8  
B) 0.2  
C) 0.6  
D) 0.4

**Respuesta correcta: C**

**Retroalimentación:** Al calcular la posición, `Count` vale 3 (el nuevo plato todavía no se agregó), por lo que la altura es `3 × 0.2 = 0.6`. El primer plato (con `Count = 0`) quedó en 0.0, el segundo en 0.2 y el tercero en 0.4. Si el cálculo se hiciera **después** del `Push`, cada plato quedaría un nivel más arriba de lo debido, dejando un hueco en la base.

---

## Q39. Cambio de nivel — Intermedio

Al pasar del nivel 1 al nivel 2, el script vuelve a llamar a `BuildGrid` con la nueva matriz, pero los jugadores reportan bloques superpuestos y colisiones extrañas. ¿Cuál es la causa más probable?

A) `int[][]` no permite cargar un segundo mapa  
B) `TextAsset` solo puede leerse una vez por partida  
C) Los bloques del nivel anterior no se destruyeron (`Destroy`) antes de generar el nuevo nivel  
D) `Quaternion.identity` rota los bloques del segundo nivel

**Respuesta correcta: C**

**Retroalimentación:** `BuildGrid` instancia bloques nuevos, pero no elimina los anteriores. Como buena práctica, antes de cargar un nuevo nivel se deben destruir los bloques generados previamente (por ejemplo, recorriendo los hijos del contenedor y llamando a `Destroy`). La matriz y el `TextAsset` pueden reutilizarse sin problema, y `Quaternion.identity` significa "sin rotación".

---

## Q40. Modificar los valores de un arreglo — Intermedio

Necesitas **duplicar** cada puntaje almacenado en `int[] scores`, guardando el resultado en el mismo arreglo. ¿Qué enfoque es correcto?

A) `foreach (int s in scores) { s = s * 2; }`  
B) `for (int i = 0; i < scores.Length; i++) { scores[i] = scores[i] * 2; }`  
C) `scores.Peek() * 2` repetido `Length` veces  
D) Cualquiera de los dos bucles sirve, porque `foreach` y `for` son equivalentes

**Respuesta correcta: B**

**Retroalimentación:** La variable de iteración de un `foreach` es de solo lectura: asignarle un valor produce un error de compilación, por eso `foreach` se recomienda solo para **leer**. Para **modificar** elementos se necesita el índice, y el bucle `for` lo proporciona (`scores[i] = ...`). Los arreglos no tienen método `Peek()`.

---

## Q41. Carácter inválido en el mapa — Difícil

Un diseñador escribe por error la línea `1,1,X,2` en el archivo del mapa. Considerando que el parser usa `int.TryParse(tokens[c], out row[c])` sin revisar el valor de retorno, ¿qué sucede?

A) El juego se cierra con una `FormatException`  
B) La fila completa se descarta como si fuera un comentario  
C) La celda con `X` se convierte en el código ASCII de la letra  
D) La celda con `X` queda con valor `0` y se trata como espacio vacío, sin ningún aviso; el error pasa desapercibido

**Respuesta correcta: D**

**Retroalimentación:** Cuando `TryParse` falla, devuelve `false` y asigna `0` a la variable de salida. Como el valor `0` significa "celda vacía", el bloque simplemente no aparece y no se muestra ningún error. La robustez evita que el juego se caiga, pero puede ocultar errores del diseñador. Una mejora razonable es verificar el `bool` devuelto y registrar un `Debug.LogWarning` con la fila y la columna afectadas.

---

## Q42. Tipo de bloque fuera de rango — Difícil

El mapa contiene un valor `5`, pero el arreglo `wallSprites` solo tiene 4 sprites (índices 0 a 3). Según la implementación de `BuildGrid`, ¿qué ocurre con esa celda?

A) Se lanza `IndexOutOfRangeException` y se detiene la construcción del mapa  
B) El bloque se instancia, pero la validación `spriteIndex < wallSprites.Length` impide asignar el sprite, así que conserva el sprite por defecto del prefab  
C) La celda no se instancia porque solo se instancian los valores del 1 al 4  
D) Se asigna automáticamente `wallSprites[0]` para evitar errores

**Respuesta correcta: B**

**Retroalimentación:** En `BuildGrid`, solo se omiten las celdas con valor `0`; cualquier otro valor llega a `Instantiate`. Después, `spriteIndex = 5 − 1 = 4` no cumple `4 < 4`, por lo que la validación evita la excepción, pero no se cambia el sprite: el bloque queda visible con la apariencia por defecto del prefab. Validar índices previene caídas, pero conviene también advertir sobre valores no reconocidos.

---

## Q43. Deshacer y rehacer — Difícil

Un editor de niveles debe soportar **Deshacer** (Ctrl+Z) y **Rehacer** (Ctrl+Y). ¿Qué diseño es el correcto?

A) Dos pilas: al deshacer se hace `Pop()` en la pila de deshacer y `Push()` de esa acción en la pila de rehacer; al realizar una acción nueva se hace `Push()` en deshacer y se vacía (`Clear()`) la pila de rehacer  
B) Una sola cola: `Dequeue()` para deshacer y `Enqueue()` para rehacer  
C) Una `List` en la que deshacer siempre elimina el índice 0  
D) Dos colas: una para deshacer y otra para rehacer, sin vaciar ninguna

**Respuesta correcta: A**

**Retroalimentación:** Tanto deshacer como rehacer trabajan con la acción **más reciente** de su historial, lo cual es LIFO, por lo que se usan dos pilas. Al deshacer, la acción pasa de la pila de deshacer a la de rehacer; al rehacer, ocurre lo inverso. Cuando se realiza una acción nueva, el historial de rehacer deja de ser válido y se vacía. Una cola o eliminar el índice 0 revertiría la acción más antigua.

---

## Q44. Rebobinar el recorrido — Difícil

Un juego registra cada casilla que pisa el jugador. Al activar una habilidad de "rebobinar", el personaje debe regresar al punto de partida **recorriendo el mismo camino en orden inverso**. ¿Qué estructura facilita esta mecánica con menos código?

A) `Queue<Vector3>`, porque guarda las posiciones en el orden en que se visitaron  
B) `Vector3[]` de tamaño fijo, recorrido con `foreach`  
C) `Stack<Vector3>`, haciendo `Push()` de cada posición al avanzar y `Pop()` al rebobinar  
D) `int[,]` con las coordenadas del mapa

**Respuesta correcta: C**

**Retroalimentación:** La pila invierte el orden de forma natural: la última posición registrada es la primera en salir, así que al hacer `Pop()` sucesivos el personaje recorre su camino hacia atrás hasta llegar al inicio. La cola devolvería las posiciones en el mismo orden en que se visitaron, es decir, comenzaría por el punto de partida. Un arreglo fijo no se adapta a la longitud variable del recorrido.

---

## Q45. Exploración de laberinto con retroceso — Difícil

Una IA explora un laberinto tipo cuadrícula: avanza por un pasillo y, cuando llega a un callejón sin salida, debe **regresar a la última bifurcación visitada** para probar otro camino. ¿Qué estructura conviene para guardar las bifurcaciones pendientes?

A) `Queue`, porque retoma la primera bifurcación encontrada en todo el recorrido  
B) `Stack`, porque retoma la bifurcación más reciente, que es justamente "la última visitada"  
C) `List`, eliminando siempre el índice 0  
D) `int[]` de tamaño fijo igual al número de filas del mapa

**Respuesta correcta: B**

**Retroalimentación:** "Volver a la **última** bifurcación" es un comportamiento LIFO: la pila devuelve siempre el punto de decisión más reciente (esto es lo que se conoce como *backtracking*). Una cola retomaría la bifurcación más antigua, haciendo que la IA salte a zonas lejanas del laberinto. Eliminar el índice 0 de una lista también recupera el elemento más antiguo.

---

## Q46. El jefe se adelanta — Difícil

Una oleada se gestiona con `Queue<GameObject>`. Un nuevo requerimiento indica que, cuando el jugador activa una alarma, **el jefe debe aparecer inmediatamente**, antes de todos los enemigos que ya estaban esperando. ¿Cuál es el análisis correcto?

A) Basta con `Enqueue(jefe)`, porque la cola atiende primero al último que entra  
B) Basta con `Peek()` para colocar al jefe al frente  
C) `Contains(jefe)` mueve al jefe al inicio de la cola si ya estaba en ella  
D) `Queue` no permite insertar al frente; se puede manejar al jefe por separado antes de la cola, o cambiar a una `List` usando `Insert(0, jefe)` y `RemoveAt(0)` para procesar

**Respuesta correcta: D**

**Retroalimentación:** La cola solo agrega al final (`Enqueue`) y retira del frente (`Dequeue`); no permite colarse. `Peek()` y `Contains()` solo consultan, no modifican el orden. Si el requerimiento exige saltar la fila, o bien se procesa al jefe fuera de la cola (por ejemplo, con una variable "jefe pendiente" que se revisa primero), o se usa una `List`, que permite insertar en cualquier posición a costa de desplazar los demás elementos.

---

## Q47. Eliminar mientras se recorre — Difícil

Cada frame se recorre una `List<GameObject> enemigos` y se deben quitar los enemigos con vida igual a cero. ¿Cuál es la forma correcta de hacerlo?

A) Usar `foreach` y llamar a `enemigos.Remove(e)` dentro del bucle  
B) Usar `for` desde `i = 0` hasta `Count - 1` y llamar a `RemoveAt(i)` sin ajustar el índice  
C) Usar `for` en sentido inverso, desde `i = enemigos.Count - 1` hasta `0`, y llamar a `RemoveAt(i)`  
D) Llamar a `enemigos.Clear()` y volver a agregar solo los enemigos vivos con `Insert(0, ...)`, sin recorrer la lista

**Respuesta correcta: C**

**Retroalimentación:** Modificar una lista dentro de un `foreach` lanza una `InvalidOperationException`, porque la colección cambió durante la enumeración. En un `for` hacia adelante, al hacer `RemoveAt(i)` los elementos siguientes se desplazan una posición y el bucle **se salta** el que ocupa ahora el índice `i`. Recorrer hacia atrás evita el problema: los desplazamientos solo afectan a posiciones que ya fueron revisadas. La opción D pierde la referencia a los enemigos antes de saber cuáles están vivos.

---

## Q48. Fila más corta en el archivo — Difícil

En un archivo de mapa, todas las filas tienen 7 valores excepto la tercera, que por error tiene 6. El mapa se carga con `ParseTextToMatrix` (que devuelve `int[][]`) y se dibuja con `BuildGrid`. ¿Qué ocurre?

A) Se lanza una `IndexOutOfRangeException` al construir la tercera fila  
B) La tercera fila se crea con 6 elementos; como `BuildGrid` recorre hasta `matrix[r].Length`, no hay excepción, pero visualmente falta la última celda de esa fila  
C) El parser rellena automáticamente la séptima celda con el valor de la fila anterior  
D) El parser descarta la tercera fila completa por tener una longitud distinta

**Respuesta correcta: B**

**Retroalimentación:** La matriz escalonada acepta filas de longitudes distintas, y el parser crea cada fila con `tokens.Length` elementos. `BuildGrid` usa `matrix[r].Length` en el bucle interno, así que recorre solo 6 columnas en esa fila y no hay excepción. El resultado es un mapa con un hueco en la última columna de la tercera fila. Esta tolerancia es una ventaja de `int[][]`, pero obliga a validar los datos si se requiere un mapa perfectamente rectangular.

---

## Q49. Funciona en el editor, falla en Android — Difícil

Los niveles se cargan con `File.ReadAllLines(Path.Combine(Application.streamingAssetsPath, "nivel1.txt"))`. En el editor de Unity todo funciona, pero en la *build* de Android el nivel no carga. Los niveles **no** necesitan ser modificados por el jugador. ¿Cuál es la decisión más apropiada?

A) Migrar la carga a `TextAsset`, que se empaqueta en la *build* y funciona de forma nativa en todas las plataformas  
B) Cambiar `File.ReadAllLines` por un `Stack<string>`  
C) Escribir la ruta absoluta `C:/Proyecto/Assets/StreamingAssets/nivel1.txt`  
D) Cambiar la matriz `int[][]` por `int[,]`

**Respuesta correcta: A**

**Retroalimentación:** En Android y WebGL, el acceso directo con `System.IO.File` a `StreamingAssets` requiere consideraciones adicionales, porque los archivos no están disponibles como archivos sueltos en el disco. Como los niveles no requieren modding, `TextAsset` es la solución recomendada: viaja dentro de la *build* y no depende de rutas. Una ruta absoluta de la PC no existe en el teléfono, y cambiar el tipo de matriz no resuelve un problema de lectura del archivo.

---

## Q50. Diseño integral de un juego — Difícil

Un juego tipo *Battle City* tiene los siguientes requerimientos:

```
I.   Un conjunto fijo de 4 sprites de bloques.
II.  Mapas de nivel diseñados por el equipo en archivos .txt, incluidos en la build.
III. Tanques enemigos que aparecen uno por uno en el orden en que fueron programados.
IV.  Un botón para deshacer la última pared colocada en el modo editor.
```

¿Qué combinación de estructuras es la más adecuada?

A) I: `List<Sprite>` — II: `int[,]` + `System.IO.File` — III: `Stack<GameObject>` — IV: `Queue<Accion>`  
B) I: `Queue<Sprite>` — II: `List<int>` + `TextAsset` — III: `List<GameObject>` — IV: `List<Accion>` eliminando el índice 0  
C) I: `Stack<Sprite>` — II: `int[][]` + `System.IO.File` — III: `Queue<GameObject>` — IV: `Queue<Accion>`  
D) I: `Sprite[]` — II: `int[][]` + `TextAsset` — III: `Queue<GameObject>` — IV: `Stack<Accion>`

**Respuesta correcta: D**

**Retroalimentación:** **I:** un conjunto fijo y conocido se representa con un arreglo `T[]` (acceso O(1) por índice). **II:** para niveles incluidos en la *build*, la combinación recomendada es `TextAsset` + `int[][]`, que equilibra portabilidad y facilidad de parseo línea por línea. **III:** aparecer "en el orden programado" es FIFO, es decir, `Queue`. **IV:** deshacer "la última" acción es LIFO, es decir, `Stack`. Las demás opciones invierten FIFO/LIFO o eligen estructuras que no se ajustan al requerimiento.

---

*Fin del examen — COM200 Estructuras de Datos en C# para Unity*  
*Total: 50 preguntas | Fácil: 20 | Intermedio: 20 | Difícil: 10*
