# ArqonShip Orchestrator Architecture

> **Synthesized from:** Gemini, Grok, GPT-5.2 (2025-12-20)
> **Pattern:** Hybrid (Central Coordinator + Distributed Workers)

---

## 🎯 The Unanimous Verdict

All three AIs converged on the **same architecture pattern**: **Hybrid**

| Aspect | Consensus |
|--------|-----------|
| **Pattern** | Central Coordinator + Distributed Workers |
| **Core Service** | Rust/Tokio async service |
| **State** | Database (SQLite for MVP, Postgres for scale) |
| **Events** | GitHub webhooks + periodic polling fallback |
| **Workers** | Tokio async tasks with Semaphore limits |

---

## 1. Architecture Pattern: Hybrid

### The Model

```
┌─────────────────────────────────────────────────────────────┐
│                    THE ADMIRAL (Coordinator)                 │
│  - Holds "Campaign State" (phase, PR count)                  │
│  - Webhook receiver (GitHub events)                          │
│  - Job scheduler (creates scan/PR tasks)                     │
│  - Triage API + dashboard backend                            │
│  - Global Kill Switch (stops all PRs instantly)              │
└─────────────────────────────────────────────────────────────┘
                            ↓ (enqueues jobs)
┌─────────────────────────────────────────────────────────────┐
│              THE MARINES (Distributed Workers)               │
│  - Stateless async Tokio tasks                               │
│  - Clone repos, run Oracle scans                             │
│  - Generate fixes via Heal module                            │
│  - Create draft PRs via GitHub API                           │
│  - Report violations back to Admiral                         │
└─────────────────────────────────────────────────────────────┘
```

### Why Hybrid Wins

| Alternative | Why Rejected |
|-------------|--------------|
| Pure Central Command | Bottleneck for 50 repos, single point of failure |
| Pure Stigmergic | Hard to coordinate canary ladder, debug failures |
| **Hybrid** | ✅ Central control + parallel execution + failure isolation |

---

## 2. Technology Stack

### Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Coordinator Binary** | Rust/Tokio + Axum | Event loop, webhooks, scheduling |
| **Worker Pool** | Tokio spawn + Semaphore | Parallel repo scanning |
| **State Database** | Postgres | Rule state, PR status, canary progress |
| **GitHub Integration** | Octocrab crate | API client with rate limiting |
| **Event Source** | GitHub App webhooks | Primary trigger |
| **Fallback Polling** | tokio::interval (15min) | Reconciliation |

### Database Schema (Core Tables)

```sql
-- Rule management
CREATE TABLE rules (
    id TEXT PRIMARY KEY,
    pack_id TEXT NOT NULL,
    schema_version INTEGER,
    content_hash TEXT,
    created_at TIMESTAMP
);

-- Campaign tracking
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY,
    rule_id TEXT NOT NULL,
    phase TEXT NOT NULL, -- 'canary', 'early', 'mid', 'fleet', 'suspended'
    active_prs JSON,     -- Array of GitHub PR IDs
    successful_merges INTEGER DEFAULT 0,
    config JSON,         -- Rollout configuration
    FOREIGN KEY (rule_id) REFERENCES rules(id)
);

-- Violation tracking (fingerprinting)
CREATE TABLE violations (
    fingerprint TEXT PRIMARY KEY,
    repo TEXT NOT NULL,
    file_path TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    state TEXT NOT NULL, -- 'open', 'in_pr', 'resolved', 'ignored'
    ignored_at TIMESTAMP,
    FOREIGN KEY (rule_id) REFERENCES rules(id)
);

-- PR tracking
CREATE TABLE prs (
    id INTEGER PRIMARY KEY,
    campaign_id INTEGER NOT NULL,
    repo TEXT NOT NULL,
    pr_number INTEGER NOT NULL,
    branch TEXT NOT NULL,
    state TEXT NOT NULL,
    checks_status TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Job queue (SKIP LOCKED pattern)
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL, -- 'scan_repo', 'create_pr', 'monitor_pr'
    payload JSON NOT NULL,
    priority INTEGER DEFAULT 0,
    scheduled_at TIMESTAMP,
    lease_until TIMESTAMP,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3
);
```

---

## 3. Canary Ladder Implementation

### The State Machine

```rust
#[derive(Debug, PartialEq, Serialize, Deserialize)]
pub enum CampaignPhase {
    Draft,           // Rule loaded, inactive
    Canary,          // 1 repo (canary_targets)
    EarlyAdopters,   // 3 repos
    MidWave,         // 10 repos
    FleetRollout,    // All remaining repos
    Completed,
    Suspended(String), // Reason for suspension
}
```

### Promotion Flow

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE: Canary                                               │
│  ├─ SELECT repo FROM canary_targets (1 repo)                │
│  ├─ CREATE draft PR                                          │
│  ├─ WAIT for CI green + human approval                       │
│  └─ IF success → PROMOTE to EarlyAdopters                    │
├─────────────────────────────────────────────────────────────┤
│  PHASE: EarlyAdopters                                        │
│  ├─ SELECT 3 repos (deterministic random)                    │
│  ├─ CREATE draft PRs                                         │
│  ├─ WAIT for 80% success rate                                │
│  └─ IF success → PROMOTE to MidWave                          │
├─────────────────────────────────────────────────────────────┤
│  PHASE: MidWave                                              │
│  ├─ SELECT 10 repos                                          │
│  ├─ CREATE draft PRs (respecting max_open_prs)              │
│  ├─ WAIT for 90% success rate                                │
│  └─ IF success → PROMOTE to FleetRollout                     │
├─────────────────────────────────────────────────────────────┤
│  PHASE: FleetRollout                                         │
│  ├─ SELECT remaining repos                                   │
│  ├─ CREATE draft PRs (batch with rate limiting)             │
│  └─ WAIT for completion → Completed                          │
└─────────────────────────────────────────────────────────────┘
```

### Success Criteria

| Metric | Definition |
|--------|------------|
| **PR Success** | CI passes + merged OR explicitly approved |
| **Phase Success** | >80% of PRs successful + 24h observation window |
| **Failure Signal** | CI fails OR PR closed without merge OR human reject |

### Rollback Mechanism

If any phase fails:
1. Set `campaign.phase = Suspended("Canary failed: CI red")`
2. Close all open PRs for this campaign
3. Create GitHub issue in rule repo with diagnostics
4. Notify rule owners
5. Require human approval to retry

---

## 4. Rust Module Structure

```
src/
├── orchestrator/
│   ├── mod.rs              // Public API
│   ├── main.rs             // Binary entry point
│   │
│   ├── db/
│   │   ├── mod.rs
│   │   ├── models.rs       // Rule, Campaign, PR, Violation structs
│   │   ├── queries.rs      // SQL queries (sqlx)
│   │   └── migrations/     // Database schema versions
│   │
│   ├── github/
│   │   ├── mod.rs
│   │   ├── client.rs       // Octocrab wrapper with rate limiting
│   │   ├── webhooks.rs     // Webhook handlers (Axum routes)
│   │   └── rate_limit.rs   // Token bucket (governor crate)
│   │
│   ├── engine/
│   │   ├── mod.rs
│   │   ├── coordinator.rs  // Main event loop
│   │   ├── scheduler.rs    // Job creation logic
│   │   └── reconciler.rs   // Periodic state sync
│   │
│   ├── campaign/
│   │   ├── mod.rs
│   │   ├── state_machine.rs // CampaignPhase transitions
│   │   ├── planner.rs       // Repo selection (canary ladder)
│   │   └── safety.rs        // max_open_prs enforcement
│   │
│   ├── worker/
│   │   ├── mod.rs
│   │   ├── scanner.rs       // Calls oracle::analyze()
│   │   ├── healer.rs        // Calls heal::propose_fix()
│   │   ├── pr_creator.rs    // GitHub PR creation
│   │   └── monitor.rs       // CI/review status polling
│   │
│   └── api/
│       ├── mod.rs
│       ├── dashboard.rs     // Triage UI endpoints
│       └── admin.rs         // Promote/pause/rollback controls
│
├── oracle/                  // (Existing) Code analysis
├── heal/                    // (Existing) Fix generation
└── ship/                    // (Existing) Release automation
```

---

## 5. Safety Mechanisms

### A. Max Open PRs Enforcement

**Two-Level Guard:**

1. **Coordinator Level** (before job enqueue):
```rust
pub fn can_create_pr(&self, campaign_id: i64) -> bool {
    let open_count = self.db.count_open_prs(campaign_id);
    let limit = self.db.get_campaign_limit(campaign_id);
    open_count < limit
}
```

2. **Database Level** (transactional):
```sql
BEGIN TRANSACTION;
SELECT COUNT(*) FROM prs 
WHERE campaign_id = ? AND state = 'open' 
FOR UPDATE;  -- Lock to prevent race

-- If count < limit:
INSERT INTO prs (...);
COMMIT;
```

### B. Fingerprint Deduplication

**Prevent Re-Opening Fixed PRs:**

```rust
pub fn should_create_pr(&self, violation: &Violation) -> bool {
    // Check if already handled
    match self.db.get_violation_state(&violation.fingerprint) {
        Some(ViolationState::InPR) => false,      // Already has PR
        Some(ViolationState::Resolved) => false,  // Fixed
        Some(ViolationState::Ignored) => false,   // Suppressed
        _ => true                                  // New violation
    }
}
```

### C. GitHub API Rate Limiting

**Token Bucket + Exponential Backoff:**

```rust
use governor::{Quota, RateLimiter};

static GITHUB_LIMITER: Lazy<RateLimiter<...>> = Lazy::new(|| {
    RateLimiter::direct(Quota::per_hour(NonZeroU32::new(4000).unwrap()))
});

pub async fn create_pr(...) -> Result<()> {
    GITHUB_LIMITER.until_ready().await; // Blocks if limit reached
    
    match octocrab.pulls(...).send().await {
        Err(e) if e.is_rate_limit() => {
            tokio::time::sleep(Duration::from_secs(60)).await;
            retry()
        }
        result => result
    }
}
```

### D. Cascading Failure Prevention

**Circuit Breaker Pattern:**

```rust
pub struct Campaign {
    consecutive_ci_failures: u32,
}

impl Campaign {
    pub fn record_ci_failure(&mut self) {
        self.consecutive_ci_failures += 1;
        
        if self.consecutive_ci_failures > 3 {
            self.phase = CampaignPhase::Suspended(
                "High CI failure rate detected".to_string()
            );
        }
    }
}
```

### E. Global Kill Switch

**Instant PR Creation Stop:**

```rust
// In Coordinator
pub fn emergency_stop(&mut self) {
    self.global_pause = true;
    // All workers check this before creating PRs
}

// In Worker
pub async fn create_pr_with_safety(&self, ...) -> Result<()> {
    if self.coordinator.is_globally_paused() {
        return Err("Global pause active");
    }
    // ... proceed
}
```

---

## 6. Deployment Model

### Local-First Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Your Infrastructure (Self-Hosted)                      │
│                                                          │
│  ┌────────────────┐       ┌────────────────┐            │
│  │  Coordinator   │◄─────►│   SQLite/      │            │
│  │  (Rust binary) │       │   Postgres     │            │
│  └────────────────┘       └────────────────┘            │
│         ↑ ↓                                              │
│  ┌────────────────┐       ┌────────────────┐            │
│  │  Worker Pool   │       │  Repo Mirror   │            │
│  │  (4-12 tasks)  │       │  Cache         │            │
│  └────────────────┘       └────────────────┘            │
└─────────────────────────────────────────────────────────┘
                    ↕ (webhooks + API calls)
┌─────────────────────────────────────────────────────────┐
│  GitHub.com (50+ private repos)                         │
└─────────────────────────────────────────────────────────┘
```

**No cloud lock-in:**
- ✅ Runs on single machine or VM
- ✅ No AWS/GCP/Azure dependencies
- ✅ All state in local database
- ✅ GitHub App = only external dependency

---

## Summary: The Orchestrator in 5 Points

1. **Hybrid Architecture**: Central brain, distributed workers
2. **Database State Machine**: All campaign state in SQL (ACID guarantees)
3. **Canary Ladder**: Explicit 4-phase rollout with human gates
4. **Safety First**: Max PR limits, fingerprinting, rate limiting, circuit breakers
5. **Local-First**: Self-hostable Rust binary, no cloud dependencies
