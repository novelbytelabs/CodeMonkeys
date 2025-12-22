# Code Monkeys Architecture

## Overview

Code Monkeys is a DevSecOps automation system implementing three core capabilities:

1. **Codebase Oracle** - Intelligent code understanding via graph + vector duality
2. **Self-Healing CI** - Autonomous repair of test failures
3. **Governed Releases** - Constitution-compliant release pipeline

![Code Monkeys Architecture](../assets/images/diagram-CodeMonkeysCLI.svg)

## Module Architecture

### Oracle Module (`crates/ship/src/oracle/`)

Provides intelligent codebase understanding through dual indexing:

| Component | Responsibility |
|-----------|---------------|
| `parser.rs` | Tree-sitter AST parsing for Rust |
| `parser_py.rs` | Tree-sitter AST parsing for Python |
| `graph.rs` | Extract code entities (functions, structs, classes) |AC
| `edges.rs` | Extract relationships (calls, imports) |
| `store.rs` | SQLite persistence for graph data |
| `schema.rs` | Database schema migrations |
| `embed.rs` | Candle-based embedding generation (MiniLM) |
| `vector_store.rs` | LanceDB for approximate nearest neighbor search |
| `query.rs` | Hybrid query combining graph + vector results |
| `hash.rs` | Deterministic content hashing for incremental updates |
| `incremental.rs` | Skip unchanged files during re-scans |

**Data Flow:**
```
Source Files → Parser → AST → GraphBuilder → Nodes/Edges → SQLite
                    ↓
              Embedder → Vectors → LanceDB
```

### Heal Module (`crates/ship/src/heal/`)

Implements autonomous self-healing per Constitution XVII:

| Component | Responsibility |
|-----------|---------------|
| `parser_rust.rs` | Parse `cargo test --message-format=json` |
| `parser_py.rs` | Parse pytest output |
| `context.rs` | Build repair context from Oracle |
| `llm.rs` | LLM trait + Candle implementation |
| `prompts.rs` | Repair prompt templates |
| `loop.rs` | Healing state machine (max 2 attempts) |
| `apply.rs` | Apply fixes using whole-block replacement |
| `verify.rs` | Gate: compile + lint + test |
| `audit.rs` | Log all attempts to SQLite |

**State Machine:**
```
ANALYZE → BUILD_CONTEXT → GENERATE_PROMPT → LLM_INFERENCE 
    ↓                                           ↓
    ← ← ← ← VERIFY ← ← APPLY_FIX ← ← ← ← ← ← ← ←
              ↓
         SUCCESS or MAX_ATTEMPTS_EXCEEDED
```

### Ship Module (`crates/ship/src/ship/`)

Implements governed releases per Constitution XVIII:

| Component | Responsibility |
|-----------|---------------|
| `checks.rs` | Pre-flight: clean git, passing tests, no untagged debt |
| `commits.rs` | Parse conventional commit history |
| `version.rs` | Calculate next SemVer version |
| `github.rs` | Create release PR via GitHub API |

## Data Storage

### Graph Database (SQLite)

```sql
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    path TEXT NOT NULL,
    type TEXT NOT NULL,      -- 'function', 'struct', 'impl'
    name TEXT NOT NULL,
    start_line INTEGER,
    end_line INTEGER,
    signature_hash TEXT,
    docstring TEXT
);

CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    source_id INTEGER REFERENCES nodes(id),
    target_id INTEGER REFERENCES nodes(id),
    type TEXT NOT NULL       -- 'calls', 'imports'
);

CREATE TABLE healing_attempts (
    run_id TEXT PRIMARY KEY,
    timestamp TEXT,
    file_path TEXT,
    error_msg TEXT,
    prompt_hash TEXT,
    diff_hash TEXT,
    outcome TEXT
);
```

### Vector Database (LanceDB)

```
Schema: code_vectors
├── id: Int64 (node ID)
├── vector: FixedSizeList[Float32, 384] (MiniLM embeddings)
└── text: Utf8 (code snippet)
```

## Constitution Alignment

| Section | Principle | Implementation |
|---------|-----------|----------------|
| XVI.1 | Graph + Vector duality | SQLite + LanceDB dual storage |
| XVI.2 | Deterministic hashing | SHA256 content hash in `hash.rs` |
| XVII.1 | Max 2 healing attempts | `HealingLoop.max_attempts = 2` |
| XVII.2 | Verification gate | `VerificationGate` (compile + lint + test) |
| XVII.3 | Whole-block replacement | `apply.rs` replaces entire files |
| XVII.4 | Audit logging | `audit.rs` → healing_attempts table |
| XVIII.1 | Pre-flight checks | `ConstitutionCheck.run_all()` |
| XVIII.2 | SemVer from commits | `calculate_next_version()` |
| XIX.1 | Structured CLI | Clap with subcommands |
| XIX.2 | Exit codes | 0=success, 1=failure |

## Performance Considerations

- **Incremental scanning**: Only re-parse changed files (hash-based)
- **Lazy model loading**: Embedding model loaded on first use
- **Batch vector inserts**: LanceDB batch operations
- **Async I/O**: Tokio runtime for concurrent operations

---

## Fleet Architecture (Moonshot)

Code Monkeys is designed to scale from a single product to 50+ products across multiple companies.

### Two-Layer Model

```
┌───────────────────────────────────────────────┐
│              CODEMONKEYS ORG                        │
│  Fleet registry + Swarm DB + Cross-repo ops  │
└───────────────────┬───────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────┐     ┌────────┐     ┌────────┐
│Code Monkeys     │Code Monkeys     │Code Monkeys
│ (repo1)│     │ (repo2)│     │ (repoN)│
└────────┘     └────────┘     └────────┘
```

### Code Monkeys Pillars

| Pillar | Job |
|--------|-----|
| **Oracle** | Code graph + semantic vectors |
| **Heal** | LLM repair + verify + rollback |
| **Docs** | Living documentation |
| **Ship** | Auto-release when gates pass |
| **Watch** | Event listener (hybrid triggers) |

### Trigger Modes (Hybrid)

| Mode | Trigger | Best For |
|------|---------|----------|
| **GitHub Actions** | CI failure event | Zero-setup, runs in CI |
| **Webhooks** | Push/PR/release events | Real-time local response |
| **Cron** | Time-based polling | Fallback, offline mode |

### Swarm Intelligence

Each Code Monkeys instance shares telemetry with a central Swarm DB:

| Store | Data | Path |
|-------|------|------|
| SQLite | Error patterns, fix templates | `~/.codemonkeys/swarm.db` |
| LanceDB | Semantic embeddings | `~/.codemonkeys/swarm_vectors/` |

Patterns learned in one repo inform fixes in all others.

### CodeMonkeysOrg Capabilities

- **Fleet Registry**: All companies, products, repos
- **Multi-Account Auth**: Different GitHub tokens per org
- **Cross-Repo Ops**: `codemonkeysorg apply --all`
- **Dashboard**: Fleet health at a glance

### Moonshot Goals

1. **Fix bugs while you sleep** — Daemon heals CI failures overnight
2. **Auto-cut releases** — Ship when all gates pass
3. **Cross-repo docs** — Update 50 READMEs at once

