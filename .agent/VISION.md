# Arqon Vision: The Solo Product Factory

> **Core Insight**: You're not building "AI coding tools." You're building a **Constitution-governed autonomous system** where the Constitution defines what's allowed, the Spec defines what to build, and everything else is execution + verification + audit.

---

## The Problem

As a solo builder shipping dozens of products:
- **Setup overhead**: Repo scaffolding, CI config, release plumbing
- **Maintenance overhead**: Keeping docs accurate, keeping CI green
- **Coordination overhead**: You vs. your own cognitive load

**North Star**: Turn product development into a mostly autonomous pipeline where you only write **Constitution + Spec**, and the system does the rest.

---

## The Arqon Trinity

| Layer | Product | Job |
|-------|---------|-----|
| **Bootstrap** | **ArqonInit** | 0 → working repo with CI/release wiring |
| **Front Half** | **ArqonDev** | Spec → Plan → Tasks → Tests (SDD+TDD) |
| **Back Half** | **ArqonShip** | Heal → Docs → Ship → Publish → Announce |

### ArqonInit — "Factory Bootstrap"
- Repo skeleton + language templates (Rust/Python/C)
- CI workflows + caching
- Release pipeline wiring
- Default Constitution + Spec templates with machine policy block
- `.arqon/config.toml` tuned to your environment

### ArqonDev — "Front-Half Loop" (spec-kit fork/wrapper)
- Spec authoring
- Task decomposition
- TDD scaffolding
- Traceability mapping (req → code/tests/docs)

### ArqonShip — "Back-Half Loop"
- **Oracle**: Code graph + semantic indexing
- **Heal**: Self-healing CI with LLM-powered fixes
- **Docs**: Living documentation that stays in sync
- **Ship**: Governed releases (semver, changelog, tags)
- **Publish**: Packages (crates.io, PyPI, Docker)
- **Announce**: Release notes, marketing copy

---

## Constitution as Runtime Policy

The Constitution is not just documentation — it's **machine-enforceable ground truth**.

```yaml
# Example policy block (embed in Constitution or config)
autonomy:
  mode: autopilot_all

heal:
  max_attempts: 2
  forbid_paths:
    - ".github/workflows/**"
    - "**/secrets/**"
  allow_paths:
    - "src/**"
    - "tests/**"

ship:
  require_green_ci: true
  label_blocks: ["do-not-merge", "wip"]

evidence:
  required: true
```

---

## Autopilot Safety Gates

Even with "Autopilot-all", these gates protect you:

1. **Verification Gate**: tests + lint + build must pass
2. **Scope Gate**: changes only in allowed paths for that action
3. **Diff-Size Gate**: >N files or >M LOC requires manual approval
4. **API/Compat Gate**: no breaking API changes unless explicitly allowed
5. **Rollback Plan**: every merge/publish has automatic rollback

---

## What "I Don't Have To Do Anything" Means

- ✅ Auto-commit to main (within gates)
- ✅ Auto-merge PRs (when verification passes)
- ✅ Auto-publish packages (crates.io, PyPI, Docker)
- ✅ Auto-generate docs (README, CLI ref, architecture)
- ✅ Auto-create marketing copy / announcements
- ✅ All decisions justified by Constitution

---

## Hardware Reality (Local LLM)

**RTX 2060 (6GB VRAM) + Dual Xeon (48 threads)**

| Model | Size | Runs Locally? |
|-------|------|---------------|
| `qwen2.5-coder:7b-instruct` | ~4.5GB | ✅ **Currently using** |
| `deepseek-coder:6.7b` | ~4GB | ✅ Good alternative |
| `codegeex4:9b` | ~5.5GB | ⚠️ Tight fit |
| 14B+ models | >8GB | ❌ CPU-only (slow) |

**GLM-4.6 is cloud-only** — cannot run locally on this hardware.

---

## USP (Unique Selling Proposition)

> **Constitution-governed Autopilot**: Spec-driven development with a governed back half — self-healing CI, living docs, and releases, all local-first.

This is the missing piece SDD doesn't cover.

---

## Milestones

### Milestone 1: Solo Factory MVP
- `init`, `scan`, `heal` for Cargo + pytest
- `ship --dry-run` with semver + changelog
- Doc drift check (README/CLI regenerated from Clap)

### Milestone 2: Living Docs + Policy Gates
- `arqon docs` command (update + enforce in CI)
- Constitution checks expand

### Milestone 3: Full Autopilot Loop
- Watch mode
- Automatic PR creation, labeling, merge
- Optional browser automation for last-mile

---

## Key Design Principle

ArqonShip is **not a chatbot**. It's an **execution engine with governance**:

```
observe → decide → act → verify → log
```

- Bounded retries
- Reversible changes
- Durable memory of repo state
- Every action justified by Constitution
