# Master Backlog

**Status**: Canonical  
**Owner**: Nexus  
**Prioritized By**: Human Operator

## Epic 1: Factory Core CLI (Sprint 1)
**Priority**: High  
**Status**: Ready to Start  
**Acceptance Proofs**:
- `codemonkeys run codemonkeys-dash` produces valid artifacts
- `codemonkeys silverback --all` passes
- `codemonkeys dash serve` launches dashboard
- CLI installed and runnable in CI

## Epic 2: Nexus Executive (Sprint 2)
**Priority**: High  
**Status**: Planned  
**Acceptance Proofs**:
- Budget exhaustion triggers request artifact
- Decision execution modifies system state and is logged
- Dash displays pending inbox/outbox counts
- Portfolio summary artifact generated

## Epic 3: Ship Pipeline (Sprint 3)
**Priority**: Medium  
**Status**: Planned  
**Acceptance Proofs**:
- PR wave limits enforced
- Changelog generated from commits
- Release artifact created and linked in Dash

## Epic 4: Codebase Oracle (Sprint 4)
**Priority**: Medium  
**Status**: Planned  
**Acceptance Proofs**:
- `codemonkeys scan` is deterministic (same hash)
- Context pack successfully boots fresh agent

## Epic 5: Self-Healing CI (Sprint 5)
**Priority**: Low (Complex)  
**Status**: Planned  
**Acceptance Proofs**:
- Fix applied automatically within 2 attempts
- Failed repair escalates to Nexus
- No prompt injection via error logs

## Epic 6: Science Handoff (Sprint 6)
**Priority**: Low (Future)  
**Status**: Planned  
**Acceptance Proofs**:
- Design Dossier ingested → new product created
- Science artifacts visible in Dash
