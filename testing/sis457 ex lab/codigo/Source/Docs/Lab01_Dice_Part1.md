# Laboratorio de Programación Orientada a Objetos en C++ / Unreal Engine
## Mini-Proyecto: Desarrollo Modular de un Dado 3D Interactivo (`ADice`)
### Parte 1: Creación del Actor Vacío y Fundamentos de Arquitectura en Unreal Engine

---

## 1. Visión General del Proyecto

En este laboratorio los estudiantes construirán paso a paso una entidad interactiva de videojuego (**un dado 3D**) aplicando principios fundamentales de la **Programación Orientada a Objetos (POO)** y la arquitectura del motor **Unreal Engine**:

1. **Herencia y Ciclo de Vida**: Especialización a partir de la clase base `AActor`.
2. **Composición sobre Herencia**: Adición de `USceneComponent` y `UStaticMeshComponent`.
3. **Encapsulamiento y Reflexión**: Exposición controlada de variables mediante macros `UPROPERTY`.
4. **Cinemática y Matemáticas 3D**: Simulación de gravedad, impulso y rotación angular en `Tick`.
5. **Álgebra Vectorial**: Detección de la cara superior mediante el **Producto Punto (Dot Product)**.

---

## 2. Hoja de Ruta del Mini-Proyecto (11 Hitos Didácticos)

| Hito | Nombre del Checkpoint Git | Descripción |
| :---: | :--- | :--- |
| **01** | `step-01-empty-actor` | **Creación de la clase `ADice` vacía derivada de `AActor`.** *(Paso actual)* |
| **02** | `step-02-basic-mesh` | Incorporación del `DummyRoot` y un cubo básico como componente visual. |
| **03** | `step-03-dice-mesh` | Reemplazo de la geometría genérica por la malla personalizada `dice.dice`. |
| **04** | `step-04-value-attribute` | Declaración del atributo `Value` (1..6) expuesto al editor con `UPROPERTY`. |
| **05** | `step-05-show-dice-face` | Implementación de `ShowDiceFace(int32 Face)` con rotaciones espaciales (`FRotator`). |
| **06** | `step-06-tick-inspection` | Inspección y prueba reactiva de `ShowDiceFace` en `Tick`. |
| **07** | `step-07-click-debug` | Configuración de colisión física (`ECC_Visibility`), Pawn raycast y logs de clic. |
| **08** | `step-08-incremental-face` | Avance cíclico de caras al hacer clic (`Value++` con reinicio al llegar a 6). |
| **09** | `step-09-jump-physics` | Cinemática de salto vertical: atributos `Force`, `Gravity` y traslación en `Tick`. |
| **10** | `step-10-air-rotation` | Rotación angular 3D aleatoria mientras el dado se encuentra en el aire. |
| **11** | `step-11-face-detection` | Aterrizaje suave, cálculo de la cara superior mediante Producto Punto y encaje plano. |

---

## 3. Objetivos de Aprendizaje de la Parte 1

Al finalizar esta primera etapa, el estudiante será capaz de:
* Comprender qué es un `AActor` en Unreal Engine y relacionarlo con conceptos de POO tradicional (C#/Delphi/Java) y Unity.
* Entender la función del **Unreal Header Tool (UHT)** y el rol de las macros `UCLASS()`, `GENERATED_BODY()` y archivos `.generated.h`.
* Distinguir las etapas del ciclo de vida básico de un Actor: **Constructor**, **`BeginPlay()`** y **`Tick()`**.
* Compilar código C++ e instanciar la clase dentro del nivel de juego verificando su presencia en el *World Outliner*.

---

## 4. Fundamentos Teóricos

### 4.1 ¿Qué es un `AActor`?
En Unreal Engine, toda entidad que puede ubicarse, orientarse o instanciarse dentro de un nivel (mundo 3D) hereda de la clase base `AActor` (que a su vez hereda de `UObject`).

* **Equivalencia en Unity**: Es el equivalente a un `GameObject`.
* **Equivalencia en Windows Forms / Delphi**: Es el equivalente a un control visual (`Control` o `TWinControl`) que pertenece a un contenedor (`Form`), pero con 3 dimensiones espaciales.
* **Prefijo 'A'**: Por convención oficial de codificación de Epic Games, todas las clases que heredan de `AActor` llevan el prefijo **`A`** (ejemplo: `ADice`), mientras que las que heredan de `UObject` o componentes llevan el prefijo **`U`** (ejemplo: `UStaticMeshComponent`).

### 4.2 El Sistema de Reflexión y el UHT
C++ estándar no posee introspección ni reflexión nativa. Unreal Engine resuelve esto mediante el **Unreal Header Tool (UHT)**, un precompilador que analiza macros especiales:
* `UCLASS()`: Registra la clase en el sistema de tipos de Unreal para recolección de basura, replicación y visualización en el editor.
* `GENERATED_BODY()`: Macro requerida dentro del cuerpo de la clase que expande el código autogenerado por el motor.
* `#include "Dice.generated.h"`: **Regla estricta:** Debe ser siempre el último archivo `#include` en la lista de cabeceras.

### 4.3 Ciclo de Vida: Constructor vs BeginPlay vs Tick

| Método | Momento de Ejecución | Responsabilidad Principal |
| :--- | :--- | :--- |
| **`ADice()` (Constructor)** | En tiempo de edición y al cargar el asset en memoria (CDO). | Inicializar valores primitivos predeterminados y crear subobjetos/componentes por defecto (`CreateDefaultSubobject`). |
| **`BeginPlay()`** | Al presionar "Play" en el editor o cuando el Actor es spawneado en runtime. | Inicializar lógica de juego que depende de que el mundo ya exista (temporizadores, suscripción a eventos, lecturas de otros actores). |
| **`Tick(float DeltaTime)`** | En cada fotograma renderizado por el motor. | Actualizaciones continuas en tiempo real (física personalizada, interpolaciones, movimiento). |

---

## 5. Implementación del Código (Paso 1)

### 5.1 Archivo de Cabecera: `Dice.h`

```cpp
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Dice.generated.h"

/**
 * Clase ADice: Entidad base para el dado de nuestro juego de puzzle.
 * Hereda de AActor para poder existir en el mundo 3D.
 */
UCLASS()
class PUZZLEDICEGAME_API ADice : public AActor
{
	GENERATED_BODY()
	
public:	
	// Constructor: Establece valores predeterminados
	ADice();

protected:
	// Llamado cuando el juego inicia o cuando el actor es instanciado en el mundo
	virtual void BeginPlay() override;

public:	
	// Llamado en cada fotograma del juego
	virtual void Tick(float DeltaTime) override;
};
```

### 5.2 Archivo de Implementación: `Dice.cpp`

```cpp
// Fill out your copyright notice in the Description page of Project Settings.

#include "Dice.h"

// Establece valores por defecto en el constructor
ADice::ADice()
{
 	// Habilitamos la función Tick() para que el motor la ejecute cada frame
	PrimaryActorTick.bCanEverTick = true;
}

// Llamado cuando el juego inicia o cuando el actor se genera
void ADice::BeginPlay()
{
	Super::BeginPlay();
	
	// Mensaje de diagnóstico para verificar que el actor cobró vida
	UE_LOG(LogTemp, Warning, TEXT("ADice ha iniciado correctamente en BeginPlay()"));
}

// Llamado cada frame
void ADice::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}
```

---

## 6. Guía Práctica de Verificación en Unreal Editor

1. **Compilación del Código**:
   * En Visual Studio: Menú `Build` $\rightarrow$ `Build Solution` (o `Ctrl + Shift + B`).
   * O directamente en Unreal Editor: Clic en el botón **Live Coding** (icono de carpetas con rayo en la barra inferior) o presionar `Ctrl + Alt + F11`.
2. **Inspección en Content Browser**:
   * Abrir la carpeta `C++ Classes` $\rightarrow$ `PuzzleDiceGame`.
   * Verificar que la clase `Dice` aparece con el icono azul de C++.
3. **Instanciación en el Nivel**:
   * Arrastrar la clase `Dice` directamente desde el Content Browser hacia la escena (nivel 3D).
4. **Verificación en el World Outliner**:
   * Comprobar que aparece listado un nuevo objeto llamado `Dice1`.
   * **Observación crítica para los alumnos**: El objeto tiene posición en el espacio, pero en el viewport 3D es solo una esfera de coordenadas o un ícono translúcido. No se puede ver ningún cuerpo geométrico porque **un `AActor` por sí mismo es un contenedor lógico; no tiene forma visual sin componentes**.

---

## 7. Registro de Versión en Git

Para registrar este hito en el repositorio del curso y que los alumnos puedan volver a este punto en cualquier momento:

```bash
# 1. Verificar estado de los archivos modificados
git status

# 2. Agregar archivos
git add Source/PuzzleDiceGame/Dice.h Source/PuzzleDiceGame/Dice.cpp

# 3. Crear commit descriptivo
git commit -m "feat(dice): Paso 01 - Creación de la clase vacía ADice derivada de AActor"

# 4. Crear etiqueta (Tag) para los alumnos
git tag step-01-empty-actor
```

---

## 8. Preguntas de Autoevaluación para el Estudiante

1. **¿Qué sucede si eliminas la línea `#include "Dice.generated.h"` o la colocas al inicio del archivo `Dice.h`?**
   * *Respuesta esperada:* El compilador UHT generará un error de sintaxis estricto, ya que las definiciones de macro autogeneradas requieren conocer todos los tipos declarados previamente.
2. **Si colocamos una instancia de `ADice` en el mapa y le damos a "Play", ¿por qué no cae hacia abajo?**
   * *Respuesta esperada:* Porque no posee ningún componente de física ni geometría que interactúe con el motor de colisiones. Solo existe como un punto de referencia en el espacio.
3. **¿Cuál es la diferencia entre colocar código en el Constructor de `ADice` vs colocarlo en `BeginPlay()`?**
   * *Respuesta esperada:* El constructor se ejecuta en tiempo de diseño/edición para crear la estructura base del asset. `BeginPlay()` se ejecuta únicamente cuando el juego corre en vivo (runtime).

---
*Próximo paso: **Paso 02 - Composición de Componentes: Añadiendo el Root y la Malla Geométrica Básica**.*
