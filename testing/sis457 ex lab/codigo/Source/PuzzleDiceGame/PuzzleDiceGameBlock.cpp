// Copyright Epic Games, Inc. All Rights Reserved.

#include "PuzzleDiceGameBlock.h"
#include "PuzzleDiceGameBlockGrid.h"
#include "UObject/ConstructorHelpers.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInstance.h"

APuzzleDiceGameBlock::APuzzleDiceGameBlock()
{
	// Structure to hold one-time initialization
	struct FConstructorStatics
	{
		ConstructorHelpers::FObjectFinderOptional<UStaticMesh> PlaneMesh;
		ConstructorHelpers::FObjectFinderOptional<UMaterial> BaseMaterial;
		ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> BlueMaterial;
		ConstructorHelpers::FObjectFinderOptional<UMaterialInstance> OrangeMaterial;
		FConstructorStatics()
			//: PlaneMesh(TEXT("/Game/Puzzle/Meshes/Dado.Dado"))
			: PlaneMesh(TEXT("/Game/Puzzle/Meshes/PuzzleCube.PuzzleCube"))
			, BaseMaterial(TEXT("/Game/Puzzle/Meshes/BaseMaterial.BaseMaterial"))
			, BlueMaterial(TEXT("/Game/Puzzle/Meshes/BlueMaterial.BlueMaterial"))
			, OrangeMaterial(TEXT("/Game/Puzzle/Meshes/OrangeMaterial.OrangeMaterial"))
			///Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial
		{
		}
	};
	static FConstructorStatics ConstructorStatics;

	// Create dummy root scene component
	DummyRoot = CreateDefaultSubobject<USceneComponent>(TEXT("Dummy0"));
	RootComponent = DummyRoot;

	// Create static mesh component
	BlockMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BlockMesh0"));

	/*ConstructorHelpers::FObjectFinderOptional<UStaticMesh> PlaneMesh2(TEXT("/Game/Puzzle/Meshes/Dado.Dado"));
	BlockMesh->SetStaticMesh(PlaneMesh2.Get());*/
	BlockMesh->SetStaticMesh(ConstructorStatics.PlaneMesh.Get());
	BlockMesh->SetRelativeScale3D(FVector(1.f,1.f,1.f));
	BlockMesh->SetRelativeLocation(FVector(0.f,0.f,25.f));
	BlockMesh->SetMaterial(0, ConstructorStatics.BlueMaterial.Get());
	BlockMesh->SetupAttachment(DummyRoot);
	BlockMesh->OnClicked.AddDynamic(this, &APuzzleDiceGameBlock::BlockClicked);
	BlockMesh->OnInputTouchBegin.AddDynamic(this, &APuzzleDiceGameBlock::OnFingerPressedBlock);

	// Save a pointer to the orange material
	BaseMaterial = ConstructorStatics.BaseMaterial.Get();
	BlueMaterial = ConstructorStatics.BlueMaterial.Get();
	OrangeMaterial = ConstructorStatics.OrangeMaterial.Get();

	
}

void APuzzleDiceGameBlock::BlockClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked)
{
	HandleClicked();
}


void APuzzleDiceGameBlock::OnFingerPressedBlock(ETouchIndex::Type FingerIndex, UPrimitiveComponent* TouchedComponent)
{
	HandleClicked();
}

void APuzzleDiceGameBlock::HandleClicked()
{
	// Check we are not already active
	if (!bIsActive)
	{
		bIsActive = true;

		// Change material
		BlockMesh->SetMaterial(0, OrangeMaterial);

		// Tell the Grid
		if (OwningGrid != nullptr)
		{
			OwningGrid->AddScore();
		}
		//mueve el objecto en z a 200
		//posixion.x, posicion.y, 200
		//ActorLocation

		// Vector CurrentPosition = ObtenerPosicion()
		// Vector NewPosition  ( CurrentPosition.x, CurrentPosition.y, 200)
		// DarNuevaPosicion (NewPosition)
		
	}
	
	FVector CurrentPosition = GetActorLocation();
	FVector NewPosition(CurrentPosition.X, CurrentPosition.Y, CurrentPosition.Z+40);
	SetActorLocation(NewPosition);
}

void APuzzleDiceGameBlock::Highlight(bool bOn)
{
	// Do not highlight if the block has already been activated.
	if (bIsActive)
	{
		return;
	}

	if (bOn)
	{
		BlockMesh->SetMaterial(0, BaseMaterial);
	}
	else
	{
		BlockMesh->SetMaterial(0, BlueMaterial);
	}
}

void APuzzleDiceGameBlock::CambiarTamanio(float newSize)
{
	FVector NewSize(newSize, newSize, newSize);
	SetActorScale3D(NewSize);
}


