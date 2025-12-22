# Spec: release-gate

Dossier: DOS-20251222-release-gate
Constitution: constitution.md
Status: Draft
Owner: nexus
Epic: release-gate

## 1. Intent
Code can currently be released without verification, violating Article I of the Constitution.
Implementing a strict Release Gate will prevent non-compliant code from leaving the Factory.

## 2. User Stories
- **As a Operator**, I want `codemonkeys ship` to fail if my environment is dirty, so I don't release uncommitted code.
- **As a Product Owner**, I want release tags to be blocked unless Silverback validation passes, so I know the Release is Constitutional.

## 3. Functional Requirements
1.  **Preflight Script**: `scripts/preflight_check.py` checks git status and runs `codemonkeys silverback --all`.
2.  **Ship Command**: `codemonkeys ship <version>` executes preflight before tagging.
3.  **Gate Logic**: Abort if preflight fails.
4.  **Bypass**: `--force` option reserved for overrides (future).

## 4. Acceptance Criteria
1. Proof 1: `codemonkeys ship` fails if git is dirty (Verified by `test_ship_preflight_fail_git_dirty`).
2. Proof 2: `codemonkeys ship` fails if Silverback fails (Verified by preflight invocation logic).
3. Proof 3: `codemonkeys ship` succeeds if preflight passes (Verified by `test_ship_preflight_pass`).

## 5. Owner & Authority
- **Feature Owner**: nexus
- **Governance**: Inherits from Dossier DOS-20251222-release-gate.
- **Approval**: Human Operator.

## 6. Budget & Stop Conditions
- **Budget**: Standard.
- **Stop Condition**: Kill switch.

## 7. Constraints & Non-goals
**Non-goals**:
- GitHub Actions pipeline (Sprint 5)

## 8. Evidence Plan
- **Artifacts**: Standard run artifacts.

## 9. Traceability Map
- `docs/dossiers/DOS-20251222-release-gate.md` -> `specs/004-release-gate/spec.md`
