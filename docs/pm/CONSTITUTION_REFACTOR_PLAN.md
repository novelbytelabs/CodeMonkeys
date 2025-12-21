# Constitution Refactor Plan

**Status**: Proposal
**Target**: Prepare for Constitution v1.0

## 1. Objective
Refactor the single monolithic `constitution.md` into a modular structure to support:
- Multiple products (Science, Code, etc.) with different needs.
- A unifying "Universal" law for all agents.
- Clear autonomy boundaries.

## 2. Proposed Structure

### A. Universal Constitution (`constitution.md` - Root)
Applies to **Nexus**, **Science Monkeys**, and **Code Monkeys**.
- **Core Values**: Truth, Evidence, Safety.
- **Universal Rights**: User overrides, Kill Switches.
- **Banana Economy**: Global resource limits.

### B. Product-Line Constitutions (Appendices/Imports)
- **Code Monkeys**: SDD, TDD, CI strictness, Release gates.
- **Science Monkeys**: Exploration bounds, Experiment logging, Hypothesis tracking.
- **Nexus**: Decision authority, Budget allocation, Escalation triggers.

### C. Domain-Specific Appendices
- **Language Rules**: Rust (Safety), Python (Type hints).
- **Security Policy**: Secret handling, dependency scanning.

## 3. New Section: Autonomy Governance
To be added to the Universal Constitution.

**Principles**:
1.  **Nexus cannot bypass gates.**
    - Even the Product Owner is subject to verification proofs.
2.  **Budgets are hard limits.**
    - If funds/tokens/time run out, operation halts.
    - No "credit" without human override.
3.  **Stop Rules.**
    - Trigger immediate "safe stop" (clean shutdown).
    - Conditions: Uncertainty, unexpected errors, scope explosion.
4.  **Evidence Requirements.**
    - No claim is accepted without an Evidence Pack.
    - "Bootstrap Proof" allowed for MVP (stubbed but structured).
5.  **Kill Switches.**
    - Hardware/file-based override must exist.

## 4. Migration Strategy
1.  Audit current `constitution.md`.
2.  Tag rules as [UNIVERSAL] or [SPECIFIC].
3.  Extract [SPECIFIC] rules to sub-documents.
4.  Write "Autonomy Governance" section in Root.
