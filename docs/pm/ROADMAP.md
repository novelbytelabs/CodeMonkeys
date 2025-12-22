# Code Monkeys Roadmap

**Status**: Canonical  
**Owner**: Nexus  
**Last Updated**: 2025-12-21

## Phase 0: Foundation (v0.2.x) - COMPLETE
**Goal**: Stable base with Dash, Schema Validation, Nexus Stubs, and CI enforcement.
- [x] Dash MVP + Fleet support
- [x] Formal schemas + artifacts
- [x] Silverback validator
- [x] Nexus executor (budget/kill-switch)
- [x] Branching workflow + CI enforcement
- [x] Vision + Decision logs

---

## Phase 1: Factory Core CLI (Sprint 1)
**Goal**: Unified control plane. Convert scripts into a cohesive `codemonkeys` CLI.
- [ ] `codemonkeys dash serve`
- [ ] `codemonkeys run <product>` (report generation)
- [ ] `codemonkeys silverback --all` (validation)
- [ ] `codemonkeys nexus exec` (decision execution)
- [ ] `codemonkeys fleet` (management)

---

## Phase 2: Nexus Executive (Sprint 2)
**Goal**: Nexus becomes a real operating executive, not just a queue.
- [ ] Decision/Request lifecycle management
- [ ] Escalation contracts (budget, governance, kill-switch)
- [ ] Automated portfolio summary artifacts
- [ ] Dashboard integration for active decisions

---

## Phase 3: Ship Pipeline (Sprint 3)
**Goal**: "Ship" becomes a disciplined, effectively autonomous process.
- [ ] PR Wave protocol (labels, blocking, limits)
- [ ] Automated changelog generation
- [ ] Release artifact pipeline
- [ ] GitHub Release automation

---

## Phase 4: Codebase Oracle (Sprint 4)
**Goal**: Fast, deterministic context retrieval for agents.
- [ ] `codemonkeys scan` (deterministic indexing)
- [ ] Context pack generation
- [ ] Agent retrieval hooks

---

## Phase 5: Self-Healing CI (Sprint 5)
**Goal**: Bounded, governed repair of CI failures.
- [ ] `codemonkeys heal` (max attempts, error-feed only)
- [ ] Repair evidence artifacts
- [ ] Escalation on failure (fail closed)

---

## Phase 6: Science Handoff (Sprint 6)
**Goal**: Bring Science Monkeys online via formal contracts.
- [ ] Design Dossier intake pipeline
- [ ] Science artifacts in Dash
- [ ] Spec generation from dossiers
