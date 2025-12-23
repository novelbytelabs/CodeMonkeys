# Oracle: Strategic Vision & Knowledge Base

> **Purpose**: This document captures all strategic decisions, research insights, and future directions for the Oracle module. It serves as the "memory" for cross-session continuity.
>
> **Last Updated**: 2025-12-23

---

## 1. Mission Statement

**Oracle is the SOTA local-first codebase understanding system that surpasses Greptile on every dimension while maintaining 100% privacy and Constitution-governed execution.**

We are not building "another RAG tool." We are building the **collective brain** for codebases.

---

## 2. Core Architecture Decisions

### 2.1 Embedding Model: Qodo-Embed-1-1.5B

**Decision**: Use Qodo-Embed-1-1.5B (GGUF Q4_K_M)

**Rationale**:
- CoIR benchmark: 68.53 (beats OpenAI's 65.17)
- 32K context window (can embed entire files)
- Synthetic hard negatives training = deep semantic understanding
- 1GB quantized size fits alongside LLM in memory

**Alternatives Rejected**:
- Jina Code V2 (too weak: ~60.0 on CoIR)
- OpenAI/Voyage (violates local-first constraint)
- Salesforce SFR-2B (larger, slightly lower score)

### 2.2 Graph Schema: Tiered SCIP + CPG

**Decision**: Two-tier graph architecture

**Tier 1 (Global)**: SCIP-based skeleton
- Nodes: File, Symbol (Class, Function), Module
- Edges: DEFINES, REFERENCES, IMPORTS, INHERITS
- Built with standard SCIP indexers

**Tier 2 (Local)**: On-demand CPG
- Generated per-function via Tree-sitter when deep reasoning needed
- Avoids massive global DFG cost

### 2.3 Retrieval: GraphRAG with RRF

**Decision**: Triple-index hybrid retrieval with Reciprocal Rank Fusion

**The Three Indices**:
1. Vector (LanceDB) — semantic similarity
2. Lexical (Tantivy/BM25) — exact keyword/symbol match
3. Graph (SQLite) — structural relationships

**Fusion**: RRF with k=60 constant

**Why GraphRAG beats standard RAG**:
- Standard RAG: Finds similar text
- GraphRAG: Finds similar text + **connected code** (call chains, dependencies)

### 2.4 Inference Stack: Rust + Candle

**Decision**: Pure Rust with Candle for ML inference

**Rationale**:
- No Python runtime overhead
- GGUF native support
- Metal/CUDA acceleration
- Single binary distribution

---

## 3. Competitive Position

### 3.1 The Counter-Strategy vs Greptile

| Aspect | Greptile | Oracle |
|--------|----------|--------|
| **How it works** | Agent browses code at runtime (O(N)) | Pre-computed graph traversal (O(1)) |
| **Speed** | 10s-60s per query | <100ms |
| **Cost** | Cloud compute per query | Zero (local) |
| **Privacy** | Code uploaded to cloud | 100% local |

**The Core Insight**: We pre-compute what their agent discovers at runtime.

### 3.2 SOTA Claims (Targets)

| Metric | Target | Greptile Estimate |
|--------|--------|-------------------|
| MRR@10 | >0.85 | ~0.80 |
| Query Latency | <100ms | 500ms-60s |
| Multi-hop Success | >90% | Limited |
| Privacy | 100% local | Cloud |

---

## 4. Superpowers Roadmap

These are the differentiating capabilities beyond basic Q&A.

### 4.1 Phase 1 Superpowers (Enabled by GraphRAG)

| Power | Description | Status |
|-------|-------------|--------|
| **Multi-hop Reasoning** | "What calls the function that writes to DB?" | Planned |
| **Impact Analysis** | "If I change X, what breaks?" | Planned |
| **Cross-file Context** | Full call chain retrieval, not random chunks | Planned |

### 4.2 Phase 2 Superpowers (Future)

| Power | Description | Difficulty |
|-------|-------------|------------|
| **Time-Travel** | Query historical code states via git indexing | Medium |
| **Semantic Diff** | PR review in full codebase context | Medium |
| **Codebase Health Score** | Tech debt dashboard, coupling metrics | Medium |
| **Auto-Documentation** | Living architecture diagrams from graph | Medium |

### 4.3 Phase 3 Superpowers (Moonshots)

| Power | Description | Difficulty |
|-------|-------------|------------|
| **Fleet Intelligence** | Cross-repo pattern search (org memory) | Hard |
| **Counterfactual** | "What if I delete this module?" | Hard |
| **Security Taint** | Source→Sink vulnerability detection | Hard |
| **Proactive Surfacing** | Anticipate what user needs | Hard |
| **Learn from Feedback** | Oracle gets smarter with use | Hard |

---

## 5. Key Research Sources

| Source | Contribution |
|--------|--------------|
| **CoIR Benchmark (ACL 2025)** | New SOTA evaluation standard for code retrieval |
| **Qodo-Embed-1 Report (2025)** | Synthetic hard negatives, 32K context |
| **Microsoft GraphRAG (2024)** | Community detection, hierarchical summaries |
| **SCIP Protocol (Sourcegraph)** | Cross-repo linking via stable URIs |
| **code4AI TSDAE Tutorial** | Unsupervised domain adaptation for embeddings |

---

## 6. Implementation Status

### Current Oracle (As of Dec 2023)

| Component | Status | Gap |
|-----------|--------|-----|
| Indexer | Basic Tree-sitter | No SCIP, no multi-language |
| Embeddings | MiniLM-L6 (384d) | Need Qodo-Embed-1 |
| Query | Keyword matching | Need GraphRAG |
| Graph | Basic nodes/edges | Need SCIP integration |
| Storage | SQLite + LanceDB | ✅ Correct stack |

### Target Oracle

| Component | Target |
|-----------|--------|
| Indexer | Tree-sitter + SCIP (20+ languages) |
| Embeddings | Qodo-Embed-1-1.5B (Q4_K_M) |
| Query | Triple-index GraphRAG with RRF |
| Graph | Tiered SCIP + on-demand CPG |
| Latency | <100ms p99 |

---

## 7. Open Questions & Decisions Needed

1. **TSDAE Integration**: Should we fine-tune embeddings on user's codebase? (Adds 2-5 min to first scan)
2. **Intent Router Model**: Qwen2.5-0.5B vs dedicated classifier?
3. **Fleet Mode Priority**: Should cross-repo be Phase 2 or Phase 3?
4. **Security Taint**: Integrate in core or separate module?

---

## 8. Related Documents

- [DOS-20251223-oracle-sota-blueprint.md](./dossiers/DOS-20251223-oracle-sota-blueprint.md) — Full technical architecture
- [constitution.md](./constitution.md) — Constitution XVI defines Oracle governance
- [architecture.md](../architecture.md) — Current implementation docs

---

## 9. Session Log

### 2025-12-23: Oracle SOTA Planning Session

**Participants**: User + Antigravity AI

**Key Decisions**:
1. Committed to surpassing Greptile as explicit goal
2. Selected Qodo-Embed-1-1.5B as embedding model
3. Adopted GraphRAG architecture with SCIP integration
4. Identified 10 "superpowers" for roadmap

**Research Obtained**: 
- 15K-word deep research report on SOTA code understanding
- CoIR benchmark analysis
- Competitive teardown of Greptile architecture

**Artifacts Created**:
- `DOS-20251223-oracle-sota-blueprint.md`
- `ORACLE_VISION.md` (this document)

---

*This document should be updated after each significant Oracle planning session.*
