---
dossier_id: DOS-20251223-oracle-sota-upgrade
type: design
status: draft
hypothesis:
  claim: "Upgrading Oracle with Neuro-Symbolic GraphRAG, TSDAE domain-adapted embeddings, and LLM→Graph query translation will establish CodeMonkeys as the uncontested SOTA leader in codebase Q&A."
  falsification: "If the upgraded Oracle fails to outperform Greptile on MRR@10, query latency, or multi-hop reasoning benchmarks."
dependencies:
  requires:
    - "Tree-sitter multi-language support"
    - "Candle/Burn Rust ML framework"
    - "LanceDB vector store"
    - "Ollama qwen2.5-coder for Neuro-Symbolic fusion"
  enables:
    - "Enhanced context for Heal module"
    - "Cross-repo fleet intelligence"
    - "Semantic work order planning"
    - "Self-improving codebase understanding"
evidence:
  - "Proof 1: MRR@10 > 0.85 on code search benchmark (Greptile claims ~0.8)"
  - "Proof 2: Query latency < 100ms p99 (local, no network)"
  - "Proof 3: Multi-hop reasoning success rate > 90%"
  - "Proof 4: 100% local execution (zero cloud API calls)"
research_sources:
  - "code4AI: SBERT/TSDAE tutorial"
  - "Microsoft GraphRAG paper"
  - "Neuro-Symbolic LLM Fusion research"
---

# Oracle SOTA Upgrade: Neuro-Symbolic GraphRAG Architecture

> **Mission**: Make CodeMonkeys Oracle the uncontested SOTA leader in codebase understanding — surpassing Greptile on **every dimension** while maintaining 100% local, Constitution-governed execution.

## Executive Summary

The current Oracle is a toy. We're going to **rebuild it** using cutting-edge techniques:

1. **TSDAE Domain Adaptation** — Tune embeddings on the user's actual codebase (unsupervised)
2. **Neuro-Symbolic Fusion** — LLM translates natural language → graph queries (not just vector lookup)
3. **UMAP-Accelerated Search** — Dimensionality reduction for 10x faster initial retrieval
4. **Rust-Native Quantized Inference** — GPU/CPU optimized with Candle, no Python bottlenecks

---

## The Gap: Current State vs SOTA

| Dimension | Current Oracle | Greptile | **Oracle SOTA (Target)** |
|-----------|----------------|----------|--------------------------|
| **Embeddings** | MiniLM-L6 (384d, text) | Proprietary | **Codestral-Embed + TSDAE tuned** |
| **Query Method** | Keyword matching | Vector + proprietary | **Neuro-Symbolic: LLM → AST Graph Queries** |
| **Ranking** | Flat score: 1.0 | ML-based | **RRF + Cross-Encoder Rerank** |
| **Multi-hop** | None | Limited | **Full graph traversal with path reasoning** |
| **Languages** | Rust, Python | 20+ | **20+ via Tree-sitter** |
| **Privacy** | 100% local | Cloud | **100% local (our edge)** |
| **Determinism** | Partial | No | **Constitution-mandated reproducibility** |

---

## Proposed Architecture: GraphRAG

```
┌─────────────────────────────────────────────────────────────────┐
│                      ORACLE GRAPHRAG                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   INDEXER    │    │  RETRIEVER   │    │   RANKER     │      │
│  │              │    │              │    │              │      │
│  │ • Tree-sitter│    │ • Vector ANN │    │ • RRF Fusion │      │
│  │ • Graph Build│    │ • Graph Walk │    │ • LLM Rerank │      │
│  │ • Embeddings │    │ • BM25 Lexical│   │ • Score Norm │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    UNIFIED STORE                            ││
│  │  SQLite (nodes, edges, metadata) + LanceDB (vectors)        ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Upgrades

### 1. Multi-Modal Indexer

**Current**: `parser.rs` + `parser_py.rs` → nodes/edges → SQLite

**Upgrade to**:

| Component | Implementation | Purpose |
|-----------|----------------|---------|
| `parser_universal.rs` | Tree-sitter with 20+ language grammars | Multi-language AST parsing |
| `graph_builder.rs` | Enhanced node/edge types | Call graph, data flow, imports, inheritance |
| `embed_code.rs` | Local code embedding model | Code-specific semantic vectors |
| `embed_chunk.rs` | Chunked embedding for large files | Context-aware chunks |

**Node Types (Extended)**:
```rust
enum NodeType {
    Function,      // Existing
    Struct,        // Existing
    Class,         // New
    Method,        // New
    Interface,     // New
    Import,        // New
    Variable,      // New
    Constant,      // New
    TypeDef,       // New
    Documentation, // New (docstrings, comments)
}
```

**Edge Types (Extended)**:
```rust
enum EdgeType {
    Calls,        // Existing
    Imports,      // Existing
    Defines,      // New: function defines variable
    Uses,         // New: function uses variable
    Inherits,     // New: class inherits
    Implements,   // New: class implements interface
    Contains,     // New: file contains function
    References,   // New: comment references symbol
    DataFlow,     // New: data flows between nodes
}
```

---

### 2. TSDAE Domain Adaptation (Key Differentiator)

> **This is how we beat Greptile**: They use generic embeddings. We tune on the user's actual codebase.

**What is TSDAE?**
Transformer-based Denoising AutoEncoder — an **unsupervised** method to adapt embeddings to a specific domain without labeled pairs. It works by corrupting input (deleting tokens) and training the model to reconstruct.

**Why it matters for code:**
- Generic embeddings (MiniLM, even CodeBERT) are trained on public data
- Your user's codebase has **custom naming conventions, domain-specific terms, internal APIs**
- TSDAE lets us "learn" this vocabulary without manual labeling

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    TSDAE TRAINING LOOP                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User's Codebase                                                │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   CORRUPT   │ →  │   ENCODE    │ →  │   DECODE    │          │
│  │   (delete   │    │   (base     │    │   (reconstruct)        │
│  │    tokens)  │    │    model)   │    │                        │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                            │                                    │
│                            ▼                                    │
│                    ┌─────────────┐                              │
│                    │  LOSS =     │                              │
│                    │  original   │                              │
│                    │  vs recon   │                              │
│                    └─────────────┘                              │
│                            │                                    │
│                            ▼                                    │
│                    Domain-Adapted Embeddings                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation Plan:**
```python
# scripts/tsdae_finetune.py (Phase 2)

from sentence_transformers import SentenceTransformer, models
from sentence_transformers.losses import DenoisingAutoEncoderLoss

def tsdae_adapt(codebase_path: Path, base_model: str = "nomic-ai/nomic-embed-text-v1.5"):
    """Unsupervised domain adaptation on user's codebase."""
    
    # 1. Collect all code snippets
    snippets = collect_code_snippets(codebase_path)  # function bodies, docstrings
    
    # 2. Load base model
    model = SentenceTransformer(base_model)
    
    # 3. Train with TSDAE loss (no labels needed!)
    train_dataset = DenoisingAutoEncoderDataset(snippets)
    train_loss = DenoisingAutoEncoderLoss(model, decoder_name_or_path=base_model)
    
    model.fit(
        train_objectives=[(train_dataset, train_loss)],
        epochs=1,  # Often 1 epoch is enough
        scheduler="warmuplinear"
    )
    
    # 4. Save tuned model locally
    model.save(codebase_path / ".codemonkeys" / "embedder")
```

**When to run:**
- **First `codemonkeys scan`**: Optional, adds ~2-5 min
- **Incremental**: Only on significant codebase changes
- **User opt-in**: `codemonkeys scan --tune-embeddings`

---

### 3. UMAP-Accelerated Search (10x Faster Retrieval)

**Problem:** High-dimensional vectors (768-dim+) are slow to search at scale.

**Solution:** Use UMAP to project embeddings to lower dimensions (~12-64) for fast initial retrieval, then rerank with full vectors.

**Two-Stage Search:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    UMAP-ACCELERATED SEARCH                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Query Embedding (768-dim)                                      │
│        │                                                        │
│        ├────────────────┐                                       │
│        ▼                ▼                                       │
│  ┌──────────┐    ┌──────────┐                                   │
│  │ UMAP     │    │ Full-dim │                                   │
│  │ Project  │    │ (backup) │                                   │
│  │ → 32-dim │    │          │                                   │
│  └──────────┘    └──────────┘                                   │
│        │                                                        │
│        ▼                                                        │
│  ┌──────────────────┐                                           │
│  │ FAST ANN SEARCH  │ ← Top-1000 candidates in <10ms            │
│  │ (32-dim space)   │                                           │
│  └──────────────────┘                                           │
│        │                                                        │
│        ▼                                                        │
│  ┌──────────────────┐                                           │
│  │ RERANK with      │ ← Full 768-dim cosine on top-100          │
│  │ full vectors     │                                           │
│  └──────────────────┘                                           │
│        │                                                        │
│        ▼                                                        │
│  Final top-K results                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation:**
```rust
// src/oracle/umap_index.rs

pub struct UMAPIndex {
    reducer: UMAPReducer,      // Trained on codebase embeddings
    compressed_vectors: Vec<[f32; 32]>,  // Low-dim for fast search
    full_vectors: Vec<Vec<f32>>,         // Full-dim for rerank
}

impl UMAPIndex {
    pub fn search(&self, query: &[f32], top_k: usize) -> Vec<SearchResult> {
        // 1. Project query to low-dim
        let compressed_query = self.reducer.transform(query);
        
        // 2. Fast ANN in compressed space (top-1000)
        let candidates = self.ann_search(&compressed_query, 1000);
        
        // 3. Rerank candidates with full vectors
        let reranked = candidates.into_iter()
            .map(|c| (c.id, cosine_sim(query, &self.full_vectors[c.id])))
            .sorted_by(|a, b| b.1.partial_cmp(&a.1).unwrap())
            .take(top_k)
            .collect();
        
        reranked
    }
}
```

**Bonus: Visualization**
UMAP projections can visualize "code clusters" — related modules that aren't explicitly linked.

---

### 4. Neuro-Symbolic Fusion (LLM → Graph Queries)

> **This is the killer feature**: Instead of just vector lookup, we translate natural language into structured graph traversals.

**The Problem with Vector-Only Search:**
- "What function calls the database writer?" → Vector search finds "database" mentions, misses the **call chain**
- "Show me everything related to authentication" → Finds auth files, misses **transitive dependencies**

**The Solution: LLM as Query Compiler**
Use the LLM to translate natural language into **graph queries** that traverse the AST.

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────┐
│                  NEURO-SYMBOLIC QUERY ENGINE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query: "What calls the function that writes to users?"    │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    LLM QUERY COMPILER                       ││
│  │                    (qwen2.5-coder)                          ││
│  │                                                             ││
│  │  Input: Natural language query + graph schema               ││
│  │  Output: Structured graph query                             ││
│  │                                                             ││
│  │  Example output:                                            ││
│  │  {                                                          ││
│  │    "type": "path_query",                                    ││
│  │    "start": {"pattern": "*write*user*"},                    ││
│  │    "edge": "Calls",                                         ││
│  │    "direction": "incoming",                                 ││
│  │    "depth": 2                                               ││
│  │  }                                                          ││
│  └─────────────────────────────────────────────────────────────┘│
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   GRAPH EXECUTOR                            ││
│  │                                                             ││
│  │  1. Find nodes matching "write*user*"                       ││
│  │  2. Traverse "Calls" edges backward 2 hops                  ││
│  │  3. Return path: caller → intermediate → target             ││
│  └─────────────────────────────────────────────────────────────┘│
│        │                                                        │
│        ▼                                                        │
│  Results with full call chain context                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Query Types to Support:**

| Query Type | Example Input | Graph Operation |
|------------|---------------|-----------------|
| `find_definition` | "Where is UserAuth defined?" | Node lookup by name |
| `find_callers` | "What calls validate_token?" | Incoming `Calls` edges |
| `find_callees` | "What does main() call?" | Outgoing `Calls` edges |
| `trace_path` | "How does request reach database?" | Shortest path search |
| `find_similar` | "Functions like parse_input" | Vector similarity + expand |
| `find_related` | "Everything about authentication" | Multi-hop expansion |

**LLM Prompt Template:**
```
You are a graph query compiler for a codebase. Given a natural language query,
output a structured JSON query to execute against the code graph.

Schema:
- Nodes: Function, Class, Method, Import, Variable
- Edges: Calls, Imports, Inherits, Implements, Defines, Uses, Contains

Query types:
- find_definition: Locate where a symbol is defined
- find_callers: What functions call this function
- find_callees: What functions does this call
- trace_path: Find path between two nodes
- find_similar: Vector similarity search
- find_related: Multi-hop expansion from seed nodes

User query: "{query}"

Output JSON:
```

**Implementation:**
```rust
// src/oracle/neuro_symbolic.rs

pub struct NeuroSymbolicEngine {
    llm: OllamaClient,
    graph: OracleStore,
    vector_store: VectorStore,
}

impl NeuroSymbolicEngine {
    pub async fn query(&self, natural_language: &str) -> Result<Vec<QueryResult>> {
        // 1. LLM compiles NL to structured query
        let structured = self.llm.compile_query(natural_language).await?;
        
        // 2. Execute based on query type
        match structured.query_type.as_str() {
            "find_definition" => self.find_definition(&structured),
            "find_callers" => self.find_callers(&structured),
            "trace_path" => self.trace_path(&structured),
            "find_similar" => self.find_similar(&structured).await,
            "find_related" => self.find_related(&structured).await,
            _ => self.fallback_vector_search(natural_language).await,
        }
    }
}
```

---

### 5. Rust-Native Quantized Inference

**Current bottleneck:** Python sentence-transformers is slow and adds dependency overhead.

**Solution:** Rust-native inference using Candle with quantized models.

| Framework | Pros | Cons |
|-----------|------|------|
| **Candle** (Hugging Face) | Pure Rust, CUDA/Metal, growing ecosystem | Newer, less models |
| **Burn** | Pure Rust, clean API | Even newer |
| **llama.cpp bindings** | Mature GGUF support | C++ dependency |
| **ONNX Runtime** | Wide model support | Large runtime |

**Recommended: Candle** for embedding models, **Ollama** for LLM (reranking/query compilation).

**Performance Targets:**

| Operation | Current (Python) | Target (Rust) |
|-----------|-----------------|---------------|
| Embed single snippet | ~50ms | <5ms |
| Embed 1000 snippets (batch) | ~30s | <3s |
| Index 10K file codebase | ~15 min | <2 min |

**Implementation:**
```rust
// src/oracle/embed_candle.rs

use candle_core::{Device, Tensor};
use candle_transformers::models::bert::BertModel;

pub struct CandleEmbedder {
    model: BertModel,
    tokenizer: Tokenizer,
    device: Device,
}

impl CandleEmbedder {
    pub fn embed_batch(&self, texts: &[&str]) -> Result<Vec<Vec<f32>>> {
        // 1. Tokenize batch
        let tokens = self.tokenizer.encode_batch(texts)?;
        
        // 2. Run inference on GPU/CPU
        let input_ids = Tensor::new(tokens, &self.device)?;
        let embeddings = self.model.forward(&input_ids)?;
        
        // 3. Mean pooling
        let pooled = mean_pool(&embeddings);
        
        pooled.to_vec2()
    }
}
```

---

### 6. SOTA Embedding Model Selection

**Recommendation based on research:**

| Model | Dims | Speed | Quality | Local | Our Choice |
|-------|------|-------|---------|-------|------------|
| **Jina Code V2** | 768 | ⚡ Fast | Good | ✓ ONNX | **Phase 1** |
| **Nomic Embed Code** | 768 | Medium | High | ✓ | Phase 1 alt |
| **Codestral Embed** | 1024 | Slower | SOTA | ✓ Ollama | **Phase 2** |
| **Qodo-Embed-1 1.5B** | 1536 | Slow | SOTA+ | ? GGUF | Phase 3 |

**Phase 1**: Jina Code V2 (fast, good quality, ONNX = easy Rust integration)
**Phase 2**: Fine-tune with TSDAE on user codebase
**Phase 3**: Upgrade to Codestral Embed when Candle support lands

---

### 3. Hybrid Retrieval Engine

**Current**: `query.rs` — keyword match only

**Upgrade to Triple-Path Retrieval**:

```
Query: "What handles authentication errors?"
         │
         ▼
┌────────────────────────────────────────────────────────────┐
│                    HYBRID RETRIEVER                        │
├──────────────────┬──────────────────┬─────────────────────┤
│   SEMANTIC PATH  │   LEXICAL PATH   │    GRAPH PATH       │
│                  │                  │                     │
│ embed(query) →   │ BM25 tokenize → │ NL→entities →       │
│ ANN search in    │ full-text search │ graph traversal     │
│ LanceDB          │ in SQLite FTS5   │ (calls, imports)    │
│                  │                  │                     │
│ Returns: top-K   │ Returns: top-K   │ Returns: connected  │
│ by cosine sim    │ by BM25 score    │ subgraph nodes      │
└──────────────────┴──────────────────┴─────────────────────┘
         │                  │                  │
         └──────────────────┴──────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  RRF FUSION     │
                  │                 │
                  │ 1/(k + rank_i)  │
                  │ for each path   │
                  └─────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  LLM RERANKER   │
                  │                 │
                  │ qwen2.5-coder   │
                  │ scores top-N    │
                  └─────────────────┘
                           │
                           ▼
                    Final Results
```

**Implementation**:
```rust
// src/oracle/query.rs

pub struct HybridQuery {
    pub semantic_results: Vec<ScoredResult>,
    pub lexical_results: Vec<ScoredResult>,
    pub graph_results: Vec<ScoredResult>,
}

impl QueryEngine {
    pub async fn query(&self, text: &str) -> Result<Vec<QueryResult>> {
        // 1. Parallel retrieval paths
        let (semantic, lexical, graph) = tokio::join!(
            self.semantic_search(text),
            self.lexical_search(text),
            self.graph_search(text),
        );
        
        // 2. Reciprocal Rank Fusion
        let fused = self.rrf_fusion(&semantic, &lexical, &graph);
        
        // 3. LLM Reranking (optional, configurable)
        if self.config.enable_llm_rerank {
            return self.llm_rerank(&fused, text).await;
        }
        
        Ok(fused)
    }
}
```

---

### 4. Graph Traversal Engine

**New capability**: Expand results by walking the code graph.

```rust
// src/oracle/graph_walk.rs

pub struct GraphWalker {
    store: OracleStore,
}

impl GraphWalker {
    /// Expand a node by traversing edges up to `depth` hops
    pub fn expand(&self, node_id: i64, depth: u32, edge_types: &[EdgeType]) -> Vec<GraphNode> {
        let mut visited = HashSet::new();
        let mut frontier = vec![node_id];
        let mut results = Vec::new();
        
        for _ in 0..depth {
            let mut next_frontier = Vec::new();
            for id in &frontier {
                if visited.insert(*id) {
                    if let Ok(node) = self.store.get_node(*id) {
                        results.push(node);
                    }
                    for edge_type in edge_types {
                        let neighbors = self.store.get_edges(*id, edge_type);
                        next_frontier.extend(neighbors);
                    }
                }
            }
            frontier = next_frontier;
        }
        
        results
    }
    
    /// Find call chain from A to B
    pub fn find_path(&self, from: i64, to: i64) -> Option<Vec<GraphNode>> {
        // BFS for shortest path
        // ...
    }
}
```

---

### 5. Expanded Language Support

Tree-sitter grammars to add (Phase 1):

| Language | Grammar Crate | Priority |
|----------|---------------|----------|
| TypeScript | `tree-sitter-typescript` | High |
| JavaScript | `tree-sitter-javascript` | High |
| Go | `tree-sitter-go` | High |
| Java | `tree-sitter-java` | Medium |
| C/C++ | `tree-sitter-c`, `tree-sitter-cpp` | Medium |
| Ruby | `tree-sitter-ruby` | Low |
| PHP | `tree-sitter-php` | Low |

**Implementation**: Language detection + dynamic grammar loading.

---

## Differentiators vs Greptile

| Dimension | Greptile | Oracle SOTA | Our Edge |
|-----------|----------|-------------|----------|
| **Privacy** | Cloud-hosted | 100% local | No data leaves machine |
| **Determinism** | ML-learned, drifts | Constitution-governed, reproducible | Same query → same results |
| **Graph Traversal** | Proprietary | Open code graph schema | Extensible, auditable |
| **Work Order Planning** | None | Oracle → Planner → Executor | Full automation loop |
| **Action Capability** | Read-only | Oracle feeds Heal for autonomous repair | We don't just find bugs, we fix them |
| **Fleet Intelligence** | Enterprise only | Swarm DB across products | Cross-repo pattern learning |

---

## Verification Plan

### Automated Tests

1. **Unit Tests** (extend `tests/oracle/`)
   ```bash
   conda run -n helios-gpu-118 pytest tests/oracle/ -v
   ```

2. **Indexing Benchmark**
   - Index CodeMonkeys repo (100+ files)
   - Assert: < 30s cold, < 5s incremental
   - Assert: graph hash deterministic

3. **Retrieval Quality** (new test suite)
   - Create ground-truth dataset: 50 queries → expected top-5 results
   - Assert: MRR@10 > 0.7 (Phase 1), > 0.8 (Phase 2)
   ```bash
   conda run -n helios-gpu-118 pytest tests/oracle/test_retrieval_quality.py -v
   ```

4. **Hybrid Fusion Test**
   - Query where semantic alone fails, graph expands to correct answer
   - Query where lexical alone fails, semantic finds it

### Manual Verification

1. **Interactive Q&A Demo**
   ```bash
   codemonkeys chat -q "What functions handle CI failure parsing?"
   # Expected: Shows `parser_rust.rs:parse_cargo_test_output`, related edges
   ```

2. **Graph Expansion Demo**
   ```bash
   codemonkeys chat -q "Show the call chain from heal to verify"
   # Expected: heal/loop.rs → heal/apply.rs → heal/verify.rs
   ```

---

## Implementation Phases

### Phase 1: Foundation (Sprint 11-12)
- [ ] Upgrade embedding model (Nomic Embed Code)
- [ ] Add FTS5 lexical search to SQLite
- [ ] Implement RRF fusion
- [ ] Add TypeScript/JavaScript Tree-sitter grammars
- [ ] Basic graph expansion (1-hop)

### Phase 2: Graph Intelligence (Sprint 13-14)
- [ ] Extended edge types (DataFlow, Inherits, Implements)
- [ ] Multi-hop graph traversal
- [ ] Path finding (call chains)
- [ ] LLM reranking (optional)

### Phase 3: SOTA Polish (Sprint 15+)
- [ ] Upgrade to Qodo-Embed-1 (if GGUF available)
- [ ] Query understanding (NL → structured query)
- [ ] Cross-repo graph stitching (Fleet mode)
- [ ] Benchmark against Greptile public demos

---

## Constitution Amendments Required

Add to **XVI. Codebase Oracle Principles**:

```markdown
### 5. Hybrid Query Contract
- **Triple-Path Retrieval:** Every query MUST execute semantic, lexical, and graph paths in parallel.
- **Fusion Determinism:** RRF fusion with fixed k=60 produces deterministic rankings for identical inputs.
- **Latency Budget:** Query latency MUST be < 500ms p99 for single-repo, < 2s p99 for fleet.

### 6. Embedding Model Governance  
- **Code-Specific Models:** General-purpose text embeddings (e.g., MiniLM) are forbidden for production Oracle.
- **Model Pinning:** Embedding model version MUST be pinned; model changes require schema migration.
- **Local-Only:** Cloud embedding APIs are forbidden per XVI.3.

### 7. Graph Completeness
- **Edge Coverage:** The graph MUST capture: Calls, Imports, Defines, Uses, Inherits, Implements, Contains.
- **No Orphans:** Every node MUST have at least one edge (containment at minimum).
```

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Large embedding models slow indexing | High | Batch embedding, GPU acceleration, lazy load |
| Tree-sitter grammars increase binary size | Medium | Feature flags, dynamic loading |
| RRF tuning sensitive to k parameter | Medium | Benchmark-driven tuning, configurable |
| LLM reranking adds latency | Low | Optional flag, async background rerank |

---

## Success Criteria

1. **Retrieval Quality**: MRR@10 ≥ 0.8 on benchmark dataset
2. **Latency**: < 200ms p99 for typical queries
3. **Language Coverage**: 10+ languages indexed correctly
4. **Privacy**: Zero network calls during indexing/querying
5. **Determinism**: Same codebase → same graph hash always
6. **Integration**: Heal module uses enhanced Oracle context

---

**Next Step**: Approve this design, then Phase 1 implementation begins.
