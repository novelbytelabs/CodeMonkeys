# Science → Code Handoff Contract (Design Dossier)

Date: 2025-12-21
Status: Draft (v0.1)

Science Monkeys may invent products without human involvement.
To safely convert inventions into production software, Science must hand Code a standard artifact: **Design Dossier**.

## 1) Purpose
- Make the invention *buildable* without additional discovery.
- Provide falsifiable claims and acceptance proofs.
- Preserve research context (math, notebooks, experiments) in a digestible form.
- Bound scope for an MVP.

## 2) Required sections (minimum)

### 2.1 Product Claim (1–3 sentences)
- What the product does
- Who it serves
- Why it is meaningfully different

### 2.2 Hypotheses (falsifiable)
List hypotheses in testable form:
- H1: If we do X, users will achieve Y within Z.
- H2: Metric M improves by ≥Δ under conditions C.

### 2.3 Acceptance Proofs (production-grade)
Define what proves success:
- Functional acceptance tests
- Non-functional checks (security, performance, reliability) where relevant
- Evidence requirements (what artifacts must exist)

### 2.4 Constraints and Non-goals
- Explicit constraints (privacy/local-first, cost caps, forbidden dependencies, etc.)
- Clear non-goals to prevent scope creep

### 2.5 Risk & Failure Modes
- Known failure modes
- Assumptions
- Safety concerns
- Rollback or containment plan (if relevant)

### 2.6 Experiment Summary
- What experiments were run
- Key results (Observed vs Derived)
- Links to notebooks/raw outputs

### 2.7 MVP Boundary + Roadmap
- MVP scope
- Next milestones
- “Do not build yet” items

## 3) Attachments
- Notebooks (if any)
- Data / experiment logs
- Prototype code (optional; must be labeled)
- Proofs / math notes

## 4) Output form
- Markdown at: `research/<product-id>/design-dossier.md`
- Attachments in: `research/<product-id>/artifacts/`
- A short summary for Dash: `research/<product-id>/summary.md`
