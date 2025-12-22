# Code Monkeys Domain Context (DDD)
> *The Ubiquitous Language of the Autonomous Fleet*

## 1. Domain Entities (The Nouns)

### The Fleet
*   **Repo**: A single git repository managed by Code Monkeys.
*   **Campaign**: A coordinated set of actions (e.g., "Upgrade React") applied across multiple Repos.
*   **Wave**: A subset of Repos targeted in a specific phase of a Campaign (Canary, Early, Fleet).

### The Governance
*   **Rule**: A specific, machine-enforceable constraint (e.g., `no-secrets.yaml`).
*   **Violation**: A detected instance of a Rule being broken.
*   **Remediation**: The specific code change proposed to fix a Violation.
*   **Verdict**: The Justice Agent's binary decision (PASS/BLOCK) on a proposed Remediation.

### The Agents
*   **Oracle**: The read-only observer that parses code and logs.
*   **Healer**: The active builder that proposes Remediations.
*   **Justice**: The adversarial judge that rejects Violations.
*   **Conductor**: The orchestrator that manages Campaigns and Waves.

---

## 2. Bounded Contexts (The Boundaries)

### Governance Context
*   **In Scope:** Rules, Verdicts, Constitution.
*   **Out of Scope:** Implementation details of *how* a fix is made. Justice only cares *that* it complies.

### Orchestration Context
*   **In Scope:** Scheduling, PR lifecycle, Rollout Phases, Rate Limiting.
*   **Out of Scope:** Code parsing. Conductor only knows "Violation Found," not "Line 42 has a bug."

### Healing Context
*   **In Scope:** Syntax trees, LLM prompts, Diff generation.
*   **Out of Scope:** Policy decisions. Healer tries to fix everything; Justice decides what is allowed.

---

## 3. Business Intent (The Why)

*   **Primary Goal:** "Multiply Developer Leverage."
    *   *Metric:* Reduction in manual time spent on cross-repo maintenance.
*   **Secondary Goal:** "Zero Regression."
    *   *Metric:* No automated PR causes a rollback.
*   **Constraint:** "Local Sovereignty."
    *   *Rule:* All core loops must be runnable on a developer laptop without cloud dependency.

---

## 4. Supply Chain (The Context Integration)

### System Inputs
*   **Codebase:** The source of truth for current state.
*   **CI Logs:** The "pain signals" of the system.
*   **Constitution:** The negative constraints (what NOT to do).
*   **User Commands:** The positive intent (what TO do).

### System Outputs
*   **PRs:** The primary unit of work.
*   **Artifacts:** Evidence of decision making (logs, artifacts).
*   **Signals:** Notifications to the human Admiral.
