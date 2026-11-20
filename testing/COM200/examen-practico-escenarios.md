# COM200 — Programación Avanzada
## Examen Práctico: Listas de Objetos en Unity 2D
**3 escenarios | Tiempo estimado por escenario: 15 minutos**

> **Modelo del examen (visto en clase):** Configurar un *player* que se pueda mover y detener, y que tenga dentro de su clase una **lista de enemigos** que se puede configurar en tiempo real (quitar y agregar enemigos). Los enemigos persiguen al player a diferentes velocidades. Cuando el player presiona `Espacio`, todos los enemigos registrados en su lista se mueven o se detienen. El objetivo es que el estudiante pueda configurar **en la escena** qué enemigos deben reaccionar al evento.

Los tres escenarios siguientes mantienen esa misma base (player que se mueve, enemigos que persiguen, lista editable desde el Inspector), y cada uno agrega una lógica distinta que obliga a **recorrer la lista, filtrar por un atributo y llamar a métodos de los objetos**.

---

## Reglas comunes para los 3 escenarios

### Base obligatoria

1. **Escena 2D** con un GameObject `Player` (un sprite cuadrado o círculo es suficiente).
2. El `Player` se mueve con las flechas o WASD y **se detiene** al soltar las teclas.
3. Un **prefab** `Enemigo` con un `SpriteRenderer` y el script `Enemigo`.
4. Al menos **6 clones** del prefab en la escena, con valores distintos en el Inspector (velocidad y el atributo propio del escenario).
5. Cada enemigo persigue al `Player` a **su propia velocidad**.
6. El script `Player` tiene un campo **`public List<Enemigo> enemigos`** que se llena **arrastrando** enemigos desde la Jerarquía al Inspector.
7. **Solo algunos** enemigos deben estar en la lista (por ejemplo, 4 de 6). Los enemigos que no están en la lista siguen persiguiendo, pero **no reaccionan** a las teclas del player.

### Referencia al player desde el prefab

Un prefab guardado en la carpeta del proyecto **no puede** tener arrastrada una referencia a un objeto de la escena. Elige una de estas dos formas y explica cuál usaste:

- Asignar el campo `objetivo` en **cada clon** de la escena (arrastrando el `Player`), o
- Buscarlo por código en `Start()` con el tag `Player`: `GameObject.FindWithTag("Player").transform`.

### Pruebas que hará el docente durante la ejecución (las 3 aplican a todos los escenarios)

- [ ] **Quitar** un enemigo de la lista en el Inspector **con el juego en Play**: ese enemigo deja de reaccionar a las teclas.
- [ ] **Agregar** a la lista, con el juego en Play, un enemigo que antes no estaba: ahora reacciona.
- [ ] Agregar un **elemento vacío** (`None`) a la lista con el `+` del Inspector: el juego **no** debe mostrar errores en la consola.

### Restricciones

- Usar el sistema de entrada clásico (`Input.GetKeyDown`, `Input.GetAxisRaw`).
- Los métodos que cambian el estado de un enemigo deben estar **en la clase `Enemigo`** y ser llamados desde `Player`. El `Player` no debe modificar directamente el color ni la posición de los enemigos.

---

## Escenario 1 — Escuadrones de colores

### Contexto

Los enemigos pertenecen a tres escuadrones: **Rojo**, **Azul** y **Verde**. El jugador tiene un radio de comunicaciones con el que puede **congelar a un escuadrón completo**, pero solo afecta a los enemigos que tiene registrados en su lista.

### Clase `Enemigo`

| Miembro | Descripción |
|---|---|
| `public ColorEquipo equipo` | Enum con los valores `Rojo`, `Azul`, `Verde`. Se elige en el Inspector. |
| `public float velocidad` | Velocidad de persecución. |
| `public Transform objetivo` | El player (ver *Referencia al player*). |
| `Start()` | Pinta el `SpriteRenderer` con el color de su equipo. |
| `Update()` | Si está en movimiento, avanza hacia el `objetivo` a su `velocidad`. |
| `public void Detener()` | Deja de moverse. |
| `public void Mover()` | Vuelve a moverse. |

### Clase `Player`

| Tecla | Acción |
|---|---|
| `1` | Detiene a los enemigos **de la lista** cuyo equipo sea **Rojo**. |
| `2` | Detiene a los enemigos de la lista del equipo **Azul**. |
| `3` | Detiene a los enemigos de la lista del equipo **Verde**. |
| `Espacio` | Hace que **todos** los enemigos de la lista vuelvan a moverse. |

Además, al presionar `1`, `2` o `3`, mostrar en consola cuántos enemigos fueron detenidos, por ejemplo: `Equipo Rojo: 2 enemigos detenidos`.

### Configuración mínima en la escena

- 6 enemigos: 2 rojos, 2 azules y 2 verdes, cada uno con una velocidad distinta (entre 1 y 4).
- En la lista del player: 1 rojo, 2 azules y 1 verde.

### Comportamiento esperado

- Al presionar `1`, se detiene **solo el rojo de la lista**; el otro rojo sigue persiguiendo. La consola muestra `Equipo Rojo: 1 enemigos detenidos`.
- Al presionar `Espacio`, todos los enemigos de la lista se mueven de nuevo.

### Rúbrica (100 pts)

| Criterio | Pts |
|---|---|
| Escena y prefab configurados (6 clones con valores distintos, colores visibles) | 15 |
| El player se mueve y se detiene | 10 |
| Los enemigos persiguen al player, cada uno a su velocidad | 15 |
| La lista se configura desde el Inspector y solo reaccionan los enemigos registrados | 20 |
| Las teclas 1/2/3 filtran por equipo y llaman a `Detener()`; `Espacio` llama a `Mover()` | 25 |
| Mensaje en consola con el conteo correcto | 5 |
| Robustez: no hay errores al agregar un elemento vacío a la lista | 10 |

---

## Escenario 2 — Los 3 más cercanos

### Contexto

El jugador tiene un arma congelante con munición limitada: al disparar solo puede congelar a los **3 enemigos más cercanos** de su lista. Los enemigos congelados se detienen y se pintan de celeste.

### Clase `Enemigo`

| Miembro | Descripción |
|---|---|
| `public float velocidad` | Velocidad de persecución. |
| `public Transform objetivo` | El player. |
| `Update()` | Si no está congelado, avanza hacia el `objetivo` a su `velocidad`. |
| `public void Congelar()` | Se detiene y cambia el color del sprite a `Color.cyan`. |
| `public void Descongelar()` | Vuelve a moverse y recupera su color original. |

### Clase `Player`

| Miembro / Tecla | Acción |
|---|---|
| `public int cantidad = 3` | Cuántos enemigos se congelan por disparo (editable en el Inspector). |
| `Espacio` | Congela a los `cantidad` enemigos **de la lista** más cercanos al player. |
| `R` | Descongela a **todos** los enemigos de la lista. |

**Reglas:**

- Si la lista tiene menos enemigos válidos que `cantidad`, se congelan todos los que haya, sin errores.
- Los elementos vacíos de la lista se ignoran.
- Un enemigo que no está en la lista nunca se congela, aunque sea el más cercano.

**Pista:** puedes copiar los enemigos válidos a una lista auxiliar y, `cantidad` veces, buscar el más cercano, congelarlo y quitarlo de la lista auxiliar. También puedes ordenar la lista auxiliar por distancia con `Sort`.

### Configuración mínima en la escena

- 6 enemigos con velocidades distintas, ubicados a distancias diferentes del player.
- 5 de ellos en la lista. Coloca el enemigo que **no** está en la lista muy cerca del player, para comprobar que no se congela.

### Comportamiento esperado

- Al presionar `Espacio`, exactamente 3 enemigos de la lista (los más cercanos en ese momento) se ponen celestes y se detienen. El enemigo que no está en la lista sigue persiguiendo aunque esté más cerca.
- Al cambiar `cantidad` a 10 en el Inspector y presionar `Espacio`, se congelan los 5 enemigos de la lista, sin errores.
- `R` devuelve el color original y el movimiento a todos.

### Rúbrica (100 pts)

| Criterio | Pts |
|---|---|
| Escena y prefab configurados (6 clones con valores distintos) | 15 |
| El player se mueve y se detiene | 10 |
| Los enemigos persiguen al player, cada uno a su velocidad | 10 |
| La lista se configura desde el Inspector y solo reaccionan los enemigos registrados | 15 |
| `Espacio` congela exactamente a los N más cercanos, calculando la distancia | 30 |
| `R` descongela y restaura el color original | 10 |
| Robustez: `cantidad` mayor que la lista y elementos vacíos no generan errores | 10 |

---

## Escenario 3 — Onda expansiva

### Contexto

El jugador lanza una onda expansiva que daña a los enemigos **de su lista** que estén dentro de un radio. Los enemigos tienen distinta cantidad de vida y desaparecen al llegar a cero, y en ese momento también deben salir de la lista del player.

### Clase `Enemigo`

| Miembro | Descripción |
|---|---|
| `public float velocidad` | Velocidad de persecución. |
| `public int vida` | Puntos de vida (entre 1 y 3), configurados en el Inspector. |
| `public Transform objetivo` | El player. |
| `Update()` | Avanza hacia el `objetivo` a su `velocidad`. |
| `public void RecibirDanio(int cantidad)` | Resta vida y muestra en consola `"<nombre> recibió daño. Vida: X"`. |
| `public bool EstaMuerto()` | Devuelve `true` si `vida <= 0`. |

### Clase `Player`

| Miembro / Tecla | Acción |
|---|---|
| `public float radio = 3f` | Alcance de la onda (editable en el Inspector). |
| `Espacio` | Cada enemigo **de la lista** que esté a una distancia menor o igual a `radio` recibe 1 de daño. Los enemigos que mueren se **quitan de la lista** y se destruyen. |
| `Tab` | Muestra en consola el enemigo de la lista con **más vida**: `"Más resistente: <nombre> (vida X)"`. Si la lista está vacía, muestra `"No hay enemigos registrados"`. |

**Reglas:**

- Eliminar elementos de una lista mientras se recorre requiere cuidado: no debe saltarse a ningún enemigo ni lanzar excepciones.
- Los elementos vacíos de la lista se ignoran (o se eliminan).
- **Bonus (+10):** dibujar el radio en la vista *Scene* con `OnDrawGizmosSelected()` y `Gizmos.DrawWireSphere`.

### Configuración mínima en la escena

- 6 enemigos con velocidades distintas y vidas de 1, 2 y 3.
- 4 de ellos en la lista.

### Comportamiento esperado

- Al presionar `Espacio` con varios enemigos cerca, todos los de la lista dentro del radio reciben daño en el mismo pulso. Los que llegan a 0 desaparecen de la escena **y** de la lista del Inspector.
- Un enemigo fuera de la lista no recibe daño aunque esté dentro del radio.
- `Tab` siempre informa correctamente al enemigo con más vida, incluso después de que algunos hayan muerto.

### Rúbrica (100 pts)

| Criterio | Pts |
|---|---|
| Escena y prefab configurados (6 clones con valores distintos) | 15 |
| El player se mueve y se detiene | 10 |
| Los enemigos persiguen al player, cada uno a su velocidad | 10 |
| La lista se configura desde el Inspector y solo reaccionan los enemigos registrados | 15 |
| `Espacio` aplica daño solo dentro del radio, llamando a `RecibirDanio()` | 20 |
| Los enemigos muertos se quitan de la lista sin saltarse elementos y se destruyen | 15 |
| `Tab` encuentra al enemigo con más vida (y maneja la lista vacía) | 10 |
| Robustez: elementos vacíos en la lista no generan errores | 5 |

---
---

# ANEXO DOCENTE — Soluciones de referencia

> No entregar esta sección a los estudiantes. Las soluciones usan el sistema de entrada clásico y movimiento por `transform` para que cada escenario pueda resolverse en unos 15 minutos.

## Script común: movimiento del `Player`

Las tres soluciones comparten este movimiento dentro de `Update()`:

```csharp
float h = Input.GetAxisRaw("Horizontal");
float v = Input.GetAxisRaw("Vertical");
transform.Translate(new Vector2(h, v).normalized * velocidad * Time.deltaTime);
```

`GetAxisRaw` devuelve 0 al soltar las teclas, así que el player se detiene sin código adicional.

## Solución Escenario 1 — Escuadrones de colores

**Enemigo.cs**

```csharp
using UnityEngine;

public enum ColorEquipo { Rojo, Azul, Verde }

public class Enemigo : MonoBehaviour
{
    public ColorEquipo equipo;
    public float velocidad = 2f;
    public Transform objetivo;

    private bool enMovimiento = true;

    void Start()
    {
        if (objetivo == null)
            objetivo = GameObject.FindWithTag("Player").transform;

        GetComponent<SpriteRenderer>().color = ObtenerColor();
    }

    void Update()
    {
        if (enMovimiento && objetivo != null)
        {
            transform.position = Vector2.MoveTowards(
                transform.position, objetivo.position, velocidad * Time.deltaTime);
        }
    }

    public void Detener() { enMovimiento = false; }
    public void Mover()   { enMovimiento = true; }

    Color ObtenerColor()
    {
        switch (equipo)
        {
            case ColorEquipo.Rojo: return Color.red;
            case ColorEquipo.Azul: return Color.blue;
            default:               return Color.green;
        }
    }
}
```

**Player.cs**

```csharp
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public float velocidad = 5f;
    public List<Enemigo> enemigos = new List<Enemigo>();

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        transform.Translate(new Vector2(h, v).normalized * velocidad * Time.deltaTime);

        if (Input.GetKeyDown(KeyCode.Alpha1)) DetenerEquipo(ColorEquipo.Rojo);
        if (Input.GetKeyDown(KeyCode.Alpha2)) DetenerEquipo(ColorEquipo.Azul);
        if (Input.GetKeyDown(KeyCode.Alpha3)) DetenerEquipo(ColorEquipo.Verde);
        if (Input.GetKeyDown(KeyCode.Space))  MoverTodos();
    }

    void DetenerEquipo(ColorEquipo equipo)
    {
        int detenidos = 0;
        foreach (Enemigo e in enemigos)
        {
            if (e == null) continue;
            if (e.equipo == equipo)
            {
                e.Detener();
                detenidos++;
            }
        }
        Debug.Log($"Equipo {equipo}: {detenidos} enemigos detenidos");
    }

    void MoverTodos()
    {
        foreach (Enemigo e in enemigos)
        {
            if (e != null) e.Mover();
        }
    }
}
```

**Errores frecuentes a observar:**

- Pintar el color desde `Player` en lugar de que el enemigo lo haga en su `Start()`.
- Olvidar `if (e == null) continue;`, lo que produce `NullReferenceException` con un elemento vacío en la lista.
- Usar `FindObjectsOfType<Enemigo>()` en lugar de la lista: así reaccionan **todos** los enemigos de la escena y se incumple el objetivo del examen.

## Solución Escenario 2 — Los 3 más cercanos

**Enemigo.cs**

```csharp
using UnityEngine;

public class Enemigo : MonoBehaviour
{
    public float velocidad = 2f;
    public Transform objetivo;

    private bool congelado = false;
    private SpriteRenderer sr;
    private Color colorOriginal;

    void Start()
    {
        if (objetivo == null)
            objetivo = GameObject.FindWithTag("Player").transform;

        sr = GetComponent<SpriteRenderer>();
        colorOriginal = sr.color;
    }

    void Update()
    {
        if (!congelado && objetivo != null)
        {
            transform.position = Vector2.MoveTowards(
                transform.position, objetivo.position, velocidad * Time.deltaTime);
        }
    }

    public void Congelar()
    {
        congelado = true;
        sr.color = Color.cyan;
    }

    public void Descongelar()
    {
        congelado = false;
        sr.color = colorOriginal;
    }
}
```

**Player.cs**

```csharp
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public float velocidad = 5f;
    public int cantidad = 3;
    public List<Enemigo> enemigos = new List<Enemigo>();

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        transform.Translate(new Vector2(h, v).normalized * velocidad * Time.deltaTime);

        if (Input.GetKeyDown(KeyCode.Space)) CongelarMasCercanos();
        if (Input.GetKeyDown(KeyCode.R))     DescongelarTodos();
    }

    void CongelarMasCercanos()
    {
        // Copia auxiliar solo con enemigos válidos, para no modificar la lista original
        List<Enemigo> candidatos = new List<Enemigo>();
        foreach (Enemigo e in enemigos)
        {
            if (e != null) candidatos.Add(e);
        }

        int n = Mathf.Min(cantidad, candidatos.Count);
        for (int k = 0; k < n; k++)
        {
            Enemigo masCercano = null;
            float menorDist = Mathf.Infinity;

            foreach (Enemigo e in candidatos)
            {
                float d = Vector2.Distance(transform.position, e.transform.position);
                if (d < menorDist)
                {
                    menorDist = d;
                    masCercano = e;
                }
            }

            masCercano.Congelar();
            candidatos.Remove(masCercano);
        }
    }

    void DescongelarTodos()
    {
        foreach (Enemigo e in enemigos)
        {
            if (e != null) e.Descongelar();
        }
    }
}
```

**Alternativa válida con `Sort`:**

```csharp
candidatos.Sort((a, b) =>
    Vector2.Distance(transform.position, a.transform.position)
        .CompareTo(Vector2.Distance(transform.position, b.transform.position)));

for (int i = 0; i < Mathf.Min(cantidad, candidatos.Count); i++)
    candidatos[i].Congelar();
```

**Errores frecuentes a observar:**

- Ordenar o eliminar elementos de la lista **original**: el Inspector del player cambia de orden o pierde enemigos.
- `for (int i = 0; i < cantidad; i++)` sin `Mathf.Min`: `ArgumentOutOfRangeException` cuando `cantidad` es mayor que la lista.
- Inicializar `menorDist` en `0`: nunca se encuentra un enemigo más cercano y `masCercano` queda en `null`.
- Guardar `colorOriginal` después de haber cambiado el color.

## Solución Escenario 3 — Onda expansiva

**Enemigo.cs**

```csharp
using UnityEngine;

public class Enemigo : MonoBehaviour
{
    public float velocidad = 2f;
    public int vida = 2;
    public Transform objetivo;

    void Start()
    {
        if (objetivo == null)
            objetivo = GameObject.FindWithTag("Player").transform;
    }

    void Update()
    {
        if (objetivo != null)
        {
            transform.position = Vector2.MoveTowards(
                transform.position, objetivo.position, velocidad * Time.deltaTime);
        }
    }

    public void RecibirDanio(int cantidad)
    {
        vida -= cantidad;
        Debug.Log($"{name} recibió daño. Vida: {vida}");
    }

    public bool EstaMuerto()
    {
        return vida <= 0;
    }
}
```

**Player.cs**

```csharp
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public float velocidad = 5f;
    public float radio = 3f;
    public List<Enemigo> enemigos = new List<Enemigo>();

    void Update()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        transform.Translate(new Vector2(h, v).normalized * velocidad * Time.deltaTime);

        if (Input.GetKeyDown(KeyCode.Space)) OndaExpansiva();
        if (Input.GetKeyDown(KeyCode.Tab))   MostrarMasResistente();
    }

    void OndaExpansiva()
    {
        // Recorrido hacia atrás: eliminar con RemoveAt(i) no salta elementos
        for (int i = enemigos.Count - 1; i >= 0; i--)
        {
            Enemigo e = enemigos[i];
            if (e == null)
            {
                enemigos.RemoveAt(i);
                continue;
            }

            float d = Vector2.Distance(transform.position, e.transform.position);
            if (d <= radio)
            {
                e.RecibirDanio(1);
                if (e.EstaMuerto())
                {
                    enemigos.RemoveAt(i);
                    Destroy(e.gameObject);
                }
            }
        }
    }

    void MostrarMasResistente()
    {
        Enemigo mejor = null;
        foreach (Enemigo e in enemigos)
        {
            if (e == null) continue;
            if (mejor == null || e.vida > mejor.vida) mejor = e;
        }

        if (mejor == null)
            Debug.Log("No hay enemigos registrados");
        else
            Debug.Log($"Más resistente: {mejor.name} (vida {mejor.vida})");
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, radio);
    }
}
```

**Errores frecuentes a observar:**

- Usar `foreach` y `enemigos.Remove(e)` dentro del mismo bucle: `InvalidOperationException`.
- Recorrer hacia adelante con `RemoveAt(i)`: cuando mueren dos enemigos seguidos, el segundo se salta en ese pulso.
- Destruir el enemigo sin quitarlo de la lista: en el siguiente `Espacio` o `Tab` aparece `MissingReferenceException`.
- Que el enemigo se destruya a sí mismo dentro de `RecibirDanio()` sin avisar al player: el objeto desaparece, pero la referencia sigue en la lista.

---

## Sugerencia de aplicación

- Asignar un escenario distinto a estudiantes que se sientan juntos.
- Antes de calificar, ejecutar en vivo las **3 pruebas comunes** (quitar, agregar y elemento vacío) y las pruebas del escenario, y pedir al estudiante que explique **en voz alta** el recorrido de su lista: qué elementos filtra, qué método llama y por qué.
