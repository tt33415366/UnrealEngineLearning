# 游戏性能力系统 (GAS) - 可视化

本文档提供了对虚幻引擎游戏性能力系统 (GAS) 的全面、可视化摘要，详细介绍了其核心组件、它们之间的交互以及高级概念。

## 摘要

游戏性能力系统是一个高度灵活且功能强大的框架，用于创建角色能力、属性和状态效果。对于许多类型的游戏，尤其是 RPG 和 MOBA，它是一个复杂但必不可少的系统，因为它处理从简单动作到复杂的、网络化的能力交互的所有内容。GAS 在设计时考虑了多人游戏，为跨客户端和服务器复制能力、属性和效果提供了强大的支持。

### 核心概念

GAS 建立在几个协同工作的关键概念之上，以创建一个健壮且可扩展的系统：

*   **能力系统组件 (ASC):** 这是 GAS 的核心枢纽。它是一个 `UActorComponent`，您可以将其添加到您的角色（或 `PlayerState` 以用于持久多人游戏数据）中。ASC 拥有能力、管理属性、处理所有游戏性效果，并处理这些元素的网络复制。

*   **游戏性能力 (GA):** 这是能力的“做什么”。它定义了角色可以执行的单个动作的逻辑，例如施法、挥剑或激活被动增益。GA 可以有消耗、冷却时间并触发各种效果。它们可以在 C++ 或蓝图中实现，并具有明确的生命周期（激活、执行、结束）。

*   **属性集 (Attribute Set):** 这包含角色的数值数据，例如 `Health`（生命值）、`Mana`（法力值）、`Stamina`（耐力）、`AttackPower`（攻击力）或 `MovementSpeed`（移动速度）。它是一个包含一系列 `FGameplayAttribute` 属性的 `UObject`。属性集跟踪基础值和当前值，允许进行临时修改（增益/减益）而不改变基础值。ASC 负责管理和复制属性集。

*   **游戏性效果 (GE):** 这是应用对 Actor 属性或游戏性标签更改的主要机制。GE 定义了属性 *如何* 被修改。它们可以是：
    *   **即时 (Instant):** 立即应用一次（例如，即时伤害、治疗）。
    *   **持续 (Duration):** 在一段时间内应用（例如，中毒效果、临时增益）。
    *   **无限 (Infinite):** 永久应用直到移除（例如，永久属性提升、持续减益）。
    GE 也用于应用能力的消耗和冷却时间。GE 的复杂计算可以通过 `UGameplayEffectExecutionCalculation` 或 `UGameplayModMagnitudeCalculation` 类处理。

*   **游戏性标签 (Gameplay Tags):** 这些是分层的、基于名称的标签（例如 `State.Stunned`、`Ability.Cooldown.Fireball`、`Effect.Buff.Speed`），在 GAS 中广泛用于过滤数据、分类能力、效果和其他游戏性元素。它们对于管理和查询游戏性状态非常高效，并有助于减少对硬引用的需求。

*   **游戏性提示 (Gameplay Cues):** 这些用于实现视觉效果，例如播放音效、粒子效果或生成 UI 小部件（例如，伤害数字）。它们通常是不可靠的多播，并且默认情况下不会在专用服务器上触发，这使得它们在不影响游戏性逻辑的情况下高效地提供视觉和音频反馈。

*   **能力任务 (Ability Tasks):** 这些是与游戏性能力一起使用的专用 `GameplayTask` 类。与立即执行的标准蓝图节点不同，能力任务可以跟踪其状态（非活动、进行中、完成）并在执行期间触发事件，从而实现更复杂的异步能力逻辑（例如 `WaitTargetData`、`WaitDelay`）。

*   **预测 (Prediction):** GAS 在设计时考虑了多人游戏的客户端预测。这允许客户端在本地模拟能力效果，减少感知延迟并提供更流畅的玩家体验，最终由服务器权威。

*   **目标选择 (Targeting):** GAS 提供了能力选择目标的机制，从简单的自我目标选择到复杂的范围效果或基于投射物的目标选择系统。

## 可视化

### 1. 核心 GAS 组件关系

此图显示了 GAS 的主要组件如何相互交互。

```mermaid
graph TD
    A["能力系统组件 (ASC)<br><i>管理能力、属性、效果</i>"] --> B("拥有并激活游戏性能力");
    A --> C("拥有并管理属性集");
    A --> D("应用并追踪游戏性效果");
    A --> E("管理游戏性标签");

    subgraph "能力逻辑"
        B --> F{"游戏性能力<br><i>(GA) - “做什么”</i>"};
    end

    subgraph "角色统计"
        C --> G["属性集<br><i>(例如, 生命值, 法力值, 耐力)</i>"];
    end

    subgraph "属性修改和状态改变"
        D --> H["游戏性效果<br><i>(GE) - “如何做”</i>"];
    end

    subgraph "视觉反馈"
        I["游戏性提示<br><i>(视觉效果, 音效)</i>"];
    end

    subgraph "异步逻辑"
        J["能力任务<br><i>(异步操作)</i>"];
    end

    F -- "应用一个..." --> H;
    H -- "修改一个..." --> G;
    F -- "触发一个..." --> I;
    F -- "使用..." --> J;
    F -- "使用..." --> E;
    H -- "使用..." --> E;
    G -- "可能受...影响" --> E;

    style A fill:#e0f7fa,stroke:#00bcd4,stroke-width:2px
    style F fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    style G fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    style H fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    style E fill:#ffebee,stroke:#f44336,stroke-width:2px
    style I fill:#e1f5fe,stroke:#2196f3,stroke-width:2px
    style J fill:#e0f2f7,stroke:#00acc1,stroke-width:2px
```

### 2. 简化的能力激活流程和效果

此序列图说明了激活能力、应用其消耗和触发其效果的基本步骤。

```mermaid
sequenceDiagram
    participant "玩家输入"
    participant "能力系统组件" as ASC
    participant "游戏性能力" as GA
    participant "目标Actor"

    玩家输入->>ASC: 1. TryActivateAbility(能力标签)
    ASC->>GA: 2. CanActivateAbility?<br><i>(通过 GE 和游戏性标签检查消耗、冷却)</i>
    GA-->>ASC: 3. 是/否 (基于检查)
    alt 如果 CanActivate 为是
        ASC->>GA: 4. ActivateAbility()
        GA->>ASC: 5. 应用消耗 GE (例如, 法力值, 耐力)
        GA->>ASC: 6. 应用冷却 GE
        GA->>GA: 7. 执行能力逻辑<br><i>(例如, 使用能力任务)</i>
        GA->>目标Actor: 8. 应用游戏性效果 (例如, 伤害, 增益)
        GA->>ASC: 9. 触发游戏性提示 (例如, 粒子, 音效)
        GA->>ASC: 10. EndAbility()
    else 如果 CanActivate 为否
        ASC-->>玩家输入: 4. 能力激活失败
    end
```