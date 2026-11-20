// Fill out your copyright notice in the Description page of Project Settings.

#include "Dice.h"
#include "PuzzleDiceGameBlockGrid.h"
// Sets default values
ADice::ADice()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	// Inicializar atributos de salto y fisica
	Force = 1000.0f;
	Gravity = 2500.0f;
	MinRollSpeed = 360.0f;
	MaxRollSpeed = 720.0f;
	bIsJumping = false;
	InitialZ = 0.0f;
	VerticalSpeed = 0.0f;
	AngularVelocity = FRotator::ZeroRotator;

	// Create dummy root scene component
	DummyRoot = CreateDefaultSubobject<USceneComponent>(TEXT("Dummy0"));
	RootComponent = DummyRoot;

	
	//StaticMesh'/Game/StarterContent/Shapes/Shape_Cone.Shape_Cone'
	// Create static mesh component
	BlockMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BlockMesh0"));
	//ConstructorHelpers::FObjectFinderOptional<UStaticMesh> PlaneMesh(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));

	ConstructorHelpers::FObjectFinderOptional<UStaticMesh> PlaneMesh(TEXT("/Game/Puzzle/Meshes/dice.dice"));
	//StaticMesh'/Game/Puzzle/Meshes/dice.dice'


	/*ConstructorHelpers::FObjectFinderOptional<UStaticMesh> Cono(TEXT("/Game/StarterContent/Shapes/Shape_Cone.Shape_Cone"));
	ConstructorHelpers::FObjectFinderOptional<UStaticMesh> Cilindro(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	ConstructorHelpers::FObjectFinderOptional<UStaticMesh> Esfera(TEXT("/Game/StarterContent/Shapes/Shape_Sphere.Shape_Sphere"));
	*///StaticMesh'/Engine/BasicShapes/Cylinder.Cylinder'

	//if (Cono.Succeeded())
	//{
	//	ConoMesh = Cono.Get();
	//}
	//if (Cilindro.Succeeded())
	//{
	//	CilindroMesh = Cilindro.Get();
	//}
	//if (Esfera.Succeeded())
	//{
	//	EsferaMesh = Esfera.Get();
	//}

	BlockMesh->SetStaticMesh(PlaneMesh.Get());
	
	BlockMesh->SetupAttachment(DummyRoot);

	// Configurar colision explicita para responder a clics del mouse y raycasts
	BlockMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	BlockMesh->SetCollisionObjectType(ECC_WorldDynamic);
	BlockMesh->SetCollisionResponseToAllChannels(ECR_Block);
	BlockMesh->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);

	BlockMesh->OnClicked.AddDynamic(this, &ADice::BlockClicked);
	//BlockMesh->OnInputTouchBegin.AddDynamic(this, &ADice::OnFingerPressedBlock);
}


void ADice::BlockClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked)
{
	//ApplyVerticalImpulse();

	//UE_LOG(LogTemp, Warning, TEXT("Hicieron Click"));

	//ShowDiceFace(Value);
	
	UE_LOG(LogTemp, Warning, TEXT("Dado Seleccionado : %s con valor %d"), *GetName(), Value);

	for (ADice* dado : OwningGrid->listaDados)
	{
		if (Value == dado->Value)
		{
			//dado->Value = FMath::RandRange(1, 6);
			//dado->ShowDiceFace(dado->Value);
			dado->ApplyVerticalImpulse();
		}
	}

}

void ADice::ApplyVerticalImpulse()
{
	// Evitar nuevo impulso si ya esta en el aire
	if (bIsJumping)
	{
		return;
	}

	InitialZ = GetActorLocation().Z;
	VerticalSpeed = Force;
	bIsJumping = true;

	// Generar una velocidad de rotacion angular aleatoria para cada eje (Pitch, Yaw, Roll)
	AngularVelocity = FRotator(
		FMath::RandRange(MinRollSpeed, MaxRollSpeed) * (FMath::RandBool() ? 1.0f : -1.0f),
		FMath::RandRange(MinRollSpeed, MaxRollSpeed) * (FMath::RandBool() ? 1.0f : -1.0f),
		FMath::RandRange(MinRollSpeed, MaxRollSpeed) * (FMath::RandBool() ? 1.0f : -1.0f)
	);

	UE_LOG(LogTemp, Warning, TEXT("Impulso aplicado! Fuerza: %f, Giro: (P: %f, Y: %f, R: %f)"),
		Force, AngularVelocity.Pitch, AngularVelocity.Yaw, AngularVelocity.Roll);
}

void ADice::OnFingerPressedBlock(ETouchIndex::Type FingerIndex, UPrimitiveComponent* TouchedComponent)
{
	UE_LOG(LogTemp, Warning, TEXT("Hicieron Click"));
	//HandleClicked();
}

// void ADice::ShowDiceFace(int32 FaceNumber)
// {
// 	if (FaceNumber == 1)
// 	{
// 		//mostrar la cara 1
// 		//rotar el objecto  (x,y,z) -> (0,0,0), (90,0,0), (180,0,0) , (0,90,0) 

// 		//Cara 1 -> (0,270,0)

// 		//Cara 2 -> (270,0,0)

// 		FRotator nuevaRotacion(-90, 0, 0);
// 		SetActorRotation(nuevaRotacion);
		
// 	}
// 	if (FaceNumber == 2)
// 	{
		
// 		FRotator nuevaRotacion(0, 0, -90);
// 		SetActorRotation(nuevaRotacion);

// 	}

// 	if (FaceNumber == 3)
// 	{
// 		FRotator nuevaRotacion(0, 90, 0);
// 		SetActorRotation(nuevaRotacion);

// 	}
// }

//BlockMesh->OnClicked.AddDynamic(this, &APuzzleDiceGameBlock::BlockClicked);

void ADice::NextFace()
{
	UE_LOG(LogTemp, Warning,  TEXT("Hicieron Click para cambiar la cara"));
	Value++;
	
	ShowDiceFace(Value);
	if(Value ==6)
	{
		Value =0;
	}
}


// Called when the game starts or when spawned
void ADice::BeginPlay()
{
	Super::BeginPlay();

	// Cambiar malla solo si se asigno validamente
	if (tipo == 1 && CilindroMesh)
	{		
		BlockMesh->SetStaticMesh(CilindroMesh);
	}
	else if (tipo == 2 && EsferaMesh)
	{
		BlockMesh->SetStaticMesh(EsferaMesh);
	}
	else if (tipo == 3 && ConoMesh)
	{
		BlockMesh->SetStaticMesh(ConoMesh);
	}

	// Asegurar colision activa en runtime
	BlockMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	BlockMesh->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);

	// Asegurar delegados dinamicos en runtime
	BlockMesh->OnClicked.AddUniqueDynamic(this, &ADice::BlockClicked);
	BlockMesh->OnInputTouchBegin.AddUniqueDynamic(this, &ADice::OnFingerPressedBlock);
	
	ShowDiceFace(Value);
}

// Called every frame
void ADice::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (bIsJumping)
	{
		// 1. Aplicar aceleracion de la gravedad a la velocidad vertical: v = v0 - (g * dt)
		VerticalSpeed -= Gravity * DeltaTime;

		// 2. Mover la posicion Z del dado: z = z0 + (v * dt)
		FVector CurrentLocation = GetActorLocation();
		CurrentLocation.Z += VerticalSpeed * DeltaTime;

		// 3. Rotar el dado en el aire en cada frame: deltaRot = velocidadAngular * dt
		AddActorLocalRotation(AngularVelocity * DeltaTime);

		// 4. Comprobar aterrizaje: si desciende y pasa por debajo o igual a la altura inicial
		if (CurrentLocation.Z <= InitialZ && VerticalSpeed < 0.0f)
		{
			CurrentLocation.Z = InitialZ;
			bIsJumping = false;
			VerticalSpeed = 0.0f;
			AngularVelocity = FRotator::ZeroRotator;

			// 5. Determinar matematicamente que cara quedo arriba usando producto punto
			Value = CalculateTopFace();

			// 6. Encajar el dado en la rotacion plana exacta de la cara ganadora
			ShowDiceFace(Value);

			UE_LOG(LogTemp, Warning, TEXT("El dado ha aterrizado! Cara ganadora: %d"), Value);
		}

		SetActorLocation(CurrentLocation);
	}
}

int32 ADice::CalculateTopFace()
{
	// 1. Obtener los vectores direccionales del dado en coordenadas de mundo
	FVector ForwardVector = GetActorForwardVector(); // Eje local +X
	FVector RightVector   = GetActorRightVector();   // Eje local +Y
	FVector UpVector      = GetActorUpVector();      // Eje local +Z

	// 2. Estructura para comparar el producto punto de cada cara contra el vector Up del mundo (0, 0, 1)
	// Como el vector Up del mundo es (0, 0, 1), el producto punto N · (0, 0, 1) equivale exactamente a N.Z
	// La cara que apunta hacia arriba tendra el valor de Z mas alto (cercano a +1.0)
	struct FFaceDirection
	{
		int32 FaceValue;
		float DotProductWithUp;
	};

	TArray<FFaceDirection> Faces = {
		{ 1, -ForwardVector.Z }, // Cara 1: normal apunta a -X
		{ 2,  RightVector.Z   }, // Cara 2: normal apunta a +Y
		{ 3,  UpVector.Z      }, // Cara 3: normal apunta a +Z
		{ 4, -UpVector.Z      }, // Cara 4: normal apunta a -Z
		{ 5, -RightVector.Z   }, // Cara 5: normal apunta a -Y
		{ 6,  ForwardVector.Z }  // Cara 6: normal apunta a +X
	};

	float BestDot = -2.0f;
	int32 TopFace = 1;

	for (const FFaceDirection& Face : Faces)
	{
		if (Face.DotProductWithUp > BestDot)
		{
			BestDot = Face.DotProductWithUp;
			TopFace = Face.FaceValue;
		}
	}

	return TopFace;
}

void ADice::ShowDiceFace(int32 FaceNumber)
{
	// FRotator order is: Pitch (Y), Yaw (Z), Roll (X)
	FRotator TargetRotation = FRotator::ZeroRotator;
	/*
	* 1-3
	2-6
	3-5
	4-2
	5-1
	6-4
	*/
	switch (FaceNumber)
	{
	case 1:
		TargetRotation = FRotator(-90.f, 0.f, 0.f);
		//TargetRotation = FRotator(0.f, 0.f, 0.f);
		break;
	case 2:
		// Rotate 90 degrees on the Y axis (Pitch)
		TargetRotation = FRotator(0.f, 0.f, -90.f);
		//TargetRotation = FRotator(90.f, 0.f, 0.f);
		break;
	case 3:
		// Rotate 90 degrees on the X axis (Roll)
		TargetRotation = FRotator(0.f, 0.f, 0.f);
		//TargetRotation = FRotator(0.f, 0.f, 90.f);
		break;
	case 4:
		// Rotate -90 degrees on the X axis (Roll)
		TargetRotation = FRotator(180.f, 0.f, 0.f);
		//TargetRotation = FRotator(0.f, 0.f, -90.f);
		break;
	case 5:
		// Rotate -90 degrees on the Y axis (Pitch)
		TargetRotation = FRotator(0.f, 0.f, 90.f);
		//TargetRotation = FRotator(-90.f, 0.f, 0.f);
		break;
	case 6:
		// Rotate 180 degrees on the Y axis (Pitch) to show the bottom face
		TargetRotation = FRotator(90.f, 0.f, 0.f);
		//TargetRotation = FRotator(180.f, 0.f, 0.f);
		break;
	default:
		// Fallback for invalid numbers
		return;
	}

	// Apply the rotation to the entire Actor
	SetActorRotation(TargetRotation);

	// Alternatively, if you only want to rotate the mesh component itself:
	// DiceMeshComponent->SetRelativeRotation(TargetRotation);
}