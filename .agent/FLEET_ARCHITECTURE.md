# ArqonOrg + ArqonShip: Fleet Architecture

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
│              ARQON ORG                        │
│  Fleet registry + Swarm DB + Cross-repo ops  │
└───────────────────┬───────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────┐     ┌────────┐     ┌────────┐
│ArqonShip     │ArqonShip     │ArqonShip
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

## ArqonShip Pillars

| Pillar | Job |
|--------|-----|
| Oracle | Code graph + semantic vectors |
| Heal | LLM repair + verify + rollback |
| Docs | Living documentation |
| Ship | Auto-release when gates pass |
| Watch | Event listener (hybrid triggers) |

---

## Swarm DB

| Store | Data | Path |
|-------|------|------|
| SQLite | Error patterns, fix templates, fleet registry | `~/.arqonship/swarm.db` |
| LanceDB | Semantic embeddings | `~/.arqonship/swarm_vectors/` |

---

## Next Implementation Steps

1. **`arqonship watch`** — event listener mode
2. **GitHub Action** — `arqonship heal` on CI failure
3. **`arqonship ship --auto`** — release when green
4. **Swarm DB** — shared cross-repo memory
5. **ArqonOrg CLI** — fleet commands
