# UE4 Self-Check Problems: All Bloom's Taxonomy Levels

---

### 1. Remembering

*   What are the three primary macros (`UCLASS()`, `UPROPERTY()`, `UFUNCTION()`) used for in Unreal Engine C++ classes?
*   What is the primary memory management system used for `UObject`s in Unreal Engine?
*   Name two types of Unreal-specific smart pointers mentioned in the resources.
*   Define what an `AActor` is in Unreal Engine.
*   Define what a `UActorComponent` is in Unreal Engine.
*   What is the name of the file that defines a module's dependencies in Unreal Engine?
*   What is the primary use of the `UE_LOG` macro?

### 2. Understanding

*   How do the `UCLASS()`, `UPROPERTY()`, `UFUNCTION()` macros enable C++ code to interact with Unreal Engine's reflection system?
*   Why must `UObject*` member variables be marked with `UPROPERTY()`?
*   What is the core principle (composition vs. inheritance) that the Actor-Component model embodies?
*   Briefly describe the role of `AGameMode` in the Gameplay Framework.
*   What is the main difference between an `APawn` and an `ACharacter`?
*   What is the fundamental purpose of a `UInterface` in Unreal Engine?
*   How does using `UInterface`s contribute to decoupling in C++ code?
*   What tool is responsible for compiling Unreal Engine projects based on these dependency files?
*   What is the difference between the `EditAnywhere` and `VisibleAnywhere` specifiers when used with `UPROPERTY()`?
*   Why is it important to call `Super::` when overriding engine functions like `BeginPlay()` or `Tick()`?
*   What is the main purpose of Unreal Insights?

### 3. Applying

*   If you want to expose a C++ function to be callable from Blueprints, which macro would you use, and where would you place it?
*   You have a `UTexture2D* MyTexture;` member variable in your `UObject`. How would you declare it to ensure it's properly managed by the garbage collector?
*   You want to add a reusable "Inventory" system to multiple different types of characters. Would you implement this as an `AActor` or a `UActorComponent`? Explain why.
*   Which class (`AGameMode`, `APlayerController`, `APawn`) is responsible for processing player input and translating it into actions for a character?
*   If you wanted to create an interface for objects that can be "activated," how would you declare a simple `Activate()` function within that interface?
*   If your C++ code needs to use functionality from the "AIModule," what specific action would you need to take in your project's build file?
*   You have a `float MovementSpeed;` variable in your character class that you want designers to be able to adjust directly in the Blueprint editor. How would you declare this `UPROPERTY()`?
*   Consider the following code: `UMyObject* MyObject = NewObject<UMyObject>();`. If `MyObject` is a member variable of an `AActor` and is *not* marked with `UPROPERTY()`, what potential issue could arise during gameplay?
*   You're trying to find out why your game is experiencing frame rate drops in a specific area. Would you primarily use `UE_LOG` or Unreal Insights for this investigation? Explain your choice.

### 4. Analyzing

*   Compare and contrast Unreal's `TArray` with C++ standard library's `std::vector`. What are the advantages of using `TArray` in an Unreal project?
*   How does the Actor-Component model, as implemented in Unreal Engine, directly support the Single Responsibility Principle (SRP) and the Open/Closed Principle (OCP)?
*   Analyze the data flow for a decoupled damage system (as visualized in the `UE4_Learning_Plan.md`). How does this design reduce dependencies compared to a system where a weapon directly calls a specific `AMonster`'s `TakeDamage` function?
*   Examine the provided `UHealthComponent` and `IDamageable` interface code. Identify how they work together to allow for flexible damage application without tight coupling.

### 5. Evaluating

*   Critique the decision to use Unreal's garbage collection system for `UObject`s instead of traditional C++ manual memory management. What are the trade-offs?
*   Evaluate the effectiveness of `UInterface`s as a mechanism for achieving the Dependency Inversion Principle (DIP) in Unreal Engine. Provide an example where an interface significantly improves code maintainability.
*   You are tasked with optimizing a game's performance. Based on your understanding of Unreal Insights and `UE_LOG`, when would you prioritize using one over the other, and what factors would influence your decision?
*   Consider a scenario where a new gameplay feature requires a custom input action. Evaluate the steps involved in setting this up, from defining the input to handling it in a `PlayerController`, and identify potential points of failure or complexity.

### 6. Creating

*   Design a simple C++ `UActorComponent` that manages a character's "Stamina." This component should have a `MaxStamina` and `CurrentStamina` property, and a `ConsumeStamina(float Amount)` function. Outline the `.h` and `.cpp` structure, including necessary macros and specifiers.
*   Propose a design for a new `UInterface` called `IInteractable` that allows a player character to interact with various objects in the world (e.g., opening a door, picking up an item). Define at least one `UFUNCTION` within this interface.
*   Formulate a plan for refactoring a monolithic `ACharacter` class that currently handles movement, health, inventory, and quest management into a more modular design using `UActorComponent`s and `UInterface`s.
*   Imagine you need to create a new type of projectile that applies a "burning" status effect over time. Describe how you would implement this using the `IDamageable` interface and potentially a new `UActorComponent` for status effects, ensuring it integrates cleanly with the existing damage system.
