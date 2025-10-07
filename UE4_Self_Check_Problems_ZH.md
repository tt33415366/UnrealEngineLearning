# UE4 自我检查问题：所有布鲁姆分类学级别

---

### 1. 记忆 (Remembering)

*   在虚幻引擎 C++ 类中，`UCLASS()`、`UPROPERTY()` 和 `UFUNCTION()` 这三个主要宏的作用是什么？
*   虚幻引擎中用于 `UObject` 的主要内存管理系统是什么？
*   请列出资源中提到的两种虚幻引擎特有的智能指针类型。
*   请定义虚幻引擎中的 `AActor` 是什么。
*   请定义虚幻引擎中的 `UActorComponent` 是什么。
*   定义模块依赖关系的文件名称是什么？
*   `UE_LOG` 宏的主要用途是什么？

### 2. 理解 (Understanding)

*   `UCLASS()`、`UPROPERTY()` 和 `UFUNCTION()` 宏如何使 C++ 代码与虚幻引擎的反射系统进行交互？
*   为什么 `UObject*` 成员变量必须用 `UPROPERTY()` 标记？
*   Actor-Component 模型体现的核心原则（组合优于继承）是什么？
*   请简要描述 `AGameMode` 在游戏框架中的作用。
*   `APawn` 和 `ACharacter` 的主要区别是什么？
*   虚幻引擎中 `UInterface` 的基本目的是什么？
*   使用 `UInterface` 如何有助于 C++ 代码的解耦？
*   负责根据这些依赖文件编译虚幻引擎项目的工具是什么？
*   `UPROPERTY()` 中 `EditAnywhere` 和 `VisibleAnywhere` 说明符的区别是什么？
*   为什么在重写 `BeginPlay()` 或 `Tick()` 等引擎函数时调用 `Super::` 很重要？
*   虚幻洞察 (Unreal Insights) 的主要用途是什么？

### 3. 应用 (Applying)

*   如果你想将一个 C++ 函数暴露给蓝图调用，你会使用哪个宏，以及将其放置在哪里？
*   你的 `UObject` 中有一个 `UTexture2D* MyTexture;` 成员变量。你将如何声明它以确保它被垃圾回收器正确管理？
*   你希望为多种不同类型的角色添加一个可重用的“库存”系统。你会将其实现为 `AActor` 还是 `UActorComponent`？请解释原因。
*   哪个类（`AGameMode`、`APlayerController`、`APawn`）负责处理玩家输入并将其转换为角色动作？
*   如果你想创建一个用于可“激活”对象的接口，你将如何在接口中声明一个简单的 `Activate()` 函数？
*   如果你的 C++ 代码需要使用“AIModule”的功能，你需要在项目的构建文件中采取什么具体行动？
*   你的角色类中有一个 `float MovementSpeed;` 变量，你希望设计师可以直接在蓝图编辑器中调整它。你将如何声明这个 `UPROPERTY()`？
*   考虑以下代码：`UMyObject* MyObject = NewObject<UMyObject>();`。如果 `MyObject` 是 `AActor` 的成员变量，并且没有用 `UPROPERTY()` 标记，那么在游戏过程中可能会出现什么潜在问题？
*   你正在尝试找出为什么你的游戏在特定区域出现帧率下降。你会主要使用 `UE_LOG` 还是虚幻洞察 (Unreal Insights) 进行此调查？请解释你的选择。

### 4. 分析 (Analyzing)

*   比较和对比虚幻引擎的 `TArray` 与 C++ 标准库的 `std::vector`。在虚幻项目中，使用 `TArray` 有哪些优势？
*   虚幻引擎中实现的 Actor-Component 模型如何直接支持单一职责原则 (SRP) 和开闭原则 (OCP)？
*   分析解耦伤害系统的数据流（如 `UE4_Learning_Plan.md` 中所示）。与武器直接调用特定 `AMonster` 的 `TakeDamage` 函数的系统相比，这种设计如何减少依赖？
*   检查提供的 `UHealthComponent` 和 `IDamageable` 接口代码。确定它们如何协同工作以实现灵活的伤害应用而无需紧密耦合。

### 5. 评估 (Evaluating)

*   评价虚幻引擎为 `UObject` 使用垃圾回收系统而不是传统的 C++ 手动内存管理的决定。有哪些权衡？
*   评估 `UInterface` 作为在虚幻引擎中实现依赖反转原则 (DIP) 机制的有效性。提供一个接口显著提高代码可维护性的示例。
*   你负责优化游戏的性能。根据你对虚幻洞察 (Unreal Insights) 和 `UE_LOG` 的理解，你何时会优先使用其中一个，以及哪些因素会影响你的决定？
*   考虑一个新游戏功能需要自定义输入操作的场景。评估从定义输入到在 `PlayerController` 中处理它所涉及的步骤，并识别潜在的故障点或复杂性。

### 6. 创建 (Creating)

*   设计一个简单的 C++ `UActorComponent` 来管理角色的“体力”。该组件应具有 `MaxStamina` 和 `CurrentStamina` 属性，以及一个 `ConsumeStamina(float Amount)` 函数。概述 `.h` 和 `.cpp` 结构，包括必要的宏和说明符。
*   提出一个名为 `IInteractable` 的新 `UInterface` 的设计，该接口允许玩家角色与世界中的各种对象（例如，打开门，拾取物品）进行交互。在此接口中定义至少一个 `UFUNCTION`。
*   制定一个计划，将目前处理移动、生命值、库存和任务管理的单一 `ACharacter` 类重构为使用 `UActorComponent` 和 `UInterface` 的更模块化设计。
*   假设你需要创建一种新的投射物，它会随着时间施加“燃烧”状态效果。描述你将如何使用 `IDamageable` 接口和可能的新 `UActorComponent` 来实现此功能，以确保它与现有伤害系统干净地集成。
