# Code Monkeys Org + Ship: Fleet Architecture

## Confirmed Decisions

| Question | Answer |
|----------|--------|
| Products to manage | 50+ across multiple companies |
| Trigger mode | **Hybrid**: GitHub Actions + webhooks + cron fallback |
| Cross-repo memory | **SQLite** (structured) + **LanceDB** (vectors) |
| Wow moments | All 3: heal-while-sleep, auto-release, cross-repo docs |

---

## Two-Layer Model

```
┌───────────────────────────────────────────────┐
│              Code Monkeys  ORG                │
│  Fleet registry + Swarm DB + Cross-repo ops   │
└───────────────────┬───────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────┐     ┌────────┐     ┌────────┐
│  Ship  │     │  Ship  │     │  Ship  │
│ (repo1)│     │ (repo2)│     │ (repoN)│
└────────┘     └────────┘     └────────┘
              ↓ Telemetry ↓
           ┌─────────────────┐
           │    Swarm DB     │
           │ SQLite+LanceDB  │
           └─────────────────┘
```

---

## Trigger Modes (Hybrid)

| Mode | Trigger | Best For |
|------|---------|----------|
| **GitHub Actions** | CI failure event | Zero-setup, runs in CI |
| **Webhooks** | Push/PR/release events | Real-time local response |
| **Cron** | Time-based polling | Fallback, offline mode |

---

## Code Monkeys Ship Pillars

| Pillar | Job |
|--------|-----|
| Oracle | Code graph + semantic vectors |
| Heal | LLM repair + verify + rollback |
| Docs | Living documentation |
| Ship | Auto-release when gates pass |
| Publish | Packages (crates.io, PyPI, Docker) |
| Announce | Website, Release notes, marketing copy |
| Monitor | Telemetry, health checks |

---

## Swarm DB

| Store | Data | Path |
|-------|------|------|
| SQLite | Error patterns, fix templates, fleet registry | `~/.codemonkeys/swarm.db` |
| LanceDB | Semantic embeddings | `~/.codemonkeys/swarm_vectors/` |

---