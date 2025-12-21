# Spec Template Sufficiency Audit

Date: 2025-12-21
Target: `.specify/templates/spec-template.md`
Question: Is **Constitution + Spec** sufficient for autonomous execution?

## Summary
Your current spec template is a strong start for *functional* development:
- prioritized user stories
- test scenarios per story
- edge cases
- functional requirements
- success criteria / measurable outcomes

However, for **fully autonomous** operation (with Nexus + swarms), the spec must also carry:
- explicit *constraints* and *non-goals*
- *non-functional* requirements (security, performance, reliability, privacy)
- *failure-mode expectations*
- an *evidence plan* (what artifacts prove claims)
- a lightweight *traceability hook* so the system can map req → tests → code → docs → evidence.

Without those, the swarm will either:
- guess (unsafe), or
- overbuild (scope creep), or
- declare “done” without the right proofs.

## What exists today (good)
Headings present:
- User Scenarios & Testing (prioritized stories + scenario tables)
- Edge Cases
- Requirements (Functional)
- Key Entities (data modeling hook)
- Success Criteria (Measurable outcomes)

## What is missing for autonomy (must add)
### 1) Constraints & Non-goals (merge-blocking)
Add a mandatory section:
- Constraints: local-first, cost budget, forbidden deps, compatibility promises, allowed scope.
- Non-goals: what NOT to build now.

### 2) Invariants & Failure Modes (required when applicable)
Add:
- Invariants (“must always be true”)
- Failure modes + expected behavior (timeouts, retries, partial failure, cancellation)

### 3) Security/Privacy posture (required when applicable)
Add:
- threat assumptions
- sensitive data handling
- auth/permissions (if any)
- secret rules

### 4) Performance/Resource envelope (required when relevant)
Add:
- latency/throughput budgets
- memory/disk bounds
- what constitutes regression

### 5) Evidence Plan (hard requirement)
Add:
- tests to run
- artifacts to attach (logs/bench outputs/sarif, etc.)
- “Observed vs Derived” claim labeling requirement

### 6) Traceability stub (minimal)
Add a short table:
- Requirement → Planned test(s) → doc(s) → evidence artifact(s)
(This can start empty but must be filled before “done”.)

## Proposed template patch (minimal additions)
Insert after Requirements / before Success Criteria:

1. **Constraints & Non-goals** *(mandatory)*
2. **Invariants & Failure Modes** *(mandatory when applicable)*
3. **Security & Privacy** *(mandatory when applicable)*
4. **Performance & Resource Bounds** *(mandatory when applicable)*
5. **Evidence Plan** *(mandatory)*
6. **Traceability Map** *(mandatory before ship)*

## Conclusion
- Constitution + Spec CAN be sufficient **if** the spec template is upgraded to include the missing autonomy-critical sections above.
- If Science Monkeys originate the product, also require a separate **Design Dossier** (HANDOFF_CONTRACT.md) before writing the production spec.
