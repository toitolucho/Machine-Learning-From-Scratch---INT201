// Copyright Epic Games, Inc. All Rights Reserved.

#include "PuzzleDiceGameBlockGrid.h"
#include "PuzzleDiceGameBlock.h"
#include "Components/TextRenderComponent.h"
#include "Engine/World.h"
#include "Dice.h"

#define LOCTEXT_NAMESPACE "PuzzleBlockGrid"

APuzzleDiceGameBlockGrid::APuzzleDiceGameBlockGrid()
{
	// Create dummy root scene component
	DummyRoot = CreateDefaultSubobject<USceneComponent>(TEXT("Dummy0"));
	RootComponent = DummyRoot;

	// Create static mesh component
	ScoreText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("ScoreText0"));
	ScoreText->SetRelativeLocation(FVector(200.f,0.f,0.f));
	ScoreText->SetRelativeRotation(FRotator(90.f,0.f,0.f));
	ScoreText->SetText(FText::Format(LOCTEXT("ScoreFmt", "Puntuacion : {0}"), FText::AsNumber(0)));
	ScoreText->SetupAttachment(DummyRoot);

	// Set defaults
	Size = 3;
	BlockSpacing = 300.f;
}
//Grilla1  2x2
//Grilla2  4x3
//Grilla3  5x2
void APuzzleDiceGameBlockGrid::BeginPlay()
{
	Super::BeginPlay();

	// Number of blocks
	const int32 NumBlocks = Rows * Columns;

	// Loop to spawn each block
	for(int32 BlockIndex=0; BlockIndex<NumBlocks; BlockIndex++)
	{
		const float XOffset = (BlockIndex/ Columns) * BlockSpacing; // Divide by dimension
		const float YOffset = (BlockIndex% Columns) * BlockSpacing; // Modulo gives remainder

		// Make position vector, offset from Grid location
		const FVector BlockLocation = FVector(XOffset, YOffset, 0.f) + GetActorLocation();

		// Spawn a block
		//APuzzleDiceGameBlock* NewBlock = GetWorld()->SpawnActor</*APuzzleDiceGameBlock*/>(BlockLocation, FRotator(0,0,0));
		ADice* NewBlock = GetWorld()->SpawnActor<ADice>(BlockLocation, FRotator(0, 0, 0));

		//insertar en la lista
		// listaDados.add(NewBlock)

		//NewBlock->CambiarTamanio(BlockSize);

		// Tell the block about its owner
		if (NewBlock != nullptr)
		{
			NewBlock->OwningGrid = this;
		}
		NewBlock->Value = FMath::RandRange(1, 6);
		NewBlock->ShowDiceFace(NewBlock->Value);
		listaDados.Add(NewBlock);
	}

	//crer una lista de dados en BlockGrid
	//TArray<   * >  listaDados;  -> en el header

	// log mostrar la cantidad de elementos de la listaDados 


	TArray<int32>  lista = { 200,330,240, 50, 30 };
	lista.Add(15);
	lista.Sort();
	lista.Num();
	for (int32 valor : lista)
	{
		UE_LOG(LogTemp, Warning, TEXT(" Score : % d "), valor);
	}
	

}


void APuzzleDiceGameBlockGrid::AddScore()
{
	// Increment score
	//Score++;  
	Score = Score + points;

	// Update text
	ScoreText->SetText(FText::Format(LOCTEXT("ScoreFmt", "Puntuacion: {0}"), FText::AsNumber(Score)));
}

#undef LOCTEXT_NAMESPACE
