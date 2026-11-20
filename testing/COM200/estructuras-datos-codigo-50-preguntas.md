# COM200 — Programación Avanzada
## Examen de Código: Estructuras de Datos en C# para Unity
**50 Preguntas | Distribución: 20 Fácil · 20 Intermedio · 10 Difícil**

> **Instrucciones:** Cada pregunta describe un escenario de uno de los juegos trabajados en clase (Pac-Man, Battle City, Dino Jump, Carrera de autos y Frogger) y el objetivo del script. Lee el código con atención, completa el espacio marcado con `______` o predice el resultado, y elige la única respuesta correcta. Recuerda que las referencias marcadas con `[SerializeField]` o `public` se asignan arrastrando objetos o prefabs desde el editor de Unity.

---

## Q1. Sprites de los bloques — Fácil — Tipo: Completar Código

**Escenario (Battle City):** El mapa usa 4 sprites de bloques (ladrillo, acero, pasto y agua). Se quieren arrastrar los 4 sprites desde el Inspector a un solo campo del script.

**Objetivo:** Declarar el campo que almacenará los sprites.

```csharp
public class GridBuilder : MonoBehaviour
{
    [SerializeField] private ______ wallSprites;
}
```

A) `Sprite[]`  
B) `Sprite[,]`  
C) `Stack<Sprite>`  
D) `int[]`

**Respuesta correcta: A**

**Retroalimentación:** Un conjunto fijo de sprites que se consulta por posición se representa con un arreglo unidimensional `Sprite[]`. Unity lo muestra en el Inspector como una lista en la que se pueden arrastrar los 4 sprites. `Sprite[,]` es una matriz de dos dimensiones que no se necesita aquí, una `Stack` obligaría a sacar elementos para leerlos, y `int[]` guarda números, no sprites.

---

## Q2. Contar puntos de una fila — Fácil — Tipo: Completar Código

**Escenario (Pac-Man):** Una fila del laberinto se guarda en un arreglo, donde `5` representa un punto (*pellet*) que Pac-Man puede comer.

**Objetivo:** Contar cuántos puntos hay en la fila.

```csharp
int[] fila = { 1, 5, 5, 0, 5, 1 };
int puntos = 0;

for (int i = 0; ______; i++)
{
    if (fila[i] == 5) puntos++;
}
```

A) `i <= fila.Length`  
B) `i < fila.Count`  
C) `i < fila.Length`  
D) `i < fila.GetLength(1)`

**Respuesta correcta: C**

**Retroalimentación:** Los índices válidos de un arreglo van de `0` a `Length - 1`, por eso la condición es `i < fila.Length`. Con `<=` el bucle intentaría leer `fila[6]` y lanzaría `IndexOutOfRangeException`. `Count` es la propiedad de `List`, no de los arreglos, y `GetLength(1)` solo existe para matrices de dos o más dimensiones.

---

## Q3. Obstáculo aleatorio — Fácil — Tipo: Completar Código

**Escenario (Dino Jump):** En el Inspector se arrastraron 3 prefabs de cactus al arreglo `obstaculos`. Cada cierto tiempo se debe instanciar uno de ellos al azar.

**Objetivo:** Elegir un índice aleatorio que pueda seleccionar **cualquiera** de los prefabs.

```csharp
[SerializeField] private GameObject[] obstaculos;
[SerializeField] private Transform puntoSpawn;

void GenerarObstaculo()
{
    int indice = Random.Range(0, ______);
    Instantiate(obstaculos[indice], puntoSpawn.position, Quaternion.identity);
}
```

A) `obstaculos.Length - 1`  
B) `obstaculos.Length`  
C) `obstaculos.Length + 1`  
D) `obstaculos.Count`

**Respuesta correcta: B**

**Retroalimentación:** `Random.Range(int min, int max)` con enteros **excluye** el valor máximo, así que `Random.Range(0, 3)` devuelve 0, 1 o 2: todos los índices válidos. Con `Length - 1` nunca aparecería el último cactus, y con `Length + 1` podría salir el índice 3, que provoca `IndexOutOfRangeException`. Los arreglos usan `Length`, no `Count`.

---

## Q4. Registrar los autos creados — Fácil — Tipo: Completar Código

**Escenario (Frogger):** Cada vez que se crea un clon del prefab de auto, se debe guardar en una lista de autos activos para poder moverlos y destruirlos después.

**Objetivo:** Agregar el clon recién creado al final de la lista.

```csharp
private List<GameObject> autos = new List<GameObject>();

void CrearAuto()
{
    GameObject clon = Instantiate(prefabAuto, puntoSpawn.position, Quaternion.identity);
    autos.______(clon);
}
```

A) `Push`  
B) `Enqueue`  
C) `Insert`  
D) `Add`

**Respuesta correcta: D**

**Retroalimentación:** `Add()` agrega un elemento al final de una `List`. `Push` pertenece a `Stack` y `Enqueue` a `Queue`, así que no existen en `List`. `Insert` sí existe, pero requiere dos argumentos (el índice y el elemento): `autos.Insert(0, clon)`.

---

## Q5. Orden de salida de los autos — Fácil — Tipo: Completar Código

**Escenario (Carrera de autos):** Los autos rivales deben salir a la pista uno por uno, **en el mismo orden** en que fueron registrados.

**Objetivo:** Agregar cada prefab de auto a la estructura que respeta ese orden.

```csharp
private Queue<GameObject> colaAutos = new Queue<GameObject>();

void Start()
{
    colaAutos.______(autoRojo);
    colaAutos.______(autoAzul);
    colaAutos.______(autoVerde);
}
```

A) `Enqueue`  
B) `Push`  
C) `Add`  
D) `Dequeue`

**Respuesta correcta: A**

**Retroalimentación:** `Enqueue()` agrega un elemento al final de una `Queue`; al retirarlos con `Dequeue()` saldrán en el mismo orden (FIFO): rojo, azul, verde. `Push` es de `Stack`, `Add` es de `List`, y `Dequeue` retira elementos en lugar de agregarlos.

---

## Q6. Leer una celda de matriz rectangular — Fácil — Tipo: Completar Código

**Escenario (Pac-Man):** El laberinto se guardó en una matriz rectangular `int[,] mapa`, donde `1` es pared.

**Objetivo:** Leer el valor de la fila `r` y la columna `c`.

```csharp
int[,] mapa = new int[,]
{
    { 1, 1, 1, 1 },
    { 1, 5, 0, 1 },
    { 1, 1, 1, 1 }
};

int celda = ______;
```

A) `mapa[r][c]`  
B) `mapa[r, c]`  
C) `mapa(r, c)`  
D) `mapa[c, r]`

**Respuesta correcta: B**

**Retroalimentación:** Una matriz rectangular `int[,]` se accede con un solo par de corchetes y una coma, con la fila primero: `mapa[r, c]`. `mapa[r][c]` es la sintaxis de una matriz escalonada `int[][]`, y los paréntesis no sirven para acceder a arreglos. `mapa[c, r]` compila, pero intercambia fila y columna y lee la celda equivocada (o se sale del rango).

---

## Q7. Leer una celda de matriz escalonada — Fácil — Tipo: Completar Código

**Escenario (Battle City):** El mapa se cargó desde un archivo `.txt` y se obtuvo una matriz escalonada `int[][] mapa`.

**Objetivo:** Leer el tipo de bloque en la fila 2, columna 4.

```csharp
int[][] mapa = MapParser.ParseTextToMatrix(mapFile.text);
int tipo = ______;
```

A) `mapa[2, 4]`  
B) `mapa.GetValue(4)`  
C) `mapa[2][4]`  
D) `mapa[4][2]`

**Respuesta correcta: C**

**Retroalimentación:** En una matriz escalonada (arreglo de arreglos), primero se elige la fila `mapa[2]`, que es un `int[]`, y luego la columna dentro de esa fila: `mapa[2][4]`. La sintaxis con coma (`[2, 4]`) solo es válida en matrices rectangulares `int[,]`. `mapa[4][2]` intercambia fila y columna.

---

## Q8. Contenido del archivo de nivel — Fácil — Tipo: Completar Código

**Escenario (Battle City):** El archivo `nivel1.txt` se arrastró desde la carpeta del proyecto al campo `mapFile` en el Inspector.

**Objetivo:** Obtener todo el contenido del archivo como texto para enviarlo al parser.

```csharp
[SerializeField] private TextAsset mapFile;

void Start()
{
    string contenido = mapFile.______;
    int[][] mapa = MapParser.ParseTextToMatrix(contenido);
}
```

A) `ToString`  
B) `name`  
C) `lines`  
D) `text`

**Respuesta correcta: D**

**Retroalimentación:** La propiedad `.text` de un `TextAsset` devuelve el contenido completo del archivo como un único `string`. `.name` devuelve el nombre del archivo ("nivel1"), no su contenido. `TextAsset` no tiene una propiedad `lines`, y `ToString` (sin paréntesis) no es una propiedad válida.

---

## Q9. Mostrar cuántos autos hay — Fácil — Tipo: Completar Código

**Escenario (Frogger):** Para depurar, se quiere mostrar en consola cuántos autos activos tiene la lista.

```csharp
Debug.Log("Autos activos: " + autos.______);
```

A) `Length`  
B) `Count`  
C) `Count()`  
D) `Size`

**Respuesta correcta: B**

**Retroalimentación:** En `List`, `Queue` y `Stack`, la cantidad de elementos se obtiene con la **propiedad** `Count`, sin paréntesis. `Length` es la propiedad equivalente en los arreglos. `Count()` con paréntesis solo funciona si se agrega `using System.Linq;` y es innecesario. `Size` no existe.

---

## Q10. Usar el último power-up — Fácil — Tipo: Completar Código

**Escenario (Battle City):** El tanque del jugador guarda los power-ups recogidos en una pila. Al presionar la tecla de uso, se activa **el último power-up recogido**, que además se retira de la pila.

```csharp
private Stack<PowerUp> pilaPowerUps = new Stack<PowerUp>();

void UsarPowerUp()
{
    if (pilaPowerUps.Count > 0)
    {
        PowerUp p = pilaPowerUps.______();
        p.Activar();
    }
}
```

A) `Pop`  
B) `Peek`  
C) `Dequeue`  
D) `RemoveAt`

**Respuesta correcta: A**

**Retroalimentación:** `Pop()` devuelve y **retira** el elemento superior de la pila, es decir, el último que se recogió (LIFO). `Peek()` lo devolvería sin retirarlo, por lo que el mismo power-up podría usarse infinitas veces. `Dequeue` pertenece a `Queue` y `RemoveAt` a `List`.

---

## Q11. Valor inicial de un arreglo — Fácil — Tipo: Predicción

**Escenario (Dino Jump):** Se crea un arreglo para guardar los mejores 3 puntajes, pero todavía no se asigna ningún valor.

```csharp
int[] mejores = new int[3];
Debug.Log(mejores[1]);
```

¿Qué se imprime en consola?

A) `null`  
B) Se lanza `IndexOutOfRangeException`  
C) `0`  
D) `3`

**Respuesta correcta: C**

**Retroalimentación:** Al crear un arreglo con `new int[3]`, cada posición toma el valor por defecto del tipo, que para `int` es `0`. El índice 1 es válido porque el arreglo tiene `Length` 3 (índices 0, 1 y 2). `null` sería el valor por defecto si el arreglo fuera de objetos, como `GameObject[]`.

---

## Q12. Sumar puntajes — Fácil — Tipo: Predicción

**Escenario (Pac-Man):** Al terminar el nivel se suman los puntos obtenidos por cada fantasma comido.

```csharp
int[] puntosFantasmas = { 200, 400, 800 };
int total = 0;

foreach (int p in puntosFantasmas)
{
    total += p;
}
Debug.Log(total);
```

¿Qué se imprime en consola?

A) `800`  
B) `3`  
C) `200400800`  
D) `1400`

**Respuesta correcta: D**

**Retroalimentación:** El `foreach` recorre cada elemento del arreglo y lo acumula en `total`: `200 + 400 + 800 = 1400`. Como `total` es un `int`, se realiza una suma numérica, no una concatenación de texto. `3` sería la cantidad de elementos (`Length`) y `800` solo el último valor.

---

## Q13. Velocidad de cada carril — Fácil — Tipo: Predicción

**Escenario (Frogger):** Cada carril de la carretera tiene una velocidad distinta, guardada en un arreglo.

```csharp
float[] velocidadCarril = { 2f, 3.5f, 1.5f, 4f };
float v = velocidadCarril[1];
```

¿Qué valor tiene `v`?

A) `2f`  
B) `3.5f`  
C) `1.5f`  
D) `4f`

**Respuesta correcta: B**

**Retroalimentación:** Los arreglos usan indexación en base cero: el índice 0 es el primer carril (`2f`) y el índice 1 es el **segundo** carril (`3.5f`). Confundir "carril 1" con "índice 1" es un error común; si el diseño numera los carriles desde 1, hay que restar 1 al acceder al arreglo.

---

## Q14. Fantasmas asustados — Fácil — Tipo: Completar Código

**Escenario (Pac-Man):** Cuando Pac-Man come un punto de poder, los fantasmas asustados se guardan en una lista. Al chocar con un fantasma, se debe verificar si está en esa lista para decidir si Pac-Man se lo come.

```csharp
private List<GameObject> fantasmasAsustados = new List<GameObject>();

void OnTriggerEnter2D(Collider2D otro)
{
    if (fantasmasAsustados.______(otro.gameObject))
    {
        ComerFantasma(otro.gameObject);
    }
}
```

A) `Contains`  
B) `Peek`  
C) `Remove`  
D) `Insert`

**Respuesta correcta: A**

**Retroalimentación:** `Contains()` devuelve `true` si el elemento está en la colección, por lo que es la condición adecuada dentro del `if`. `Remove()` también devuelve un `bool`, pero además eliminaría al fantasma de la lista en el momento de la verificación, un efecto secundario no deseado en una condición. `Peek` no existe en `List` e `Insert` no devuelve un valor.

---

## Q15. Anunciar el próximo obstáculo — Fácil — Tipo: Completar Código

**Escenario (Dino Jump):** Los obstáculos de la partida están en una cola. La interfaz debe mostrar cuál será el próximo obstáculo **sin sacarlo** de la cola.

```csharp
if (colaObstaculos.Count > 0)
{
    GameObject proximo = colaObstaculos.______();
    textoProximo.text = "Próximo: " + proximo.name;
}
```

A) `Dequeue`  
B) `Pop`  
C) `Peek`  
D) `First`

**Respuesta correcta: C**

**Retroalimentación:** `Peek()` devuelve el primer elemento de la cola sin retirarlo. `Dequeue()` lo retiraría, y el obstáculo ya no aparecería en el juego porque solo se quería mostrar su nombre. `Pop` pertenece a `Stack`, y `First` no es un método de `Queue` (solo existe como extensión de LINQ).

---

## Q16. Número de filas del laberinto — Fácil — Tipo: Completar Código

**Escenario (Pac-Man):** El laberinto es una matriz rectangular `int[,] mapa` de 21 filas y 19 columnas.

**Objetivo:** Obtener la cantidad de **filas** para el bucle externo.

```csharp
int filas = mapa.______;
```

A) `GetLength(0)`  
B) `GetLength(1)`  
C) `Length`  
D) `Count`

**Respuesta correcta: A**

**Retroalimentación:** En una matriz rectangular, `GetLength(0)` devuelve el tamaño de la primera dimensión (filas = 21) y `GetLength(1)` el de la segunda (columnas = 19). `Length` en un `int[,]` devuelve el **total de celdas** (21 × 19 = 399), no las filas. `Count` no existe en los arreglos.

---

## Q17. Número de filas de un mapa leído — Fácil — Tipo: Completar Código

**Escenario (Battle City):** El parser devolvió una matriz escalonada `int[][] mapa`.

**Objetivo:** Recorrer todas las filas del mapa.

```csharp
for (int r = 0; r < ______; r++)
{
    // procesar fila r
}
```

A) `mapa.GetLength(0)`  
B) `mapa[r].Length`  
C) `mapa.Count`  
D) `mapa.Length`

**Respuesta correcta: D**

**Retroalimentación:** En una matriz escalonada, `mapa.Length` devuelve la cantidad de filas (la cantidad de arreglos internos). `mapa[r].Length` es la longitud de una fila específica y se usa en el bucle **interno** de columnas; además, en la condición del bucle externo `r` todavía puede estar fuera de rango. `GetLength(0)` es la forma habitual de hacerlo en matrices rectangulares, y `Count` no existe en arreglos.

---

## Q18. Reiniciar la partida — Fácil — Tipo: Lectura de Código

**Escenario (Frogger):** Cuando la rana pierde todas sus vidas, se ejecuta el siguiente código:

```csharp
void GameOver()
{
    autos.Clear();
}
```

¿Qué ocurre con los autos que estaban en la escena?

A) Desaparecen de la escena porque `Clear()` los destruye  
B) Siguen visibles en la escena; `Clear()` solo vacía la lista, pero no destruye los GameObjects  
C) Se convierten en prefabs  
D) Se lanza una excepción porque la lista tenía elementos

**Respuesta correcta: B**

**Retroalimentación:** La lista solo guarda **referencias** a los GameObjects. `Clear()` elimina esas referencias, pero los autos siguen existiendo en la escena (y moviéndose si tienen su propio script). Para eliminarlos hay que recorrer la lista y llamar a `Destroy(auto)` **antes** de vaciarla. Confundir la colección con los objetos de la escena es un error frecuente.

---

## Q19. Retirar con seguridad — Fácil — Tipo: Completar Código

**Escenario (Carrera de autos):** Se retira el siguiente auto de la cola para hacerlo salir a la pista, pero el script no debe fallar si la cola ya está vacía.

```csharp
if (colaAutos.______ > 0)
{
    GameObject siguiente = colaAutos.Dequeue();
    Instantiate(siguiente, puntoSalida.position, Quaternion.identity);
}
```

A) `Length`  
B) `Peek()`  
C) `Count`  
D) `Capacity`

**Respuesta correcta: C**

**Retroalimentación:** `Count` indica cuántos elementos hay en la cola. Verificar `Count > 0` evita llamar a `Dequeue()` sobre una cola vacía, lo que lanzaría una `InvalidOperationException`. `Length` es de arreglos, `Peek()` devuelve un `GameObject` (no se puede comparar con `0`) y también falla si la cola está vacía, y `Queue` no tiene la propiedad `Capacity`.

---

## Q20. Error en el recorrido — Fácil — Tipo: Depuración

**Escenario (Dino Jump):** Al iniciar la partida, este código desactiva todos los obstáculos guardados en el arreglo, pero la consola muestra un error.

```csharp
for (int i = 0; i <= obstaculos.Length; i++)
{
    obstaculos[i].SetActive(false);
}
```

¿Cuál es el problema?

A) `SetActive` no existe en `GameObject`  
B) El bucle debería empezar en `i = 1`  
C) Los arreglos no pueden recorrerse con `for`  
D) La condición `<=` hace que en la última iteración se acceda a `obstaculos[Length]`, que está fuera de rango

**Respuesta correcta: D**

**Retroalimentación:** Si el arreglo tiene 3 elementos, los índices válidos son 0, 1 y 2. Con `i <= obstaculos.Length` el bucle llega a `i = 3` y lanza `IndexOutOfRangeException`. La condición correcta es `i < obstaculos.Length`. Empezar en 1 haría que se omitiera el primer obstáculo.

---

## Q21. Posición de cada bloque — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** El script `BuildGrid` coloca cada bloque del mapa en el mundo. La fila 0 del archivo debe quedar en la parte superior y las filas siguientes deben ir hacia abajo.

```csharp
Vector3 origin = transform.position;

Vector3 worldPos = new Vector3(
    origin.x + (c * cellWidth),
    ______,
    0f
);
```

A) `origin.y + (r * cellHeight)`  
B) `origin.y - (r * cellHeight)`  
C) `origin.y - (c * cellHeight)`  
D) `origin.x - (r * cellHeight)`

**Respuesta correcta: B**

**Retroalimentación:** Las columnas avanzan en el eje +X y las filas avanzan hacia **abajo**, es decir, en el eje −Y: `origin.y - (r * cellHeight)`. Con `+` el mapa quedaría invertido verticalmente. Usar `c` en el eje Y mezclaría filas con columnas, y el componente Y no debe calcularse a partir de `origin.x`.

---

## Q22. Saltar las celdas vacías — Intermedio — Tipo: Completar Código

**Escenario (Pac-Man):** Al construir el laberinto, las celdas con valor `0` son pasillo vacío y no deben generar ningún objeto, pero el resto de la fila debe seguir procesándose.

```csharp
for (int r = 0; r < matrix.Length; r++)
{
    for (int c = 0; c < matrix[r].Length; c++)
    {
        int tileType = matrix[r][c];
        if (tileType == 0) ______;

        Instantiate(wallPrefab, CalcularPosicion(r, c), Quaternion.identity, transform);
    }
}
```

A) `continue`  
B) `break`  
C) `return`  
D) `tileType = 1`

**Respuesta correcta: A**

**Retroalimentación:** `continue` salta a la siguiente iteración del bucle interno, así que solo se omite esa celda. `break` terminaría el bucle de columnas y se perdería **el resto de la fila**; `return` saldría de todo el método y el laberinto quedaría incompleto. Asignar `tileType = 1` convertiría el pasillo en pared.

---

## Q23. Elegir el sprite del bloque — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** Los valores del mapa son `1` = ladrillo, `2` = acero, `3` = pasto y `4` = agua, y en el Inspector se arrastraron los sprites en ese mismo orden al arreglo `wallSprites` (índices 0 a 3).

```csharp
GameObject tile = Instantiate(wallPrefab, worldPos, Quaternion.identity, transform);

int spriteIndex = ______;
if (spriteIndex >= 0 && spriteIndex < wallSprites.Length)
    tile.GetComponent<SpriteRenderer>().sprite = wallSprites[spriteIndex];
```

A) `tileType`  
B) `tileType + 1`  
C) `tileType - 1`  
D) `wallSprites.Length - tileType`

**Respuesta correcta: C**

**Retroalimentación:** El valor `0` se reserva para celdas vacías, por lo que el tipo `1` (ladrillo) debe corresponder al índice `0` del arreglo: `spriteIndex = tileType - 1`. Usar `tileType` directamente desplazaría todos los sprites una posición (el ladrillo se vería como acero) y el agua (`4`) quedaría fuera de rango.

---

## Q24. Separar el archivo en líneas — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** El archivo del mapa fue creado en Windows, donde cada línea termina en `\r\n`. El parser debe obtener solo las líneas con contenido.

```csharp
string[] rawLines = textContent.Split(
    ______, StringSplitOptions.RemoveEmptyEntries);
```

A) `new[] { ',' }`  
B) `new[] { ' ', '\t' }`  
C) `new[] { '\n' }` (sin `RemoveEmptyEntries`)  
D) `new[] { '\r', '\n' }`

**Respuesta correcta: D**

**Retroalimentación:** Separar por `'\r'` y `'\n'` cubre los saltos de línea de Windows, Linux y Mac. Entre `\r` y `\n` aparece una cadena vacía, que `RemoveEmptyEntries` descarta. Las comas, espacios y tabuladores se usan en el paso siguiente, para separar las **celdas** dentro de cada línea, no las líneas del archivo.

---

## Q25. Ignorar comentarios en el mapa — Intermedio — Tipo: Completar Código

**Escenario (Pac-Man):** Los diseñadores escriben notas en el archivo del mapa con líneas que comienzan con `#`. Esas líneas no deben convertirse en filas del laberinto.

```csharp
for (int r = 0; r < rawLines.Length; r++)
{
    string line = rawLines[r].Trim();
    if (string.IsNullOrEmpty(line) || ______)
        continue;

    // separar celdas y convertir a números...
}
```

A) `line.EndsWith("#")`  
B) `line.StartsWith("#")`  
C) `line.Contains("1")`  
D) `line.Length > 0`

**Respuesta correcta: B**

**Retroalimentación:** `StartsWith("#")` detecta las líneas que **comienzan** con el símbolo de comentario, y `continue` las salta. `EndsWith` revisaría el final de la línea. `Contains("1")` descartaría casi todas las filas con paredes, y `line.Length > 0` descartaría todas las líneas con contenido.

---

## Q26. Convertir cada celda a número — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** Cada línea ya se dividió en `tokens` (textos como `"1"`, `"2"`, `"0"`). Se deben convertir a enteros sin que el juego se detenga si algún token no es numérico.

```csharp
int[] row = new int[tokens.Length];

for (int c = 0; c < tokens.Length; c++)
    ______;

matrixList.Add(row);
```

A) `int.TryParse(tokens[c], out row[c])`  
B) `row[c] = int.Parse(tokens[c])`  
C) `row[c] = tokens[c]`  
D) `row[c] = (int)tokens[c]`

**Respuesta correcta: A**

**Retroalimentación:** `int.TryParse` intenta la conversión y deja el resultado en `row[c]` mediante `out`; si falla, asigna `0` y no lanza excepción. `int.Parse` funciona con datos válidos, pero lanza `FormatException` ante un carácter inválido. Las opciones C y D no compilan: no se puede asignar ni convertir directamente un `string` a `int`.

---

## Q27. Salida escalonada de autos — Intermedio — Tipo: Completar Código

**Escenario (Carrera de autos):** Los autos rivales deben salir de la cola uno por uno, con 2 segundos de separación entre cada uno.

```csharp
IEnumerator SalidaDeAutos()
{
    while (colaAutos.Count > 0)
    {
        GameObject siguiente = colaAutos.Dequeue();
        Instantiate(siguiente, puntoSalida.position, Quaternion.identity);
        ______;
    }
}
```

A) `Thread.Sleep(2000)`  
B) `return new WaitForSeconds(2f)`  
C) `yield return new WaitForSeconds(2f)`  
D) `Invoke("SalidaDeAutos", 2f)`

**Respuesta correcta: C**

**Retroalimentación:** Dentro de una corrutina (`IEnumerator` iniciada con `StartCoroutine`), `yield return new WaitForSeconds(2f)` pausa la ejecución 2 segundos sin congelar el juego y luego continúa el bucle. `Thread.Sleep` congelaría todo Unity. Un `return` sin `yield` no compila en un iterador, e `Invoke` iniciaría una nueva llamada en lugar de esperar dentro del bucle.

---

## Q28. Traza de la cola de autos — Intermedio — Tipo: Predicción

**Escenario (Carrera de autos):**

```csharp
Queue<string> cola = new Queue<string>();
cola.Enqueue("Rojo");
cola.Enqueue("Azul");
cola.Enqueue("Verde");

string a = cola.Dequeue();
cola.Enqueue("Amarillo");
string b = cola.Dequeue();

Debug.Log(a + " - " + b + " - " + cola.Peek());
```

¿Qué se imprime en consola?

A) `Verde - Azul - Rojo`  
B) `Rojo - Azul - Amarillo`  
C) `Rojo - Rojo - Azul`  
D) `Rojo - Azul - Verde`

**Respuesta correcta: D**

**Retroalimentación:** La cola es FIFO. El primer `Dequeue()` devuelve `"Rojo"`. Luego `"Amarillo"` se agrega **al final**: la cola queda `Azul, Verde, Amarillo`. El segundo `Dequeue()` devuelve `"Azul"`, y `Peek()` muestra el siguiente sin retirarlo: `"Verde"`.

---

## Q29. Traza de la pila de power-ups — Intermedio — Tipo: Predicción

**Escenario (Battle City):**

```csharp
Stack<string> pila = new Stack<string>();
pila.Push("Escudo");
pila.Push("Estrella");
pila.Push("Granada");

string usado = pila.Pop();
pila.Push("Reloj");

Debug.Log(usado + " - " + pila.Peek() + " - " + pila.Count);
```

¿Qué se imprime en consola?

A) `Granada - Reloj - 3`  
B) `Escudo - Reloj - 4`  
C) `Granada - Estrella - 2`  
D) `Granada - Reloj - 4`

**Respuesta correcta: A**

**Retroalimentación:** La pila es LIFO. `Pop()` retira `"Granada"`, el último en entrar; quedan `Escudo` y `Estrella`. Luego `Push("Reloj")` lo coloca en la cima, así que `Peek()` devuelve `"Reloj"` y la pila tiene 3 elementos (Escudo, Estrella, Reloj).

---

## Q30. Eliminar autos que salen de pantalla — Intermedio — Tipo: Completar Código

**Escenario (Frogger):** Los autos se mueven de derecha a izquierda. Cuando un auto pasa el límite izquierdo, debe destruirse y quitarse de la lista, sin saltarse ningún auto.

```csharp
for (______)
{
    if (autos[i].transform.position.x < limiteIzquierdo)
    {
        Destroy(autos[i]);
        autos.RemoveAt(i);
    }
}
```

A) `int i = 0; i < autos.Count; i++`  
B) `int i = autos.Count - 1; i >= 0; i--`  
C) `int i = autos.Count; i > 0; i--`  
D) `int i = 0; i <= autos.Count; i++`

**Respuesta correcta: B**

**Retroalimentación:** Al eliminar con `RemoveAt(i)`, los elementos siguientes se desplazan una posición. Recorriendo **hacia atrás** (desde `Count - 1` hasta `0`), los desplazamientos solo afectan a posiciones ya revisadas. Hacia adelante (A) se saltaría el auto que ocupa el lugar del eliminado. La opción C empieza en `Count` (fuera de rango) y la D llega a `Count`, lo que lanza `ArgumentOutOfRangeException`.

---

## Q31. Condición de victoria — Intermedio — Tipo: Completar Código

**Escenario (Pac-Man):** Todos los puntos del laberinto se guardaron en una lista al construir el nivel. Cada vez que Pac-Man come uno, se retira de la lista y se destruye. El nivel termina cuando no quedan puntos.

```csharp
void ComerPunto(GameObject punto)
{
    puntos.Remove(punto);
    Destroy(punto);

    if (______)
        Victoria();
}
```

A) `puntos == null`  
B) `puntos.Contains(punto)`  
C) `puntos.Count == 0`  
D) `puntos[0] == null`

**Respuesta correcta: C**

**Retroalimentación:** `puntos.Count == 0` indica que la lista ya no tiene elementos, es decir, que Pac-Man se comió todos los puntos. La lista no se vuelve `null` al vaciarse; sigue existiendo, solo que vacía. `Contains(punto)` será `false` después de `Remove`, lo que daría la victoria con el primer punto. `puntos[0]` lanzaría una excepción cuando la lista esté vacía.

---

## Q32. Tabla de récords — Intermedio — Tipo: Predicción

**Escenario (Dino Jump):** Al terminar la partida se actualiza la tabla de puntajes.

```csharp
List<int> puntajes = new List<int> { 120, 300, 80 };
puntajes.Add(250);
puntajes.Sort();     // ordena de menor a mayor
puntajes.Reverse();  // invierte el orden

Debug.Log(puntajes[1]);
```

¿Qué se imprime en consola?

A) `120`  
B) `300`  
C) `80`  
D) `250`

**Respuesta correcta: D**

**Retroalimentación:** Después de `Add(250)` la lista es `{120, 300, 80, 250}`. `Sort()` la ordena de menor a mayor: `{80, 120, 250, 300}`. `Reverse()` invierte el orden: `{300, 250, 120, 80}`. El índice 1 es el **segundo** elemento: `250`. Así, `puntajes[0]` es siempre el récord más alto.

---

## Q33. La base del jugador — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** La base del jugador siempre tiene la misma forma: un bloque de 3 filas y 5 columnas que nunca cambia de tamaño.

**Objetivo:** Crear una matriz rectangular vacía con esas dimensiones.

```csharp
int[,] baseJugador = ______;
```

A) `new int[3, 5]`  
B) `new int[5, 3]`  
C) `new int[3][5]`  
D) `new int[15]`

**Respuesta correcta: A**

**Retroalimentación:** En `new int[filas, columnas]` la primera dimensión son las filas: `new int[3, 5]`. `new int[5, 3]` crearía 5 filas y 3 columnas. `new int[3][5]` no es una sintaxis válida en C# (una matriz escalonada se crea como `new int[3][]` y luego cada fila por separado). `new int[15]` es un arreglo de una sola dimensión.

---

## Q34. Matriz escalonada sin filas — Intermedio — Tipo: Depuración

**Escenario (Frogger):** Se prepara una matriz escalonada para guardar las posiciones de los troncos en 3 carriles del río.

```csharp
int[][] troncos = new int[3][];
troncos[0][0] = 2;
```

Al ejecutar, aparece un error en la segunda línea. ¿Por qué?

A) Porque las matrices escalonadas no pueden guardar el número 2  
B) Porque `new int[3][]` solo crea el arreglo de filas; cada fila es `null` hasta que se le asigna un arreglo, así que se lanza `NullReferenceException`  
C) Porque el índice 0 está fuera de rango  
D) Porque se debió escribir `troncos[0, 0] = 2`

**Respuesta correcta: B**

**Retroalimentación:** En una matriz escalonada, `new int[3][]` crea un arreglo con 3 posiciones, pero cada posición es un arreglo `int[]` que todavía vale `null`. Antes de usar una fila hay que crearla, por ejemplo `troncos[0] = new int[4];`. La sintaxis con coma solo es válida para matrices rectangulares.

---

## Q35. Torre de frutas en el HUD — Intermedio — Tipo: Completar Código

**Escenario (Pac-Man):** Cada fruta que come Pac-Man se muestra apilada en una esquina de la pantalla, una sobre otra, a 0.5 unidades de distancia. La primera fruta debe quedar exactamente en `puntoDeApilado`.

```csharp
public void AgregarFruta(GameObject prefabFruta)
{
    Vector3 pos = puntoDeApilado.position + Vector3.up * ______;
    GameObject nueva = Instantiate(prefabFruta, pos, Quaternion.identity, puntoDeApilado);
    pilaFrutas.Push(nueva);
}
```

A) `((pilaFrutas.Count + 1) * 0.5f)`  
B) `(pilaFrutas.Count - 1) * 0.5f`  
C) `(pilaFrutas.Count * 0.5f)`  
D) `0.5f`

**Respuesta correcta: C**

**Retroalimentación:** La posición se calcula **antes** del `Push`. Con la pila vacía, `Count` es 0 y la primera fruta queda en la base. La segunda se calcula con `Count = 1` (0.5 unidades arriba), y así sucesivamente. Con `Count + 1` quedaría un hueco en la base; con `Count - 1` la primera fruta quedaría por debajo del punto; con un valor fijo todas se superpondrían.

---

## Q36. Elegir un power-up de la lista — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** El jugador guarda power-ups en una lista y los selecciona con las teclas numéricas. El índice llega desde la interfaz y puede ser inválido si el jugador presiona una tecla sin power-up.

```csharp
public void SeleccionarPowerUp(int indice)
{
    if (______)
    {
        powerUps[indice].Activar();
        powerUps.RemoveAt(indice);
    }
}
```

A) `indice < powerUps.Count`  
B) `indice >= 0 && indice <= powerUps.Count`  
C) `powerUps.Contains(indice)`  
D) `indice >= 0 && indice < powerUps.Count`

**Respuesta correcta: D**

**Retroalimentación:** Un índice válido debe cumplir `0 <= indice < Count`. La opción A no protege contra índices negativos. La B acepta `indice == Count`, que está fuera de rango y lanza `ArgumentOutOfRangeException`. La C busca si el número existe **como elemento** de la lista, no si es una posición válida.

---

## Q37. Contar autos por carril — Intermedio — Tipo: Predicción

**Escenario (Frogger):** Cada carril tiene una cantidad distinta de autos, por eso se usa una matriz escalonada (`1` = auto, `0` = espacio libre).

```csharp
int[][] carriles = {
    new int[] { 1, 0, 1 },
    new int[] { 1, 1, 0, 1, 1 },
    new int[] { 0, 1 }
};

int total = 0;
for (int r = 0; r < carriles.Length; r++)
    for (int c = 0; c < carriles[r].Length; c++)
        if (carriles[r][c] == 1) total++;

Debug.Log(carriles.Length + " carriles, " + total + " autos");
```

¿Qué se imprime en consola?

A) `3 carriles, 10 autos`  
B) `3 carriles, 7 autos`  
C) `10 carriles, 7 autos`  
D) `3 carriles, 5 autos`

**Respuesta correcta: B**

**Retroalimentación:** `carriles.Length` es la cantidad de filas: 3. Contando los `1` de cada fila: 2 + 4 + 1 = 7. El valor 10 es la cantidad total de **celdas**, incluidos los espacios libres. Gracias a `carriles[r].Length`, cada fila se recorre según su propia longitud, sin salirse de rango.

---

## Q38. Oleada de tanques enemigos — Intermedio — Tipo: Predicción

**Escenario (Battle City):** En el nivel solo pueden aparecer tanques mientras queden más de 2 en espera; los 2 últimos quedan como reserva.

```csharp
Queue<string> tanques = new Queue<string>();
tanques.Enqueue("Básico");
tanques.Enqueue("Rápido");
tanques.Enqueue("Blindado");
tanques.Enqueue("Pesado");

while (tanques.Count > 2)
{
    tanques.Dequeue();
}
Debug.Log(tanques.Peek() + " - " + tanques.Count);
```

¿Qué se imprime en consola?

A) `Blindado - 2`  
B) `Rápido - 2`  
C) `Pesado - 2`  
D) `Básico - 4`

**Respuesta correcta: A**

**Retroalimentación:** El bucle retira elementos mientras haya más de 2. Salen `"Básico"` y `"Rápido"` (los primeros en entrar), y quedan `Blindado` y `Pesado`. `Peek()` devuelve el primero de la cola sin retirarlo: `"Blindado"`, y `Count` es 2.

---

## Q39. ¿Todas las metas ocupadas? — Intermedio — Tipo: Completar Código

**Escenario (Frogger):** Al otro lado del río hay 5 metas. Cuando una rana llega a una, se marca como ocupada en un arreglo `bool[] metas`. El nivel se gana cuando **todas** están ocupadas.

```csharp
private bool[] metas = new bool[5];

bool TodasOcupadas()
{
    for (int i = 0; i < metas.Length; i++)
    {
        ______
    }
    return true;
}
```

A) `if (metas[i]) return true;`  
B) `if (metas[i]) return false;`  
C) `if (!metas[i]) return false;`  
D) `metas[i] = true;`

**Respuesta correcta: C**

**Retroalimentación:** Basta con encontrar **una** meta libre para saber que el nivel no ha terminado: `if (!metas[i]) return false;`. Si el bucle termina sin encontrar ninguna libre, se llega a `return true`. La opción A devolvería `true` con la primera meta ocupada, aunque las demás estén libres. La B tiene la lógica invertida. La D marcaría todas las metas como ocupadas.

---

## Q40. Limpiar el nivel anterior — Intermedio — Tipo: Completar Código

**Escenario (Battle City):** Todos los bloques se instanciaron como hijos del objeto que tiene el script (`Instantiate(..., transform)`). Antes de construir el siguiente nivel se deben eliminar los bloques del nivel anterior.

```csharp
void LimpiarNivel()
{
    foreach (Transform hijo in transform)
    {
        ______;
    }
}
```

A) `Destroy(hijo)`  
B) `hijo.gameObject.SetActive(true)`  
C) `transform.DetachChildren()`  
D) `Destroy(hijo.gameObject)`

**Respuesta correcta: D**

**Retroalimentación:** El `foreach` sobre `transform` recorre los componentes `Transform` de los hijos. Para eliminar el bloque completo hay que destruir su **GameObject**: `Destroy(hijo.gameObject)`. `Destroy(hijo)` intenta destruir solo el componente `Transform`, algo que Unity no permite. Activar los hijos o desvincularlos no los elimina de la escena.

---

## Q41. Error de escritura en el mapa — Difícil — Tipo: Predicción

**Escenario (Battle City):** Un diseñador escribió por error una letra en el archivo del mapa. El parser procesa esta línea:

```csharp
string line = "1, X, 2";
string[] tokens = line.Split(new[] { ',', ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
int[] row = new int[tokens.Length];

for (int c = 0; c < tokens.Length; c++)
    int.TryParse(tokens[c], out row[c]);
```

¿Cuál es el contenido final de `row`?

A) `{ 1, 0, 2 }`  
B) `{ 1, 2 }`  
C) Se lanza `FormatException` y `row` queda vacío  
D) `{ 1, 88, 2 }` (88 es el código ASCII de `X`)

**Respuesta correcta: A**

**Retroalimentación:** El `Split` con comas y espacios y `RemoveEmptyEntries` produce los tokens `"1"`, `"X"` y `"2"`, así que `row` tiene 3 posiciones. `TryParse("X")` falla, devuelve `false` y asigna `0` a `row[1]` sin lanzar excepción. Como `0` significa celda vacía, en el juego faltará un bloque **sin ningún aviso**. Por eso conviene revisar el `bool` que devuelve `TryParse` y registrar un `Debug.LogWarning`.

---

## Q42. Traza completa del parser — Difícil — Tipo: Predicción

**Escenario (Pac-Man):** El archivo `nivel1.txt` tiene este contenido (la tercera línea contiene solo un espacio):

```
# Laberinto de prueba
1,1,1
 
1,5,1
1 1 1 1
```

Se procesa con `MapParser.ParseTextToMatrix`, que separa por `\r` y `\n` con `RemoveEmptyEntries`, aplica `Trim()`, ignora las líneas vacías y las que comienzan con `#`, y separa las celdas por coma, espacio o tabulador.

¿Cuántas filas tiene la matriz resultante y cuál es la longitud de cada una?

A) 5 filas: 0, 3, 0, 3, 4  
B) 3 filas: 3, 3, 3  
C) 3 filas: 3, 3, 4  
D) 4 filas: 3, 0, 3, 4

**Respuesta correcta: C**

**Retroalimentación:** La línea `#` se descarta por ser un comentario. La línea con un espacio no es vacía para `RemoveEmptyEntries`, pero después de `Trim()` queda vacía y se salta con `continue`. Quedan 3 filas: `1,1,1` (3 celdas), `1,5,1` (3 celdas) y `1 1 1 1` (4 celdas, separadas por espacios). La matriz escalonada acepta que la última fila sea más larga.

---

## Q43. Rebobinar al fantasma — Difícil — Tipo: Depuración

**Escenario (Pac-Man):** Un fantasma registra cada posición por la que pasa en una pila. Al presionar la tecla `R`, debe **regresar paso a paso** por su camino hasta el inicio, de forma visible.

```csharp
private Stack<Vector3> historial = new Stack<Vector3>();

void Update()
{
    if (Input.GetKeyDown(KeyCode.R))
    {
        while (historial.Count > 0)
        {
            transform.position = historial.Pop();
        }
    }
}
```

El fantasma aparece instantáneamente en el punto de inicio, sin mostrar el recorrido. ¿Cuál es la causa y la solución?

A) La pila devuelve las posiciones en orden incorrecto; hay que usar una `Queue`  
B) El `while` vacía toda la pila dentro de un único frame, así que solo se ve la última posición asignada; hay que usar una corrutina con `yield return` entre cada `Pop()`  
C) `Pop()` no modifica la pila; hay que usar `Peek()`  
D) `Input.GetKeyDown` se ejecuta en cada frame; hay que cambiarlo por `Input.GetKey`

**Respuesta correcta: B**

**Retroalimentación:** La pila es la estructura correcta: `Pop()` devuelve las posiciones en orden inverso, de la más reciente a la más antigua. El problema es de **tiempo**: Unity solo dibuja la escena al terminar el frame, y el `while` recorre todas las posiciones antes de eso. Con una corrutina (`IEnumerator`) que haga `yield return new WaitForSeconds(0.05f)` (o `yield return null`) después de cada `Pop()`, el retroceso se ve paso a paso. Una `Queue` regresaría en el orden en que se recorrió el camino.

---

## Q44. Deshacer y rehacer en el editor de niveles — Difícil — Tipo: Completar Código

**Escenario (Battle City):** El editor de niveles permite colocar bloques y usa dos pilas: `deshacer` y `rehacer`.

```csharp
private Stack<Accion> deshacer = new Stack<Accion>();
private Stack<Accion> rehacer = new Stack<Accion>();

public void RealizarAccion(Accion a)
{
    a.Ejecutar();
    deshacer.Push(a);
    rehacer.Clear();
}

public void Deshacer()
{
    if (deshacer.Count > 0)
    {
        Accion a = deshacer.Pop();
        a.Revertir();
        ______;
    }
}
```

A) `deshacer.Push(a)`  
B) `rehacer.Clear()`  
C) `rehacer.Pop()`  
D) `rehacer.Push(a)`

**Respuesta correcta: D**

**Retroalimentación:** La acción deshecha debe guardarse en la pila `rehacer` para poder restaurarla después: `rehacer.Push(a)`. Volver a meterla en `deshacer` crearía un ciclo en el que siempre se deshace la misma acción. Vaciar `rehacer` aquí borraría el historial que se acaba de crear; eso solo se hace al realizar una acción **nueva**, como ya ocurre en `RealizarAccion`. `rehacer.Pop()` fallaría con la pila vacía.

---

## Q45. Un auto que nunca desaparece — Difícil — Tipo: Predicción

**Escenario (Frogger):** La lista contiene 4 autos: `[A, B, C, D]`. Los autos **A y B** ya pasaron el límite izquierdo. Se ejecuta este código **una sola vez**:

```csharp
for (int i = 0; i < autos.Count; i++)
{
    if (autos[i].transform.position.x < limiteIzquierdo)
    {
        Destroy(autos[i]);
        autos.RemoveAt(i);
    }
}
```

¿Cómo queda la lista al terminar el bucle?

A) `[B, C, D]`: el auto B se saltó porque ocupó la posición del auto A después de eliminarlo  
B) `[C, D]`: ambos autos se eliminaron correctamente  
C) `[A, C, D]`: el auto A se saltó  
D) Se lanza `InvalidOperationException`

**Respuesta correcta: A**

**Retroalimentación:** Con `i = 0` se elimina A y la lista pasa a ser `[B, C, D]`: B ahora ocupa el índice 0. Luego `i++` hace que `i = 1`, que corresponde a C, así que B nunca se revisa en esta pasada. Este es el error clásico de eliminar mientras se recorre hacia adelante; la solución es recorrer desde `Count - 1` hasta `0`. La `InvalidOperationException` aparece al modificar la lista dentro de un `foreach`, no dentro de un `for`.

---

## Q46. Reutilizar autos con una cola — Difícil — Tipo: Completar Código

**Escenario (Carrera de autos):** Para no crear y destruir autos constantemente, se crean 5 autos al inicio y se reutilizan. Cuando un auto sale por la izquierda se desactiva y vuelve a la cola de disponibles. Para generar un auto nuevo se toma uno disponible de la cola.

```csharp
private Queue<GameObject> disponibles = new Queue<GameObject>();

public void Reciclar(GameObject auto)
{
    auto.SetActive(false);
    disponibles.Enqueue(auto);
}

public void GenerarAuto()
{
    if (disponibles.Count > 0)
    {
        GameObject auto = ______;
        auto.transform.position = puntoSpawn.position;
        auto.SetActive(true);
    }
}
```

A) `disponibles.Peek()`  
B) `Instantiate(prefabAuto)`  
C) `disponibles.Dequeue()`  
D) `disponibles.Pop()`

**Respuesta correcta: C**

**Retroalimentación:** `Dequeue()` retira de la cola el auto que lleva más tiempo disponible y lo entrega para reactivarlo. Con `Peek()` el auto se reactivaría pero **seguiría en la cola**, de modo que la próxima llamada tomaría el mismo auto y lo teletransportaría al punto de salida. `Instantiate` volvería a crear objetos nuevos, que es justo lo que se quería evitar, y `Pop` pertenece a `Stack`.

---

## Q47. El mapa aparece de cabeza — Difícil — Tipo: Depuración

**Escenario (Battle City):** En el archivo del mapa, la base del jugador está en la **última fila** (abajo). Sin embargo, en el juego la base aparece arriba y las paredes superiores aparecen abajo.

```csharp
Vector3 worldPos = new Vector3(
    origin.x + (c * cellWidth),
    origin.y + (r * cellHeight),
    0f
);
```

¿Qué cambio corrige el problema?

A) Cambiar `c * cellWidth` por `-c * cellWidth`  
B) Cambiar `origin.y + (r * cellHeight)` por `origin.y - (r * cellHeight)`  
C) Recorrer la matriz con `foreach` en lugar de `for`  
D) Cambiar la matriz `int[][]` por `int[,]`

**Respuesta correcta: B**

**Retroalimentación:** En la matriz, las filas avanzan hacia abajo (`r` crece), pero en Unity el eje Y positivo apunta hacia arriba. Con `+`, cada fila nueva se dibuja más arriba y el mapa queda invertido verticalmente. Con `-`, la fila 0 queda arriba y la última fila (la base) abajo, tal como en el archivo. Negar `c` invertiría el mapa horizontalmente, y cambiar el tipo de matriz o de bucle no afecta a las posiciones.

---

## Q48. ¿En qué celda está Pac-Man? — Difícil — Tipo: Completar Código

**Escenario (Pac-Man):** Antes de mover a Pac-Man, se necesita saber en qué celda de la matriz se encuentra para revisar si la celda siguiente es pared. Es el cálculo **inverso** a la fórmula de `BuildGrid` (`x = origin.x + c * cellWidth`, `y = origin.y - r * cellHeight`).

```csharp
Vector3 pos = pacman.position;
int c = Mathf.RoundToInt((pos.x - origin.x) / cellWidth);
int r = Mathf.RoundToInt(______);
```

A) `(pos.y - origin.y) / cellHeight`  
B) `(pos.x - origin.y) / cellHeight`  
C) `(origin.x - pos.y) / cellWidth`  
D) `(origin.y - pos.y) / cellHeight`

**Respuesta correcta: D**

**Retroalimentación:** Si se despeja `r` en `y = origin.y - r * cellHeight`, se obtiene `r = (origin.y - y) / cellHeight`. Como las filas crecen hacia abajo, cuanto más abajo está Pac-Man (`pos.y` menor), mayor es `r`. La opción A da filas negativas, y las opciones B y C mezclan los ejes X e Y o usan la medida equivocada.

---

## Q49. Revisar la celda vecina sin salirse del mapa — Difícil — Tipo: Mejor Enfoque

**Escenario (Battle City):** El tanque quiere moverse a la celda `(r, c)`. Solo puede hacerlo si la celda existe dentro del mapa escalonado `int[][] mapa` y su valor es `0` (vacío). Si el tanque está en un borde, `r` o `c` pueden quedar fuera del mapa.

¿Cuál condición es correcta y segura?

A) `r >= 0 && r < mapa.Length && c >= 0 && c < mapa[r].Length && mapa[r][c] == 0`  
B) `mapa[r][c] == 0 && r >= 0 && r < mapa.Length && c >= 0 && c < mapa[r].Length`  
C) `r >= 0 && r < mapa.Length || c >= 0 && c < mapa[r].Length && mapa[r][c] == 0`  
D) `c >= 0 && c < mapa[r].Length && r >= 0 && r < mapa.Length && mapa[r][c] == 0`

**Respuesta correcta: A**

**Retroalimentación:** El operador `&&` evalúa de izquierda a derecha y se detiene en la primera condición falsa (evaluación en cortocircuito). Por eso primero se valida `r`, después `c` usando `mapa[r].Length` (que solo es seguro cuando `r` ya es válido), y al final se lee `mapa[r][c]`. La opción B lee la celda **antes** de validar y lanza `IndexOutOfRangeException`. La D usa `mapa[r]` antes de validar `r`. La C usa `||`, que permite leer la celda aunque `c` esté fuera de rango.

---

## Q50. Invertir el orden de una oleada — Difícil — Tipo: Predicción

**Escenario (Dino Jump):** En el modo "reversa", la secuencia de obstáculos debe salir en orden inverso. Para lograrlo se combina una cola con una pila:

```csharp
Queue<string> cola = new Queue<string>();
cola.Enqueue("Cactus");
cola.Enqueue("Ave");
cola.Enqueue("Roca");

Stack<string> pila = new Stack<string>();
while (cola.Count > 0)
    pila.Push(cola.Dequeue());

while (pila.Count > 0)
    cola.Enqueue(pila.Pop());

Debug.Log(cola.Dequeue() + " - " + cola.Peek() + " - " + cola.Count);
```

¿Qué se imprime en consola?

A) `Cactus - Ave - 2`  
B) `Roca - Ave - 2`  
C) `Roca - Cactus - 3`  
D) `Ave - Roca - 2`

**Respuesta correcta: B**

**Retroalimentación:** El primer bucle saca de la cola en orden FIFO (Cactus, Ave, Roca) y los apila, así que `Roca` queda en la cima. El segundo bucle desapila en orden LIFO (Roca, Ave, Cactus) y los vuelve a encolar: la cola queda `Roca, Ave, Cactus`. `Dequeue()` devuelve `"Roca"`, `Peek()` muestra `"Ave"` y quedan 2 elementos. Pasar los elementos por una pila es la forma clásica de invertir una secuencia.

---

*Fin del examen — COM200 Estructuras de Datos en C# para Unity (Código)*  
*Total: 50 preguntas | Fácil: 20 | Intermedio: 20 | Difícil: 10*
