### 1. Core C++ Class Structure

This is the most fundamental concept. All C++ objects managed by Unreal derive from a base class and use special macros to integrate with the engine's systems like garbage collection and the Blueprint editor.

**Key takeaway:** Your C++ classes will use `UCLASS()`, `GENERATED_BODY()`, `UPROPERTY()`, and `UFUNCTION()` to communicate with the engine.

**Core Example: A Basic `UObject`**
This demonstrates the simplest possible Unreal-aware C++ class.

```cpp
class UMyObject : public UObject
{
    GENERATED_BODY()

public:
    // Constructor
    UMyObject();

    // Example property exposed to the engine
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MyObject")
    float MyFloatValue;

    // Example function exposed to the engine
    UFUNCTION(BlueprintCallable, Category = "MyObject")
    void MyFunction();
};
```
*Source: [Programming with C++ in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)*

---

### 2. The Gameplay Framework: Actors

`Actors` are the primary objects you place in your game world. The following snippet shows a complete, basic `AActor` implementation, which is a cornerstone of the Actor-Component model we planned.

**Key takeaway:** An `AActor` is the base for any object in your level. It has a lifecycle managed by functions like `BeginPlay()` (called when the object enters the world) and `Tick()` (called every frame).

**Core Example: A Basic `AActor`**

```cpp
// MyActor.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"

UCLASS()
class MYPROJECT_API AMyActor : public AActor
{
    GENERATED_BODY()

public:    
    // Sets default values for this actor's properties
    AMyActor();

protected:
    // Called when the game starts or when spawned
    virtual void BeginPlay() override;

public:    
    // Called every frame
    virtual void Tick(float DeltaTime) override;
};

// MyActor.cpp
#include "MyActor.h"

AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = true; // Allow this Actor to Tick each frame
}

void AMyActor::BeginPlay()
{
    Super::BeginPlay(); // Important: Always call the parent's version!
    
    UE_LOG(LogTemp, Warning, TEXT("MyActor has begun play!"));
}

void AMyActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime); // Important: Always call the parent's version!
}
```
*Source: [Skeletal Mesh Assets in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletal-mesh-assets-in-unreal-engine_application_version=5)*

---

### 3. Essential Data Structures & Patterns

Your C++11 knowledge is transferable, but Unreal provides its own battle-tested implementations for common patterns and containers.

#### Containers
Instead of `std::vector` or `std::map`, you will primarily use Unreal's `TArray` and `TMap`. They are designed to be efficient and work with the `UPROPERTY` system.

**Core Example: Unreal Containers**
```cpp
// Example using TArray (like std::vector)
TArray<int32> MyIntArray;
MyIntArray.Add(10);
MyIntArray.Add(20);

// Example using TMap (like std::map)
TMap<FString, int32> MyStringToIntMap;
MyStringToIntMap.Add("Key1", 100);
MyStringToIntMap.Add("Key2", 200);
```
*Source: [Containers in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)*

#### Delegates (Callbacks)
Delegates are Unreal's powerful and safe version of function pointers, essential for event-driven programming.

**Core Example: Declaring a Delegate**
```cpp
// Declare a delegate with no parameters
DECLARE_DELEGATE(FMyDelegate);

// Declare a delegate that takes one integer parameter
DECLARE_DELEGATE_OneParam(FMyDelegateWithParam, int32);

// You can then bind this to a UObject's member function and execute it later.
```
*Source: [Delegates in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)*

---

### 4. Getting Started in the Editor

The documentation recommends creating a project from a C++ template to see these concepts in action.

*   **Recommendation:** Create a new project using the **C++ Top Down** template.
*   **Action:** Once created, you can find the C++ implementation for the `PlayerController` in the Class Viewer to see how user input is handled.

---

## Additional Resources

Here are more detailed resources that align with the topics in the `UE4_Learning_Plan.md`.

### Core C++ Deep Dives

*   **The UObject Reflection System:**
    *   [Official Documentation: Unreal Object Handling](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine) - The definitive source on how `UObjects` are managed by the engine.
    *   [Official Blog: The Property System (Reflection)](https://unrealengine.com/en-US/blog/unreal-property-system-reflection) - A detailed official blog post explaining how the Unreal Header Tool (UHT) and macros work together.
*   **Memory Management & Smart Pointers:**
    *   [Official Documentation: Smart Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/cplusplus-programming/smart-pointers) - A comprehensive guide on when and how to use `TSharedPtr`, `TUniquePtr`, and `TWeakPtr`.

### Gameplay Architecture

*   **The Gameplay Framework:**
    *   [Tom Looman's C++ Guide](https://www.tomlooman.com/unreal-engine-cpp-guide/) - A highly-regarded, practical guide for C++ developers that covers the gameplay framework.
    *   [Official Documentation: Gameplay Architecture](https://epicgames.com/developers/docs/unreal-engine/gameplay-architecture) - The official reference for all framework classes.
*   **Working with C++ Interfaces:**
    *   [Official Documentation: C++ Interfaces](https://dev.epicgames.com/documentation/en-us/unreal-engine/cplusplus-programming/interfaces) - A complete guide to declaring and implementing interfaces in C++.
*   **The Build System:**
    *   [Official Documentation: Unreal Build System](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEKDO0HunVzEJtTne-VkEqVAlWc_5CQbZlUJqql0o66U8WI7UTZGa1R7wh_iMOFuCPdGAORWByfw5JaOaN2oHzvheICMf7hdHofLMpCvBd1Gvc0h7czxftj29qJzUIgC9XXSSJoNDWyhL33pQDaBxelqYoCi9J0tftiSyq7Xt9MuwBeyfUGBqn2zN3e7qqQNCUrtk8CIuv5QaOUcqFQsd0K3Tg=) - Explains the structure of `.Build.cs` files and how the UnrealBuildTool (UBT) compiles your project.

### Debugging & Profiling

*   **Debugging C++ Code:**
    *   [Official Documentation: Debugging C++](https://docs.unrealengine.com/5.3/en-US/debugging-cpp-code-in-unreal-engine/) - Covers setting up and using the Visual Studio debugger with Unreal Engine.
    *   [JetBrains Rider: Debugging Unreal Engine](https://www.jetbrains.com/help/rider/Debugging_Unreal_Engine_Project.html) - Guide for debugging with the Rider IDE.
*   **Performance Profiling with Unreal Insights:**
    *   [Official Documentation: Unreal Insights](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUdC7Ha17rpqUroW2yD-HVXxsRPOYkvCBKuqiM9B9jeYOkh7vwA9047vIlWqECKX_dJdicJJXf4jQn-JOEvO6AKYpDr28Z6Hw4DAN_ow8b8LALX8Yby38344PmW-AXIPVuZexA2jWuxsM7WTApzHIYJt6x2rbB4eHZLk4wC1FzYUYzo1PUtUm1nOhxNLvaA-M4_JKYkZMo) - An overview of how to use this powerful profiling tool.
    *   [YouTube Tutorial: Introduction to Unreal Insights](https://www.youtube.com/watch?v=J3i-9tH1HwM) - A video walkthrough of capturing and analyzing performance data.

### Advanced Topics

*   **The Gameplay Ability System (GAS):**
    *   [Official Documentation: Gameplay Ability System](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine) - The official starting point for learning GAS.
    *   [GitHub: GAS Documentation by `tranek`](https://github.com/tranek/GASDocumentation) - An extremely detailed and highly-recommended community-maintained guide to understanding and using GAS.
