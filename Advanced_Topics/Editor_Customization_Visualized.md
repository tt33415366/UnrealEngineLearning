# Editor Customization Visualized

This guide explains how to extend the Unreal Editor with custom tools and UI using C++. Customizing the editor is a powerful way to improve workflow, create game-specific tools, and streamline content creation for your team.

**Note:** All editor customization code must be placed in an **Editor-only module**. This is a module of type `Editor` in your `.uproject` or `.uplugin` file, which ensures it is not compiled into your final packaged game.

## Table of Contents
- [Custom Asset Actions](#custom-asset-actions)
- [Details Panel Customization (IDetailCustomization)](#details-panel-customization-idetailcustomization)
- [Custom Editor Modes (FEdMode)](#custom-editor-modes-fedmode)
- [Custom Asset Types (UFactory)](#custom-asset-types-ufactory)

## Custom Asset Actions

### Concept
Custom asset actions allow you to add new options to the right-click context menu of assets in the Content Browser. This is one of the simplest and most common ways to add asset-specific utilities, such as custom validation, data processing, or batch operations.

To do this, you create a class that inherits from `FAssetTypeActions_Base` and register it with the `FAssetToolsModule`.

### Code Example: Custom Action for a Data Asset

```cpp
// MyDataAssetActions.h
#pragma once

#include "CoreMinimal.h"
#include "AssetTypeActions_Base.h"
#include "MyDataAsset.h"

class FMyDataAssetActions : public FAssetTypeActions_Base
{
public:
    // IAssetTypeActions Implementation
    virtual FText GetName() const override { return FText::FromString("My Data Asset"); }
    virtual FColor GetTypeColor() const override { return FColor::Cyan; }
    virtual UClass* GetSupportedClass() const override { return UMyDataAsset::StaticClass(); }
    virtual uint32 GetCategories() override { return EAssetTypeCategories::Misc; }

    // Add custom actions to the context menu
    virtual void GetActions(const TArray<UObject*>& InObjects, FMenuBuilder& MenuBuilder) override;

private:
    // The function to be executed by our custom action
    void ExecuteCustomAction(TArray<TWeakObjectPtr<UMyDataAsset>> InDataAssets);
};
```

```cpp
// MyDataAssetActions.cpp
#include "MyDataAssetActions.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"

void FMyDataAssetActions::GetActions(const TArray<UObject*>& InObjects, FMenuBuilder& MenuBuilder)
{
    // Convert selected objects to our specific data asset type
    TArray<TWeakObjectPtr<UMyDataAsset>> DataAssets;
    for (UObject* Obj : InObjects)
    {
        if (UMyDataAsset* DataAsset = Cast<UMyDataAsset>(Obj))
        {
            DataAssets.Add(DataAsset);
        }
    }

    // Add a new section to the menu
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
            // ... perform your logic here ...
        }
    }
}
```

**Registering the Action:** In your editor module's `StartupModule` function:

```cpp
// MyEditorModule.cpp
#include "AssetToolsModule.h"
#include "MyDataAssetActions.h"

void FMyEditorModule::StartupModule()
{
    IAssetTools& AssetTools = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools").Get();
    TSharedRef<IAssetTypeActions> Action = MakeShareable(new FMyDataAssetActions);
    AssetTools.RegisterAssetTypeActions(Action);
    // Remember to store the action so you can unregister it in ShutdownModule
    CreatedAssetTypeActions.Add(Action);
}
```

### Visualization: Custom Asset Action Flow

```mermaid
graph TD
    A[Right-click on UMyDataAsset in Content Browser] --> B{GetActions() called on FMyDataAssetActions}
    B --> C[MenuBuilder.AddMenuEntry() adds a new UI button]
    C --> D[User clicks "Perform Custom Action"]
    D --> E[FUIAction executes ExecuteCustomAction()]
    E --> F[Custom logic runs on the selected assets]
```

## Details Panel Customization (IDetailCustomization)

### Concept
Details panel customization allows you to completely change how a class's properties are displayed in the Details panel. This is essential for creating user-friendly interfaces for complex data, replacing raw data fields with intuitive buttons, sliders, or custom Slate widgets.

You achieve this by creating a class that inherits from `IDetailCustomization` and registering it with the `FPropertyEditorModule`.

### Code Example: Customizing a Details Panel

```cpp
// MyActorDetailsCustomization.h
#pragma once

#include "CoreMinimal.h"
#include "IDetailCustomization.h"

class FMyActorDetailsCustomization : public IDetailCustomization
{
public:
    // IDetailCustomization interface
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
    // Get the object being customized
    TArray<TWeakObjectPtr<UObject>> Objects;
    DetailBuilder.GetObjectsBeingCustomized(Objects);
    if (Objects.Num() > 0)
    {
        MyActor = Cast<AMyActor>(Objects[0].Get());
    }

    // Create a new category
    IDetailCategoryBuilder& MyCategory = DetailBuilder.EditCategory("My Custom Category", FText::GetEmpty(), ECategoryPriority::Important);

    // Add a custom button to the category
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

**Registering the Customization:** In your editor module's `StartupModule` function:

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

### Visualization: Details Panel Customization

```mermaid
graph TD
    subgraph Default Details Panel
        A[Category: Transform]
        B[Category: MyActor]
        C[MyInt: 10]
        D[MyFloat: 3.14]
    end

    subgraph Customized Details Panel
        E[Category: Transform]
        F[Category: My Custom Category]
        G[Button: "Execute My Logic"]
    end

    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#fcf,stroke:#333,stroke-width:2px
```

## Custom Editor Modes (FEdMode)

### Concept
Custom Editor Modes (`FEdMode`) are the most powerful way to customize the editor. They allow you to take over the editor viewport, providing custom rendering, input handling (mouse clicks, keyboard presses), and custom tools or gizmos. This is how the built-in modes like Foliage, Landscape, and Mesh Painting are implemented.

### Code Example: A Simple Drawing Editor Mode

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

    // FEdMode interface
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
    // Draw a circle at the world origin
    DrawCircle(PDI, FVector::ZeroVector, FVector(1,0,0), FVector(0,1,0), FColor::Yellow, 100.0f, 32, SDPG_World);
}

bool FMyEdMode::InputKey(FEditorViewportClient* ViewportClient, FViewport* Viewport, FKey Key, EInputEvent Event)
{
    if (Key == EKeys::LeftMouseButton && Event == IE_Pressed)
    {
        UE_LOG(LogTemp, Warning, TEXT("Left mouse button pressed in MyEdMode."));
        return true; // We handled this input
    }
    return false;
}
```

**Registering the Mode:** In your editor module's `StartupModule` function:

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

### Visualization: Editor Mode Viewport Takeover

```mermaid
graph TD
    A[Editor Viewport] --> B{Is FMyEdMode Active?}
    B -- Yes --> C[FMyEdMode::Render() is called every frame]
    C --> D[Custom drawing (e.g., circles, lines) appears in the viewport]
    B -- No --> E[Default viewport rendering]

    F[User presses key] --> G{Is FMyEdMode Active?}
    G -- Yes --> H[FMyEdMode::InputKey() is called]
    H --> I[Custom input logic is executed]
```

## Custom Asset Types (UFactory)

### Concept
To create a completely new type of asset that can be created and managed in the Content Browser, you need to create a `UFactory`. The factory class tells the editor how to create a new instance of your custom asset.

### Code Example: Factory for a Custom Data Asset

First, define your custom asset:
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

Next, create the factory:
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

    // UFactory interface
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

### Visualization: Custom Asset Creation Flow

```mermaid
flowchart TD
    A[User right-clicks in Content Browser] --> B[Selects "My Custom Asset"]
    B --> C{Editor finds UMyCustomAssetFactory}
    C --> D[FactoryCreateNew() is called]
    D --> E[New UMyCustomAsset object is created]
    E --> F[New asset appears in Content Browser]
```
