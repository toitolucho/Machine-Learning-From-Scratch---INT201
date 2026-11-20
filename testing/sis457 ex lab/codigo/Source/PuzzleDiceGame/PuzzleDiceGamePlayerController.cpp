// Copyright Epic Games, Inc. All Rights Reserved.

#include "PuzzleDiceGamePlayerController.h"

APuzzleDiceGamePlayerController::APuzzleDiceGamePlayerController()
{
	bShowMouseCursor = true;
	bEnableClickEvents = true;
	bEnableTouchEvents = true;
	DefaultMouseCursor = EMouseCursor::Crosshairs;
}
