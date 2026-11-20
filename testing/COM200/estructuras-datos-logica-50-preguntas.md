# COM200 — Programación Avanzada
## Examen de Lógica y Criterio: Estructuras de Datos en Juegos 2D con Unity
**50 Preguntas | Distribución: 20 Fácil · 20 Intermedio · 10 Difícil**

> **Instrucciones:** Cada pregunta describe un escenario de un juego 2D, el objetivo que se quiere lograr y, en algunos casos, un fragmento de código. Elige la opción que **mejor** cumple el objetivo. Varias opciones pueden parecer razonables; analiza cuál funciona correctamente en todos los casos descritos y cuál es la más adecuada para el problema.

**Distribución por tema:**

| Tema | Preguntas |
|---|---|
| Arreglos | Q1, Q10, Q15, Q24, Q33 |
| Matrices | Q5, Q14, Q23, Q29, Q35, Q49 |
| Archivos y Parseo | Q6, Q16, Q28, Q36, Q45 |
| List | Q4, Q9, Q13, Q17, Q21, Q25, Q30, Q39, Q40, Q44 |
| Queue | Q2, Q7, Q11, Q18, Q22, Q26, Q31, Q37, Q42, Q46, Q48 |
| Stack | Q3, Q8, Q12, Q19, Q27, Q32, Q38, Q41, Q47 |
| Integración | Q20, Q34, Q43, Q50 |

---

## Q1. Prefabs de cactus en el Inspector — Fácil — Tema: Arreglos

**Escenario:** En un juego tipo *endless runner* hay exactamente 3 prefabs de cactus. El diseñador quiere arrastrarlos desde el Inspector a un solo campo del script `SpawnerCactus` y el script debe elegir uno al azar. La cantidad de prefabs no cambia durante la partida.

**Objetivo:** Elegir la declaración más simple y adecuada.

A) `public Queue<GameObject> cactus;`  
B) `public GameObject cactus1, cactus2, cactus3;`  
C) `public GameObject[] cactus;`  
D) `public Stack<GameObject> cactus;`

**Respuesta correcta: C**

**Retroalimentación:** Un arreglo es ideal para un conjunto fijo que se elige por índice (`cactus[Random.Range(0, cactus.Length)]`), y Unity lo muestra en el Inspector para arrastrar los prefabs. Unity **no muestra** `Queue` ni `Stack` en el Inspector, así que no podrían asignarse arrastrando. Tres variables separadas funcionan, pero obligan a escribir un `if` o `switch` para elegir al azar y no escalan si se agrega un cuarto cactus.

---

## Q2. Fantasmas que salen de la casa — Fácil — Tema: Queue

**Escenario:** En un juego de laberinto, 4 fantasmas esperan dentro de una casa central. Cada 5 segundos sale uno, **siempre en el mismo orden** en que fueron registrados al inicio del nivel.

**Objetivo:** Elegir la estructura para administrar a los fantasmas que esperan.

A) `Queue<GameObject>`: se registran con `Enqueue()` y cada 5 segundos se libera uno con `Dequeue()`  
B) `Stack<GameObject>`: se registran con `Push()` y cada 5 segundos se libera uno con `Pop()`  
C) `GameObject[]`: cada 5 segundos se libera un fantasma elegido con `Random.Range`  
D) `List<GameObject>`: cada 5 segundos se libera el último elemento de la lista

**Respuesta correcta: A**

**Retroalimentación:** "Salir en el mismo orden en que se registraron" es FIFO, el comportamiento de una `Queue`. Un `Stack` liberaría primero al último registrado (orden inverso). La elección aleatoria rompe el orden, y liberar el último elemento de una lista también invierte el orden.

---

## Q3. Cajas sobre la cabeza — Fácil — Tema: Stack

**Escenario:** En un juego de plataformas 2D, el personaje recoge cajas y las va apilando sobre su cabeza. Al presionar la tecla de lanzar, **solo puede lanzar la caja que está arriba**.

**Objetivo:** Elegir la estructura que modela las cajas cargadas.

A) `Queue<GameObject>`, porque las cajas se recogen en orden  
B) `GameObject[]` con tamaño 10  
C) `List<GameObject>`, lanzando siempre la caja del índice 0  
D) `Stack<GameObject>`, usando `Push()` al recoger y `Pop()` al lanzar

**Respuesta correcta: D**

**Retroalimentación:** La caja de arriba es la última recogida: LIFO. `Push()` la coloca en la cima y `Pop()` la retira para lanzarla. Una `Queue` lanzaría la primera caja recogida, que está en la base de la torre. Lanzar el índice 0 de una lista también corresponde a la caja más antigua, y un arreglo de tamaño 10 impone un límite arbitrario.

---

## Q4. Enemigos en pantalla — Fácil — Tema: List

**Escenario:** En un *shooter* 2D aparecen enemigos en momentos distintos. Cada bala tiene un `Collider2D` con `isTrigger` activado y, cuando toca a un enemigo, ese enemigo muere. Los enemigos mueren **en cualquier orden**. Un `EnemyManager` necesita saber en todo momento qué enemigos siguen vivos.

**Objetivo:** Elegir cómo guardar los enemigos vivos.

A) `Queue<GameObject>`, retirando con `Dequeue()` cada vez que muere un enemigo  
B) `List<GameObject>`, con `Add()` al aparecer y `Remove(enemigo)` al morir  
C) `Stack<GameObject>`, retirando con `Pop()` cada vez que muere un enemigo  
D) `GameObject[]` con el tamaño de la primera oleada

**Respuesta correcta: B**

**Retroalimentación:** Como los enemigos mueren en cualquier orden, hay que poder quitar **un enemigo específico**, y `List.Remove(enemigo)` lo permite. `Dequeue()` quitaría al primero que apareció y `Pop()` al último, que no necesariamente son los que murieron. Un arreglo de tamaño fijo no puede crecer cuando aparecen nuevas oleadas.

---

## Q5. Tablero de tres en raya — Fácil — Tema: Matrices

**Escenario:** Se programa un juego de tres en raya (3×3). Cada casilla puede estar vacía, tener una X o tener una O. Al hacer clic en una casilla se conoce su fila y su columna.

**Objetivo:** Elegir cómo representar el estado del tablero.

A) `Queue<char>` con 9 elementos  
B) `char[,] tablero = new char[3, 3];` accediendo con `tablero[fila, columna]`  
C) `List<char>` que crece con cada jugada  
D) `Stack<char>` donde cada jugada hace `Push()`

**Respuesta correcta: B**

**Retroalimentación:** El tablero tiene dimensiones fijas y uniformes, y cada clic da directamente la fila y la columna: una matriz rectangular es la representación natural. Además, verificar si hay tres en línea es sencillo recorriendo filas, columnas y diagonales. Las colas y pilas no permiten consultar una casilla por posición, y una lista que solo crece con cada jugada pierde la relación con la casilla jugada.

---

## Q6. Niveles para WebGL — Fácil — Tema: Archivos y Parseo

**Escenario:** El equipo diseñó 8 niveles en archivos `.txt`. El juego se publicará en WebGL y en Android, y los jugadores **no** deben modificar los niveles.

**Objetivo:** Elegir la forma de cargar los niveles.

A) Un arreglo `TextAsset[] niveles` asignado desde el Inspector, leyendo `niveles[i].text`  
B) `File.ReadAllLines("C:/MiJuego/Niveles/nivel1.txt")`  
C) Copiar el contenido de cada nivel dentro de un `Stack<string>` en el código  
D) Pedir al jugador que seleccione el archivo del nivel al iniciar el juego

**Respuesta correcta: A**

**Retroalimentación:** `TextAsset` se empaqueta en la *build* y funciona en todas las plataformas sin depender de rutas. Un arreglo `TextAsset[]` permite además cambiar de nivel con un índice. Una ruta absoluta de la PC no existe en Android ni en el navegador. Escribir los niveles en el código o pedir archivos al jugador complica el diseño sin necesidad.

---

## Q7. Diálogo de un NPC — Fácil — Tema: Queue

**Escenario:** Al acercarse a un NPC (detectado con `OnTriggerEnter2D`), se carga su diálogo de 5 líneas. Cada vez que el jugador presiona `Espacio` debe mostrarse **la siguiente línea**, en el orden en que fueron escritas, hasta terminar.

**Objetivo:** Elegir la lógica más adecuada.

A) Guardar las líneas en un `Stack<string>` y mostrar `Pop()` en cada pulsación  
B) Guardar las líneas en un `string[]` y mostrar siempre `lineas[0]`  
C) Guardar las líneas en una `Queue<string>` y mostrar `Dequeue()` en cada pulsación mientras `Count > 0`  
D) Guardar las líneas en una `List<string>` y mostrar una línea elegida al azar

**Respuesta correcta: C**

**Retroalimentación:** El diálogo se consume en orden y cada línea se muestra una sola vez: una `Queue` lo modela directamente, y `Count > 0` indica cuándo termina. Con un `Stack` el diálogo saldría al revés, empezando por la última línea. Mostrar siempre `lineas[0]` repite la misma línea, y el azar rompe la conversación.

---

## Q8. Submenús de pausa — Fácil — Tema: Stack

**Escenario:** El menú de pausa abre *Opciones*; desde *Opciones* se abre *Audio*; desde *Audio* se abre *Volumen avanzado*. El botón **Atrás** siempre debe regresar al panel que se abrió **justo antes** del actual.

**Objetivo:** Elegir cómo recordar los paneles abiertos.

A) Una `Queue<GameObject>` de paneles  
B) Una variable `GameObject panelAnterior`  
C) Un arreglo `GameObject[] paneles` recorrido con `foreach`  
D) Un `Stack<GameObject>` de paneles: `Push()` al abrir y `Pop()` al presionar Atrás

**Respuesta correcta: D**

**Retroalimentación:** La navegación hacia atrás es LIFO: el último panel abierto es el primero en cerrarse. Una sola variable `panelAnterior` funciona para un nivel, pero al retroceder dos veces ya no recuerda el panel anterior al anterior. Una `Queue` regresaría al primer panel abierto, y recorrer un arreglo no indica el orden de navegación.

---

## Q9. Puntos de control — Fácil — Tema: List

**Escenario:** El nivel tiene varios puntos de control (*checkpoints*) con colliders `isTrigger`. El jugador puede tocarlos en cualquier orden y varias veces, pero cada checkpoint debe **contarse una sola vez**.

```csharp
private List<GameObject> tocados = new List<GameObject>();

void OnTriggerEnter2D(Collider2D other)
{
    if (other.CompareTag("Checkpoint"))
    {
        // ???
    }
}
```

**Objetivo:** Elegir el código que reemplaza a `// ???`.

A) `if (!tocados.Contains(other.gameObject)) tocados.Add(other.gameObject);`  
B) `tocados.Add(other.gameObject);`  
C) `tocados.Remove(other.gameObject); tocados.Add(other.gameObject);`  
D) `if (tocados.Count == 0) tocados.Add(other.gameObject);`

**Respuesta correcta: A**

**Retroalimentación:** `Contains` evita agregar un checkpoint que ya está registrado, así que cada uno cuenta una sola vez. La opción B lo agregaría cada vez que el jugador pasa por encima. La C evita duplicados, pero hace trabajo innecesario y cambia el orden de registro. La D solo registraría el primer checkpoint.

---

## Q10. Corazones de vida — Fácil — Tema: Arreglos

**Escenario:** El HUD muestra 3 corazones, guardados en `GameObject[] corazones` (índices 0, 1 y 2). La variable `vidas` empieza en 3. Cuando un enemigo choca con el jugador (`OnCollisionEnter2D`), se pierde una vida y debe ocultarse el corazón correspondiente, empezando por el de la derecha (índice 2).

**Objetivo:** Elegir el código correcto.

A) `corazones[vidas].SetActive(false); vidas--;`  
B) `vidas--; corazones[0].SetActive(false);`  
C) `if (vidas > 0) { vidas--; corazones[vidas].SetActive(false); }`  
D) `corazones[vidas - 1].SetActive(false);`

**Respuesta correcta: C**

**Retroalimentación:** Con `vidas = 3`, primero se decrementa a 2 y se oculta `corazones[2]`; luego el 1 y el 0. La condición `vidas > 0` evita valores negativos si el jugador recibe golpes estando sin vidas. La opción A accede a `corazones[3]` y lanza `IndexOutOfRangeException`. La B siempre oculta el mismo corazón. La D oculta el corazón correcto la primera vez, pero nunca decrementa `vidas`.

---

## Q11. Vista previa de la siguiente pieza — Fácil — Tema: Queue

**Escenario:** En un juego de bloques que caen, las próximas piezas se generan al inicio y se guardan en una `Queue`. Una ventana del HUD debe mostrar **cuál será la siguiente pieza** mientras la pieza actual sigue cayendo.

**Objetivo:** Elegir la operación adecuada para la vista previa.

A) `colaPiezas.Dequeue()`, mostrando la pieza que devuelve  
B) `colaPiezas.Peek()`, mostrando la pieza sin retirarla  
C) `colaPiezas.Clear()` y luego volver a generar las piezas  
D) `colaPiezas.Contains(pieza)`

**Respuesta correcta: B**

**Retroalimentación:** La vista previa solo **consulta**; la pieza debe seguir en la cola hasta que realmente le toque caer. `Peek()` devuelve el primer elemento sin retirarlo. Con `Dequeue()` la pieza mostrada saldría de la cola y nunca llegaría a jugarse. `Contains` solo indica si una pieza está en la cola, no cuál es la siguiente.

---

## Q12. Lanzar sin cajas — Fácil — Tema: Stack

**Escenario:** Continuando con el personaje que apila cajas, a veces el jugador presiona el botón de lanzar **sin tener cajas**, y la consola muestra una `InvalidOperationException`.

```csharp
void Update()
{
    if (Input.GetKeyDown(KeyCode.F))
    {
        GameObject caja = pilaCajas.Pop();
        Lanzar(caja);
    }
}
```

**Objetivo:** Corregir el problema de la forma más adecuada.

A) Cambiar `Pop()` por `Peek()`  
B) Envolver todo el `Update` en un bloque `try/catch` vacío  
C) Cambiar la pila por una `Queue` y usar `Dequeue()`  
D) Agregar la condición `pilaCajas.Count > 0` antes de llamar a `Pop()`

**Respuesta correcta: D**

**Retroalimentación:** `Pop()` sobre una pila vacía lanza `InvalidOperationException`; verificar `Count > 0` antes evita el error y expresa claramente la regla "solo se lanza si hay cajas". `Peek()` también falla con la pila vacía y además no retira la caja. Un `try/catch` vacío oculta el problema en lugar de resolverlo, y `Dequeue()` en una cola vacía falla igual.

---

## Q13. Ranuras del inventario — Fácil — Tema: List

**Escenario:** El jugador recoge objetos durante la partida y puede usar **cualquiera** de ellos presionando las teclas 1 a 9 (la tecla 1 corresponde al primer objeto).

**Objetivo:** Elegir la estructura y el acceso correctos.

A) `List<Item> inventario`, usando `inventario[tecla - 1]` después de validar que el índice sea menor que `Count`  
B) `Queue<Item> inventario`, usando `Dequeue()` al presionar cualquier tecla  
C) `Stack<Item> inventario`, usando `Pop()` al presionar cualquier tecla  
D) `Item[] inventario = new Item[9]`, usando `inventario[tecla]`

**Respuesta correcta: A**

**Retroalimentación:** Se necesita acceso por posición y tamaño variable: `List<Item>` con `inventario[tecla - 1]`. Se resta 1 porque la tecla 1 corresponde al índice 0, y se valida contra `Count` porque el jugador podría presionar una tecla sin objeto. Cola y pila solo permiten usar un extremo. La opción D usa `inventario[tecla]` sin restar 1, por lo que la tecla 9 accede al índice 9, fuera de rango.

---

## Q14. Movimiento por casillas — Fácil — Tema: Matrices

**Escenario:** En un juego de laberinto, el personaje se mueve **de casilla en casilla** asignando directamente `transform.position` a la posición de la siguiente celda. Las paredes tienen `BoxCollider2D`, pero el personaje las atraviesa.

**Objetivo:** Elegir la forma correcta de impedir que el personaje entre en una pared.

A) Agregar más colliders a las paredes  
B) Aumentar la masa del `Rigidbody2D` del personaje  
C) Antes de moverse, consultar la matriz del mapa y moverse solo si la celda destino no es pared (`mapa[r][c] != 1`)  
D) Mover al personaje dos casillas en lugar de una

**Respuesta correcta: C**

**Retroalimentación:** Asignar `transform.position` "teletransporta" al objeto: el motor de física no tiene oportunidad de bloquear el movimiento, así que los colliders no lo detienen. En un movimiento por casillas, la fuente de verdad es la **matriz del mapa**: basta con revisar la celda destino antes de moverse. Agregar colliders o cambiar la masa no afecta a un objeto que se teletransporta.

---

## Q15. Patrulla en bucle — Fácil — Tema: Arreglos

**Escenario:** Un guardia patrulla entre 4 puntos (`Transform[] waypoints`, asignados en el Inspector). Al llegar al último punto debe **volver al primero** y seguir patrullando indefinidamente.

```csharp
void SiguientePunto()
{
    indice = ______;
}
```

**Objetivo:** Elegir la expresión que calcula el siguiente índice.

A) `indice + 1`  
B) `(indice + 1) % waypoints.Length`  
C) `waypoints.Length - indice`  
D) `Random.Range(0, waypoints.Length)`

**Respuesta correcta: B**

**Retroalimentación:** El operador `%` (módulo) hace que el índice vuelva a 0 al llegar al final: con 4 puntos, la secuencia es 0, 1, 2, 3, 0, 1, … Con `indice + 1` se llega a 4 y se lanza `IndexOutOfRangeException`. La opción C produce una secuencia que no recorre los puntos en orden, y la D convierte la patrulla en un movimiento aleatorio.

---

## Q16. Formato del archivo de nivel — Fácil — Tema: Archivos y Parseo

**Escenario:** Los diseñadores van a escribir los mapas a mano en el Bloc de notas y el parser los convertirá en una matriz `int[][]`.

**Objetivo:** Elegir el formato de archivo más claro y fácil de procesar.

A) Todos los números en una sola línea larga, sin separadores: `1110211001`  
B) Un número por línea, con todo el mapa en una sola columna  
C) Los valores mezclados con descripciones: `ladrillo,1;acero,2;...`  
D) Una línea del archivo por cada fila del mapa, con los valores separados por comas o espacios

**Respuesta correcta: D**

**Retroalimentación:** Si cada línea es una fila y cada valor está separado por un delimitador, el archivo **se ve igual que el mapa** y el parser solo divide por saltos de línea y luego por delimitadores. Una sola línea sin separadores no indica dónde termina cada fila ni permite valores de dos dígitos. Una columna de números pierde la forma del mapa, y mezclar descripciones complica el parseo sin beneficio.

---

## Q17. Enemigo destruido, referencia viva — Fácil — Tema: List

**Escenario:** Cuando una bala toca a un enemigo, el script de la bala ejecuta `Destroy(other.gameObject)`. Más tarde, el `EnemyManager` recorre su lista `enemigos` para moverlos y aparece una `MissingReferenceException`.

**Objetivo:** Elegir la corrección más adecuada.

A) Usar `Destroy(other.gameObject, 5f)` para destruirlo más tarde  
B) Llamar a `enemigos.Clear()` cada vez que muere un enemigo  
C) Antes de destruir al enemigo, quitarlo de la lista: `enemigos.Remove(other.gameObject);` y luego `Destroy(other.gameObject);`  
D) Desactivar el collider de la bala

**Respuesta correcta: C**

**Retroalimentación:** La lista guarda una **referencia** al enemigo; `Destroy` elimina el objeto de la escena, pero no lo quita de la lista. Por eso, al recorrerla, se intenta usar un objeto que ya no existe. Hay que mantener la lista sincronizada quitando la referencia al destruir. Retrasar el `Destroy` solo aplaza el error, y `Clear()` haría que el manager pierda a todos los demás enemigos.

---

## Q18. Moverse a los puntos marcados — Fácil — Tema: Queue

**Escenario:** En un juego de estrategia 2D, el jugador hace clic en varios puntos del mapa y la unidad debe visitarlos **en el orden de los clics**, uno tras otro.

**Objetivo:** Elegir cómo almacenar los destinos.

A) `Queue<Vector2>`: `Enqueue()` en cada clic y `Dequeue()` cuando la unidad llega al destino actual  
B) `Stack<Vector2>`: `Push()` en cada clic y `Pop()` al llegar  
C) Una sola variable `Vector2 destino` que se sobrescribe en cada clic  
D) `Vector2[] destinos = new Vector2[3]`

**Respuesta correcta: A**

**Retroalimentación:** Los destinos se visitan en el orden en que se agregaron: FIFO, una `Queue`. Un `Stack` visitaría primero el último clic. Una sola variable olvida los clics anteriores, y un arreglo de 3 posiciones limita arbitrariamente cuántos puntos se pueden marcar.

---

## Q19. Deshacer en un puzzle — Fácil — Tema: Stack

**Escenario:** En un puzzle de empujar cajas por casillas, el jugador puede presionar `Z` para deshacer su último movimiento, varias veces seguidas, hasta volver al inicio del nivel.

**Objetivo:** Elegir la estructura para el historial de movimientos.

A) `Queue<Movimiento>`, deshaciendo con `Dequeue()`  
B) `Stack<Movimiento>`, guardando cada movimiento con `Push()` y deshaciendo con `Pop()`  
C) `List<Movimiento>`, deshaciendo siempre el índice 0  
D) Una variable `Movimiento ultimo`

**Respuesta correcta: B**

**Retroalimentación:** Deshacer siempre revierte el movimiento **más reciente**, y luego el anterior a ese: LIFO. `Pop()` entrega exactamente ese orden. `Dequeue()` y el índice 0 revertirían el movimiento más antiguo. Una sola variable solo permite deshacer una vez.

---

## Q20. Tres necesidades, tres estructuras — Fácil — Tema: Integración

**Escenario:** Un juego necesita:

```
I.   Hacer aparecer enemigos en el orden en que fueron programados.
II.  Deshacer la última construcción colocada por el jugador.
III. Llevar el registro de las balas activas, que se destruyen en cualquier orden.
```

**Objetivo:** Elegir la combinación más adecuada.

A) I: `Stack` — II: `Queue` — III: `List`  
B) I: `List` — II: `List` — III: `Queue`  
C) I: `Queue` — II: `List` — III: `Stack`  
D) I: `Queue` — II: `Stack` — III: `List`

**Respuesta correcta: D**

**Retroalimentación:** **I** es FIFO, una `Queue`. **II** es LIFO, un `Stack`. **III** requiere quitar elementos específicos en cualquier orden, una `List`. Elegir la estructura según el **orden de salida** que exige el problema es la decisión clave en todos estos casos.

---

## Q21. Máximo de balas en pantalla — Intermedio — Tema: List

**Escenario:** En un juego de tanques, el jugador puede tener **como máximo 2 balas** en pantalla al mismo tiempo. Cada bala se destruye al chocar con algo (`OnCollisionEnter2D`).

**Objetivo:** Elegir el diseño que respeta el límite en todo momento.

A) Guardar las balas en una `List<GameObject>`: agregar al disparar, quitar cuando la bala se destruye, y permitir el disparo solo si `balas.Count < 2`  
B) Contar los disparos con un `int` que solo se incrementa, y disparar mientras sea menor que 2  
C) Usar un `GameObject[] balas = new GameObject[2]` y disparar siempre en `balas[0]`  
D) Esperar 1 segundo entre disparos con una corrutina

**Respuesta correcta: A**

**Retroalimentación:** El límite depende de cuántas balas **siguen activas**, no de cuántas se dispararon. Con una lista sincronizada (agregar al disparar y quitar al destruir), `Count` siempre refleja las balas en pantalla. Un contador que solo sube bloquearía el disparo para siempre tras 2 tiros. Usar siempre `balas[0]` sobrescribe la referencia, y un tiempo de espera no garantiza el límite si las balas tardan en chocar.

---

## Q22. Reciclar balas — Intermedio — Tema: Queue

**Escenario:** El juego crea 20 balas al inicio y las guarda desactivadas en una `Queue<GameObject> disponibles`. Al disparar se toma una con `Dequeue()`, se posiciona y se activa.

```csharp
void OnCollisionEnter2D(Collision2D col)
{
    // La bala chocó con algo
    // ???
}
```

**Objetivo:** Elegir lo que debe hacer la bala al chocar para que el sistema de reciclaje funcione.

A) `Destroy(gameObject);`  
B) `disponibles.Clear();`  
C) `gameObject.SetActive(false);` y devolverla con `disponibles.Enqueue(gameObject);`  
D) `disponibles.Dequeue();`

**Respuesta correcta: C**

**Retroalimentación:** La idea del reciclaje (*object pool*) es **no destruir**: la bala se desactiva y vuelve a la cola para reutilizarse en un disparo posterior. Con `Destroy` la cola se quedaría vacía tras 20 disparos. `Clear()` perdería todas las balas disponibles, y `Dequeue()` sacaría otra bala en lugar de devolver la que chocó.

---

## Q23. Explosión en cruz — Intermedio — Tema: Matrices

**Escenario:** En un juego de colocar bombas en una cuadrícula, la explosión avanza hacia la derecha hasta `alcance` casillas. Las casillas vacías dejan pasar la explosión; el **ladrillo** se destruye y detiene la explosión; el **acero** no se destruye y también la detiene.

```csharp
for (int i = 1; i <= alcance; i++)
{
    int c2 = c + i;
    if (c2 >= mapa[r].Length) break;

    if (mapa[r][c2] == ACERO)
    {
        ______;
    }
    if (mapa[r][c2] == LADRILLO)
    {
        DestruirLadrillo(r, c2);
        break;
    }
    MostrarFuego(r, c2);
}
```

**Objetivo:** Elegir la instrucción para el caso del acero.

A) `continue`  
B) `break`  
C) `return`  
D) `mapa[r][c2] = 0`

**Respuesta correcta: B**

**Retroalimentación:** `break` detiene solo el avance **en esta dirección**, que es exactamente lo que hace el acero. `continue` saltaría la casilla de acero y la explosión lo atravesaría. `return` saldría de todo el método y cancelaría también las otras direcciones de la explosión (izquierda, arriba y abajo). Asignar 0 destruiría el acero, que debe ser indestructible.

---

## Q24. Carriles sin repetir — Intermedio — Tema: Arreglos

**Escenario:** En un juego de cruzar la carretera, los autos aparecen en uno de 4 carriles (`float[] posicionesY`). Se quiere que **nunca aparezcan dos autos seguidos en el mismo carril**.

**Objetivo:** Elegir la lógica correcta.

A) `int carril = Random.Range(0, posicionesY.Length - 1);`  
B) Ordenar el arreglo `posicionesY` antes de cada spawn  
C) `int carril = (ultimoCarril + 1) % posicionesY.Length;` sin ningún componente aleatorio  
D) Guardar `ultimoCarril` y elegir otro índice aleatorio mientras sea igual al último; después actualizar `ultimoCarril`

**Respuesta correcta: D**

**Retroalimentación:** Recordar el último carril y volver a sortear mientras coincida garantiza que nunca se repita, manteniendo el azar (funciona siempre que haya más de un carril). La opción A solo excluye el último carril del arreglo, pero sí puede repetir. La C no repite carriles, pero el patrón es completamente predecible: el jugador sabrá siempre dónde aparecerá el siguiente auto. Ordenar el arreglo no tiene relación con el problema.

---

## Q25. Misil al enemigo más cercano — Intermedio — Tema: List

**Escenario:** Un misil teledirigido debe elegir como objetivo al enemigo **más cercano** de la lista `enemigos`.

```csharp
GameObject masCercano = null;
float menorDist = ______;

foreach (GameObject e in enemigos)
{
    float d = Vector2.Distance(transform.position, e.transform.position);
    if (d < menorDist)
    {
        menorDist = d;
        masCercano = e;
    }
}
```

**Objetivo:** Elegir el valor inicial de `menorDist`.

A) `Mathf.Infinity`  
B) `0f`  
C) `enemigos.Count`  
D) `-1f`

**Respuesta correcta: A**

**Retroalimentación:** Para encontrar un mínimo, el valor inicial debe ser mayor que cualquier distancia posible, de modo que el primer enemigo siempre lo reemplace. `Mathf.Infinity` cumple esa condición. Con `0f` o `-1f` ninguna distancia sería menor y `masCercano` quedaría en `null`. `enemigos.Count` es una cantidad de elementos, no una distancia: podría ser menor que la distancia real y descartar a todos los enemigos.

---

## Q26. Un personaje muere esperando turno — Intermedio — Tema: Queue

**Escenario:** En un combate por turnos, los personajes esperan en una `Queue<Personaje>`. Un hechizo de área puede matar a un personaje **que todavía está en medio de la cola**. `Queue` no permite eliminar un elemento del medio.

**Objetivo:** Elegir la solución más simple que mantiene el orden de turnos.

A) Usar `Clear()` y volver a encolar a todos los personajes cada vez que alguien muere  
B) Cambiar la `Queue` por un `Stack`  
C) Al tomar el siguiente turno con `Dequeue()`, verificar si el personaje sigue vivo; si está muerto, descartarlo y tomar el siguiente  
D) Ignorar el problema, porque los personajes muertos no hacen nada

**Respuesta correcta: C**

**Retroalimentación:** La validación "perezosa" (revisar al momento de sacar el elemento) mantiene la cola intacta y salta a los personajes muertos cuando les tocaría su turno. Vaciar y reconstruir la cola funciona, pero es más complejo y propenso a errores de orden. Un `Stack` cambia el orden de los turnos. Ignorar el problema haría que un personaje muerto "consuma" un turno o, peor, que actúe.

---

## Q27. Pila de descarte — Intermedio — Tema: Stack

**Escenario:** En un juego de cartas, las cartas jugadas se colocan en una pila de descarte. Un jugador solo puede jugar una carta si es **del mismo color** que la carta superior de la pila.

```csharp
public bool IntentarJugar(Carta carta)
{
    if (descarte.Count == 0 || ______)
    {
        descarte.Push(carta);
        return true;
    }
    return false;
}
```

**Objetivo:** Elegir la condición que valida la jugada sin alterar la pila.

A) `descarte.Pop().color == carta.color`  
B) `descarte.Peek().color == carta.color`  
C) `descarte.Contains(carta)`  
D) `descarte.Count == carta.color`

**Respuesta correcta: B**

**Retroalimentación:** `Peek()` consulta la carta superior **sin retirarla**, lo correcto para una validación. Con `Pop()` la carta superior se perdería aunque la jugada no sea válida. `Contains` revisa si la carta ya está en algún lugar de la pila, lo cual no tiene relación con la regla del color, y comparar `Count` con un color carece de sentido.

---

## Q28. Posición inicial en el archivo — Intermedio — Tema: Archivos y Parseo

**Escenario:** El diseñador quiere marcar la posición inicial del jugador con la letra `P` dentro del archivo del mapa:

```
1,1,1,1
1,P,0,1
1,1,1,1
```

El parser actual usa `int.TryParse` para cada celda.

**Objetivo:** Elegir la forma más adecuada de soportar la `P`.

A) No cambiar nada: `TryParse` convertirá la `P` en la posición del jugador  
B) Pedir al diseñador que escriba la posición del jugador en otro archivo  
C) Cambiar `TryParse` por `int.Parse`  
D) Antes de convertir cada token, revisar si es `"P"`: en ese caso guardar `(r, c)` como posición inicial y asignar `0` a la celda; en caso contrario usar `TryParse`

**Respuesta correcta: D**

**Retroalimentación:** Los símbolos especiales deben detectarse **antes** de la conversión numérica. Así se registra la posición del jugador y la celda queda como pasillo vacío. `TryParse` solo convertiría la `P` en `0`, sin guardar la posición: el jugador nunca sabría dónde aparecer. `int.Parse` lanzaría una excepción, y un segundo archivo complica la edición sin necesidad.

---

## Q29. Nivel con forma irregular — Intermedio — Tema: Matrices

**Escenario:** Un nivel tiene forma de pirámide: la primera fila tiene 3 celdas, la segunda 5, la tercera 7, y así sucesivamente. El mapa se lee desde un archivo `.txt`.

**Objetivo:** Elegir la representación más adecuada.

A) `int[][]`, porque cada fila es un arreglo independiente con su propia longitud  
B) `int[,]` del tamaño de la fila más larga, rellenando las celdas sobrantes con valores inventados  
C) `int[]` con todas las celdas seguidas, sin indicar dónde termina cada fila  
D) `Queue<int>` con todas las celdas

**Respuesta correcta: A**

**Retroalimentación:** Una matriz escalonada permite filas de longitudes diferentes y se construye de forma natural línea por línea. Con `int[,]` habría que inventar valores de relleno y recordar cuáles son reales. Un arreglo plano pierde la estructura de filas, y una cola no permite consultar una celda por su posición.

---

## Q30. Torreta y zona de detección — Intermedio — Tema: List

**Escenario:** Una torreta tiene un `CircleCollider2D` grande con `isTrigger` como zona de detección. Los enemigos entran y salen de la zona **en cualquier orden**. La torreta debe disparar al enemigo que **lleva más tiempo dentro** de la zona.

**Objetivo:** Elegir el diseño más adecuado.

A) `Queue<GameObject>`: `Enqueue` en `OnTriggerEnter2D` y `Dequeue` en `OnTriggerExit2D`  
B) `Stack<GameObject>`: `Push` al entrar, `Pop` al salir y disparar a `Peek()`  
C) `List<GameObject>`: `Add` en `OnTriggerEnter2D`, `Remove(other.gameObject)` en `OnTriggerExit2D`, y disparar a `enemigos[0]` si `Count > 0`  
D) Una sola variable `GameObject objetivo` que se sobrescribe en cada `OnTriggerEnter2D`

**Respuesta correcta: C**

**Retroalimentación:** La lista conserva el orden de entrada (el índice 0 es el que lleva más tiempo dentro) y, además, permite quitar **al enemigo exacto** que sale, sin importar su posición. Con una `Queue`, `Dequeue` en `OnTriggerExit2D` quitaría al primero de la fila aunque el que salió sea otro. El `Stack` apuntaría al último que entró. Una sola variable apunta siempre al más reciente y no sabe qué pasa cuando sale.

---

## Q31. Robot programable — Intermedio — Tema: Queue

**Escenario:** En un puzzle, el jugador arma una secuencia de órdenes (`Arriba`, `Arriba`, `Derecha`, …) que se guarda en `Queue<string> comandos`. Al presionar **Play**, el robot debe ejecutar **todas** las órdenes en orden, con medio segundo entre cada una.

**Objetivo:** Elegir la corrutina correcta.

A)
```csharp
for (int i = 0; i < comandos.Count; i++)
{
    Mover(comandos.Dequeue());
    yield return new WaitForSeconds(0.5f);
}
```
B)
```csharp
while (comandos.Count > 0)
{
    Mover(comandos.Dequeue());
    yield return new WaitForSeconds(0.5f);
}
```
C)
```csharp
while (comandos.Count > 0)
{
    Mover(comandos.Peek());
    yield return new WaitForSeconds(0.5f);
}
```
D)
```csharp
foreach (string cmd in comandos)
{
    Mover(comandos.Dequeue());
    yield return new WaitForSeconds(0.5f);
}
```

**Respuesta correcta: B**

**Retroalimentación:** El `while` se repite mientras queden órdenes y `Dequeue()` consume una en cada vuelta: se ejecutan todas, en orden. En la opción A, `Count` disminuye en cada `Dequeue` mientras `i` aumenta, así que el bucle termina **a la mitad** de la secuencia. En la C, `Peek()` nunca retira la orden: el robot repite la primera orden para siempre. En la D, modificar la cola dentro de su propio `foreach` lanza `InvalidOperationException`.

---

## Q32. Volver a la sala anterior — Intermedio — Tema: Stack

**Escenario:** En un juego de exploración, cada sala visitada se guarda con `Push()` en `Stack<Sala> historial`, **incluida la sala actual**, que siempre está en la cima. El botón **Regresar** debe llevar al jugador a la sala en la que estaba antes de la actual.

**Objetivo:** Elegir la lógica correcta del botón Regresar.

A) `IrA(historial.Pop());`  
B) `IrA(historial.Peek());`  
C) `historial.Clear(); IrA(salaInicial);`  
D) `if (historial.Count > 1) { historial.Pop(); IrA(historial.Peek()); }`

**Respuesta correcta: D**

**Retroalimentación:** Como la cima es la sala **actual**, primero hay que retirarla con `Pop()`; entonces la nueva cima es la sala anterior, que se consulta con `Peek()` (y se queda en la pila porque ahora es la actual). La condición `Count > 1` evita quedarse sin sala. La opción A devuelve la sala actual, así que el jugador "regresa" al mismo lugar. La B tampoco cambia de sala, y la C pierde todo el historial.

---

## Q33. Multiplicador de combo — Intermedio — Tema: Arreglos

**Escenario:** Los multiplicadores de puntaje se guardan en `int[] multiplicadores = { 1, 2, 4, 8 };`. La variable `combo` aumenta con cada enemigo derrotado sin recibir daño y **puede superar 3**. A partir del combo 3, el multiplicador debe quedarse en 8.

**Objetivo:** Elegir cómo obtener el multiplicador sin errores.

A) `multiplicadores[Mathf.Min(combo, multiplicadores.Length - 1)]`  
B) `multiplicadores[combo]`  
C) `multiplicadores[combo % multiplicadores.Length]`  
D) `multiplicadores[multiplicadores.Length]`

**Respuesta correcta: A**

**Retroalimentación:** `Mathf.Min` limita el índice al último válido (3), así que cualquier combo mayor usa el multiplicador 8. Con `multiplicadores[combo]` se lanza `IndexOutOfRangeException` en el combo 4. El módulo hace que el multiplicador **vuelva a 1** en el combo 4, castigando al jugador. `multiplicadores[Length]` está siempre fuera de rango.

---

## Q34. ¿Quién avisa que el enemigo murió? — Intermedio — Tema: Integración

**Escenario:** El `EnemyManager` guarda los enemigos vivos en una `List<Enemigo>`. Los enemigos pueden morir por balas, por trampas, por caer al vacío o por explosiones, y cada causa está programada en scripts diferentes.

**Objetivo:** Elegir el diseño que mantiene la lista siempre correcta con menos riesgo de errores.

A) Que cada script que causa daño (bala, trampa, explosión…) llame a `manager.enemigos.Remove(...)` antes de destruir al enemigo  
B) Recorrer cada frame todas las balas y trampas para adivinar qué enemigos murieron  
C) Que el propio `Enemigo`, en su método `Morir()`, se quite de la lista del manager (por ejemplo, `manager.Quitar(this)`) y luego se destruya; todas las causas de daño solo llaman a `RecibirDanio()`  
D) Vaciar la lista con `Clear()` cada 10 segundos

**Respuesta correcta: C**

**Retroalimentación:** Si la eliminación ocurre en **un solo lugar** (`Morir()`), todas las causas de muerte, presentes y futuras, mantienen la lista sincronizada automáticamente. Repartir el `Remove` entre muchos scripts (A) funciona hasta que alguien agrega una causa nueva y se olvida de hacerlo. Adivinar desde fuera es frágil y costoso, y vaciar la lista periódicamente borra también a los enemigos vivos.

---

## Q35. Colocar torres en la cuadrícula — Intermedio — Tema: Matrices

**Escenario:** En un juego de defensa de torres, el mapa es `int[,] mapa` (`0` = libre, `1` = camino, `2` = torre). El jugador hace clic en una celda `(r, c)` para colocar una torre. Una celda solo admite una torre y no se puede construir sobre el camino.

**Objetivo:** Elegir la lógica correcta.

A) Instanciar la torre en `(r, c)` siempre que el jugador tenga dinero  
B) `if (mapa[r, c] == 0) { Instantiate(torrePrefab, pos, Quaternion.identity); mapa[r, c] = 2; }`  
C) `if (mapa[r, c] != 1) Instantiate(torrePrefab, pos, Quaternion.identity);`  
D) `mapa[r, c] = 2; if (mapa[r, c] == 0) Instantiate(torrePrefab, pos, Quaternion.identity);`

**Respuesta correcta: B**

**Retroalimentación:** Se verifica que la celda esté libre y, después de construir, se **marca como ocupada** en la matriz para que no se pueda construir otra torre encima. La opción C impide construir sobre el camino, pero no actualiza la matriz, así que se pueden apilar torres infinitas en la misma celda. La D marca la celda antes de comprobarla, por lo que la condición nunca se cumple. La A ignora todas las reglas.

---

## Q36. Pasar al siguiente nivel — Intermedio — Tema: Archivos y Parseo

**Escenario:** Los niveles están en `TextAsset[] niveles` (asignado en el Inspector) y `nivelActual` guarda el índice del nivel en juego. Al completar un nivel se debe cargar el siguiente, y al completar **el último** se debe mostrar la pantalla de victoria.

**Objetivo:** Elegir la lógica correcta.

A) `nivelActual++; CargarNivel(niveles[nivelActual].text);`  
B) `nivelActual = (nivelActual + 1) % niveles.Length; CargarNivel(niveles[nivelActual].text);`  
C) `if (nivelActual < niveles.Length) CargarNivel(niveles[nivelActual + 1].text);`  
D) `if (nivelActual + 1 < niveles.Length) { nivelActual++; CargarNivel(niveles[nivelActual].text); } else { MostrarVictoria(); }`

**Respuesta correcta: D**

**Retroalimentación:** Se comprueba **antes** de avanzar que exista un nivel siguiente; si no existe, el juego terminó. La opción A lanza `IndexOutOfRangeException` al completar el último nivel. La B reinicia en el nivel 1 sin mostrar la victoria. La C usa una condición incorrecta: cuando `nivelActual` es el último índice, la condición se cumple y `nivelActual + 1` queda fuera de rango.

---

## Q37. Oleadas con tiempos distintos — Intermedio — Tema: Queue

**Escenario:** Cada enemigo de una oleada tiene su propio prefab y su propio tiempo de espera antes de aparecer (por ejemplo: murciélago tras 1 s, golem tras 4 s, murciélago tras 0.5 s).

**Objetivo:** Elegir la forma más clara y segura de almacenar la oleada.

A) Una clase `EntradaOleada { GameObject prefab; float espera; }` y una `Queue<EntradaOleada>`  
B) Dos colas separadas, `Queue<GameObject>` y `Queue<float>`, que deben retirarse siempre juntas  
C) Una `Queue<GameObject>` y un único tiempo de espera para todos  
D) Un `Stack<EntradaOleada>`

**Respuesta correcta: A**

**Retroalimentación:** Agrupar en un solo objeto los datos que pertenecen juntos (prefab y espera) garantiza que nunca se desincronicen, y la `Queue` mantiene el orden de la oleada. Dos colas paralelas funcionan, pero basta un `Dequeue` olvidado en una de ellas para que todos los tiempos queden desfasados. Un único tiempo no cumple el requerimiento, y un `Stack` invertiría el orden de la oleada.

---

## Q38. Guardar el movimiento para deshacer — Intermedio — Tema: Stack

**Escenario:** En un puzzle por casillas, cada movimiento del jugador debe poder deshacerse con `Z`, devolviéndolo a la posición en la que estaba antes de moverse.

**Objetivo:** Elegir el par de métodos correcto.

A)
```csharp
void Mover(Vector3 destino) { transform.position = destino; historial.Push(transform.position); }
void Deshacer() { if (historial.Count > 0) transform.position = historial.Pop(); }
```
B)
```csharp
void Mover(Vector3 destino) { historial.Push(destino); transform.position = destino; }
void Deshacer() { if (historial.Count > 0) transform.position = historial.Peek(); }
```
C)
```csharp
void Mover(Vector3 destino) { historial.Push(transform.position); transform.position = destino; }
void Deshacer() { if (historial.Count > 0) transform.position = historial.Pop(); }
```
D)
```csharp
void Mover(Vector3 destino) { historial.Push(transform.position); transform.position = destino; }
void Deshacer() { transform.position = historial.Pop(); historial.Clear(); }
```

**Respuesta correcta: C**

**Retroalimentación:** Hay que guardar la posición **anterior** al movimiento (antes de cambiarla) y, al deshacer, recuperarla con `Pop()`. En la A y la B se guarda el destino, así que deshacer deja al jugador donde ya está. Además, la B usa `Peek()`, que no retira el registro. La D funciona solo una vez: `Clear()` borra el resto del historial y, sin validar `Count`, falla con la pila vacía.

---

## Q39. Fin de partida — Intermedio — Tema: List

**Escenario:** Cuando el jugador pierde, todos los enemigos de la lista `enemigos` deben desaparecer de la escena y la lista debe quedar vacía para la siguiente partida.

**Objetivo:** Elegir el código correcto.

A)
```csharp
enemigos.Clear();
foreach (GameObject e in enemigos) Destroy(e);
```
B)
```csharp
foreach (GameObject e in enemigos) Destroy(e);
enemigos.Clear();
```
C)
```csharp
foreach (GameObject e in enemigos) enemigos.Remove(e);
```
D)
```csharp
enemigos.Clear();
```

**Respuesta correcta: B**

**Retroalimentación:** Primero se destruye cada GameObject usando las referencias de la lista y **después** se vacía la lista. `Destroy` no modifica la lista, así que el `foreach` es seguro. En la A la lista se vacía antes, por lo que el `foreach` no recorre nada y los enemigos siguen en la escena. La C modifica la lista dentro del `foreach` (lanza `InvalidOperationException`) y nunca destruye nada. La D solo vacía la lista.

---

## Q40. Monedas generadas desde el mapa — Intermedio — Tema: List

**Escenario:** Las monedas se instancian al leer el archivo del mapa (valor `7` = moneda). **No se sabe cuántas monedas hay** hasta terminar de recorrer todo el mapa, y cada nivel tiene una cantidad distinta. Durante la partida, las monedas recogidas deben quitarse de la colección.

**Objetivo:** Elegir la colección para las monedas.

A) `GameObject[] monedas = new GameObject[100];`  
B) `Stack<GameObject> monedas`  
C) `GameObject[,] monedas` con el tamaño del mapa  
D) `List<GameObject> monedas`, con `Add()` al instanciar y `Remove()` al recoger

**Respuesta correcta: D**

**Retroalimentación:** Cuando la cantidad se conoce solo **en tiempo de ejecución** y cambia durante la partida, `List` es la elección natural: crece al instanciar y se reduce al recoger, y `Count` indica cuántas faltan. Un arreglo de 100 es un límite arbitrario (sobra o falta espacio). Un `Stack` no permite quitar la moneda específica que se recogió, y una matriz del tamaño del mapa desperdicia espacio y complica contar las monedas restantes.

---

## Q41. Rebobinar solo los últimos 3 segundos — Difícil — Tema: Stack

**Escenario:** El jugador puede rebobinar el tiempo, pero **solo los últimos 3 segundos** (150 posiciones registradas en `FixedUpdate`). Actualmente se usa un `Stack<Vector2>` con un `Push` por cada `FixedUpdate`, y la memoria crece sin límite durante partidas largas.

**Objetivo:** Elegir la solución más adecuada.

A) Llamar a `Clear()` en la pila cada 3 segundos  
B) Usar una `List<Vector2>`: agregar al final en cada `FixedUpdate` y, si `Count > 150`, eliminar el más antiguo con `RemoveAt(0)`; al rebobinar, recorrer desde el final hacia el inicio  
C) Mantener el `Stack` y hacer `Pop()` cuando tenga más de 150 elementos  
D) Usar una `Queue<Vector2>` y rebobinar con `Dequeue()`

**Respuesta correcta: B**

**Retroalimentación:** Se necesitan dos cosas: descartar el registro **más antiguo** cuando se excede el límite y recorrer los registros del **más reciente al más antiguo** al rebobinar. Un `Stack` solo da acceso a la cima: `Pop()` eliminaría la posición más reciente, no la más antigua. `Clear()` haría que, justo después del borrado, no hubiera nada que rebobinar. Una `Queue` descarta bien lo antiguo, pero `Dequeue()` rebobinaría en el orden equivocado (de lo más antiguo a lo más reciente). La `List` permite ambas cosas. Un arreglo circular de 150 posiciones sería todavía más eficiente.

---

## Q42. Búsqueda del camino más corto — Difícil — Tema: Queue

**Escenario:** Un fantasma busca el camino más corto hacia el jugador en la cuadrícula del laberinto. Para ello usa una búsqueda en anchura: encola la celda inicial, y mientras la cola no esté vacía, hace `Dequeue()` de una celda y encola sus vecinas libres. Un estudiante **olvidó marcar las celdas como visitadas** (`bool[,] visitado`).

**Objetivo:** Elegir qué sucede y por qué.

A) Las celdas se vuelven a encolar una y otra vez (A encola a B y B vuelve a encolar a A), la cola nunca se vacía y el juego se congela  
B) El algoritmo funciona igual, solo que un poco más lento  
C) Se lanza `IndexOutOfRangeException` en la primera iteración  
D) El fantasma encuentra el camino más largo en lugar del más corto

**Respuesta correcta: A**

**Retroalimentación:** Sin marcar las celdas visitadas, cada celda vuelve a encolar a sus vecinas, incluida la celda de la que vino. La cola crece sin fin, el `while (cola.Count > 0)` nunca termina y, como corre en un solo frame, Unity se congela. La matriz `visitado` (marcada al **encolar** cada celda) garantiza que cada celda entre a la cola una sola vez. El error no tiene relación con los índices ni invierte el resultado de la búsqueda.

---

## Q43. Bloques conectados del mismo color — Difícil — Tema: Integración

**Escenario:** En un puzzle de bloques de colores sobre una cuadrícula `int[,] colores`, al hacer clic en un bloque se deben eliminar **todos los bloques del mismo color conectados** con él (arriba, abajo, izquierda y derecha), sin importar cuántos sean.

**Objetivo:** Elegir el algoritmo correcto.

A) Revisar solo las 4 celdas vecinas del bloque clicado y eliminar las que tengan el mismo color  
B) Recorrer toda la matriz y eliminar todos los bloques de ese color, estén conectados o no  
C) Usar un `Stack` de celdas, pero sin registrar cuáles ya fueron procesadas  
D) Usar un `Stack<Vector2Int>` con la celda inicial y una matriz `bool[,] visitado`; mientras la pila no esté vacía, hacer `Pop()`, guardar la celda y hacer `Push()` de las vecinas válidas del mismo color que no estén visitadas, marcándolas como visitadas

**Respuesta correcta: D**

**Retroalimentación:** Este algoritmo (relleno por inundación o *flood fill*) explora desde la celda inicial hacia todas las celdas conectadas, a cualquier distancia, y la matriz `visitado` impide procesar una celda dos veces. Revisar solo las 4 vecinas no detecta bloques conectados a mayor distancia. Eliminar todos los del mismo color ignora la regla de conexión. Sin `visitado`, dos celdas vecinas se apilarían mutuamente para siempre.

---

## Q44. La torreta apunta a un fantasma — Difícil — Tema: List

**Escenario:** La torreta de Q30 guarda los enemigos que entran a su zona en `List<GameObject> enemigos` y dispara a `enemigos[0]`. Cuando un enemigo muere **dentro de la zona** (destruido por otra torreta), a veces la lista conserva una referencia a un objeto destruido y aparece una `MissingReferenceException` al apuntarle.

**Objetivo:** Elegir la solución más robusta dentro del script de la torreta.

A) Llamar a `enemigos.Clear()` en cada frame  
B) Cambiar `enemigos[0]` por `enemigos[enemigos.Count - 1]`  
C) Antes de elegir el objetivo, recorrer la lista **hacia atrás** y eliminar con `RemoveAt(i)` las posiciones donde `enemigos[i] == null`  
D) Aumentar el radio del `CircleCollider2D`

**Respuesta correcta: C**

**Retroalimentación:** En Unity, una referencia a un objeto destruido se compara como igual a `null`. Limpiar esas entradas antes de usar la lista garantiza que `enemigos[0]` sea un enemigo vivo, sin importar quién lo destruyó. Se recorre hacia atrás para no saltarse elementos al eliminar. Vaciar la lista cada frame haría que la torreta olvide a los enemigos que siguen dentro. Elegir el último elemento no evita que también esté destruido, y cambiar el radio no tiene relación con el problema.

---

## Q45. Validar que el mapa sea rectangular — Difícil — Tema: Archivos y Parseo

**Escenario:** El generador de niveles exige que el mapa sea perfectamente rectangular. Algunos diseñadores olvidan un valor en una fila, y el juego carga el nivel con huecos sin que nadie lo note. Después de `ParseTextToMatrix` se obtiene `int[][] mapa`.

**Objetivo:** Elegir la validación más útil.

A) Convertir la matriz a `int[,]` y dejar que falle si algo está mal  
B) Recorrer las filas y comparar `mapa[r].Length` con `mapa[0].Length`; si alguna es distinta, registrar `Debug.LogError` indicando el número de fila y su longitud, y no construir el nivel  
C) Verificar únicamente que `mapa.Length > 0`  
D) Rellenar las filas cortas con ceros sin avisar

**Respuesta correcta: B**

**Retroalimentación:** La validación compara cada fila con la primera y, ante un error, informa **dónde** está el problema (fila y longitud), para que el diseñador lo corrija rápidamente. Dejar que algo falle más adelante produce mensajes confusos que no indican la fila. Verificar solo que haya filas no detecta el problema, y rellenar con ceros sin avisar oculta el error, que es justo lo que se quería evitar.

---

## Q46. Vehículos de emergencia primero — Difícil — Tema: Queue

**Escenario:** En un simulador de tráfico, los autos esperan en una `Queue` para entrar a la carretera. Las **ambulancias** deben entrar antes que cualquier auto normal que esté esperando, pero entre ambulancias se respeta el orden de llegada (y lo mismo entre autos normales).

**Objetivo:** Elegir el diseño más adecuado.

A) Dos colas: `ambulancias` y `normales`. Al liberar un vehículo, si `ambulancias.Count > 0` se hace `Dequeue()` de esa cola; si no, de `normales`  
B) Una sola `Queue` en la que las ambulancias se encolan dos veces  
C) Un `Stack` para todos los vehículos  
D) Una sola `Queue`, ordenada alfabéticamente por tipo de vehículo cada vez que llega uno

**Respuesta correcta: A**

**Retroalimentación:** Dos colas mantienen el orden FIFO dentro de cada tipo, y revisar primero la cola de ambulancias implementa la prioridad de forma simple y clara. Encolar dos veces duplica vehículos en lugar de adelantarlos. Un `Stack` atendería al último en llegar. Una `Queue` no se puede ordenar directamente, y reconstruirla en cada llegada es complejo e innecesario.

---

## Q47. Escape en el menú principal — Difícil — Tema: Stack

**Escenario:** Los paneles de menú se gestionan con `Stack<GameObject> paneles`. El menú principal se agrega con `Push()` al iniciar y siempre debe quedar visible como base. La tecla `Escape` cierra el panel actual y muestra el anterior.

**Objetivo:** Elegir el código correcto para `Escape`.

A)
```csharp
paneles.Pop().SetActive(false);
paneles.Peek().SetActive(true);
```
B)
```csharp
if (paneles.Count > 0) paneles.Pop().SetActive(false);
```
C)
```csharp
if (paneles.Count > 1)
{
    paneles.Pop().SetActive(false);
    paneles.Peek().SetActive(true);
}
```
D)
```csharp
paneles.Peek().SetActive(false);
paneles.Pop().SetActive(true);
```

**Respuesta correcta: C**

**Retroalimentación:** Con `Count > 1` se asegura que siempre quede al menos el menú principal. Se retira y oculta el panel actual, y luego se muestra el nuevo panel superior **sin retirarlo**. La opción A, en el menú principal, lo cierra y luego `Peek()` lanza una excepción con la pila vacía. La B permite cerrar el menú principal y nunca muestra el panel anterior. La D oculta el panel actual y lo vuelve a activar con `Pop()`, dejando en pantalla el mismo panel.

---

## Q48. La serpiente que crece — Difícil — Tema: Queue

**Escenario:** En un juego de la serpiente sobre una cuadrícula, el cuerpo se guarda en una `Queue<Vector2Int> cuerpo`: la **cola** de la serpiente es el primer elemento y la **cabeza** es el último. En cada paso la cabeza avanza a una nueva celda. Si la serpiente come una manzana, debe crecer un segmento.

**Objetivo:** Elegir la lógica correcta de cada paso.

A) Siempre `cuerpo.Dequeue()` y luego `cuerpo.Enqueue(nuevaCabeza)`, y al comer volver a hacer `Dequeue()`  
B) `cuerpo.Enqueue(nuevaCabeza)` en cada paso, sin `Dequeue()` nunca  
C) `cuerpo.Dequeue()` de la cabeza y `cuerpo.Enqueue()` de la cola  
D) `cuerpo.Enqueue(nuevaCabeza)` en cada paso; si **no** comió, `cuerpo.Dequeue()` para retirar el último segmento de la cola; si comió, no se retira nada

**Respuesta correcta: D**

**Retroalimentación:** Cada paso agrega la nueva cabeza al final. Si la serpiente no comió, el segmento más antiguo (la punta de la cola) se retira con `Dequeue()`, por lo que la longitud se mantiene. Si comió, se omite el `Dequeue()` y la serpiente crece exactamente un segmento. La opción A hace que la serpiente **se encoja** al comer, la B la hace crecer en cada paso, y la C confunde los extremos: `Dequeue()` retira la punta de la cola, no la cabeza.

---

## Q49. Rotar una pieza 90° — Difícil — Tema: Matrices

**Escenario:** Una pieza de un juego de bloques se guarda en una matriz cuadrada `int[,] original` de tamaño `n × n`. Para rotarla 90° **en sentido horario**, se crea una matriz nueva `rotada` del mismo tamaño y se recorre `original` con `r` (fila) y `c` (columna).

```csharp
for (int r = 0; r < n; r++)
    for (int c = 0; c < n; c++)
        ______ = original[r, c];
```

**Objetivo:** Elegir la asignación correcta. (Pista: en una rotación horaria, la esquina superior izquierda pasa a la esquina superior derecha.)

A) `rotada[r, c]`  
B) `rotada[c, n - 1 - r]`  
C) `rotada[n - 1 - c, r]`  
D) `rotada[c, r]`

**Respuesta correcta: B**

**Retroalimentación:** Comprobando con la pista: `(0, 0)` debe ir a `(0, n−1)`. Con `rotada[c, n − 1 − r]` se obtiene `(0, n−1)` ✓. Y la esquina superior derecha `(0, n−1)` va a `(n−1, n−1)`, la esquina inferior derecha ✓. La opción A copia la pieza sin rotarla, la C la rota en sentido **antihorario** y la D la refleja sobre la diagonal (transpuesta), que no es una rotación. Probar con una o dos esquinas es una buena estrategia para verificar fórmulas con índices.

---

## Q50. Diseño de un *endless runner* — Difícil — Tema: Integración

**Escenario:** Un *endless runner* 2D tiene los siguientes requerimientos:

```
I.   3 carriles con posiciones Y fijas, definidas en el Inspector.
II.  Obstáculos que se mueven de derecha a izquierda; los que salen de la pantalla
     se reutilizan en lugar de destruirse.
III. Los obstáculos activos en pantalla deben recorrerse cada frame para moverlos,
     y salen de la pantalla en cualquier orden según su velocidad.
IV.  Un power-up "escudo" que se puede acumular, y al recibir un golpe se consume
     el último escudo obtenido.
```

**Objetivo:** Elegir la combinación de estructuras más adecuada.

A) I: `float[]` — II: `Queue<GameObject>` como reserva de obstáculos reutilizables — III: `List<GameObject>` de obstáculos activos — IV: `Stack<Escudo>`  
B) I: `List<float>` que crece en cada frame — II: `Stack<GameObject>` — III: `Queue<GameObject>` — IV: `Queue<Escudo>`  
C) I: `float[,]` — II: `List<GameObject>` con `Destroy` — III: `Stack<GameObject>` — IV: `int[]`  
D) I: `Queue<float>` — II: `Queue<GameObject>` — III: `Queue<GameObject>` — IV: `List<Escudo>`

**Respuesta correcta: A**

**Retroalimentación:** **I:** un conjunto fijo de valores configurado en el Inspector es un arreglo `float[]`. **II:** la reserva de reutilización (*object pool*) funciona bien con una `Queue`: `Dequeue()` para usar y `Enqueue()` para devolver. **III:** los obstáculos activos se recorren cada frame y salen en cualquier orden, así que se necesita una `List`, que permite quitar cualquier elemento. **IV:** consumir el último escudo obtenido es LIFO, un `Stack`. En las demás opciones, una `Queue` o un `Stack` no permiten quitar al obstáculo exacto que salió, una `Queue` no se muestra en el Inspector, o `Destroy` contradice el requisito de reutilizar.

---

*Fin del examen — COM200 Lógica y Criterio con Estructuras de Datos en Juegos 2D*  
*Total: 50 preguntas | Fácil: 20 | Intermedio: 20 | Difícil: 10*
