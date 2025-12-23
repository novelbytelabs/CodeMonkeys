# Code Monkeys 🚀

[![CI](https://github.com/novelbytelabs/CodeMonkeys/actions/workflows/ci.yml/badge.svg)](https://github.com/novelbytelabs/CodeMonkeys/actions/workflows/ci.yml)
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

**Code Monkeys does all of it. Automatically.**

---

## What Code Monkeys Does

| Pillar | What It Does | Your Benefit |
|--------|--------------|--------------|
| 🧠 **Oracle** | Semantic code understanding | Query your codebase in natural language |
| 🩺 **Heal** | LLM-powered CI repair | Wake up to green builds |
| 📚 **Docs** | Living documentation | README never goes stale |
| 🚀 **Ship** | Governed releases | One-click publish with guardrails |
| 👁️ **Watch** | Always-on monitoring | Catches issues before you do |

---

## Why Code Monkeys?

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
Code Monkeys: Detected CI failure (E0308: type mismatch)
Code Monkeys: Generated fix via Qwen-7B
Code Monkeys: Applied fix, verified, committed
Code Monkeys: All tests passing ✅
You: *wake up* → Green CI, fixed code, audit log
```

**Demo it yourself:**
```bash
# Create a broken test
echo 'fn add(a: i32, b: i32) -> i32 { a - b // bug' > tests/broken.rs

# Generate failure log
cargo test --message-format=json > fail.json

# Watch Code Monkeys fix it
codemonkeys heal --log-file fail.json
```

---

## Quick Start

```bash
# Install
cargo install --path .

# Initialize
codemonkeys init

# Scan your codebase
codemonkeys scan

# Query your code
codemonkeys chat -q "What functions handle errors?"

# Self-heal failures
codemonkeys heal --log-file test.json

# Ship a release
codemonkeys ship --dry-run
```

---

## Commands

| Command | Description |
|---------|-------------|
| `codemonkeys init` | Initialize Code Monkeys in current repo |
| `codemonkeys scan` | Build Codebase Oracle (parse → graph → embed) |
| `codemonkeys chat` | Query codebase with natural language |
| `codemonkeys heal` | Autonomous self-healing for CI failures |
| `codemonkeys ship` | Governed release pipeline |
| `codemonkeys watch` | *(Coming)* Always-on daemon mode |

---

## The Vision: Solo Product Factory

Code Monkeys is part of a larger system:

| Layer | Product | Job |
|-------|---------|-----|
| Bootstrap | **CodeMonkeysInit** | 0 → working repo |
| Front Half | **CodeMonkeysDev** | Spec → Plan → Tasks |
| Back Half | **Code Monkeys** | Heal → Docs → Ship |
| Fleet | **CodeMonkeysOrg** | 50+ products at once |

**You write Constitution + Spec. The system does the rest.**

---

## Documentation

- [Architecture](https://novelbytelabs.github.io/Code Monkeys/architecture)
- [CLI Reference](https://novelbytelabs.github.io/Code Monkeys/cli-reference)
- [Configuration](https://novelbytelabs.github.io/Code Monkeys/configuration)
- [Developer Guide](https://novelbytelabs.github.io/Code Monkeys/developer-guide)

---

## Requirements

- Rust 1.82+
- Ollama with `qwen2.5-coder:7b-instruct`
- ~2GB disk for models

---

## License

Copyright 2024 Novel Byte Labs. Apache 2.0.
