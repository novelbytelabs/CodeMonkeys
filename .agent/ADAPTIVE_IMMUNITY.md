# ArqonShip: Adaptive Immunity Architecture

> **Synthesized from:** Gemini AI Studio + Microsoft Copilot (2025-12-20)
> **Replaces:** "Antibody Propagation" (deemed too risky)

---

## 🚨 The Problem We Solved

**Original Idea: "Antibody Propagation"**
- Fix bug in Repo A → auto-patch 49 other repos

**Why It's Dangerous:**
- Context differs between repos
- A "fix" in one context may be a "bug" in another
- One mistake = 50 simultaneous outages
- "Blast-radius amplifier"

**Consensus from 3 AIs:** ❌ Kill it.

---

## ✅ The New Architecture: Adaptive Immunity

### Core Principle

> **Propagate RULES, not CODE. Propagate as PR waves, not patches.**

LLMs are **advisors**, not autonomous patchers.

---

## 📋 The 5-Stage Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1: INCIDENT RECORD                                           │
│  ├─ What happened, impact, root cause class                         │
│  ├─ Signature (stack trace / error patterns)                        │
│  └─ Affected components                                             │
├─────────────────────────────────────────────────────────────────────┤
│  STAGE 2: RULE EXTRACTION ("Living Linter")                         │
│  ├─ Create detection rule that catches risky pattern                │
│  ├─ Roll out as ADVISORY first (non-blocking)                       │
│  └─ Require: named incident, reproduction, intent statement         │
├─────────────────────────────────────────────────────────────────────┤
│  STAGE 3: REMEDIATION RECIPE (Optional)                             │
│  ├─ Codemod-like transformation with constraints                    │
│  ├─ "If pattern X + structure Y → replace with Z"                   │
│  └─ Includes tests/invariants                                       │
├─────────────────────────────────────────────────────────────────────┤
│  STAGE 4: CANDIDATE DISCOVERY                                       │
│  ├─ Oracle similarity search finds matches                          │
│  ├─ Rank by confidence: AST match > fuzzy semantic                  │
│  └─ Require confidence features (same lib, func shape, call chain)  │
├─────────────────────────────────────────────────────────────────────┤
│  STAGE 5: PR WAVE (Not Patch Wave!)                                 │
│  ├─ Generate PRs repo-by-repo                                       │
│  ├─ Each PR must pass repo's CI                                     │
│  ├─ Merge only if green + no blocked labels                         │
│  └─ If any fails → STOP wave, refine rule/recipe                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🪜 The Canary Ladder

Before touching 50 repos, promote through tiers:

| Tier | Repos | Gate to Promote |
|------|-------|-----------------|
| **Canary** | 1 repo (closest match) | CI passes, 24h no issues |
| **Early Adopter** | 3 repos | >90% success, failures understood |
| **Mid Wave** | 10 repos | >95% success |
| **Fleet** | Remaining 36+ | >99% success |

**If any tier fails, STOP and refine before continuing.**

---

## 📊 Rule Severity Ladder

| Level | Name | CI Impact | When to Use |
|-------|------|-----------|-------------|
| 0 | **Shadow** | None | Testing new rules |
| 1 | **Advisory** | Info only | Building confidence |
| 2 | **Warning** | Visible, non-blocking | Proven pattern |
| 3 | **Error** | Blocks merge | High-signal, low-FP |
| 4 | **Critical** | Blocks even legacy | Security-critical |

**Promotion requires:**
- Pass rate threshold (configurable per tier)
- No unexplained failures
- Human approval for tier 3+

---

## 🛡️ Governance Guardrails

### Rule Bundles Must Have:
- [ ] Version number
- [ ] Named incident link
- [ ] Minimal reproduction / test
- [ ] Intent statement ("what risk does this prevent?")
- [ ] Scope conditions (languages, frameworks, risk levels)
- [ ] Expiry/TTL for exemptions

### Per-Repo Controls:
- [ ] Exempt specific rules with TTL + owner
- [ ] Override severity level
- [ ] Opt-in/opt-out for recipes (not rules)

### Audit & Security:
- [ ] Signed rule bundles (prevent tampering)
- [ ] Audit log of all rule changes
- [ ] Canary rollout for new rules

---

## 🤖 Where LLMs Fit (Safely)

| LLM Role | Safe? | Notes |
|----------|-------|-------|
| **Classification** ("is this the same bug class?") | ✅ | Read-only |
| **Explanation** ("why is this risky?") | ✅ | Advisory |
| **Drafting** remediation proposal | ✅ | Proposal only |
| **Auto-patching 50 repos** | ❌ | NEVER |

**Rule:** LLM outputs must pass through deterministic gates (CI, AST validation, human review) before any code mutation.

---

## 📅 Updated Roadmap

| Week | Original | New Approach |
|------|----------|--------------|
| 1 | Supreme Court | **Same** — Constitution + Justice Agent |
| 2 | Nervous System | **Same** — CI/CD hooks + log parsing |
| 3 | Actuator | **Same** — Git handlers + Reality Forks |
| 4 | ~~Antibody Propagation~~ | **Adaptive Immunity** — Rule extraction + PR waves |
| 5 | Documentation Reflector | **Same** — Self-updating docs |
| 6 | ~~Ouroboros~~ | **Removed** — Only humans amend Constitution |

---

## 🏁 Summary

| Aspect | Old (Antibody) | New (Adaptive Immunity) |
|--------|----------------|-------------------------|
| Action | Auto-patch code | Propose PRs |
| Blast radius | 50 repos at once | 1 → 3 → 10 → rest |
| Human review | None | Required for merges |
| Rollback | Nightmare | Revert single PR |
| Learning | Risky | Safe + grows rule library |

**Bottom line:** We get the "swarm intelligence" benefit (cross-repo learning) without the "auto-immune collapse" risk.
