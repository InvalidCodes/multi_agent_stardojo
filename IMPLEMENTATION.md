# StarDojo Multi-Agent System (MAS) Implementation README

## 1. Overview

This repository contains a 24-hour implementation of a **Manager–Worker Multi-Agent System (MAS)** built on top of the original StarDojo single-agent pipeline.

The goal of this implementation is to preserve the existing execution stack while introducing a lightweight coordination layer that:
- extracts a compact shared state from environment observations,
- routes control to specialized workers,
- reuses the existing action/skill execution pipeline,
- supports demo and evaluation for a course project setting.

This implementation focuses on **minimum viable multi-agent orchestration** rather than full end-to-end replacement of the original architecture.

---

## 2. Design Goal

The original baseline follows a monolithic single-agent flow: one agent receives processed observations, plans actions, and executes them through the existing skill system.

This implementation introduces a **Manager–Worker abstraction** to address the following problem:

- a single agent must reason about farming, combat, and resource management at once;
- this leads to context interference and makes long-horizon decision-making harder;
- specialized workers can reduce decision scope, while a manager coordinates which worker should act.

The current implementation is intentionally lightweight:
- **Manager / Router** is deterministic and rule-based;
- **Steward** and **Adventurer** are functional workers;
- **Socialite** and **Logistician** are scaffolds for future extension.

---

## 3. What Is Implemented

### 3.1 Core MAS Layer
The system includes the following conceptual components:

- **SharedState**  
  A normalized state object built from environment observations. It summarizes the information needed for routing and logging.

- **Router**  
  A rule-based policy that selects which worker should act next.

- **ManagerRouter**  
  The orchestration layer that:
  1. builds shared state,
  2. selects a worker,
  3. calls that worker,
  4. records routing decisions and logs.

- **Worker interface**  
  A shared interface for all worker modules so they can be invoked in a uniform way.

### 3.2 Real Workers
Two workers are meaningfully implemented:

- **Steward**
  - farm-oriented behavior
  - simple fallback logic for low-energy / late-night return-home behavior
  - basic safe actions for non-combat contexts

- **Adventurer**
  - combat / mine-oriented behavior
  - reuses existing skill expressions
  - uses simple attack/mining actions depending on context
  - logs routing and action choices

### 3.3 Placeholder Workers
Two workers are scaffolded but not fully implemented:

- **Socialite**
  - placeholder only
  - currently logs invocation and returns no meaningful task behavior

- **Logistician**
  - placeholder only
  - currently logs invocation and returns no meaningful task behavior

These placeholders exist to complete the architecture and provide extension points for later development.

---

## 4. Architecture

## 4.1 High-Level Flow

The MAS flow is:

1. Environment produces processed observation
2. SharedState is built from observation
3. Router selects a worker
4. ManagerRouter invokes the selected worker
5. Worker returns a list of skill expressions / actions
6. Existing execution pipeline executes those actions
7. Logs record state, worker selection, and action output

Conceptually:

```text
Observation
   ↓
SharedState Builder
   ↓
Router
   ↓
ManagerRouter
   ↓
Selected Worker
   ↓
Skill Expressions / Actions
   ↓
Existing Skill Execution Pipeline