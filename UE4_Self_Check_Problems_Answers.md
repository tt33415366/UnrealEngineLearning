# UE4 Self-Check Problems: Answers

---

### 1. Remembering - Answers

*   **What are the three primary macros (`UCLASS()`, `UPROPERTY()`, `UFUNCTION()`) used for in Unreal Engine C++ classes?**
    *   `UCLASS()`: Used to declare a class as an Unreal Engine class, enabling reflection, garbage collection, and Blueprint integration.
    *   `UPROPERTY()`: Used to declare a member variable as an Unreal property, enabling reflection, serialization, garbage collection tracking, and exposure to the editor/Blueprints.
    *   `UFUNCTION()`: Used to declare a member function as an Unreal function, enabling reflection, Blueprint callable/overridable functionality, and RPCs for networking.

*   **What is the primary memory management system used for `UObject`s in Unreal Engine?**
    *   Unreal Engine uses a custom garbage collection system for `UObject`s.

*   **Name two types of Unreal-specific smart pointers mentioned in the resources.**
    *   `TSharedPtr`
    *   `TUniquePtr`
    *   (Also `TWeakPtr`, `TSharedRef`)

*   **Define what an `AActor` is in Unreal Engine.**
    *   An `AActor` is an object that can be placed or spawned in a level. It is the base class for all objects that participate in gameplay, such as characters, props, and cameras. Actors have a transform (location, rotation, scale) and can own `UActorComponent`s.

*   **Define what a `UActorComponent` is in Unreal Engine.**
    *   A `UActorComponent` is a reusable piece of functionality that can be attached to an `AActor`. Components allow for modular design and composition of Actor behavior.

*   **What is the name of the file that defines a module's dependencies in Unreal Engine?**
    *   A `.Build.cs` file.

*   **What is the primary use of the `UE_LOG` macro?**
    *   `UE_LOG` is primarily used for printing messages to the Unreal Engine output log, which is useful for debugging, tracing execution, and providing information during development.

### 2. Understanding - Answers

*   **How do the `UCLASS()`, `UPROPERTY()`, `UFUNCTION()` macros enable C++ code to interact with Unreal Engine's reflection system?**
    *   These macros are processed by the Unreal Header Tool (UHT) during compilation. UHT generates additional C++ code that creates metadata about the classes, properties, and functions. This metadata is then used by the reflection system at runtime to allow the engine to understand and manipulate these C++ elements, enabling features like serialization, garbage collection, Blueprint integration, and editor details panels.

*   **Why must `UObject*` member variables be marked with `UPROPERTY()`?**
    *   Marking `UObject*` member variables with `UPROPERTY()` is crucial because it allows Unreal Engine's garbage collector to track references to these objects. If a `UObject*` is not a `UPROPERTY()`, the garbage collector will not know that it's being referenced, and the object it points to might be prematurely destroyed, leading to crashes or undefined behavior (dangling pointers).

*   **What is the core principle (composition vs. inheritance) that the Actor-Component model embodies?**
    *   The Actor-Component model primarily embodies the principle of **composition over inheritance**. Instead of building complex hierarchies through inheritance, functionality is composed by attaching various `UActorComponent`s to an `AActor`.

*   **Briefly describe the role of `AGameMode` in the Gameplay Framework.**
    *   `AGameMode` defines the rules of the game. It dictates how players join, spawn, win/lose, and the overall flow of the game. It exists only on the server.

*   **What is the main difference between an `APawn` and an `ACharacter`?**
    *   An `APawn` is a non-physical representation of a player or AI in the world, capable of being possessed by a `Controller`. It doesn't have built-in movement capabilities.
    *   An `ACharacter` is a specialized type of `APawn` that includes a `CharacterMovementComponent` and a `CapsuleComponent`, providing built-in support for bipedal movement, collision, and common character actions.

*   **What is the fundamental purpose of a `UInterface` in Unreal Engine?**
    *   The fundamental purpose of a `UInterface` is to provide a contract for behavior that multiple unrelated `UObject` classes can implement. It allows for polymorphism and communication between objects without requiring them to share a common base class, promoting loose coupling.

*   **How does using `UInterface`s contribute to decoupling in C++ code?**
    *   `UInterface`s contribute to decoupling by allowing objects to interact with each other through a defined interface rather than through concrete class types. This means an object doesn't need to know the specific implementation details of another object; it only needs to know that the other object implements a certain interface. This reduces dependencies and makes code more flexible and easier to maintain.

*   **What tool is responsible for compiling Unreal Engine projects based on these dependency files?**
    *   The Unreal Build Tool (UBT).

*   **What is the difference between the `EditAnywhere` and `VisibleAnywhere` specifiers when used with `UPROPERTY()`?**
    *   `EditAnywhere`: The property can be edited in the Details panel of the Unreal Editor, regardless of whether the object is a Blueprint default or an instance in the world.
    *   `VisibleAnywhere`: The property is visible in the Details panel but cannot be edited. It's useful for displaying read-only information.

*   **Why is it important to call `Super::` when overriding engine functions like `BeginPlay()` or `Tick()`?**
    *   Calling `Super::` ensures that the base class's implementation of the function is executed. Engine functions often contain critical logic (e.g., initializing components, registering for events, performing internal updates) that must run for the object to function correctly. Failing to call `Super::` can lead to unexpected behavior, bugs, or features not working as intended.

*   **What is the main purpose of Unreal Insights?**
    *   Unreal Insights is a profiling and analysis tool used to visualize and understand the performance characteristics of an Unreal Engine application. It helps identify bottlenecks in CPU, GPU, memory, and networking.

### 3. Applying - Answers

*   **If you want to expose a C++ function to be callable from Blueprints, which macro would you use, and where would you place it?**
    *   You would use the `UFUNCTION()` macro, typically with the `BlueprintCallable` specifier. It would be placed directly above the function declaration in the class header file (`.h`).
    *   Example: `UFUNCTION(BlueprintCallable) void MyBlueprintCallableFunction();`

*   **You have a `UTexture2D* MyTexture;` member variable in your `UObject`. How would you declare it to ensure it's properly managed by the garbage collector?**
    *   You would declare it as a `UPROPERTY()`:
    ```cpp
    UPROPERTY()
    UTexture2D* MyTexture;
    ```

*   **You want to add a reusable "Inventory" system to multiple different types of characters. Would you implement this as an `AActor` or a `UActorComponent`? Explain why.**
    *   You would implement this as a `UActorComponent`.
    *   **Why:** An inventory system is a piece of functionality that *belongs to* a character (an `AActor`) rather than being an independent entity in the world. Using a `UActorComponent` allows you to encapsulate the inventory logic, make it reusable across different character types, and easily add/remove it from Actors without modifying their base class. This adheres to the composition over inheritance principle.

*   **Which class (`AGameMode`, `APlayerController`, `APawn`) is responsible for processing player input and translating it into actions for a character?**
    *   `APlayerController`. The `APlayerController` receives raw input and then typically possesses an `APawn` (or `ACharacter`) to execute actions based on that input.

*   **If you wanted to create an interface for objects that can be "activated," how would you declare a simple `Activate()` function within that interface?**
    *   In the interface header file (`.h`):
    ```cpp
    // IMyActivatableInterface.h
    #pragma once

    #include "CoreMinimal.h"
    #include "UObject/Interface.h"
    #include "MyActivatableInterface.generated.h"

    UINTERFACE(MinimalAPI)
    class UMyActivatableInterface : public UInterface
    {
        GENERATED_BODY()
    };

    class IMYPROJECT_API IMyActivatableInterface
    {
        GENERATED_BODY()

    public:
        UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category = "Activation")
        void Activate();
    };
    ```
    *   (Note: `BlueprintNativeEvent` allows both C++ and Blueprint implementations.)

*   **If your C++ code needs to use functionality from the "AIModule," what specific action would you need to take in your project's build file?**
    *   You would need to add "AIModule" to the `PublicDependencyModuleNames` array in your project's `.Build.cs` file.
    *   Example: `PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "AIModule" });`

*   **You have a `float MovementSpeed;` variable in your character class that you want designers to be able to adjust directly in the Blueprint editor. How would you declare this `UPROPERTY()`?**
    *   You would use the `UPROPERTY()` macro with the `EditAnywhere` specifier (and optionally `BlueprintReadWrite` if you want Blueprints to be able to read/write it at runtime).
    ```cpp
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement")
    float MovementSpeed;
    ```

*   **Consider the following code: `UMyObject* MyObject = NewObject<UMyObject>();`. If `MyObject` is a member variable of an `AActor` and is *not* marked with `UPROPERTY()`, what potential issue could arise during gameplay?**
    *   The primary issue is that `MyObject` could be **garbage collected prematurely**. Since it's not a `UPROPERTY()`, the garbage collector doesn't know that the `AActor` is still referencing it. If no other `UPROPERTY()` or root set reference exists, the object pointed to by `MyObject` could be destroyed, leaving `MyObject` as a dangling pointer, which would lead to crashes or undefined behavior if accessed.

*   **You're trying to find out why your game is experiencing frame rate drops in a specific area. Would you primarily use `UE_LOG` or Unreal Insights for this investigation? Explain your choice.**
    *   You would primarily use **Unreal Insights**.
    *   **Explanation:** While `UE_LOG` can provide some basic information, it's not designed for detailed performance analysis. Unreal Insights provides a comprehensive visual timeline of CPU, GPU, memory, and networking usage, allowing you to pinpoint exactly where the frame rate drops are occurring, what systems are consuming the most resources, and identify specific bottlenecks. `UE_LOG` is better for tracking logical flow or specific variable values, not broad performance profiling.

### 4. Analyzing - Answers

*   **Compare and contrast Unreal's `TArray` with C++ standard library's `std::vector`. What are the advantages of using `TArray` in an Unreal project?**
    *   **Similarities:** Both `TArray` and `std::vector` are dynamic arrays that provide contiguous memory storage, efficient random access, and dynamic resizing.
    *   **Differences/Advantages of `TArray` in Unreal:**
        *   **Memory Management:** `TArray` integrates with Unreal's memory allocators, which are optimized for the engine's specific needs and can be more efficient than `std::vector`'s default allocator in an Unreal context.
        *   **Serialization:** `TArray` is designed to be easily serialized by Unreal's reflection system, making it straightforward to save/load game data containing arrays. `std::vector` requires custom serialization logic.
        *   **Garbage Collection Awareness:** If `TArray` holds `UObject*` pointers, it can be made garbage collection aware (e.g., `TArray<TObjectPtr<UMyObject>>` or `TArray<UMyObject*> UPROPERTY()`), ensuring referenced objects are not prematurely collected.
        *   **Debugging:** `TArray` often has better debugging visualization in Unreal's debugging tools.
        *   **Consistency:** Using `TArray` promotes consistency within the Unreal codebase, making it easier for developers familiar with the engine to understand and maintain code.
        *   **Built-in Utilities:** `TArray` often comes with additional utility functions tailored for game development.

*   **How does the Actor-Component model, as implemented in Unreal Engine, directly support the Single Responsibility Principle (SRP) and the Open/Closed Principle (OCP)?**
    *   **Single Responsibility Principle (SRP):** The Actor-Component model encourages SRP by allowing `AActor`s to focus on their core identity (e.g., "I am a character," "I am a projectile") while delegating specific behaviors and functionalities to specialized `UActorComponent`s (e.g., `MovementComponent`, `HealthComponent`, `InventoryComponent`). Each component can then have a single, well-defined responsibility.
    *   **Open/Closed Principle (OCP):** It supports OCP because `AActor`s are "open for extension" (new functionality can be added by attaching new components) but "closed for modification" (the core `AActor` class doesn't need to be changed to add new behaviors). Similarly, components can be extended or new ones created without modifying existing Actor or component code.

*   **Analyze the data flow for a decoupled damage system (as visualized in the `UE4_Learning_Plan.md`). How does this design reduce dependencies compared to a system where a weapon directly calls a specific `AMonster`'s `TakeDamage` function?**
    *   In a decoupled system (e.g., using an `IDamageable` interface), the data flow typically involves:
        1.  A damage source (e.g., weapon, projectile) detects a hit on an `AActor`.
        2.  The damage source queries the hit `AActor` to see if it implements the `IDamageable` interface.
        3.  If it does, the damage source calls a generic `ReceiveDamage()` (or similar) function on the interface.
        4.  The `AActor`'s implementation of `ReceiveDamage()` (often delegating to a `UHealthComponent`) then processes the damage.
    *   **Reduction in Dependencies:**
        *   **No Knowledge of Concrete Types:** The damage source doesn't need to know if it hit an `AMonster`, `APlayerCharacter`, or a destructible `AProp`. It only cares if the target is `IDamageable`. This removes a direct dependency on specific target classes.
        *   **Flexibility:** New types of damageable objects can be added simply by implementing the `IDamageable` interface, without modifying the damage source code.
        *   **Maintainability:** Changes to how a specific `AMonster` takes damage (e.g., adding armor, resistances) are encapsulated within the monster's `ReceiveDamage` implementation or its `UHealthComponent`, not in the weapon's code.
        *   **Testability:** Individual components (damage source, health component, interface implementation) can be tested more in isolation.

*   **Examine the provided `UHealthComponent` and `IDamageable` interface code. Identify how they work together to allow for flexible damage application without tight coupling.**
    *   The `IDamageable` interface defines a contract (e.g., a `ReceiveDamage` function) that any object wishing to be damaged must adhere to. It acts as an abstraction.
    *   The `UHealthComponent` is a concrete implementation of health management. An `AActor` that wants health functionality can simply add a `UHealthComponent`.
    *   **Working Together:** An `AActor` that has a `UHealthComponent` would typically also implement the `IDamageable` interface. Its `ReceiveDamage` function (from the interface) would then delegate the actual damage processing to its owned `UHealthComponent`.
    *   **Flexible Damage Application without Tight Coupling:**
        *   Any damage-dealing entity (e.g., a projectile) only needs to know about the `IDamageable` interface. It can query any hit `AActor` for this interface.
        *   It doesn't need to know *how* the damage is handled (e.g., if it's a `UHealthComponent`, a shield system, or something else). This allows different `AActor`s to handle damage in unique ways while still responding to the same `ReceiveDamage` call.
        *   The `UHealthComponent` itself is reusable and can be attached to any `AActor` that needs health, further promoting modularity.

### 5. Evaluating - Answers

*   **Critique the decision to use Unreal's garbage collection system for `UObject`s instead of traditional C++ manual memory management. What are the trade-offs?**
    *   **Pros (Advantages of GC):**
        *   **Reduced Boilerplate:** Developers don't need to manually `delete` `UObject`s, reducing the chance of memory leaks or double-frees.
        *   **Safety:** Helps prevent dangling pointers to `UObject`s that are no longer referenced.
        *   **Productivity:** Frees developers to focus on gameplay logic rather than intricate memory management.
        *   **Reflection Integration:** GC works seamlessly with Unreal's reflection system, automatically tracking references through `UPROPERTY()`s.
    *   **Cons (Trade-offs):**
        *   **Performance Overhead:** GC introduces a performance cost, as the engine periodically scans for unreferenced objects. This can cause hitches if not managed carefully (e.g., running GC during gameplay).
        *   **Predictability:** The exact timing of object destruction can be less predictable than manual `delete`, which can be an issue for very performance-critical systems or when dealing with external resources.
        *   **Learning Curve:** Requires understanding Unreal's specific GC rules (e.g., `UPROPERTY()`, `AddReferencedObjects`, `TWeakPtr`) which differ from standard C++ memory management.
        *   **Not for Everything:** GC is only for `UObject`s. Raw C++ objects, structs, and non-UObject data still require manual management or smart pointers.
    *   **Critique:** The decision is generally effective for game development. The benefits of increased safety and productivity often outweigh the performance overhead, especially given Unreal's optimizations for GC. However, developers must understand its nuances to avoid performance issues and correctly manage non-UObject memory.

*   **Evaluate the effectiveness of `UInterface`s as a mechanism for achieving the Dependency Inversion Principle (DIP) in Unreal Engine. Provide an example where an interface significantly improves code maintainability.**
    *   **Effectiveness for DIP:** `UInterface`s are highly effective for achieving DIP in Unreal Engine. DIP states that high-level modules should not depend on low-level modules; both should depend on abstractions. Also, abstractions should not depend on details; details should depend on abstractions. `UInterface`s provide exactly these abstractions.
        *   **High-level modules (e.g., a `UInteractionComponent`) can depend on an `IInteractable` interface (abstraction) rather than concrete classes like `ADoor` or `APickupItem` (low-level details).**
        *   **Low-level modules (e.g., `ADoor`, `APickupItem`) implement the `IInteractable` interface, meaning their details depend on the abstraction.**
    *   **Example for Improved Maintainability:**
        *   **Scenario without Interface:** A `UInteractionComponent` has a `TryInteract(AActor* TargetActor)` function. Inside, it uses `Cast<ADoor>(TargetActor)` and `Cast<APickupItem>(TargetActor)` to check types and call specific functions like `ADoor->Open()` or `APickupItem->Collect()`. If a new interactable object (e.g., `ALever`) is added, `UInteractionComponent` *must* be modified to add another `Cast` and specific function call. This violates OCP and makes `UInteractionComponent` tightly coupled to all interactable types.
        *   **Scenario with `IInteractable` Interface:**
            ```cpp
            // IInteractable.h
            UINTERFACE(MinimalAPI) class UInteractable : public UInterface { GENERATED_BODY() };
            class IInteractable { GENERATED_BODY() public: UFUNCTION(BlueprintCallable, BlueprintNativeEvent) void Interact(AActor* Interactor); };

            // UInteractionComponent.cpp
            void UInteractionComponent::TryInteract(AActor* TargetActor)
            {
                if (TargetActor && TargetActor->Implements<UInteractable>())
                {
                    IInteractable::Execute_Interact(TargetActor, GetOwner()); // Call interface function
                }
            }

            // ADoor.cpp (implements IInteractable)
            void ADoor::Interact_Implementation(AActor* Interactor) { Open(); }

            // APickupItem.cpp (implements IInteractable)
            void APickupItem::Interact_Implementation(AActor* Interactor) { Collect(); }
            ```
        *   **Maintainability Improvement:** When a new interactable object like `ALever` is introduced, `UInteractionComponent` does *not* need to be modified. `ALever` simply implements `IInteractable`, and the existing `UInteractionComponent` can interact with it seamlessly. This significantly improves maintainability by localizing changes and reducing ripple effects across the codebase.

*   **You are tasked with optimizing a game's performance. Based on your understanding of Unreal Insights and `UE_LOG`, when would you prioritize using one over the other, and what factors would influence your decision?**
    *   **Prioritize Unreal Insights when:**
        *   **Goal:** Identifying broad performance bottlenecks (CPU, GPU, memory, networking), understanding frame time distribution, or profiling specific systems over time.
        *   **Factors:** You suspect a general performance issue, want to see how different systems (rendering, physics, AI) contribute to frame time, need to track memory allocations, or analyze network traffic. It's excellent for "where is the time going?" questions.
    *   **Prioritize `UE_LOG` when:**
        *   **Goal:** Debugging specific logical flows, tracking variable values, confirming execution paths, or providing textual feedback during development.
        *   **Factors:** You're trying to understand *why* a specific piece of code is behaving unexpectedly, need to see the value of a variable at a certain point, or want to confirm that a particular function was called. It's excellent for "what is happening here?" questions.
    *   **Combined Use:** Often, they are used together. `UE_LOG` can be used to mark specific events or states in the Insights timeline, providing context to performance spikes or dips. For example, logging "Starting complex AI calculation" might correlate with a CPU spike in Insights.

*   **Consider a scenario where a new gameplay feature requires a custom input action. Evaluate the steps involved in setting this up, from defining the input to handling it in a `PlayerController`, and identify potential points of failure or complexity.**
    *   **Steps Involved:**
        1.  **Define Input Action:** Create a new `UInputAction` asset (e.g., `IA_Jump`) in the Content Browser.
        2.  **Define Input Mapping Context:** Create a new `UInputMappingContext` asset (e.g., `IMC_Player`) and add the `IA_Jump` action to it, mapping it to a specific key (e.g., Spacebar).
        3.  **Apply Input Mapping Context:** In the `APlayerController` (or `APlayerCharacter` if using Enhanced Input directly there), add the `IMC_Player` to the Enhanced Input Local Player Subsystem.
        4.  **Bind Input Action:** In the `APlayerController` (or `APlayerCharacter`), bind the `IA_Jump` action to a C++ function (e.g., `HandleJump()`) using the Enhanced Input Component. This involves binding to `Triggered`, `Started`, `Completed`, etc.
        5.  **Implement Handler Function:** Write the C++ function (`HandleJump()`) that will be executed when the input action is triggered.
    *   **Potential Points of Failure or Complexity:**
        *   **Missing Input Mapping Context:** Forgetting to add the `IMC_Player` to the Local Player Subsystem means the input won't be processed.
        *   **Incorrect Binding Event:** Binding to the wrong event (e.g., `Started` instead of `Triggered` for a continuous action) can lead to unexpected behavior.
        *   **Input Priority:** If multiple `InputMappingContext`s are active, their priorities can conflict, leading to one overriding another.
        *   **Input Consumption:** If an input is consumed by a UI element or another system, it might not reach the `PlayerController`/`Character`.
        *   **Asynchronous Input:** Enhanced Input actions can have different trigger types (e.g., `Hold`, `Tap`), which require careful handling in the bound function.
        *   **Replication:** If the input action affects gameplay state, ensuring proper client-server replication is crucial, adding network complexity.
        *   **Debugging:** Debugging input issues can be tricky, requiring use of the Input Debugger or `UE_LOG` to trace input events.

### 6. Creating - Answers

*   **Design a simple C++ `UActorComponent` that manages a character's "Stamina." This component should have a `MaxStamina` and `CurrentStamina` property, and a `ConsumeStamina(float Amount)` function. Outline the `.h` and `.cpp` structure, including necessary macros and specifiers.**

    *   **`UStaminaComponent.h`:**
        ```cpp
        #pragma once

        #include "CoreMinimal.h"
        #include "Components/ActorComponent.h"
        #include "StaminaComponent.generated.h"

        DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnStaminaChanged, float, CurrentStamina, float, MaxStamina);

        UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
        class MYPROJECT_API UStaminaComponent : public UActorComponent
        {
            GENERATED_BODY()

        public:
            UStaminaComponent();

        protected:
            virtual void BeginPlay() override;

        public:
            // Properties
            UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stamina")
            float MaxStamina;

            UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stamina")
            float CurrentStamina;

            // Functions
            UFUNCTION(BlueprintCallable, Category = "Stamina")
            bool ConsumeStamina(float Amount);

            UFUNCTION(BlueprintCallable, Category = "Stamina")
            void RestoreStamina(float Amount);

            UFUNCTION(BlueprintPure, Category = "Stamina")
            float GetStaminaPercentage() const;

            // Delegates
            UPROPERTY(BlueprintAssignable, Category = "Stamina")
            FOnStaminaChanged OnStaminaChanged;

        private:
            void UpdateStamina(float NewStamina);
        };
        ```

    *   **`UStaminaComponent.cpp`:**
        ```cpp
        #include "StaminaComponent.h"

        UStaminaComponent::UStaminaComponent()
        {
            PrimaryComponentTick.bCanEverTick = false; // Stamina doesn't need to tick by default
            MaxStamina = 100.0f;
            CurrentStamina = MaxStamina;
        }

        void UStaminaComponent::BeginPlay()
        {
            Super::BeginPlay();
            // Ensure CurrentStamina is initialized to MaxStamina at start
            CurrentStamina = MaxStamina;
            OnStaminaChanged.Broadcast(CurrentStamina, MaxStamina);
        }

        bool UStaminaComponent::ConsumeStamina(float Amount)
        {
            if (Amount <= 0.0f) return true; // Nothing to consume
            if (CurrentStamina >= Amount)
            {
                UpdateStamina(CurrentStamina - Amount);
                return true;
            }
            return false; // Not enough stamina
        }

        void UStaminaComponent::RestoreStamina(float Amount)
        {
            if (Amount <= 0.0f) return;
            UpdateStamina(CurrentStamina + Amount);
        }

        float UStaminaComponent::GetStaminaPercentage() const
        {
            return (MaxStamina > 0) ? (CurrentStamina / MaxStamina) : 0.0f;
        }

        void UStaminaComponent::UpdateStamina(float NewStamina)
        {
            CurrentStamina = FMath::Clamp(NewStamina, 0.0f, MaxStamina);
            OnStaminaChanged.Broadcast(CurrentStamina, MaxStamina);
        }
        ```

*   **Propose a design for a new `UInterface` called `IInteractable` that allows a player character to interact with various objects in the world (e.g., opening a door, picking up an item). Define at least one `UFUNCTION` within this interface.**

    *   **`IInteractable.h`:**
        ```cpp
        #pragma once

        #include "CoreMinimal.h"
        #include "UObject/Interface.h"
        #include "Interactable.generated.h"

        // This class does not need to be modified.
        UINTERFACE(MinimalAPI, Blueprintable) // Blueprintable allows Blueprints to implement this interface
        class UInteractable : public UInterface
        {
            GENERATED_BODY()
        };

        /**
         * Interface for objects that can be interacted with by a player or other Actors.
         */
        class MYPROJECT_API IInteractable
        {
            GENERATED_BODY()

        public:
            /**
             * Called when an Actor attempts to interact with this object.
             * @param Interactor - The Actor that initiated the interaction.
             * @return True if the interaction was successful, false otherwise.
             */
            UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category = "Interaction")
            bool Interact(AActor* Interactor);

            /**
             * Optional: Called to get a description of the interaction for UI purposes.
             * @return A localized text describing the interaction.
             */
            UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category = "Interaction")
            FText GetInteractionText() const;
        };
        ```

*   **Formulate a plan for refactoring a monolithic `ACharacter` class that currently handles movement, health, inventory, and quest management into a more modular design using `UActorComponent`s and `UInterface`s.**

    *   **Current State:** `AMonolithicCharacter` has direct implementations for `Move()`, `TakeDamage()`, `AddItemToInventory()`, `StartQuest()`, etc., and holds all related data.
    *   **Refactoring Plan:**
        1.  **Identify Responsibilities:** Break down the `AMonolithicCharacter`'s responsibilities into distinct functional areas:
            *   Movement (already handled by `CharacterMovementComponent`, but custom logic might exist)
            *   Health/Damage
            *   Inventory Management
            *   Quest Management
            *   Interaction (if the character can interact with objects)
        2.  **Create `UActorComponent`s for Each Responsibility:**
            *   `UHealthComponent`: Encapsulate `CurrentHealth`, `MaxHealth`, `TakeDamage()`, `Heal()`, `OnDeath` delegate.
            *   `UInventoryComponent`: Encapsulate `TArray<UItem*>` (or similar), `AddItem()`, `RemoveItem()`, `UseItem()`.
            *   `UQuestLogComponent`: Encapsulate `TArray<UQuest*>` (or similar), `StartQuest()`, `CompleteQuest()`, `UpdateQuestProgress()`.
        3.  **Define `UInterface`s for Cross-Component/Actor Communication:**
            *   `IDamageable`: For objects that can take damage (implemented by `ACharacter` and delegating to `UHealthComponent`).
            *   `IInventoryOwner`: For objects that can own an inventory (implemented by `ACharacter` and delegating to `UInventoryComponent`).
            *   `IQuestGiver`: For NPCs that can give quests.
        4.  **Migrate Logic and Data:**
            *   Move health-related variables and functions from `AMonolithicCharacter` to `UHealthComponent`.
            *   Move inventory-related variables and functions to `UInventoryComponent`.
            *   Move quest-related variables and functions to `UQuestLogComponent`.
            *   Update `AMonolithicCharacter` to *add* these components in its constructor or `BeginPlay()`.
        5.  **Implement Interfaces in `ACharacter`:**
            *   Make `ACharacter` implement `IDamageable` and `IInventoryOwner`.
            *   The interface functions in `ACharacter` will simply call the corresponding functions on its `UHealthComponent` and `UInventoryComponent`.
        6.  **Update External References:**
            *   Any code that previously called `AMonolithicCharacter->TakeDamage()` directly will now query for `IDamageable` interface and call `Execute_ReceiveDamage()`.
            *   Any code that needed to access the inventory will now query for `IInventoryOwner` and call its interface functions.
        7.  **Remove Redundant Code:** Delete the old, monolithic implementations from `AMonolithicCharacter`.
        8.  **Testing:** Thoroughly test each component and the refactored character to ensure all functionality works as expected and no regressions are introduced.

*   **Imagine you need to create a new type of projectile that applies a "burning" status effect over time. Describe how you would implement this using the `IDamageable` interface and potentially a new `UActorComponent` for status effects, ensuring it integrates cleanly with the existing damage system.**

    *   **Assumptions:**
        *   An `IDamageable` interface exists with a `ReceiveDamage(float DamageAmount, FDamageEvent DamageEvent, AController* EventInstigator, AActor* DamageCauser)` function.
        *   `AActor`s that can be damaged implement `IDamageable` and delegate to a `UHealthComponent`.
        *   A `FDamageEvent` (or custom derivative) can carry additional information.

    *   **Implementation Steps:**

        1.  **Create `UStatusEffectComponent`:**
            *   This `UActorComponent` would be responsible for managing all status effects on an `AActor`.
            *   Properties: `TArray<FActiveStatusEffect>` (a struct holding effect type, duration, intensity, etc.).
            *   Functions: `ApplyStatusEffect(FStatusEffectData EffectData)`, `RemoveStatusEffect(EStatusEffectType EffectType)`.
            *   Tick: In its `TickComponent`, it would update active effects (e.g., apply burning damage over time, decrement duration).
            *   Delegates: `OnStatusEffectApplied`, `OnStatusEffectRemoved`.

        2.  **Define `FStatusEffectData` (Struct):**
            *   A `USTRUCT` to define the data for a status effect (e.g., `EStatusEffectType::Burning`, `Duration`, `TickDamage`, `TickInterval`).

        3.  **Modify `IDamageable::ReceiveDamage` (or `UHealthComponent::TakeDamage`):**
            *   The `ReceiveDamage` function (or the `UHealthComponent`'s `TakeDamage` function it delegates to) would be updated to check the `FDamageEvent` for any associated status effect data.
            *   If the `FDamageEvent` indicates a "burning" effect should be applied, it would:
                1.  Get or create the `UStatusEffectComponent` on the damaged `AActor`.
                2.  Call `UStatusEffectComponent->ApplyStatusEffect(BurningEffectData)`.

        4.  **Create `ABurningProjectile` (or modify existing projectile):**
            *   When `ABurningProjectile` hits an `AActor`:
                1.  It would query the hit `AActor` for the `IDamageable` interface.
                2.  If `IDamageable` is found, it would construct a `FDamageEvent` (perhaps a custom `FBurningDamageEvent` derived from `FDamageEvent`) that includes the `FStatusEffectData` for burning.
                3.  It would then call `IDamageable::Execute_ReceiveDamage()` passing this `FDamageEvent`.

        5.  **Integration Cleanliness:**
            *   **Decoupling:** The `ABurningProjectile` doesn't need to know about `UStatusEffectComponent` directly. It only interacts with the `IDamageable` interface and passes data via the `FDamageEvent`.
            *   **Modularity:** The `UStatusEffectComponent` is a self-contained unit for managing all status effects, making it reusable and easy to extend with new effects.
            *   **Extensibility:** Adding new status effects (e.g., "poisoned," "slowed") would primarily involve defining new `FStatusEffectData` and updating the `UStatusEffectComponent`'s `TickComponent` logic, without modifying the damage system or projectiles.
            *   **Clarity:** The damage system remains focused on applying damage, while the status effect system handles the ongoing effects.

---