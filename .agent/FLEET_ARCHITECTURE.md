# CodeMonkeysOrg + Code Monkeys: Fleet Architecture

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

## Code Monkeys Pillars

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
| SQLite | Error patterns, fix templates, fleet registry | `~/.codemonkeys/swarm.db` |
| LanceDB | Semantic embeddings | `~/.codemonkeys/swarm_vectors/` |

---

## Next Implementation Steps

1. **`codemonkeys watch`** — event listener mode
2. **GitHub Action** — `codemonkeys heal` on CI failure
3. **`codemonkeys ship --auto`** — release when green
4. **Swarm DB** — shared cross-repo memory
5. **CodeMonkeysOrg CLI** — fleet commands
