# ArqonShip 🚀

[![CI](https://github.com/novelbytelabs/ArqonShip/actions/workflows/ci.yml/badge.svg)](https://github.com/novelbytelabs/ArqonShip/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/rust-1.82%2B-orange.svg)](https://www.rust-lang.org/)

> **The Solo Product Factory**: Constitution-governed automation that fixes bugs while you sleep, ships releases automatically, and scales to 50+ products.

---

## The Problem

You're building multiple products. Every repo needs:
- CI that stays green
- Docs that don't drift
- Releases that follow the rules
- Hours of maintenance you don't have

**ArqonShip does all of it. Automatically.**

---

## What ArqonShip Does

| Pillar | What It Does | Your Benefit |
|--------|--------------|--------------|
| 🧠 **Oracle** | Semantic code understanding | Query your codebase in natural language |
| 🩺 **Heal** | LLM-powered CI repair | Wake up to green builds |
| 📚 **Docs** | Living documentation | README never goes stale |
| 🚀 **Ship** | Governed releases | One-click publish with guardrails |
| 👁️ **Watch** | Always-on monitoring | Catches issues before you do |

---

## Why ArqonShip?

### 🏠 100% Local
Your code never leaves your machine. Runs on your hardware with Ollama.

### 📜 Constitution-Governed
Every action follows your rules. No surprises. Full audit trail.

### 🔄 Self-Healing
Compiler error at 3am? Fixed by 3:01am. Automatically.

### 🌐 Fleet-Ready
One product or fifty. Same workflow. Swarm intelligence across repos.

---

## Proof It Works

```
You: *sleeping*
ArqonShip: Detected CI failure (E0308: type mismatch)
ArqonShip: Generated fix via Qwen-7B
ArqonShip: Applied fix, verified, committed
ArqonShip: All tests passing ✅
You: *wake up* → Green CI, fixed code, audit log
```

**Demo it yourself:**
```bash
# Create a broken test
echo 'fn add(a: i32, b: i32) -> i32 { a - b // bug' > tests/broken.rs

# Generate failure log
cargo test --message-format=json > fail.json

# Watch ArqonShip fix it
arqon heal --log-file fail.json
```

---

## Quick Start

```bash
# Install
cargo install --path .

# Initialize
arqon init

# Scan your codebase
arqon scan

# Query your code
arqon chat -q "What functions handle errors?"

# Self-heal failures
arqon heal --log-file test.json

# Ship a release
arqon ship --dry-run
```

---

## Commands

| Command | Description |
|---------|-------------|
| `arqon init` | Initialize ArqonShip in current repo |
| `arqon scan` | Build Codebase Oracle (parse → graph → embed) |
| `arqon chat` | Query codebase with natural language |
| `arqon heal` | Autonomous self-healing for CI failures |
| `arqon ship` | Governed release pipeline |
| `arqon watch` | *(Coming)* Always-on daemon mode |

---

## The Vision: Solo Product Factory

ArqonShip is part of a larger system:

| Layer | Product | Job |
|-------|---------|-----|
| Bootstrap | **ArqonInit** | 0 → working repo |
| Front Half | **ArqonDev** | Spec → Plan → Tasks |
| Back Half | **ArqonShip** | Heal → Docs → Ship |
| Fleet | **ArqonOrg** | 50+ products at once |

**You write Constitution + Spec. The system does the rest.**

---

## Documentation

- [Architecture](https://novelbytelabs.github.io/ArqonShip/architecture)
- [CLI Reference](https://novelbytelabs.github.io/ArqonShip/cli-reference)
- [Configuration](https://novelbytelabs.github.io/ArqonShip/configuration)
- [Developer Guide](https://novelbytelabs.github.io/ArqonShip/developer-guide)

---

## Requirements

- Rust 1.82+
- Ollama with `qwen2.5-coder:7b-instruct`
- ~2GB disk for models

---

## License

Copyright 2024 Novel Byte Labs. Apache 2.0.
