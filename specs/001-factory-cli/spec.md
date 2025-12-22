# Spec: Factory Core CLI

Dossier: DOS-20251222-factory-cli
Constitution: constitution.md
**Status**: Draft  
**Owner**: Nexus  
**Epic**: Factory Core CLI (Sprint 1)

## 1. Intent
Replace ad-hoc scripts with a unified `codemonkeys` CLI tool to provide a consistent control plane for the autonomous factory. This "spine" will wrap existing functionality and enable consistent invocation by both humans and agents.

## 2. User Stories
- **As an Operator**, I want to type `codemonkeys dash serve` to launch the dashboard without remembering python paths.
- **As an Operator**, I want to run `codemonkeys run <product>` to generate a run report and artifacts.
- **As an Operator**, I want to run `codemonkeys silverback --all` to validate the entire fleet.
- **As Nexus**, I want to execute `codemonkeys nexus exec` to process my outbox decisions reliably.
- **As a Developer**, I want the CLI to be installable via `pip install -e .` so it's available in my shell.

## 3. Functional Requirements
1.  **Command Structure**:
    - `codemonkeys dash serve [--port]`
    - `codemonkeys run <product_id> [--path]`
    - `codemonkeys silverback [--all] [--nexus] [--target <file>]`
    - `codemonkeys nexus exec [--dry-run]`
    - `codemonkeys fleet list` (optional but helpful)
2.  **Implementation**:
    - Python package `codemonkeys` (or similar name)
    - `pyproject.toml` or `setup.py` for installation
    - Entry point `codemonkeys`
    - Wraps `scripts/generate_run_report.py`, `scripts/silverback_validate.py`, `scripts/nexus_executor.py`
3.  **Output**:
    - Structured stdout/stderr
    - Consistent exit codes (0=success, non-zero=failure)

## 4. Acceptance Criteria
1.  `codemonkeys --help` displays all available commands.
2.  `codemonkeys run codemonkeys-dash` produces a valid `last_run.json`.
3.  `codemonkeys silverback --all` runs validation and returns correct exit code.
4.  `codemonkeys nexus exec --dry-run` executes the nexus logic.
5.  CI can install and use the CLI for the build steps.

## 5. Owner & Authority
- **Feature Owner**: Nexus Agent
- **Governance**: Must inherit all rules from `constitution.md`.
- **Approval**: Human Operator for initial spec; Nexus for implementation details.

## 6. Budget & Stop Conditions
- **Budget**: 500 tokens / 5 minutes per run (inherited from Dash default).
- **Stop Condition**: Kill switch enabled in `last_run.json`.
- **Constraint**: CLI *must not* execute run logic if kill switch is ON.

## 7. Constraints & Non-goals
- **Constraint**: Must verify schemas for all outputs.
- **Constraint**: Local-first only (no cloud deps).
- **Non-goal**: Replacing the actual logic scripts (just wrapping them for now).

## 8. Evidence Plan
- **Artifacts**: `last_run.json` updated by `codemonkeys run`.
- **Logs**: `pytest_output.log`, `silverback_output.log`.
- **Screenshots**: Dash showing updated products.

## 9. Traceability Map
- `specs/001-factory-cli/spec.md` -> `src/codemonkeys/cli.py`
- `specs/001-factory-cli/spec.md` -> `src/codemonkeys/commands/*.py`

