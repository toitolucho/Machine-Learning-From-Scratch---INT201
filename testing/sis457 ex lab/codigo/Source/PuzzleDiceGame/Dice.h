// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Dice.generated.h"

UCLASS()
class PUZZLEDICEGAME_API ADice : public AActor
{
	GENERATED_BODY()
	/** Dummy root component */
	UPROPERTY(Category = Block, VisibleDefaultsOnly, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	class USceneComponent* DummyRoot;


	/** StaticMesh component for the clickable block */
	UPROPERTY(Category = Block, VisibleDefaultsOnly, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
		class UStaticMeshComponent* BlockMesh;

	
	
public:	
	// Sets default values for this actor's properties
	ADice();
	UPROPERTY(Category = Dice, EditAnywhere, BlueprintReadOnly)
		int32 tipo = 0;

	UPROPERTY(Category = Dice, EditAnywhere, BlueprintReadOnly)
		int32 Value = 1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mallas")
		class UStaticMesh* ConoMesh;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mallas")
		class UStaticMesh* CilindroMesh;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mallas")
		class UStaticMesh* EsferaMesh;

	/** Fuerza vertical para el impulso del salto */
	UPROPERTY(Category = "Dice|Physics", EditAnywhere, BlueprintReadWrite)
		float Force = 1000.0f;

	/** Gravedad que frena el salto y hace caer el dado */
	UPROPERTY(Category = "Dice|Physics", EditAnywhere, BlueprintReadWrite)
		float Gravity = 2500.0f;

	/** Velocidad minima de rotacion en el aire (grados por segundo) */
	UPROPERTY(Category = "Dice|Physics", EditAnywhere, BlueprintReadWrite)
		float MinRollSpeed = 360.0f;

	/** Velocidad maxima de rotacion en el aire (grados por segundo) */
	UPROPERTY(Category = "Dice|Physics", EditAnywhere, BlueprintReadWrite)
		float MaxRollSpeed = 720.0f;

	/** Aplica un impulso vertical hacia arriba al dado */
	UFUNCTION(BlueprintCallable, Category = "Dice|Physics")
		void ApplyVerticalImpulse();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

	/** Indica si el dado se encuentra actualmente en el aire */
	bool bIsJumping = false;

	/** Altura inicial en el eje Z antes del salto */
	float InitialZ = 0.0f;

	/** Velocidad vertical actual */
	float VerticalSpeed = 0.0f;

	/** Velocidad de rotacion angular actual en el aire */
	FRotator AngularVelocity = FRotator::ZeroRotator;

public:	
	/** Grid that owns us */
	UPROPERTY()
		class APuzzleDiceGameBlockGrid* OwningGrid;


	// Called every frame
	virtual void Tick(float DeltaTime) override;
	void ShowDiceFace(int32 FaceNumber);
	void NextFace();

	/** Calcula matematicamente que cara del dado quedo apuntando hacia arriba */
	UFUNCTION(BlueprintCallable, Category = "Dice|Logic")
	int32 CalculateTopFace();
	/** Handle the block being clicked */
	UFUNCTION()
		void BlockClicked(UPrimitiveComponent* ClickedComp, FKey ButtonClicked);
		// void BlockClicked();
	/** Handle the block being touched  */
	UFUNCTION()
		void OnFingerPressedBlock(ETouchIndex::Type FingerIndex, UPrimitiveComponent* TouchedComponent);
};
