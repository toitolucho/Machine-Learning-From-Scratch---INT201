# Evaluación con Andamiaje: Construyendo la Moneda (`ACoin`) paso a paso
### Programación Orientada a Objetos en C++ / Unreal Engine — Proyecto `PuzzleDiceGame`

---

## Instrucciones

En esta evaluación construirás una nueva clase **`ACoin`** (una moneda con dos lados: **CARA** y **SELLO**) dentro del mismo proyecto donde trabajamos el dado (`ADice`).

* Las preguntas están **encadenadas**: cada una agrega una pieza al código de la anterior. Usa tus respuestas previas como base.
* Hay preguntas **teóricas** (🧠) y preguntas **de código** (💻). Algunas piden **predecir** un resultado (🔮) o **encontrar un error** (🐞).
* Al final de cada etapa hay un **✅ Punto de verificación**: compila y comprueba en el motor que tu cambio funciona antes de continuar.
* Tiempo sugerido: **50 minutos**. Puntaje: **5 puntos por pregunta (100 en total)**.

### Requerimientos finales de la moneda

1. Clase `ACoin` derivada de `AActor`.
2. Atributos `bEsCara` (lado visible) y `Lanzamientos` (número de lanzamientos).
3. Malla de cilindro (`/Engine/BasicShapes/Cylinder.Cylinder`) **escalada** para parecer una moneda.
4. Material **naranja = CARA**, **azul = SELLO**.
5. Lado aleatorio al iniciar el juego.
6. Al hacer clic: se lanza la moneda, aumenta el contador y se imprime un log.
7. La grilla (`APuzzleDiceGameBlockGrid`) crea la moneda y la moneda se comunica con la grilla.

---

## Etapa 1 — La clase vacía

### Pregunta 1 🧠 (opción múltiple)
Queremos que la moneda pueda **colocarse en el nivel**, tener posición/rotación y recibir clics. ¿De qué clase debe heredar y qué prefijo debe llevar su nombre?

- a) `UObject` → `UCoin`
- b) `AActor` → `ACoin`
- c) `UStaticMeshComponent` → `UCoin`
- d) `APawn` → `ACoin`, porque todo objeto que se clickea debe ser un Pawn

### Pregunta 2 💻 (completar)
Completa los espacios del archivo `Coin.h`:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include ______(1)______

______(2)______
class PUZZLEDICEGAME_API ACoin : public AActor
{
    ______(3)______

public:
    ACoin();
};
```

Además responde: **¿por qué el `include` del espacio (1) debe ser el último?**

### Pregunta 3 🧠 (relacionar)
Relaciona cada momento del ciclo de vida con lo que **debería** hacerse ahí en nuestra moneda:

| Método | | Acción |
|---|---|---|
| (A) Constructor `ACoin()` | | (1) Elegir un lado aleatorio al empezar la partida |
| (B) `BeginPlay()` | | (2) Crear los componentes y asignar la malla |
| (C) `Tick(float DeltaTime)` | | (3) Animar algo cuadro a cuadro (por ejemplo, girar mientras está en el aire) |

> ✅ **Punto de verificación 1:** compila, arrastra `ACoin` desde el *Content Browser → C++ Classes* al nivel y comprueba que aparece en el *World Outliner* (aunque todavía no se vea nada).

---

## Etapa 2 — Los atributos

### Pregunta 4 💻 (escribir)
Declara en `Coin.h` (sección `public`) los dos atributos de la moneda, ambos **editables desde el editor**, en la categoría `"Moneda"`:

* `bEsCara`: indica si el lado visible es CARA. Valor inicial `true`.
* `Lanzamientos`: cuántas veces se ha lanzado. Valor inicial `0`.

Justifica el **tipo de dato** que elegiste para cada uno y explica por qué en Unreal se usa `int32` en lugar de `int`.

### Pregunta 5 🧠 (opción múltiple)
¿Qué ocurre si declaras `int32 Lanzamientos = 0;` **sin** la macro `UPROPERTY(...)`?

- a) No compila.
- b) Compila y funciona en C++, pero la variable **no aparece** en el panel *Details* ni es visible para el sistema de reflexión / Blueprints.
- c) La variable se vuelve privada automáticamente.
- d) La variable se reinicia a 0 en cada `Tick`.

### Pregunta 6 🐞 (encontrar el error)
Un compañero escribió:

```cpp
UPROPERTY(VisibleAnywhere, Category = "Moneda")
int32 Lanzamientos = 0;
```

En el panel *Details* ve el valor, pero **no puede modificarlo** para hacer pruebas. ¿Cuál es el problema y cómo se corrige?

> ✅ **Punto de verificación 2:** compila, selecciona la moneda en el nivel y verifica que en *Details → Moneda* aparecen `bEsCara` (checkbox) y `Lanzamientos` (número), y que puedes editarlos.

---

## Etapa 3 — La malla en el constructor

### Pregunta 7 💻 (completar)
Agrega los componentes. Primero en `Coin.h` (privados, como en `ADice`):

```cpp
UPROPERTY(VisibleDefaultsOnly, Category = "Moneda")
class USceneComponent* DummyRoot;

UPROPERTY(VisibleDefaultsOnly, Category = "Moneda")
class UStaticMeshComponent* CoinMesh;
```

Ahora completa el constructor en `Coin.cpp`:

```cpp
ACoin::ACoin()
{
    DummyRoot = ______(1)______<USceneComponent>(TEXT("Dummy0"));
    ______(2)______ = DummyRoot;

    CoinMesh = CreateDefaultSubobject<______(3)______>(TEXT("CoinMesh0"));
    CoinMesh->______(4)______(DummyRoot);
}
```

### Pregunta 8 🧠 (respuesta corta)
La moneda **tiene un** `CoinMesh` que ella misma crea en su constructor y que se destruye junto con ella.
a) ¿Qué tipo de relación entre objetos es esta: **asociación, agregación o composición**?
b) Compárala con la relación entre `APuzzleDiceGameBlockGrid` y los dados guardados en `listaDados`. ¿Es el mismo tipo? Justifica.

### Pregunta 9 💻 + 🧠
Completa la carga de la malla del cilindro y asígnala al componente:

```cpp
#include "UObject/ConstructorHelpers.h"
// ...
ConstructorHelpers::FObjectFinderOptional<UStaticMesh> Cilindro(TEXT("______(1)______"));
CoinMesh->______(2)______(Cilindro.Get());
```

Luego responde: **¿qué pasaría si movemos estas líneas de `ConstructorHelpers` al método `BeginPlay()`?**

### Pregunta 10 🔮 (predecir)
El cilindro básico de Unreal mide **100 × 100 × 100 unidades** (100 de diámetro y 100 de alto). Si escribimos:

```cpp
CoinMesh->SetRelativeScale3D(FVector(0.5f, 0.5f, 0.05f));
```

a) ¿Cuál será el **diámetro** y el **grosor** de la moneda en unidades?
b) ¿Qué eje del vector controla el grosor? ¿Por qué?
c) Escribe la escala para una moneda de **80 unidades de diámetro y 8 de grosor**.

### Pregunta 11 🔮 (predecir / elegir)
Queremos la moneda **parada de canto** (como una rueda), no acostada. Recuerda que el constructor de `FRotator` recibe los ángulos en el orden **(Pitch, Yaw, Roll)**. ¿Cuál de estas líneas lo logra?

- a) `CoinMesh->SetRelativeRotation(FRotator(0.f, 90.f, 0.f));`
- b) `CoinMesh->SetRelativeRotation(FRotator(0.f, 0.f, 90.f));`
- c) `CoinMesh->SetRelativeRotation(FRotator(0.f, 0.f, 0.f));`
- d) `CoinMesh->SetRelativeScale3D(FVector(0.f, 0.f, 90.f));`

Explica por qué la opción (a) **no** sirve.

> ✅ **Punto de verificación 3:** compila. La moneda ya debe **verse** en el nivel con forma de moneda. Prueba la rotación de la pregunta 11 y luego déjala acostada (sin rotación) para las siguientes etapas.

---

## Etapa 4 — Representar CARA y SELLO con materiales

### Pregunta 12 💻 + 🧠
Declara en `Coin.h` los punteros a los materiales y cárgalos en el constructor usando los materiales que ya existen en el proyecto (`/Game/Puzzle/Meshes/OrangeMaterial.OrangeMaterial` y `/Game/Puzzle/Meshes/BlueMaterial.BlueMaterial`):

```cpp
// Coin.h
UPROPERTY()
class UMaterialInstance* MatCara;

UPROPERTY()
class UMaterialInstance* MatSello;
```

a) Escribe las líneas del constructor que cargan ambos materiales y los guardan en `MatCara` y `MatSello`.
b) ¿Por qué estos punteros llevan `UPROPERTY()` aunque no se muestren en el editor? (Pista: ¿quién libera la memoria de los `UObject` en Unreal?)

### Pregunta 13 💻 + 🔮
Implementa el método `void MostrarLado();` que asigna `MatCara` si `bEsCara` es verdadero y `MatSello` en caso contrario (usa `SetMaterial(0, ...)`).

**Predice:** si en el panel *Details* desmarcas `bEsCara` y llamas a `MostrarLado()`, ¿de qué color se verá la moneda?

---

## Etapa 5 — Inicio del juego

### Pregunta 14 💻 + 🧠
Declara y escribe `BeginPlay()` para que la moneda empiece con un lado **aleatorio** y lo muestre.

```cpp
// Coin.h  (protected)
virtual void BeginPlay() override;
```

```cpp
// Coin.cpp
void ACoin::BeginPlay()
{
    // tu código aquí (3 líneas)
}
```

¿Qué palabra clave del encabezado indica que estamos **redefiniendo** un método de la clase padre, y qué puede fallar si olvidas llamar a `Super::BeginPlay()`?

### Pregunta 15 🧠 (respuesta corta)
Un estudiante pone `bEsCara = FMath::RandBool();` dentro del **constructor** en lugar de `BeginPlay()`. Explica por qué esta no es una buena práctica en Unreal. (Pista: ¿cuándo se ejecuta el constructor? ¿se ejecuta también en el editor? ¿qué pasa con los valores que cambias en el panel *Details*?)

> ✅ **Punto de verificación 4:** presiona **Play** varias veces. La moneda debe aparecer a veces naranja y a veces azul.

---

## Etapa 6 — Interacción con el clic

### Pregunta 16 💻 + 🧠
Declara el método que responderá al clic y conéctalo al evento `OnClicked` del componente, igual que en `ADice`:

```cpp
// Coin.h
______(1)______
void CoinClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked);
```

```cpp
// Coin.cpp — dentro del constructor
CoinMesh->OnClicked.______(2)______(this, &ACoin::CoinClicked);
```

¿Por qué el método **obligatoriamente** necesita la macro del espacio (1) para poder conectarse con `AddDynamic`?

### Pregunta 17 💻 + 🔮
Implementa `CoinClicked` para que:
1. invierta el lado (`bEsCara`),
2. incremente `Lanzamientos`,
3. llame a `MostrarLado()`,
4. imprima: `Moneda: CARA - lanzamientos: N` (o `SELLO`).

**Predice:** si la moneda empieza en **CARA** y haces **3 clics**, escribe las 3 líneas que aparecerán en el *Output Log*.

### Pregunta 18 🐞 (encontrar el error)
Esta línea no compila. Encuentra el error y corrígelo:

```cpp
UE_LOG(LogTemp, Warning, TEXT("Moneda: %s - lanzamientos: %d"), bEsCara ? "CARA" : "SELLO", Lanzamientos);
```

Bonus: si quisiéramos que el lado sea **realmente aleatorio** en cada clic (y no solo alternar), ¿qué línea cambiarías?

> ✅ **Punto de verificación 5:** en Play, haz clic en la moneda. Debe cambiar de color (si alternas) y el *Output Log* debe mostrar el contador aumentando.

---

## Etapa 7 — Comunicación con la grilla

### Pregunta 19 💻
Ya no queremos arrastrar la moneda a mano: la **grilla** debe crearla. En `PuzzleDiceGameBlockGrid.cpp`:

a) ¿Qué `#include` debes agregar?
b) Escribe la línea dentro de `BeginPlay()` (después del ciclo que crea los dados) que crea una moneda **300 unidades a la izquierda** de la grilla (`X = -300`), usando `GetWorld()->SpawnActor<...>(...)`, y guarda el puntero en una variable `ACoin* NuevaMoneda`.
c) ¿Por qué se usa `SpawnActor` y **no** `new ACoin()`?

### Pregunta 20 💻 + 🧠 (integración final)
Ahora la moneda debe **avisar a la grilla**: cada vez que sale **CARA**, la grilla suma puntos llamando a su método existente `AddScore()`.

a) Agrega a `ACoin` el atributo que guarda a la grilla dueña (pista: copia la idea de `OwningGrid` en `ADice`, con su forward declaration `class ...*`).
b) En la grilla, después de crear la moneda, completa la línea que **asocia** la moneda con la grilla.
c) En `CoinClicked`, escribe el `if` que llama a `AddScore()` solo cuando sale CARA (protegiéndote de un puntero nulo).
d) Completa la tabla con el tipo de relación (**composición, agregación o asociación**):

| Relación | Tipo |
|---|---|
| `ACoin` → `CoinMesh` | |
| `APuzzleDiceGameBlockGrid` → `listaDados` (los dados) | |
| `ACoin` → `OwningGrid` | |

> ✅ **Punto de verificación final:** en Play aparecen los dados y la moneda sin colocarla a mano. Cada clic que deja la moneda en CARA aumenta la **Puntuación** de la grilla.

---
---

# 🔑 Clave de respuestas (solo docente)

> Quita esta sección antes de entregar la evaluación a los estudiantes.

| # | Respuesta esperada | Criterio de evaluación |
|---|---|---|
| **1** | **b)** `AActor` → `ACoin`. Prefijo `A` para clases derivadas de `AActor`; `U` para `UObject`/componentes. `APawn` es para entidades **poseídas** por un jugador/IA, no hace falta para recibir clics. | Opción correcta (5). |
| **2** | (1) `"Coin.generated.h"` (2) `UCLASS()` (3) `GENERATED_BODY()`. Debe ser el último include porque el **UHT** genera código que depende de todo lo declarado antes. | 1 pt por espacio, 2 pts justificación. |
| **3** | A–2, B–1, C–3. | Todo correcto (5); una mal (3). |
| **4** | `UPROPERTY(EditAnywhere, Category = "Moneda") bool bEsCara = true;` / `UPROPERTY(EditAnywhere, Category = "Moneda") int32 Lanzamientos = 0;` — `bool` porque son solo dos estados; `int32` porque es un contador entero. `int32` garantiza **32 bits en todas las plataformas** (el tamaño de `int` depende del compilador). | 3 pts código, 2 pts justificación. |
| **5** | **b)** | Opción correcta (5). |
| **6** | `VisibleAnywhere` = solo lectura. Cambiar a `EditAnywhere`. | 5. |
| **7** | (1) `CreateDefaultSubobject` (2) `RootComponent` (3) `UStaticMeshComponent` (4) `SetupAttachment` | Cada espacio, más 1 punto si está todo correcto. |
| **8** | a) **Composición**: la moneda crea y es dueña del componente; el ciclo de vida de ambos es el mismo. b) **No** es igual: la grilla guarda **referencias** en un `TArray` → **agregación** (los dados son actores independientes del mundo; borrar el `TArray` no destruye los dados). Aceptar "asociación" si se justifica que solo guarda punteros. | 2.5 + 2.5. |
| **9** | (1) `/Engine/BasicShapes/Cylinder.Cylinder` (2) `SetStaticMesh`. En `BeginPlay` el motor lanza un **error/assert**: `ConstructorHelpers` solo puede usarse **dentro de un constructor** (carga de recursos al crear el objeto por defecto, el CDO). | 3 código + 2 teoría. |
| **10** | a) Diámetro **50**, grosor **5**. b) **Z**, porque el eje del cilindro es vertical (Z = arriba en Unreal). c) `FVector(0.8f, 0.8f, 0.08f)`. | a) 2, b) 1, c) 2. |
| **11** | **b)** `FRotator(0, 0, 90)` (Roll 90 sobre el eje X). (a) es **Yaw**: gira la moneda sobre el eje vertical Z; como es simétrica, no cambia nada visible. (d) cambia la escala, no la rotación (y la deja con tamaño 0 en X, Y). | 3 opción + 2 explicación. |
| **12** | a) `ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> Orange(TEXT("/Game/Puzzle/Meshes/OrangeMaterial.OrangeMaterial"));` (igual con `Blue`) → `MatCara = Orange.Get(); MatSello = Blue.Get();` (+ `#include "Materials/MaterialInstance.h"`). b) Así el **Garbage Collector** sabe que el objeto los está usando y **no los libera** (si no, el puntero podría quedar inválido). | 3 + 2. |
| **13** | `void ACoin::MostrarLado(){ CoinMesh->SetMaterial(0, bEsCara ? MatCara : MatSello); }` (if/else también es válido). Predicción: **azul**. | 4 código + 1 predicción. |
| **14** | `Super::BeginPlay(); bEsCara = FMath::RandBool(); MostrarLado();` — `override` (+`virtual`). Sin `Super::BeginPlay()` no se ejecuta la lógica de `AActor` (inicialización de componentes, Blueprints, `ReceiveBeginPlay`); el actor puede comportarse de forma incorrecta. | 3 + 2. |
| **15** | El constructor se ejecuta al crear el **objeto por defecto (CDO)**, en el editor y al cargar; define **valores por defecto y componentes**. Luego Unreal aplica los valores guardados del nivel/*Details*, así que la lógica de juego puede ser sobrescrita o ejecutarse cuando no hay partida. La lógica de juego va en `BeginPlay`. | Mencionar al menos 2 ideas: CDO/editor, sobrescritura de valores, separación defaults vs. lógica de juego. |
| **16** | (1) `UFUNCTION()` (2) `AddDynamic`. Los **delegados dinámicos** conectan la función **por nombre** mediante el sistema de reflexión; sin `UFUNCTION()` el UHT no la registra y el enlace falla. | 1 + 1 + 3. |
| **17** | `bEsCara = !bEsCara; Lanzamientos++; MostrarLado(); UE_LOG(LogTemp, Warning, TEXT("Moneda: %s - lanzamientos: %d"), bEsCara ? TEXT("CARA") : TEXT("SELLO"), Lanzamientos);` — Log: `SELLO - 1`, `CARA - 2`, `SELLO - 3`. | 3 código + 2 predicción. |
| **18** | Las cadenas literales deben ir con `TEXT(...)`: `bEsCara ? TEXT("CARA") : TEXT("SELLO")` (`UE_LOG` usa `TCHAR`). Bonus: `bEsCara = FMath::RandBool();` en lugar de `!bEsCara`. | 5 (+1 bonus). |
| **19** | a) `#include "Coin.h"` b) `ACoin* NuevaMoneda = GetWorld()->SpawnActor<ACoin>(GetActorLocation() + FVector(-300.f, 0.f, 0.f), FRotator::ZeroRotator);` c) `SpawnActor` registra el actor en el **mundo** (lo coloca, llama al constructor, inicializa componentes, ejecuta `BeginPlay` y lo administra el GC); con `new` el motor no lo conocería. | 1 + 2 + 2. |
| **20** | a) `UPROPERTY() class APuzzleDiceGameBlockGrid* OwningGrid;` b) `if (NuevaMoneda) { NuevaMoneda->OwningGrid = this; }` c) `if (bEsCara && OwningGrid) { OwningGrid->AddScore(); }` (+ `#include "PuzzleDiceGameBlockGrid.h"` en `Coin.cpp`). d) Composición / Agregación / Asociación. | 1 por inciso a–c, 2 por la tabla. |

---

## Código de referencia completo

<details>
<summary><code>Coin.h</code></summary>

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Coin.generated.h"

UCLASS()
class PUZZLEDICEGAME_API ACoin : public AActor
{
    GENERATED_BODY()

    UPROPERTY(VisibleDefaultsOnly, Category = "Moneda")
    class USceneComponent* DummyRoot;

    UPROPERTY(VisibleDefaultsOnly, Category = "Moneda")
    class UStaticMeshComponent* CoinMesh;

    UPROPERTY()
    class UMaterialInstance* MatCara;

    UPROPERTY()
    class UMaterialInstance* MatSello;

public:
    ACoin();

    UPROPERTY(EditAnywhere, Category = "Moneda")
    bool bEsCara = true;

    UPROPERTY(EditAnywhere, Category = "Moneda")
    int32 Lanzamientos = 0;

    UPROPERTY()
    class APuzzleDiceGameBlockGrid* OwningGrid;

    void MostrarLado();

    UFUNCTION()
    void CoinClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked);

protected:
    virtual void BeginPlay() override;
};
```
</details>

<details>
<summary><code>Coin.cpp</code></summary>

```cpp
#include "Coin.h"
#include "PuzzleDiceGameBlockGrid.h"
#include "UObject/ConstructorHelpers.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInstance.h"

ACoin::ACoin()
{
    DummyRoot = CreateDefaultSubobject<USceneComponent>(TEXT("Dummy0"));
    RootComponent = DummyRoot;

    CoinMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CoinMesh0"));
    CoinMesh->SetupAttachment(DummyRoot);

    ConstructorHelpers::FObjectFinderOptional<UStaticMesh> Cilindro(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
    ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> Orange(TEXT("/Game/Puzzle/Meshes/OrangeMaterial.OrangeMaterial"));
    ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> Blue(TEXT("/Game/Puzzle/Meshes/BlueMaterial.BlueMaterial"));

    CoinMesh->SetStaticMesh(Cilindro.Get());
    CoinMesh->SetRelativeScale3D(FVector(0.8f, 0.8f, 0.08f));

    MatCara = Orange.Get();
    MatSello = Blue.Get();

    CoinMesh->OnClicked.AddDynamic(this, &ACoin::CoinClicked);
}

void ACoin::BeginPlay()
{
    Super::BeginPlay();
    bEsCara = FMath::RandBool();
    MostrarLado();
}

void ACoin::MostrarLado()
{
    CoinMesh->SetMaterial(0, bEsCara ? MatCara : MatSello);
}

void ACoin::CoinClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked)
{
    bEsCara = !bEsCara;
    Lanzamientos++;
    MostrarLado();

    UE_LOG(LogTemp, Warning, TEXT("Moneda: %s - lanzamientos: %d"),
        bEsCara ? TEXT("CARA") : TEXT("SELLO"), Lanzamientos);

    if (bEsCara && OwningGrid)
    {
        OwningGrid->AddScore();
    }
}
```
</details>

<details>
<summary>Cambios en <code>PuzzleDiceGameBlockGrid.cpp</code></summary>

```cpp
#include "Coin.h"
// ...
void APuzzleDiceGameBlockGrid::BeginPlay()
{
    Super::BeginPlay();
    // ... ciclo que crea los dados ...

    ACoin* NuevaMoneda = GetWorld()->SpawnActor<ACoin>(
        GetActorLocation() + FVector(-300.f, 0.f, 0.f), FRotator::ZeroRotator);
    if (NuevaMoneda)
    {
        NuevaMoneda->OwningGrid = this;
    }
}
```
</details>

> **Nota para el docente:** `AddScore()` suma `points`, que no tiene valor inicial en el constructor de la grilla. Asigna `points` en el *Details* de la grilla (o inicialízalo en el constructor) para que el punto de verificación final muestre un cambio.
