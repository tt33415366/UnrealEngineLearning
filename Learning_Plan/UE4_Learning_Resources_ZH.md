### 1. 核心C++类结构

这是最基础的概念。所有由虚幻引擎管理的C++对象都派生自一个基类，并使用特殊的宏来与引擎的系统（如垃圾回收和蓝图编辑器）集成。

**核心要点:** 您的C++类将使用`UCLASS()`、`GENERATED_BODY()`、`UPROPERTY()`和`UFUNCTION()`来与引擎通信。

**核心示例：一个基础的`UObject`**
这展示了最简单的能被虚幻引擎感知的C++类。

```cpp
class UMyObject : public UObject
{
    GENERATED_BODY()

public:
    // 构造函数
    UMyObject();

    // 暴露给引擎的示例属性
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MyObject")
    float MyFloatValue;

    // 暴露给引擎的示例函数
    UFUNCTION(BlueprintCallable, Category = "MyObject")
    void MyFunction();
};
```
*来源: [在虚幻引擎中进行C++编程](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)*

---

### 2. 游戏框架：Actors

`Actors`是您放置在游戏世界中的主要对象。以下代码片段展示了一个完整的、基础的`AActor`实现，这是我们计划中Actor-Component模型的基石。

**核心要点:** `AActor`是您关卡中任何对象的基础。它有一个由`BeginPlay()`（当对象进入世界时调用）和`Tick()`（每帧调用）等函数管理的生命周期。

**核心示例：一个基础的`AActor`**

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
    // 为此actor的属性设置默认值
    AMyActor();

protected:
    // 当游戏开始或生成时调用
    virtual void BeginPlay() override;

public:    
    // 每帧调用
    virtual void Tick(float DeltaTime) override;
};

// MyActor.cpp
#include "MyActor.h"

AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = true; // 允许此Actor每帧Tick
}

void AMyActor::BeginPlay()
{
    Super::BeginPlay(); // 重要：始终调用父类的版本！
    
    UE_LOG(LogTemp, Warning, TEXT("MyActor has begun play!"));
}

void AMyActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime); // 重要：始终调用父类的版本！
}
```
*来源: [虚幻引擎中的骨骼网格体资产](https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletal-mesh-assets-in-unreal-engine_application_version=5)*

---

### 3. 核心数据结构与模式

您的C++11知识是可转移的，但虚幻引擎为通用模式和容器提供了自己的、经过实战检验的实现。

#### 容器
您将主要使用虚幻的`TArray`和`TMap`，而不是`std::vector`或`std::map`。它们被设计为高效的，并能与`UPROPERTY`系统协同工作。

**核心示例：虚幻容器**
```cpp
// 使用TArray的示例 (类似 std::vector)
TArray<int32> MyIntArray;
MyIntArray.Add(10);
MyIntArray.Add(20);

// 使用TMap的示例 (类似 std::map)
TMap<FString, int32> MyStringToIntMap;
MyStringToIntMap.Add("Key1", 100);
MyStringToIntMap.Add("Key2", 200);
```
*来源: [虚幻引擎中的容器](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)*

#### 委托 (回调)

委托是虚幻引擎强大且安全的函数指针版本，对于事件驱动编程至关重要。

**核心示例：声明一个委托**
```cpp
// 声明一个没有参数的委托
DECLARE_DELEGATE(FMyDelegate);

// 声明一个带有一个整数参数的委托
DECLARE_DELEGATE_OneParam(FMyDelegateWithParam, int32);

// 然后您可以将它绑定到一个UObject的成员函数上并稍后执行。
```
*来源: [虚幻引擎中的委托](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-with-cplusplus-in-unreal-engine)*

---

### 4. 在编辑器中入门

文档建议从C++模板创建一个项目，以查看这些概念的实际应用。

*   **建议:** 使用 **C++ Top Down** 模板创建一个新项目。
*   **行动:** 创建后，您可以在类查看器中找到`PlayerController`的C++实现，以了解用户输入是如何处理的。

---

## 额外资源

这里有一些更详细的资源，与 `UE4_Learning_Plan_ZH.md` 中的主题对齐。

### 核心C++深度解析

*   **UObject反射系统:**
    *   [官方文档: Unreal对象处理](https://epicgames.com/developers/docs/unreal-engine/cplusplus-programming/unreal-object-handling) - 关于`UObject`如何被引擎管理的权威来源。
    *   [官方博客: 属性系统(反射)](https://unrealengine.com/en-US/blog/unreal-property-system-reflection) - 一篇详细的官方博客文章，解释了虚幻头文件工具（UHT）和宏是如何协同工作的。
*   **内存管理和智能指针:**
    *   [官方文档: 智能指针](https://epicgames.com/developers/docs/unreal-engine/cplusplus-programming/smart-pointers) - 一份关于何时以及如何使用`TSharedPtr`、`TUniquePtr`和`TWeakPtr`的综合指南。

### 游戏性架构

*   **游戏性框架:**
    *   [Tom Looman的C++指南](https://www.tomlooman.com/unreal-engine-cpp-guide/) - 一份备受推崇的、为C++开发者准备的实用指南，其中涵盖了游戏性框架。
    *   [官方文档: 游戏性架构](https://epicgames.com/developers/docs/unreal-engine/gameplay-architecture) - 所有框架类的官方参考。
*   **使用C++接口:**
    *   [官方文档: C++接口](https://epicgames.com/developers/docs/unreal-engine/cplusplus-programming/interfaces) - 一份关于在C++中声明和实现接口的完整指南。
*   **构建系统:**
    *   [官方文档: 虚幻构建系统](https://epicgames.com/developers/docs/unreal-engine/build-system) - 解释了`.Build.cs`文件的结构以及虚幻构建工具（UBT）如何编译您的项目。

### 调试与性能分析

*   **调试C++代码:**
    *   [官方文档: 调试C++](https://epicgames.com/developers/docs/unreal-engine/cplusplus-programming/debugging) - 涵盖了使用Visual Studio调试器设置和调试虚幻引擎。
    *   [JetBrains Rider: 调试虚幻引擎](https://www.jetbrains.com/help/rider/Debugging_Unreal_Engine_Project.html) - 使用Rider IDE进行调试的指南。
*   **使用Unreal Insights进行性能分析:**
    *   [官方文档: Unreal Insights](https://epicgames.com/developers/docs/unreal-engine/performance-and-profiling/unreal-insights) - 关于如何使用这个强大的性能分析工具的概述。
    *   [YouTube教程: Unreal Insights简介](https://www.youtube.com/watch?v=J3i-9tH1HwM) - 一个关于捕获和分析性能数据的视频演练。

### 高级主题

*   **游戏性能力系统 (GAS):**
    *   [官方文档: 游戏性能力系统](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine) - 学习GAS的官方起点。
    *   [GitHub: `tranek`的GAS文档](https://github.com/tranek/GASDocumentation) - 一份极其详细且备受推崇的社区维护指南，用于理解和使用GAS。
