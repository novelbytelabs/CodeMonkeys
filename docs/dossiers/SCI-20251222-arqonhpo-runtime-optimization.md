---
schema_version: "0.1"
dossier_type: "science"
dossier_id: "SCI-20251222-arqonhpo-runtime-optimization"
topic: "Runtime Optimization Control Loop"
owner: "science-monkeys"
status: "validated"
created_at: "2025-12-22"
hypothesis:
  statement: "If we replace static parameter tuning with a continuous control loop that measures → decides → applies → measures, then systems will maintain optimal performance under drift without human intervention."
  null_hypothesis: "Continuous in-loop optimization provides no benefit over periodic offline tuning."
  significance_level: 0.05
experiment_links:
  - name: "ArqonHPO Benchmark Suite"
    path: "ArqonHPO/benches/"
    description: "Micro-benchmarks proving sub-microsecond overhead"
  - name: "PCR Probe Design"
    path: "ArqonHPO/docs/pcr_probe.md"
    description: "Prime-recurrence sequence for bounded parameter search"
  - name: "T1/T2 Architecture"
    path: "ArqonHPO/project/constitution.md"
    description: "Hot-path timing contracts"
acceptance_hooks:
  code_proofs:
    - "T2 decide/observe latency < 500ns p99"
    - "T1 apply latency < 200ns p99"
    - "Deterministic replay from seed + audit trail"
    - "Bounded deltas: no wild parameter jumps"
  test_requirements:
    - "Benchmark regression tests in CI"
    - "Property tests for determinism"
    - "Safety guardrail tests (bounds, max_delta, cooldown)"
  evidence_artifacts:
    - "benches/criterion output"
    - "CI benchmark comparison"
    - "Audit trail JSON examples"
risks:
  - risk: "Hot-path overhead exceeds budget"
    mitigation: "Tiered architecture (T1/T2) with strict timing contracts"
  - risk: "Unbounded oscillation in parameter space"
    mitigation: "Max-delta limits, cooldown periods, rollback hooks"
  - risk: "Determinism broken by floating-point drift"
    mitigation: "Stable parameter ordering, seeded RNG, audit trail"
constraints:
  - "Must run in-process, not as external service"
  - "Zero GC pauses (Rust-first)"
  - "No blocking in hot path"
  - "Single-node first, fleet later"
evidence_plan:
  final_artifacts:
    - "Rust library with Python bindings"
    - "Benchmark evidence (criterion)"
    - "Example integrations (ask/tell loop)"
    - "Constitution document"
  validation_method: "Benchmark regression + property tests + integration examples"
constitution_refs:
  - "ArqonHPO/project/constitution.md"
  - "constitution.md"
---

# Science Dossier: ArqonHPO Runtime Optimization

## 1. Research Question

**Can we make optimization a control loop primitive instead of an offline workflow?**

Traditional HPO: Run experiments → Wait → Retune manually → System drifts between sessions.
Proposed: Measure → Decide → Apply → Measure again. Continuous, bounded, auditable.

## 2. Hypothesis

> If we replace static parameter tuning with a continuous control loop, systems will maintain optimal performance under drift without human intervention.

**Falsification criteria:**
- Overhead exceeds 1μs per decision (kills hot-path use case)
- Oscillation or instability in parameter space
- Non-deterministic behavior (can't replay/audit)

## 3. Key Innovations

### 3.1 Tiered Architecture
- **T2 (Adaptive Engine)**: Online optimizer, ~200ns/decision
- **T1 (Safety Executor)**: Guardrails, ~120ns/apply

### 3.2 Bounded Autonomy
- Allowlist-only parameters
- Max-delta per step
- Cooldown/dwell periods
- Instant rollback to baseline

### 3.3 Deterministic Replay
- Stable parameter ordering
- Seeded decisioning
- Full audit trail

## 4. Current Evidence

| Proof | Status | Evidence |
|-------|--------|----------|
| Sub-μs overhead | ✅ Proven | criterion benchmarks |
| Bounded deltas | ✅ Proven | guardrail tests |
| Determinism | ✅ Proven | replay tests |
| Drift resistance | 🔄 In progress | simulation suite |

## 5. Handoff Requirements

For Code Monkeys to productize this:
1. Python bindings via maturin
2. CLI for shadow-mode testing
3. Integration examples (reliability, caching, LLM serving)
4. Constitution-compliant governance
