# Directive: Persistence & Continuity

## Purpose
To ensure that all strategic momentum, decisions, and task progress are preserved across conversation sessions, even if the individual chat thread history is lost or filtered.

## 1. Thread Anchoring
*   **Mandatory Task List**: Every conversation thread MUST begin or end by updating a `task.md` file in the workspace root.
*   **State Verification**: Before executing new complex tasks, the agent must verify the current "State of Play" by reading the `task.md`.

## 2. Workspace Orchestrator
*   **The Source of Truth**: Every workspace must maintain a `directives/ORCHESTRATOR.md` (or similar, e.g., `FUNDRAISE_ORCHESTRATOR.md`).
*   **Content**: This file acts as the "Master Memory," recording:
    *   Active Strategic Decisions (e.g., agreed commission rates, target criteria).
    *   Project Roadmap & Milestones.
    *   Lessons Learned (what messaging failed, what intro worked).
*   **Updates**: This file should be updated at the end of every high-stakes strategic session.

## 3. Context Restoration
*   **Starting New Threads**: When starting a conversation where the previous history is not visible, the user or agent should "instantiate" the session by reading the `ORCHESTRATOR.md` and `task.md`.
*   **Cross-Workspace Continuity**: If working across workspaces (e.g., GTM and FUNDRAISE), the agent must explicitly state which workspace context it is pulling from.
