# Directive: System Initialization & Health

## Goal
Ensure the 3-layer agentic architecture is operational, directories are present, and the orchestration layer (Layer 2) has clear instructions for common tasks.

## Inputs
- Workspace root path.
- Existing `AGENTS.md` rules.

## Tools/Scripts
- `execution/verify_structure.py`: Checks for existence of `directives/`, `execution/`, and `.tmp/`.

## Outputs
- Status report on system readiness.

## Edge Cases
- Missing `.env` file: Orchestrator should alert the user if API keys are needed for execution.
- Read-only filesystem: Orchestrator should report permission issues.

## Instructions
1. Run `execution/verify_structure.py`.
2. Check if `.env` exists in the root.
3. Verify that `directives/` contains at least one functional SOP.
4. If everything is green, report "System Primed."
