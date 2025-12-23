---
dossier_id: DOS-20251223-oracle-sota-blueprint
type: design
status: approved
hypothesis:
  claim: "A Local-First GraphRAG architecture using Qodo-Embed-1-1.5B, SCIP/CPG hybrid graphs, and RRF fusion will surpass Greptile as the SOTA codebase understanding system."
  falsification: "If Oracle fails to achieve MRR@10 > 0.85, query latency < 100ms, or cannot handle 1M+ file repos on consumer hardware."
dependencies:
  requires:
    - "Qodo-Embed-1-1.5B (GGUF Q4_K_M)"
    - "Candle inference framework"
    - "LanceDB vector store"
    - "Tree-sitter (polyglot parsing)"
    - "SCIP indexers (cross-repo linking)"
    - "SQLite (graph store)"
  enables:
    - "SOTA semantic code search"
    - "Multi-hop graph reasoning"
    - "Cross-repo navigation"
    - "Context-aware Heal module"
research_sources:
  - "CoIR: Code Information Retrieval Benchmark (ACL 2025)"
  - "Qodo-Embed Technical Report (2025)"
  - "Microsoft GraphRAG (2024)"
  - "GraphCodeBERT (2021)"
  - "SCIP Code Intelligence Protocol (Sourcegraph)"
---

# Oracle: Architectural Blueprint for a State-of-the-Art Local-First Code Understanding System

> **Mission**: Build the SOTA local-first codebase understanding system that surpasses Greptile on every dimension while maintaining 100% privacy and Constitution-governed execution.

---

## 1. Executive Summary

### 1.1 The Local-First Imperative

The current market leaders (Greptile, Sourcegraph, GitHub Copilot) rely on cloud-centric architectures that require uploading proprietary source code. This creates:

- **Privacy risks**: Code leaves the developer's machine
- **Latency bottlenecks**: Cloud RTT adds 100-500ms
- **Vendor dependency**: Uptime and pricing tied to third parties

**Oracle is the antithesis**: A local-first, privacy-preserving system that runs entirely on developer hardware (Apple Silicon, consumer GPUs) without sacrificing depth of analysis.

### 1.2 Key Differentiators

| Dimension | Greptile | Oracle |
|-----------|----------|--------|
| **Architecture** | Cloud-Native, Agentic Loops | **Local-First, Embedded DB** |
| **Indexing** | Runtime agent browsing | **Pre-computed GraphRAG** |
| **Privacy** | Data leaves premises | **100% Local / Air-gapped** |
| **Search** | Agentic recursive search | **Hybrid RRF + Graph Traversal** |
| **Latency** | High (Cloud RTT + Agent think) | **Ultra-Low (<100ms)** |

### 1.3 The Counter-Strategy

> **Greptile's Approach**: An LLM agent "browses" your code at query time, recursively searching. Powerful but slow (10s-1min) and costly.
>
> **Oracle's Counter**: Pre-compute the relationships Greptile discovers at runtime. Turn O(N) agentic search into O(1) graph traversal.

---

## 2. Code Embedding Models (SOTA 2024-2025)

### 2.1 The Benchmark: CoIR

The **CoIR (Code Information Retrieval)** benchmark has emerged as the new SOTA standard, superseding CodeSearchNet. It comprises 10 datasets spanning 8 distinct retrieval tasks across 7 domains.

### 2.2 Model Comparison

| Rank | Model | Params | CoIR Avg | License | Local Viability |
|------|-------|--------|----------|---------|-----------------|
| 1 | Salesforce SFR-Embedding-Code-2B_R | 2B | 67.41 | MIT/Apache | High (GGUF) |
| 2 | **Qodo-Embed-1-7B** | 7B | 71.5 | Commercial | Med (High VRAM) |
| 3 | **Qodo-Embed-1-1.5B** | 1.5B | 68.53 | Openrail++ | **Optimal** |
| 4 | Voyage-Code-2 | Unknown | ~69.0 | Proprietary | None (API) |
| 5 | Jina-Embeddings-v2-base-code | 137M | ~60.0 | Apache 2.0 | Very High |
| 6 | CodeSage-large-v2 | 1.3B | 64.18 | Apache 2.0 | High |

### 2.3 Selection: Qodo-Embed-1-1.5B

**Why Qodo-Embed-1-1.5B is optimal:**

- **Performance**: Scores 68.53 on CoIR, outperforming OpenAI's text-embedding-3-large (65.17)
- **Efficiency**: 25% smaller than Salesforce 2B but higher score
- **Context Window**: Massive 32K tokens — can embed entire files
- **Secret Sauce**: Trained on **synthetic data** with hard negatives, forcing deep semantic understanding

**Configuration:**
```
Model: Qodo-Embed-1-1.5B
Format: GGUF (Q4_K_M quantization)
Size: ~1GB (down from 3GB FP16)
Latency: <50ms per batch on M2
Dimensions: 1536 (stored as Float16)
```

---

## 3. Code Graph Representations

### 3.1 The Tiered Graph Architecture

Oracle implements a **Tiered Graph** approach:

#### Tier 1: Global Reference Graph (SCIP-based)

A lightweight skeleton capturing high-level relationships.

| Node Types | Edge Types |
|------------|-----------|
| File | DEFINES |
| Symbol (Class, Function) | REFERENCES |
| Module | IMPORTS |
| Interface | INHERITS |

**Storage**: SQLite with SCIP string IDs as primary keys (e.g., `cargo pkg 1.0.0 src/main.rs/MyStruct#`)

**Indexers**: Use standard SCIP indexers — `scip-typescript`, `rust-analyzer`, `scip-python`

#### Tier 2: On-Demand Semantic Graph (CPG-Lite)

For deep reasoning, generate localized CPG on the fly:

- When user queries specific function, parse with Tree-sitter
- Build local Control Flow Graph in memory
- Avoids massive overhead of global DFG generation

### 3.2 Cross-Repository Linking

**The Problem**: `import React from 'react'` refers to code outside user's source tree.

**The Solution**: SCIP URIs

- The SCIP ID for React: `npm/react/18.2.0/index.d.ts/React#`
- Oracle indexes user project + top dependencies
- Graph contains "stub nodes" pointing to external SCIP IDs
- Enables "Go to Definition" that jumps into library code

### 3.3 Graph-Augmented Embedding

Instead of embedding just the code, append graph context:

```
function foo(x) { ... }
// Called by: bar(), baz()
// Calls: db.query()
```

This injects structural context into the vector space.

---

## 4. Hybrid Retrieval: GraphRAG with RRF

### 4.1 The Three-Index Pipeline

Oracle executes three queries in parallel:

| Index | Engine | Purpose |
|-------|--------|---------|
| **Vector** | LanceDB | Semantic similarity |
| **Lexical** | Tantivy/BM25 | Exact keyword/symbol matching |
| **Graph** | SQLite | Structural relationships |

### 4.2 Reciprocal Rank Fusion (RRF)

To combine disparate lists without tuning weights:

```
RRF_score(d) = Σ 1/(k + rank_r(d))
```

Where `k = 60` (constant) and `r` iterates over rankers.

**Result**: A file appearing in both Vector top-10 and Graph top-10 skyrockets to #1.

### 4.3 Graph Expansion

For top results (Anchors), perform graph expansion:

**Contextual Radius** — if Function A retrieved:
- Definition of Function A
- Callers of Function A (usage examples)
- Callees of Function A (dependencies)

```sql
SELECT source_id FROM edges 
WHERE target_id = 'Function_A_ID' AND type = 'CALLS'
```

### 4.4 Multi-Hop Reasoning

For queries like "What controller triggers payment processing?":

1. **Intent Detection**: Identify as "Upstream Trace"
2. **Anchor**: Find `PaymentService` via vector search
3. **Traverse**: BFS backward along `CALLS` edges
4. **Answer**: Feed entire path `Controller → Helper → Service` to LLM

### 4.5 Community Detection

Inspired by Microsoft GraphRAG:

1. **Cluster**: Run Leiden algorithm on call graph during indexing
2. **Summarize**: LLM generates summary per cluster
3. **Retrieve**: Broad queries hit cluster summaries instead of 500 individual files

---

## 5. Query Understanding & Intent Detection

### 5.1 Intent Taxonomy

| Intent | Example | Action |
|--------|---------|--------|
| **Navigational** | "Where is UserFactory?" | Exact symbol lookup (SCIP) |
| **Concept** | "How do I implement Auth?" | Vector search (semantic) |
| **Trace** | "Who calls login?" | Graph traversal (BFS) |
| **Debug** | "Why is this failing?" | Local context + reasoning |

### 5.2 The Intent Router

Use a quantized SLM (Qwen2.5-0.5B or BERT-Tiny) as classifier:

**Input**: User query  
**Output**: 
```json
{
  "intent": "TRACE",
  "symbol": "User",
  "path_constraint": "src/models"
}
```

### 5.3 Query Expansion

Build local synonym map from codebase:
- If codebase contains `AuthenticationService` and `AuthUtils`
- Query "Auth" expands to `Auth OR Authentication`

---

## 6. Indexing & Incremental Updates

### 6.1 Smart Chunking with Tree-sitter

**Syntax-Aware Chunking**:

1. **Parse**: Tree-sitter generates CST
2. **Identify**: Scope nodes (function, class, module)
3. **Coalesce**: Keep functions as single units if possible

**The "Context Sandwich" Technique**:

For large functions (2000+ lines):
- Split body into 500-token chunks
- **Prepend** function signature + docstring to every chunk
- A chunk from line 1500 retains: "I am part of `process_payment`"

### 6.2 Git-Diff Aware Incremental Indexing

**Merkle Tree Approach**:

1. On startup: `git diff --name-only HEAD`
2. Check `file_hash` cache in SQLite
3. Update only changed files

**Lazy Propagation**:
- Don't re-index dependent files
- SCIP's stable IDs handle linking
- Reduces update time from O(Graph) to O(1)

---

## 7. Local Inference Optimization

### 7.1 The Rust Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Inference** | Candle | Pure Rust, GGUF native, Metal/CUDA |
| **Vector Store** | LanceDB | Embedded, disk-based ANN, Arrow format |
| **Graph Store** | SQLite | Relational edges, no external process |
| **Parsing** | Tree-sitter | Polyglot, fast, incremental |

### 7.2 Pipeline Parallelism

Assembly line using `tokio` channels:

```
Thread 1 (CPU): Read Files
Thread 2-4 (CPU): Tree-sitter Parse (Rayon parallel)
Thread 5 (CPU): Chunking
Thread 6 (GPU): Candle Embedding (Batched)
Thread 7 (I/O): Write to LanceDB
```

**Result**: GPU never waits for disk I/O.

### 7.3 Performance Targets

| Operation | Current (Python) | Target (Rust) |
|-----------|-----------------|---------------|
| Embed single snippet | ~50ms | <5ms |
| Embed 1000 snippets | ~30s | <3s |
| Index 10K files | ~15 min | <2 min |
| Query latency | ~500ms | <100ms |

---

## 8. Competitive Analysis

### 8.1 Oracle vs. Greptile

| Feature | Greptile | Oracle |
|---------|----------|--------|
| **How it works** | Agent browses code at runtime | Pre-computed graph traversal |
| **Speed** | 10s-1min (agent think time) | <100ms (graph lookup) |
| **Cost** | Cloud compute per query | Zero (local) |

**The Counter**:
```
Greptile: "Let me search for who calls X... found Y... who calls Y?"
Oracle:   SELECT * FROM edges WHERE type='CALLS'  -- 0.5ms
```

### 8.2 Oracle vs. Sourcegraph (Cody)

| Feature | Sourcegraph | Oracle |
|---------|-------------|--------|
| **Index** | SCIP (precise, rigid) | **Hybrid SCIP + Tree-sitter + Vector** |
| **Context** | Heuristic script | **GraphRAG (mathematically proven relevance)** |

---

## 9. Evaluation & Benchmarks

### 9.1 Private Benchmark Methodology

Public benchmarks are contaminated. Use **Synthetic Private Benchmark**:

1. **Sample**: Select 50 random functions from user's codebase
2. **Generate**: LLM creates query for each: "Find the function that handles X"
3. **Gold Standard**: The file containing the function
4. **Metric**: Recall@5 on user's specific coding style

### 9.2 Expected Performance

Based on Qodo-Embed-1 benchmarks and LanceDB performance:

| Metric | Target |
|--------|--------|
| Indexing Speed | ~10MB code/second on M1 Max |
| Query Latency | <50ms retrieval, <5s answer generation |
| Recall | +15-20% over vanilla RAG due to graph injection |
| MRR@10 | >0.85 |

---

## 10. Implementation Roadmap

### Phase 1: Core Foundation
- [ ] Rust CLI scaffold
- [ ] Tree-sitter integration (Rust, Python, TypeScript, Go)
- [ ] LanceDB vector storage
- [ ] Qodo-Embed-1-1.5B via Candle (GGUF Q4_K_M)

### Phase 2: Graph Intelligence
- [ ] SCIP indexer integration
- [ ] SQLite graph schema
- [ ] RRF fusion algorithm
- [ ] Graph traversal queries

### Phase 3: Brain Layer
- [ ] Intent Router (SLM classifier)
- [ ] Query expansion from codebase vocabulary
- [ ] Community detection (Leiden algorithm)
- [ ] Multi-hop reasoning

### Phase 4: Polish & Scale
- [ ] Incremental indexing via git diff
- [ ] Cross-repo dependency graphs
- [ ] Pipeline parallelism optimization
- [ ] Benchmark suite

---

## 11. Constitution Amendments Required

Add to **XVI. Codebase Oracle Principles**:

```markdown
### 5. GraphRAG Contract
- **Triple-Index Retrieval**: Every query MUST execute vector, lexical, and graph paths in parallel.
- **RRF Fusion**: Use k=60 constant for deterministic ranking.
- **Graph Expansion**: Retrieve 1-hop neighborhood for all anchor nodes.

### 6. Embedding Model Governance
- **Code-Specific Models**: General text embeddings forbidden for production Oracle.
- **Default Model**: Qodo-Embed-1-1.5B (GGUF Q4_K_M).
- **Dimension**: 1536, stored as Float16.

### 7. SCIP Integration
- **Cross-Repo Linking**: Dependencies indexed as read-only graphs.
- **Stable IDs**: Use SCIP URI scheme for all symbol references.
- **Lazy Propagation**: Don't re-index dependents on file change.

### 8. Performance Budgets
- **Query Latency**: <100ms p99 for retrieval.
- **Indexing Speed**: >10MB/s on M1-class hardware.
- **Memory**: Embedding model + vector cache <4GB.
```

---

## 12. Academic References

| Paper | Year | Contribution |
|-------|------|--------------|
| **CoIR Benchmark** | 2025 | New SOTA evaluation standard |
| **Qodo-Embed-1** | 2025 | Synthetic hard negatives, 32K context |
| **Microsoft GraphRAG** | 2024 | Community detection, hierarchical summaries |
| **GraphCodeBERT** | 2021 | Data flow in pre-training |
| **SCIP Protocol** | 2022 | Cross-repo linking via stable URIs |
| **UniXcoder** | 2022 | AST + comment alignment |

---

## 13. Conclusion

Oracle represents the convergence of high-performance systems engineering (Rust) and modern AI (Embeddings/LLMs). By rejecting the cloud default, it addresses the critical industry need for privacy and speed.

The architecture defined herein:
- **Qodo-Embed-1** for semantics
- **SCIP/CPG** for structure  
- **GraphRAG** for retrieval
- **LanceDB/Candle** for execution

...provides a robust path to **surpassing Greptile**.

---

**Status**: Approved for Implementation  
**Next Step**: Phase 1 implementation begins Sprint 11
