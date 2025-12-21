# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## Constraints & Non-goals *(mandatory)*

<!--
  ACTION REQUIRED: Explicitly list what the system will NOT do and the boundaries.
  WARNING: Leaving this blank blocks implementation readiness.
-->

### Constraints
- **C-001**: [e.g., Must run on local hardware with < 4GB RAM]
- **C-002**: [e.g., No external API calls allowed in the hot path]

### Non-goals
- **NG-001**: [e.g., Will not support mobile layouts in v1]
- **NG-002**: [e.g., No real-time synchronization]

## Invariants & Failure Modes *(when applicable)*

<!--
  ACTION REQUIRED: Define truths that must always be true and how the system fails safely.
  WARNING: Leaving this blank blocks implementation readiness.
-->

### Invariants
- **INV-001**: [e.g., User balance can never be negative]

### Failure Modes
- **FM-001**: [e.g., If database is unreachable, fail closed and deny access]

## Security & Privacy *(when applicable)*

<!--
  ACTION REQUIRED: Define security controls and privacy requirements.
  WARNING: Leaving this blank blocks implementation readiness.
-->

- **SEC-001**: [e.g., All PII must be encrypted at rest]
- **PRIV-001**: [e.g., Users must explicitly consent to telemetry]

## Performance & Resource Bounds *(when relevant)*

<!--
  ACTION REQUIRED: Define performance limits and resource usage caps.
  WARNING: Leaving this blank blocks implementation readiness.
-->

- **PERF-001**: [e.g., API response time < 200ms at p95]
- **RES-001**: [e.g., Docker container max memory 512MB]

## Evidence Plan *(mandatory)*

<!--
  ACTION REQUIRED: Define what artifacts prove the feature is working.
  WARNING: Leaving this blank blocks implementation readiness.
-->

- **EV-001**: [e.g., Screenshot of settings page]
- **EV-002**: [e.g., Log output showing successful transaction]
- **EV-003**: [e.g., CI pass link]

## Traceability Map *(mandatory before ship)*

<!--
  ACTION REQUIRED: Map requirements to code and tests.
  WARNING: Leaving this blank blocks implementation readiness.
-->

| Requirement | File/Component | Test Case | Status |
|-------------|----------------|-----------|--------|
| FR-001      | `src/auth.rs`  | `tests/auth_test.rs` | Pending |

## Owner & Authority *(mandatory)*

<!--
  ACTION REQUIRED: Define who owns this feature and the autonomy level.
  WARNING: Leaving this blank blocks implementation readiness.
-->

- **Primary Owner**: [e.g., Nexus Agent]
- **Escalation Policy**: [e.g., Notify Human if P0 failure or budget exceeded > 50%]
- **Autonomy Level**: [autonomous | autonomous-with-review | human-required]

## Budget & Stop Conditions *(mandatory)*

<!--
  ACTION REQUIRED: Define resource limits and conditions that must stop the loop.
  WARNING: Leaving this blank blocks implementation readiness.
-->

### Budgets
- **Max PRs per run**: [e.g., 1]
- **Max CI Retries**: [e.g., 2]
- **Compute/Time**: [e.g., 600s wall time]
- **Token Limits**: [e.g., 50k tokens]

### Stop Conditions
- **Condition**: [e.g., Repeated CI failure (3x)]
- **Condition**: [e.g., Scope creep (diff > 500 lines)]
- **Condition**: [e.g., Confidence score < 0.7]
- **Condition**: [e.g., Missing acceptance proof hooks]

## Rollout / Rollback *(mandatory when shipping)*

<!--
  ACTION REQUIRED: Define how this releases and how to undo it.
  WARNING: Leaving this blank blocks implementation readiness.
-->

- **Bootstrap Mode**: [Allowed/Not Allowed] (Local-only testing)
- **Feature Flag**: [e.g., ENABLE_NEW_AUTH]
- **Rollback Plan**: [e.g., Revert commit, disable flag]

## Observability & Ops Notes *(mandatory when applicable)*

<!--
  ACTION REQUIRED: Define telemetry, logs, and dashboard requirements.
  WARNING: Leaving this blank blocks implementation readiness.
-->

- **Logged Events**: [e.g., Transaction completion, Error traces]
- **Run Reports**: [e.g., Written to .codemonkeys/runs/<id>/report.json]
- **Dash Telemetry**: [e.g., Must show success/failure status in MVP Dash]
- **Failure Surface**: [e.g., Log to stderr, update status file]
