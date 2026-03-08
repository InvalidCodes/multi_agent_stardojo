1. Title

StarDojo Multi-Agent System: A Manager–Worker Architecture for Long-Horizon Control in Stardew Valley

2. Problem

单 agent 在 farming / combat / inventory 同时出现时会 context overload，导致 latency 上升、成功率下降、决策混乱。

NeurIPS_2024__1_

3. Goal

把单体 agent 改成 Manager–Worker MAS，用 shared state 和 LangGraph router 把高层决策与低层执行拆开，提高长时程任务表现。

NeurIPS_2024__1_

4. Method

Shared state：Time / Energy / Threats / Inventory / Map / Goal

Manager / Router：按状态分配 worker

Workers：

Steward：farm / forage

Adventurer：mine / combat

Socialite：NPC interaction

Logistician：resource management 

NeurIPS_2024__1_

5. Deliverables

MAS codebase

demo video

minimal evaluation against baseline 

NeurIPS_2024__1_

6. 24-hour Scope

实现完整架构和两个核心 worker，其他 worker 先做接口与占位逻辑；重点验证 routing 和 autonomous switching。