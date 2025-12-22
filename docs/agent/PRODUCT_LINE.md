# Novel Byte Labs: Product Line Structure

> *Building the tools that build software*

---

## The Umbrella

| Entity | Role |
|--------|------|
| **Novel Byte Labs** | Parent company / organization |

---

## Product Lines

### 1. Code Monkeys (MAS Division)
**Focus:** Multi-Agent Systems & Runtime Optimization

| Product | Engine | Binary | Purpose |
|---------|--------|--------|---------|
| **Code Monkeys Factory** | CodeMonkeys | `codemonkeys` | Probe-gated optimization, runtime adaptation |

**Tagline:** *"Runtime optimization infrastructure for live production systems."*

---

### 2. CodeMonkeys (DevSecOps Division)
**Focus:** Autonomous Software Development Automation

| Product | Engine | Binary | Purpose |
|---------|--------|--------|---------|
| **CodeMonkeys** | (standalone) | `codemonkeys` | Governance, healing, chaos testing |

**Tagline:** *"The Autonomous Software Troop."*

**The Troop:**

- 🦍 **Silverback** — Governance (`check`)
- 🐒 **Code Monkey** — Builder (`heal`)
- 🦧 **Foreman** — Planner (`plan`)
- 🐵 **Chaos Monkey** — Fuzzer (`chaos`) [v0.2]
- 🐵 **Scout** — Reconnaissance (`scout`) [v0.2]

---

## Branding Guidelines

### Novel Byte Labs
- **Usage:** Copyright notices, legal, "A Novel Byte Labs project"
- **Style:** Professional, understated

### Code Monkeys
- **Usage:** MAS/optimization products only
- **Style:** Enterprise, technical, performance-focused
- **Colors:** Dark mode, blues/purples

### CodeMonkeys
- **Usage:** DevSecOps automation
- **Style:** Professional by default, playful with `--fun` mode
- **Mascot:** 🐒 (Monkey emoji family)
- **Economy:** 🍌 (Banana tokens)

---

## Repository Structure

```
github.com/novelbytelabs/
├── CodeMonkeys/           # Rust core for runtime optimization
├── CodeMonkeys/        # DevSecOps automation (formerly Code Monkeys)
└── (other projects)
```

---

## Note on Code Monkeys

**Code Monkeys** was the original codename for CodeMonkeys during development.
It is now **deprecated** as a product name.

---

**Version:** 1.0.0
**Date:** 2025-12-20
