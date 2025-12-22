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

## How to Add a Decision

1. Create new entry with next DEC-NNNN number
2. Fill all five fields
3. Commit with message `docs: add DEC-NNNN <title>`
