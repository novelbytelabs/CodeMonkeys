# Code Monkeys — Decisions Log

**Doc ID**: PM-DECISIONS  
**Purpose**: Append-only log of major decisions to prevent strategy drift

---

## Format

Each entry follows:

```
### DEC-NNNN: <Short Title>
**Date**: YYYY-MM-DD  
**Decision**: What was decided  
**Why**: Rationale  
**Alternatives Rejected**: What we didn't do  
**Consequences**: What this implies going forward  
```

---

## Decisions

### DEC-0001: Governance-First Development
**Date**: 2025-12-21  
**Decision**: Governance rules (constitution, autonomy governance) are merge gates, not guidelines.  
**Why**: Unbounded autonomy leads to drift and unverifiable claims. We need executable enforcement.  
**Alternatives Rejected**: Advisory-only governance (too weak), human-in-loop for every action (doesn't scale).  
**Consequences**: Must build Silverback validator, CI enforcement, and schema contracts.

---

### DEC-0002: Evidence-First Artifacts
**Date**: 2025-12-21  
**Decision**: All claims must be backed by schema-valid artifacts (logs, JSON, screenshots).  
**Why**: Narration is not verifiable. Artifacts are the source of truth.  
**Alternatives Rejected**: Trust agent self-reports without validation.  
**Consequences**: Dash becomes evidence viewer. Report generator produces validated artifacts.

---

### DEC-0003: Branching Workflow (main → dev → feature/*)
**Date**: 2025-12-21  
**Decision**: main is stable (PRs only), dev is integration, feature/* is work.  
**Why**: Prevents accidental commits to stable branch. Enables batched releases.  
**Alternatives Rejected**: Trunk-based with direct commits (too risky for solo operator).  
**Consequences**: All work requires feature branches and PRs.

---

### DEC-0004: Nexus as Artifact-Driven Command Queue
**Date**: 2025-12-21  
**Decision**: Nexus uses inbox/outbox JSON artifacts, not live API calls.  
**Why**: Local-first, auditable, reproducible. Artifacts can be validated by Silverback.  
**Alternatives Rejected**: REST API for decisions (adds complexity, less auditable).  
**Consequences**: nexus_executor.py applies decisions from outbox to run artifacts.

---

### DEC-0005: Naming — Arqon/ArqonShip Forbidden
**Date**: 2025-12-22  
**Decision**: "Arqon" and "ArqonShip" are forbidden in all new code and documentation. The project identity is "Code Monkeys" with CLI command `codemonkeys`.  
**Why**: ArqonShip was the legacy name for a different project (HPO optimizer). This repo hosts the Code Monkeys Factory, not ArqonShip.  
**Alternatives Rejected**: Keeping "Arqon" branding (confusing), renaming the repo immediately (too disruptive for current sprint).  
**Consequences**: All docs updated. Host repo folder remains `/ArqonShip` temporarily until a clean break is made. Final publish target is `codemonkeys/` repo.

---

### DEC-0006: Warnings Treated as Errors on Main
**Date**: 2025-12-22  
**Decision**: Silverback warnings are treated as errors on `main` branch. CI must fail if warnings > 0 on `main`.  
**Why**: We achieved 0 warnings with v0.4.1. Keeping the signal strong prevents governance drift from creeping back.  
**Alternatives Rejected**: Warnings allowed on main (too weak), only count specific warning types (adds complexity).  
**Consequences**: All specs must have complete sections before merge to main. CI enforces `codemonkeys silverback --all` with warning-as-error mode.

---

## How to Add a Decision

1. Create new entry with next DEC-NNNN number
2. Fill all five fields
3. Commit with message `docs: add DEC-NNNN <title>`
