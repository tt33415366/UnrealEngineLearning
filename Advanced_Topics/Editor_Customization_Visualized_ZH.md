# 编辑器自定义可视化

本指南解释了如何使用 C++ 扩展 Unreal 编辑器，添加自定义工具和 UI。自定义编辑器是为您的团队改善工作流程、创建特定于游戏的工具以及简化内容创建过程的强大方法。

**注意：** 所有编辑器自定义代码都必须放在一个**仅编辑器模块 (Editor-only module)** 中。这是在您的 `.uproject` 或 `.uplugin` 文件中类型为 `Editor` 的模块，以确保它不会被编译到您的最终打包游戏中。

## 目录
- [自定义资产操作](#自定义资产操作)
- [细节面板自定义 (IDetailCustomization)](#细节面板自定义-idetailcustomization)
- [自定义编辑器模式 (FEdMode)](#自定义编辑器模式-fedmode)
- [自定义资产类型 (UFactory)](#自定义资产类型-ufactory)

## 自定义资产操作

### 概念
自定义资产操作允许您向内容浏览器中资产的右键单击上下文菜单添加新选项。这是添加特定于资产的实用程序（如自定义验证、数据处理或批量操作）的最简单和最常见的方法之一。

要做到这一点，您需要创建一个继承自 `FAssetTypeActions_Base` 的类，并将其注册到 `FAssetToolsModule`。

### 代码示例：数据资产的自定义操作

```cpp
// MyDataAssetActions.h
#pragma once

#include "CoreMinimal.h"
#include "AssetTypeActions_Base.h"
#include "MyDataAsset.h"

class FMyDataAssetActions : public FAssetTypeActions_Base
{
public:
    // IAssetTypeActions 实现
    virtual FText GetName() const override { return FText::FromString("My Data Asset"); }
    virtual FColor GetTypeColor() const override { return FColor::Cyan; }
    virtual UClass* GetSupportedClass() const override { return UMyDataAsset::StaticClass(); }
    virtual uint32 GetCategories() override { return EAssetTypeCategories::Misc; }

    // 向上下文菜单添加自定义操作
    virtual void GetActions(const TArray<UObject*>& InObjects, FMenuBuilder& MenuBuilder) override;

private:
    // 由我们的自定义操作执行的函数
    void ExecuteCustomAction(TArray<TWeakObjectPtr<UMyDataAsset>> InDataAssets);
};
```

```cpp
// MyDataAssetActions.cpp
#include "MyDataAssetActions.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"

void FMyDataAssetActions::GetActions(const TArray<UObject*>& InObjects, FMenuBuilder& MenuBuilder)
{
    // 将选定的对象转换为我们的特定数据资产类型
    TArray<TWeakObjectPtr<UMyDataAsset>> DataAssets;
    for (UObject* Obj : InObjects)
    {
        if (UMyDataAsset* DataAsset = Cast<UMyDataAsset>(Obj))
        {
            DataAssets.Add(DataAsset);
        }
    }

    // 向菜单添加一个新部分
    MenuBuilder.AddMenuEntry(
        FText::FromString("Perform Custom Action"),
        FText::FromString("This is a tooltip for our custom action."),
        FSlateIcon(),
        FUIAction(
            FExecuteAction::CreateSP(this, &FMyDataAssetActions::ExecuteCustomAction, DataAssets),
            FCanExecuteAction()
        )
    );
}

void FMyDataAssetActions::ExecuteCustomAction(TArray<TWeakObjectPtr<UMyDataAsset>> InDataAssets)
{
    for (auto& DataAssetPtr : InDataAssets)
    {
        if (UMyDataAsset* DataAsset = DataAssetPtr.Get())
        {
            UE_LOG(LogTemp, Warning, TEXT("Performing custom action on: %s"), *DataAsset->GetName());
            // ... 在这里执行您的逻辑 ...
        }
    }
}
```

**注册操作：** 在您的编辑器模块的 `StartupModule` 函数中：

```cpp
// MyEditorModule.cpp
#include "AssetToolsModule.h"
#include "MyDataAssetActions.h"

void FMyEditorModule::StartupModule()
{
    IAssetTools& AssetTools = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools").Get();
    TSharedRef<IAssetTypeActions> Action = MakeShareable(new FMyDataAssetActions);
    AssetTools.RegisterAssetTypeActions(Action);
    // 记住存储操作，以便在 ShutdownModule 中注销它
    CreatedAssetTypeActions.Add(Action);
}
```

### 可视化：自定义资产操作流程

```mermaid
graph TD
    A[在内容浏览器中右键单击 UMyDataAsset] --> B{在 FMyDataAssetActions 上调用 GetActions()}
    B --> C[MenuBuilder.AddMenuEntry() 添加一个新 UI 按钮]
    C --> D[用户点击“执行自定义操作”]
    D --> E[FUIAction 执行 ExecuteCustomAction()]
    E --> F[在选定的资产上运行自定义逻辑]
```

## 细节面板自定义 (IDetailCustomization)

### 概念
细节面板自定义允许您完全更改类的属性在细节面板中的显示方式。这对于为复杂数据创建用户友好的界面、用直观的按钮、滑块或自定义 Slate 小部件替换原始数据字段至关重要。

您可以通过创建一个继承自 `IDetailCustomization` 的类并将其注册到 `FPropertyEditorModule` 来实现这一点。

### 代码示例：自定义细节面板

```cpp
// MyActorDetailsCustomization.h
#pragma once

#include "CoreMinimal.h"
#include "IDetailCustomization.h"

class FMyActorDetailsCustomization : public IDetailCustomization
{
public:
    // IDetailCustomization 接口
    virtual void CustomizeDetails(IDetailLayoutBuilder& DetailBuilder) override;

    static TSharedRef<IDetailCustomization> MakeInstance();

private:
    FReply OnCustomButtonClicked();
    TWeakObjectPtr<AMyActor> MyActor;
};
```

```cpp
// MyActorDetailsCustomization.cpp
#include "MyActorDetailsCustomization.h"
#include "DetailLayoutBuilder.h"
#include "DetailCategoryBuilder.h"
#include "DetailWidgetRow.h"
#include "Widgets/Input/SButton.h"
#include "MyActor.h"

TSharedRef<IDetailCustomization> FMyActorDetailsCustomization::MakeInstance()
{
    return MakeShareable(new FMyActorDetailsCustomization);
}

void FMyActorDetailsCustomization::CustomizeDetails(IDetailLayoutBuilder& DetailBuilder)
{
    // 获取正在自定义的对象
    TArray<TWeakObjectPtr<UObject>> Objects;
    DetailBuilder.GetObjectsBeingCustomized(Objects);
    if (Objects.Num() > 0)
    {
        MyActor = Cast<AMyActor>(Objects[0].Get());
    }

    // 创建一个新类别
    IDetailCategoryBuilder& MyCategory = DetailBuilder.EditCategory("My Custom Category", FText::GetEmpty(), ECategoryPriority::Important);

    // 向类别添加一个自定义按钮
    MyCategory.AddCustomRow(FText::FromString("Custom Button"))
    .ValueContent()
    [
        SNew(SButton)
        .Text(FText::FromString("Execute My Logic"))
        .OnClicked(this, &FMyActorDetailsCustomization::OnCustomButtonClicked)
    ];
}

FReply FMyActorDetailsCustomization::OnCustomButtonClicked()
{
    if (MyActor.IsValid())
    {
        MyActor->SomeFunctionToExecute();
        UE_LOG(LogTemp, Warning, TEXT("Custom button clicked for actor: %s"), *MyActor->GetName());
    }
    return FReply::Handled();
}
```

**注册自定义：** 在您的编辑器模块的 `StartupModule` 函数中：

```cpp
// MyEditorModule.cpp
#include "PropertyEditorModule.h"
#include "MyActorDetailsCustomization.h"
#include "MyActor.h"

void FMyEditorModule::StartupModule()
{
    FPropertyEditorModule& PropertyModule = FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");
    PropertyModule.RegisterCustomClassLayout(
        AMyActor::StaticClass()->GetFName(),
        FOnGetDetailCustomizationInstance::CreateStatic(&FMyActorDetailsCustomization::MakeInstance)
    );
}
```

### 可视化：细节面板自定义

```mermaid
graph TD
    subgraph 默认细节面板
        A[类别: Transform]
        B[类别: MyActor]
        C[MyInt: 10]
        D[MyFloat: 3.14]
    end

    subgraph 自定义细节面板
        E[类别: Transform]
        F[类别: My Custom Category]
        G[按钮: "执行我的逻辑"]
    end

    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#fcf,stroke:#333,stroke-width:2px
```

## 自定义编辑器模式 (FEdMode)

### 概念
自定义编辑器模式 (`FEdMode`) 是自定义编辑器的最强大方式。它们允许您接管编辑器视口，提供自定义渲染、输入处理（鼠标点击、键盘按键）以及自定义工具或小部件。内置的模式如植物、地形和网格绘制就是这样实现的。

### 代码示例：一个简单的绘图编辑器模式

```cpp
// MyEdMode.h
#pragma once

#include "CoreMinimal.h"
#include "EdMode.h"

class FMyEdMode : public FEdMode
{
public:
    const static FEditorModeID EM_MyEdModeId;

    FMyEdMode();
    virtual ~FMyEdMode();

    // FEdMode 接口
    virtual void Enter() override;
    virtual void Exit() override;
    virtual void Render(const FSceneView* View, FViewport* Viewport, FPrimitiveDrawInterface* PDI) override;
    virtual bool InputKey(FEditorViewportClient* ViewportClient, FViewport* Viewport, FKey Key, EInputEvent Event) override;
};
```

```cpp
// MyEdMode.cpp
#include "MyEdMode.h"
#include "EditorModeManager.h"

const FEditorModeID FMyEdMode::EM_MyEdModeId = TEXT("EM_MyEdMode");

FMyEdMode::FMyEdMode() {}
FMyEdMode::~FMyEdMode() {}

void FMyEdMode::Enter()
{
    FEdMode::Enter();
    UE_LOG(LogTemp, Warning, TEXT("Entered MyEdMode."));
}

void FMyEdMode::Exit()
{
    FEdMode::Exit();
    UE_LOG(LogTemp, Warning, TEXT("Exited MyEdMode."));
}

void FMyEdMode::Render(const FSceneView* View, FViewport* Viewport, FPrimitiveDrawInterface* PDI)
{
    // 在世界原点绘制一个圆
    DrawCircle(PDI, FVector::ZeroVector, FVector(1,0,0), FVector(0,1,0), FColor::Yellow, 100.0f, 32, SDPG_World);
}

bool FMyEdMode::InputKey(FEditorViewportClient* ViewportClient, FViewport* Viewport, FKey Key, EInputEvent Event)
{
    if (Key == EKeys::LeftMouseButton && Event == IE_Pressed)
    {
        UE_LOG(LogTemp, Warning, TEXT("Left mouse button pressed in MyEdMode."));
        return true; // 我们处理了此输入
    }
    return false;
}
```

**注册模式：** 在您的编辑器模块的 `StartupModule` 函数中：

```cpp
// MyEditorModule.cpp
#include "MyEdMode.h"
#include "EditorModeRegistry.h"

void FMyEditorModule::StartupModule()
{
    FEditorModeRegistry::Get().RegisterMode<FMyEdMode>(
        FMyEdMode::EM_MyEdModeId,
        FText::FromString("My Custom Mode"),
        FSlateIcon(),
        true
    );
}
```

### 可视化：编辑器模式视口接管

```mermaid
graph TD
    A[编辑器视口] --> B{FMyEdMode 是否激活？}
    B -- 是 --> C[每帧调用 FMyEdMode::Render()]
    C --> D[自定义绘图（例如，圆、线）出现在视口中]
    B -- 否 --> E[默认视口渲染]

    F[用户按键] --> G{FMyEdMode 是否激活？}
    G -- 是 --> H[调用 FMyEdMode::InputKey()]
    H --> I[执行自定义输入逻辑]
```

## 自定义资产类型 (UFactory)

### 概念
要创建一个可以在内容浏览器中创建和管理的全新资产类型，您需要创建一个 `UFactory`。工厂类告诉编辑器如何创建您的自定义资产的新实例。

### 代码示例：自定义数据资产的工厂

首先，定义您的自定义资产：
```cpp
// MyCustomAsset.h
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "MyCustomAsset.generated.h"

UCLASS()
class YOURPROJECT_API UMyCustomAsset : public UDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, Category = "Custom Data")
    FString Description;

    UPROPERTY(EditAnywhere, Category = "Custom Data")
    int32 Value;
};
```

接下来，创建工厂：
```cpp
// MyCustomAssetFactory.h
#pragma once

#include "CoreMinimal.h"
#include "Factories/Factory.h"
#include "MyCustomAssetFactory.generated.h"

UCLASS()
class YOURPROJECTEDITOR_API UMyCustomAssetFactory : public UFactory
{
    GENERATED_BODY()

public:
    UMyCustomAssetFactory();

    // UFactory 接口
    virtual UObject* FactoryCreateNew(UClass* InClass, UObject* InParent, FName InName, EObjectFlags Flags, UObject* Context, FFeedbackContext* Warn) override;
};
```

```cpp
// MyCustomAssetFactory.cpp
#include "MyCustomAssetFactory.h"
#include "MyCustomAsset.h"

UMyCustomAssetFactory::UMyCustomAssetFactory()
{
    bCreateNew = true;
    bEditAfterNew = true;
    SupportedClass = UMyCustomAsset::StaticClass();
}

UObject* UMyCustomAssetFactory::FactoryCreateNew(UClass* InClass, UObject* InParent, FName InName, EObjectFlags Flags, UObject* Context, FFeedbackContext* Warn)
{
    return NewObject<UMyCustomAsset>(InParent, InClass, InName, Flags);
}
```

### 可视化：自定义资产创建流程

```mermaid
flowchart TD
    A[用户在内容浏览器中右键单击] --> B[选择“我的自定义资产”]
    B --> C{编辑器找到 UMyCustomAssetFactory}
    C --> D[调用 FactoryCreateNew()]
    D --> E[创建新的 UMyCustomAsset 对象]
    E --> F[新资产出现在内容浏览器中]
```
