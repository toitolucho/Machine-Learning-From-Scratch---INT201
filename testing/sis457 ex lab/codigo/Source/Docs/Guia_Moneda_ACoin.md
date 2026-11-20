# Guía de Laboratorio: Construcción de la Clase `ACoin`
## Programación Orientada a Objetos en C++ / Unreal Engine — Proyecto `PuzzleDiceGame`

---

## 1. Propósito

En esta guía el estudiante construye, paso a paso, una nueva clase **`ACoin`** que representa una moneda con dos lados, **CARA** y **SELLO**, dentro del mismo proyecto en el que se desarrolló la clase `ADice`. La mayor parte del código se proporciona; el estudiante debe completar algunos espacios sencillos, integrar la clase en el proyecto, configurarla en el editor de Unreal y **demostrar su funcionamiento** mediante escenarios de prueba.

## 2. Objetivos de aprendizaje

Al finalizar la guía, el estudiante será capaz de:

1. Crear una clase C++ derivada de `AActor` desde el editor de Unreal.
2. Declarar atributos expuestos al editor mediante `UPROPERTY`.
3. Construir la representación visual de un objeto con componentes y una malla básica, aplicando escala.
4. Distinguir las responsabilidades del constructor, de `BeginPlay()` y de los eventos.
5. Responder a la interacción del jugador mediante el evento `OnClicked`.
6. Establecer comunicación entre objetos (moneda y grilla) mediante un puntero de asociación.

## 3. Requisitos previos

* Proyecto `PuzzleDiceGame` abierto y compilando sin errores.
* Visual Studio configurado para el proyecto.
* Conocimiento de la clase `ADice` desarrollada en clase (se utilizará como referencia).

## 4. Convenciones de la guía

* Los espacios marcados con `______` deben ser completados por el estudiante. Cada uno se acompaña de una pista en un comentario `// PISTA:`.
* Cada paso termina con un **Punto de verificación**, que describe lo que debe observarse en el editor antes de continuar.
* Los **Escenarios de demostración** (sección 5) se realizan al final y constituyen la evidencia de la entrega.
* Cuando se modifica un archivo `.h` (se agregan atributos o métodos), se recomienda **cerrar el editor de Unreal y compilar desde Visual Studio** (configuración *Development Editor*). Para cambios solo en archivos `.cpp`, puede utilizarse el botón **Compile** del editor.

---

## Paso 1. Creación de la clase vacía

### 1.1 Procedimiento

1. En el editor de Unreal, abrir el menú **File → New C++ Class...**
2. Seleccionar la clase padre **Actor** y presionar **Next**.
3. Asignar el nombre **`Coin`**. Unreal agregará automáticamente el prefijo `A`, por lo que la clase se llamará `ACoin`.
4. Presionar **Create Class**. Se generarán los archivos `Coin.h` y `Coin.cpp` en la carpeta `Source/PuzzleDiceGame/`.

### 1.2 Fundamento

Toda entidad que puede ubicarse en el nivel, poseer posición y rotación, y recibir eventos, hereda de `AActor`. Por convención de Epic Games, las clases derivadas de `AActor` llevan el prefijo `A`, mientras que las derivadas de `UObject` y los componentes llevan el prefijo `U`.

### 1.3 Limpieza del código generado

Reemplazar el contenido de `Coin.h` por el siguiente esqueleto y completar el espacio:

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "______"        // PISTA: nombre del archivo + ".generated.h". Debe ser el último include.

UCLASS()
class PUZZLEDICEGAME_API ACoin : public AActor
{
    GENERATED_BODY()

public:
    ACoin();
};
```

Reemplazar el contenido de `Coin.cpp` por:

```cpp
#include "Coin.h"

ACoin::ACoin()
{
}
```

### Punto de verificación 1

Compilar el proyecto. En el **Content Browser**, dentro de **C++ Classes → PuzzleDiceGame**, debe aparecer la clase `Coin`. Arrastrarla al nivel y comprobar que aparece en el **World Outliner** con el nombre `Coin`. Todavía no es visible en la escena, porque no tiene malla.

---

## Paso 2. Atributos de la moneda

### 2.1 Código

En `Coin.h`, dentro de la sección `public`, agregar los atributos y completar los espacios:

```cpp
public:
    ACoin();

    /** Indica si el lado visible es CARA (true) o SELLO (false). */
    UPROPERTY(______, Category = "Moneda")      // PISTA: especificador que permite EDITAR el valor en el panel Details.
    bool bEsCara = true;

    /** Número de veces que la moneda ha sido lanzada. */
    UPROPERTY(EditAnywhere, Category = "Moneda")
    ______ Lanzamientos = 0;                      // PISTA: tipo entero de 32 bits que utiliza Unreal.

    /** Si es verdadero, la moneda elige un lado al azar al iniciar la partida. */
    UPROPERTY(EditAnywhere, Category = "Moneda")
    bool bLadoAleatorio = true;
```

### 2.2 Fundamento

* `bool` representa un valor con dos estados; es adecuado para el lado de la moneda.
* `int32` garantiza un entero de 32 bits en cualquier plataforma, a diferencia de `int`, cuyo tamaño depende del compilador.
* La macro `UPROPERTY` registra el atributo en el **sistema de reflexión** de Unreal. Sin ella, el atributo existe en C++, pero no aparece en el editor.
* El atributo `bLadoAleatorio` permite controlar desde el editor si el lado inicial es aleatorio o fijo; se utilizará en los escenarios de demostración.

### Punto de verificación 2

Cerrar el editor, compilar desde Visual Studio y volver a abrir el proyecto. Seleccionar la moneda en el nivel y verificar que en el panel **Details** aparece la categoría **Moneda** con los atributos `bEsCara`, `Lanzamientos` y `bLadoAleatorio`, y que sus valores pueden modificarse.

---

## Paso 3. Componentes y malla en el constructor

### 3.1 Declaración de componentes

En `Coin.h`, inmediatamente después de `GENERATED_BODY()` (antes de `public:`), declarar los componentes como privados:

```cpp
    /** Componente raíz de la moneda. */
    UPROPERTY(VisibleDefaultsOnly, Category = "Moneda")
    class USceneComponent* DummyRoot;

    /** Malla visible de la moneda. */
    UPROPERTY(VisibleDefaultsOnly, Category = "Moneda")
    class UStaticMeshComponent* CoinMesh;
```

### 3.2 Construcción de la malla

En `Coin.cpp`, agregar los `include` necesarios y completar el constructor:

```cpp
#include "Coin.h"
#include "UObject/ConstructorHelpers.h"
#include "Components/StaticMeshComponent.h"

ACoin::ACoin()
{
    // 1. Componente raíz
    DummyRoot = CreateDefaultSubobject<USceneComponent>(TEXT("Dummy0"));
    RootComponent = DummyRoot;

    // 2. Componente de malla, unido a la raíz
    CoinMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CoinMesh0"));
    CoinMesh->SetupAttachment(DummyRoot);

    // 3. Carga de la malla básica del cilindro
    ConstructorHelpers::FObjectFinderOptional<UStaticMesh> Cilindro(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
    CoinMesh->______(Cilindro.Get());            // PISTA: método que asigna una malla estática (Set + Static + Mesh).

    // 4. Escala: el cilindro mide 100 x 100 x 100 unidades; se reduce su altura (eje Z)
    CoinMesh->SetRelativeScale3D(FVector(0.8f, 0.8f, ______));   // PISTA: grosor de 8 unidades -> 8 / 100.

    // 5. Colisión para poder recibir clics del ratón
    CoinMesh->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
}
```

### 3.3 Fundamento

* La moneda **crea y es dueña** de sus componentes; estos se destruyen junto con ella. Esta relación es una **composición**.
* `ConstructorHelpers` solo puede utilizarse dentro del constructor. Si se traslada a otro método, el motor detiene la ejecución con un error.
* La escala multiplica el tamaño original en cada eje: con `FVector(0.8f, 0.8f, 0.08f)` la moneda tiene 80 unidades de diámetro y 8 de grosor.

### Punto de verificación 3

Compilar. La moneda colocada en el nivel debe verse como un disco delgado. Si se arrastra una nueva moneda al nivel, debe tener la misma forma.

---

## Paso 4. Representación de CARA y SELLO con materiales

### 4.1 Declaración

En `Coin.h`, en la sección privada (junto a los componentes), agregar:

```cpp
    /** Material para el lado CARA (naranja). */
    UPROPERTY()
    class UMaterialInstance* MatCara;

    /** Material para el lado SELLO (azul). */
    UPROPERTY()
    class UMaterialInstance* MatSello;
```

En la sección `public`, declarar el método:

```cpp
    /** Aplica el material correspondiente al lado visible. */
    void MostrarLado();
```

### 4.2 Carga de materiales e implementación

En `Coin.cpp`, agregar el `include` del material:

```cpp
#include "Materials/MaterialInstance.h"
```

Al final del constructor, cargar los materiales que ya existen en el proyecto:

```cpp
    // 6. Materiales existentes en el proyecto
    ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> Orange(TEXT("/Game/Puzzle/Meshes/OrangeMaterial.OrangeMaterial"));
    ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> Blue(TEXT("/Game/Puzzle/Meshes/BlueMaterial.BlueMaterial"));
    MatCara = Orange.Get();
    MatSello = Blue.Get();
```

Implementar el método después del constructor y completar el espacio:

```cpp
void ACoin::MostrarLado()
{
    if (______)                                  // PISTA: atributo que indica si el lado visible es CARA.
    {
        CoinMesh->SetMaterial(0, MatCara);
    }
    else
    {
        CoinMesh->SetMaterial(0, MatSello);
    }
}
```

### 4.3 Fundamento

Los punteros `MatCara` y `MatSello` llevan `UPROPERTY()` aunque no se muestren en el editor. De este modo, el **recolector de basura** de Unreal sabe que los materiales están en uso y no los libera.

### Punto de verificación 4

Compilar. El proyecto debe compilar sin errores. Todavía no se observa un cambio de color, porque `MostrarLado()` aún no se invoca.

---

## Paso 5. Inicio de la partida (`BeginPlay`)

### 5.1 Código

En `Coin.h`, agregar una sección `protected`:

```cpp
protected:
    virtual void BeginPlay() override;
```

En `Coin.cpp`, implementar el método y completar el espacio:

```cpp
void ACoin::BeginPlay()
{
    Super::BeginPlay();

    if (bLadoAleatorio)
    {
        bEsCara = FMath::______();               // PISTA: función de FMath que devuelve true o false al azar (Rand + Bool).
    }

    MostrarLado();
}
```

### 5.2 Fundamento

* `override` indica que se redefine un método virtual de la clase padre `AActor`.
* `Super::BeginPlay()` ejecuta la lógica de inicialización de `AActor`; no debe omitirse.
* El constructor define componentes y valores por defecto, y se ejecuta también en el editor. La lógica de juego, como elegir un lado al azar, corresponde a `BeginPlay()`, que se ejecuta cuando inicia la partida.

### Punto de verificación 5

Presionar **Play** varias veces. La moneda debe aparecer en algunas ejecuciones de color naranja (CARA) y en otras de color azul (SELLO).

---

## Paso 6. Interacción con el clic

### 6.1 Declaración

En `Coin.h`, sección `public`:

```cpp
    /** Responde al clic del jugador sobre la moneda. */
    UFUNCTION()
    void CoinClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked);
```

### 6.2 Conexión del evento

En `Coin.cpp`, al final del constructor:

```cpp
    // 7. Conexión del evento de clic
    CoinMesh->OnClicked.AddDynamic(this, &ACoin::CoinClicked);
```

### 6.3 Implementación

En `Coin.cpp`, implementar el método y completar los espacios:

```cpp
void ACoin::CoinClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked)
{
    bEsCara = FMath::RandBool();                 // Lanzamiento aleatorio
    ______;                                      // PISTA: incrementar en uno el atributo Lanzamientos (operador ++).
    MostrarLado();

    UE_LOG(LogTemp, Warning, TEXT("Moneda %s: %s - lanzamientos: %d"),
        *GetName(),
        bEsCara ? ______("CARA") : TEXT("SELLO"),   // PISTA: macro que convierte el literal al tipo de texto de Unreal.
        Lanzamientos);
}
```

### 6.4 Fundamento

* `OnClicked` es un **delegado dinámico** del componente; `AddDynamic` le asocia un método.
* Los delegados dinámicos enlazan el método por su nombre mediante el sistema de reflexión; por ello el método debe estar marcado con `UFUNCTION()`.
* `UE_LOG` trabaja con cadenas de tipo `TCHAR`; los literales deben envolverse en la macro `TEXT(...)`.

### Punto de verificación 6

Abrir el registro con **Window → Developer Tools → Output Log**. Presionar **Play** y hacer clic varias veces sobre la moneda. En cada clic, el color debe corresponder al lado indicado en el registro, y el contador de lanzamientos debe aumentar en uno.

---

## Paso 7. Comunicación con la grilla

En este paso la moneda deja de colocarse manualmente: la **grilla** la crea al iniciar la partida y la moneda **notifica** a la grilla cada vez que sale CARA.

### 7.1 Atributo de asociación en la moneda

En `Coin.h`, sección `public`:

```cpp
    /** Grilla dueña de la moneda. */
    UPROPERTY()
    class APuzzleDiceGameBlockGrid* OwningGrid;
```

En `Coin.cpp`, agregar el `include` de la grilla:

```cpp
#include "PuzzleDiceGameBlockGrid.h"
```

Al final de `CoinClicked`, agregar la notificación y completar el espacio:

```cpp
    if (bEsCara && ______)                       // PISTA: puntero a la grilla; se comprueba que no sea nulo.
    {
        OwningGrid->AddScore();
    }
```

En el constructor, inicializar el puntero:

```cpp
    OwningGrid = nullptr;
```

### 7.2 Creación de la moneda desde la grilla

En `PuzzleDiceGameBlockGrid.cpp`, agregar el `include`:

```cpp
#include "Coin.h"
```

En `APuzzleDiceGameBlockGrid::BeginPlay()`, **después** del ciclo `for` que crea los dados, agregar y completar:

```cpp
    // Creación de la moneda a la izquierda de la grilla
    ACoin* NuevaMoneda = GetWorld()->______<ACoin>(       // PISTA: mismo método que se usa para crear los dados.
        GetActorLocation() + FVector(-300.f, 0.f, 0.f), FRotator::ZeroRotator);

    if (NuevaMoneda)
    {
        NuevaMoneda->OwningGrid = this;
    }
```

### 7.3 Fundamento

* `SpawnActor` registra el actor en el mundo: ejecuta su constructor, inicializa sus componentes y llama a `BeginPlay()`. Un objeto creado con `new` no formaría parte del nivel.
* La moneda conoce a la grilla solo mediante el puntero `OwningGrid`, para enviarle mensajes. Esta relación es una **asociación**, la misma que existe entre `ADice` y la grilla.
* La comprobación de `OwningGrid` distinto de nulo evita un fallo cuando la moneda se coloca manualmente en el nivel, sin grilla.

### Punto de verificación 7

Compilar. Eliminar del nivel las monedas colocadas manualmente. Al presionar **Play** debe aparecer una moneda a la izquierda de la grilla de dados, sin haberla colocado en el editor.

---

## Paso 8. Resumen de la estructura final

| Elemento | Ubicación | Responsabilidad |
|---|---|---|
| `bEsCara`, `Lanzamientos`, `bLadoAleatorio` | `public`, con `UPROPERTY(EditAnywhere)` | Estado de la moneda, editable desde el editor |
| `DummyRoot`, `CoinMesh` | privados | Representación visual (composición) |
| `MatCara`, `MatSello` | privados, con `UPROPERTY()` | Materiales de cada lado |
| `OwningGrid` | `public` | Comunicación con la grilla (asociación) |
| Constructor | `Coin.cpp` | Componentes, malla, escala, materiales y conexión de eventos |
| `BeginPlay()` | `protected` | Lado inicial de la partida |
| `MostrarLado()` | `public` | Aplicar el material del lado visible |
| `CoinClicked()` | `public`, `UFUNCTION()` | Lanzamiento, contador, registro y notificación a la grilla |

---

## 5. Escenarios de demostración

Cada escenario debe configurarse en el editor de Unreal y documentarse con la evidencia indicada (captura de pantalla del nivel, del panel **Details** o del **Output Log**, según corresponda).

### Escenario A — Moneda colocada manualmente con lado fijo

1. Arrastrar una moneda `Coin` al nivel, lejos de la grilla.
2. En **Details → Moneda**, desmarcar `bLadoAleatorio` y desmarcar `bEsCara`.
3. Presionar **Play** tres veces.

**Resultado esperado:** la moneda inicia siempre de color **azul** (SELLO).
**Evidencia:** captura del panel **Details** y captura del nivel en ejecución.

### Escenario B — Tres monedas con configuraciones distintas

1. Colocar tres monedas en el nivel, una junto a otra.
2. Configurar en **Details**:
   * Moneda 1: `bLadoAleatorio` desmarcado, `bEsCara` marcado.
   * Moneda 2: `bLadoAleatorio` desmarcado, `bEsCara` desmarcado.
   * Moneda 3: `bLadoAleatorio` marcado.
3. Presionar **Play** y hacer clic dos veces sobre la moneda 1.

**Resultado esperado:** al iniciar, la moneda 1 es naranja, la moneda 2 es azul y la moneda 3 tiene un color aleatorio. Las tres son objetos distintos de la misma clase: el clic sobre la moneda 1 solo modifica su propio estado, y el registro muestra su nombre con `lanzamientos: 1` y `lanzamientos: 2`.
**Evidencia:** captura del nivel al iniciar y captura del **Output Log**.

### Escenario C — Escala de la instancia

1. Seleccionar una de las monedas colocadas manualmente.
2. En **Details → Transform → Scale**, asignar `2.0` en los tres ejes.
3. Presionar **Play** y hacer clic sobre ella.

**Resultado esperado:** la moneda es del doble de tamaño que las demás y sigue respondiendo al clic.
**Evidencia:** captura del nivel en ejecución.

### Escenario D — Valor inicial del contador

1. Seleccionar una moneda colocada manualmente y asignar `Lanzamientos = 10` en **Details**.
2. Presionar **Play** y hacer clic una vez sobre ella.

**Resultado esperado:** el registro muestra `lanzamientos: 11`, lo que demuestra que el valor configurado en el editor reemplaza al valor por defecto del constructor.
**Evidencia:** captura del **Output Log**.

### Escenario E — Integración con la grilla y la puntuación

1. Eliminar del nivel todas las monedas colocadas manualmente.
2. Seleccionar la grilla (`PuzzleDiceGameBlockGrid`) en el **World Outliner**.
3. En **Details → Grid**, asignar `Points = 5`, `Rows = 2` y `Columns = 3`.
4. Presionar **Play** y hacer clic sobre la moneda creada por la grilla hasta obtener al menos dos resultados CARA.

**Resultado esperado:** la grilla muestra 6 dados y una moneda a su izquierda. Cada resultado CARA incrementa la **Puntuación** en 5 puntos; los resultados SELLO no la modifican.
**Evidencia:** captura del nivel en ejecución con la puntuación visible y captura del **Output Log** con los lanzamientos.

---

## 6. Entregables

1. Archivos `Coin.h` y `Coin.cpp` completos, y `PuzzleDiceGameBlockGrid.cpp` modificado.
2. Un documento con las capturas de los escenarios A a E, cada una con un título que identifique el escenario.
3. Respuesta breve (de dos a tres líneas cada una) a las siguientes preguntas:
   * ¿Qué relación existe entre `ACoin` y `CoinMesh`, y cuál entre `ACoin` y la grilla? Justificar.
   * ¿Por qué el lado aleatorio se elige en `BeginPlay()` y no en el constructor?
   * ¿Qué demuestra el escenario B sobre la diferencia entre clase y objeto?

## 7. Criterios de evaluación

| Criterio | Puntaje |
|---|---|
| La clase compila y la moneda se visualiza con la forma correcta (pasos 1 a 3) | 20 |
| Materiales y lado inicial funcionan correctamente (pasos 4 y 5) | 15 |
| El clic cambia el lado, incrementa el contador y registra el mensaje (paso 6) | 20 |
| La grilla crea la moneda y la puntuación aumenta con CARA (paso 7) | 20 |
| Evidencia completa de los escenarios A a E | 15 |
| Respuestas a las preguntas de reflexión | 10 |
| **Total** | **100** |
