// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Dice.h"
#include "PuzzleDiceGameBlockGrid.generated.h"


/** Class used to spawn blocks and manage score */
UCLASS(minimalapi)
class APuzzleDiceGameBlockGrid : public AActor
{
	GENERATED_BODY()

	/** Dummy root component */
	UPROPERTY(Category = Grid, VisibleDefaultsOnly, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	class USceneComponent* DummyRoot;

	/** Text component for the score */
	UPROPERTY(Category = Grid, VisibleDefaultsOnly, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	class UTextRenderComponent* ScoreText;

public:
	APuzzleDiceGameBlockGrid();

	/** How many blocks have been clicked */
	UPROPERTY(Category = Grid, EditAnywhere, BlueprintReadOnly)
	int32 Score;

	/** Number of blocks along each side of grid */
	UPROPERTY(Category=Grid, EditAnywhere, BlueprintReadOnly)
	int32 Size;

	UPROPERTY(Category = Grid, EditAnywhere, BlueprintReadOnly)
		int32 Rows;
	UPROPERTY(Category = Grid, EditAnywhere, BlueprintReadOnly)
		int32 Columns;

	
	/** Spacing of blocks */
	UPROPERTY(Category=Grid, EditAnywhere, BlueprintReadOnly)
	float BlockSpacing;

	//define un atributo de incremento de puntaje 
	// entero puntos = 5
	UPROPERTY(Category = Grid, EditAnywhere, BlueprintReadOnly)
		int32 points;
	UPROPERTY(Category = Grid, EditAnywhere, BlueprintReadOnly)
		float BlockSize;

	/** list of dices */
	UPROPERTY(Category = Grid, EditAnywhere, BlueprintReadOnly)
		TArray<ADice*> listaDados;

protected:
	// Begin AActor interface
	virtual void BeginPlay() override;
	// End AActor interface

public:

	/** Handle the block being clicked */
	void AddScore();

	/** Returns DummyRoot subobject **/
	FORCEINLINE class USceneComponent* GetDummyRoot() const { return DummyRoot; }
	/** Returns ScoreText subobject **/
	FORCEINLINE class UTextRenderComponent* GetScoreText() const { return ScoreText; }
};



