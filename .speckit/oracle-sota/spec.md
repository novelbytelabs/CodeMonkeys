# Oracle SOTA Upgrade Specification

> **Feature**: Upgrade Oracle to surpass Greptile as SOTA codebase understanding system
> **Status**: Planning
> **Priority**: P0 (Strategic Differentiator)
> **Owner**: CodeMonkeys Core Team

---

## 1. Problem Statement

Current Oracle has critical gaps:
- **Embeddings**: MiniLM-L6 (384d, text-only) → CoIR score ~60
- **Query**: Keyword matching only, no semantic search
- **Graph**: Basic nodes/edges, no cross-repo linking

**Target**: Beat Greptile's MRR@10 ~0.80 with 100% local execution.

---

## 2. Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| MRR@10 | Unknown | >0.85 |
| Query Latency | ~500ms | <100ms p99 |
| Multi-hop Success | 0% | >90% |
| Languages | 2 (Rust, Python) | 10+ |
| Privacy | 100% local | 100% local |

---

## 3. Technical Decisions

### 3.1 Embedding Model
**Choice**: Qodo-Embed-1-1.5B (GGUF Q4_K_M)
- CoIR: 68.53
- Context: 32K tokens
- Size: ~1GB quantized

### 3.2 Graph Schema
**Choice**: Tiered SCIP + On-demand CPG
- Global: SCIP indexers for cross-repo linking
- Local: Tree-sitter CPG per-function

### 3.3 Retrieval
**Choice**: GraphRAG with RRF (k=60)
- Vector (LanceDB) + Lexical (BM25) + Graph (SQLite)

### 3.4 Inference
**Choice**: Candle (Rust-native)
- No Python overhead
- Metal/CUDA acceleration

---

## 4. Superpowers Roadmap

### Phase 1 (Core)
- [ ] Qodo-Embed-1 integration
- [ ] Triple-index retrieval
- [ ] RRF fusion
- [ ] Basic graph expansion

### Phase 2 (Intelligence)
- [ ] Impact Analysis ("what breaks if I change X?")
- [ ] Time-Travel (git history queries)
- [ ] Semantic Diff (contextual PR review)

### Phase 3 (Moonshots)
- [ ] Fleet Intelligence (cross-repo)
- [ ] Security Taint Analysis
- [ ] Proactive Surfacing

---

## 5. Non-Goals

- Cloud deployment (violates Constitution)
- Proprietary embedding models
- Non-deterministic results

---

## 6. Dependencies

- Tree-sitter grammars for target languages
- SCIP indexers (scip-typescript, rust-analyzer, scip-python)
- Candle with GGUF support
- LanceDB for vector storage

---

## 7. Related Documents

- [ORACLE_VISION.md](./ORACLE_VISION.md) — Strategic vision & session logs
- [DOS-20251223-oracle-sota-blueprint.md](../dossiers/DOS-20251223-oracle-sota-blueprint.md) — Full architecture
- [Constitution XVI](./constitution.md) — Oracle governance rules
