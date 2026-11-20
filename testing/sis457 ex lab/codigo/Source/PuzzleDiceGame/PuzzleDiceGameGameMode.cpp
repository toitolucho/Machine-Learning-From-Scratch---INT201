// Copyright Epic Games, Inc. All Rights Reserved.

#include "PuzzleDiceGameGameMode.h"
#include "PuzzleDiceGamePlayerController.h"
#include "PuzzleDiceGamePawn.h"

APuzzleDiceGameGameMode::APuzzleDiceGameGameMode()
{
	// no pawn by default
	DefaultPawnClass = APuzzleDiceGamePawn::StaticClass();
	// use our own player controller class
	PlayerControllerClass = APuzzleDiceGamePlayerController::StaticClass();
}
