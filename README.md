# ArqonShip 🚀

[![CI](https://github.com/novelbytelabs/ArqonShip/actions/workflows/ci.yml/badge.svg)](https://github.com/novelbytelabs/ArqonShip/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/rust-1.82%2B-orange.svg)](https://www.rust-lang.org/)

**DevSecOps CLI for Intelligent Codebase Understanding, Self-Healing CI, and Governed Releases**

## Features

- 🔍 **Codebase Oracle** - Semantic code search via graph + vector duality
- 🔧 **Self-Healing CI** - Autonomous repair of test failures using local AI
- 🚀 **Governed Releases** - Constitution-compliant release pipeline

## Installation

```bash
# From source
cargo install --path .

# Or build locally
cargo build --release
./target/release/arqon --help
```

## Quick Start

```bash
# Initialize in your project
arqon init

# Scan your codebase
arqon scan

# Query your code
arqon chat -q "How does error handling work?"

# Self-heal test failures
cargo test --message-format=json > test.json
arqon heal --log-file test.json

# Create a governed release
arqon ship --dry-run
```

## Commands

| Command | Description |
|---------|-------------|
| `arqon init` | Initialize ArqonShip in current repository |
| `arqon scan` | Build Codebase Oracle (parse, graph, embed) |
| `arqon chat` | Query codebase with natural language |
| `arqon heal` | Autonomous self-healing for test failures |
| `arqon ship` | Governed release pipeline |

## Documentation

- [Architecture](docs/architecture.md)
- [CLI Reference](docs/cli-reference.md)
- [Configuration](docs/configuration.md)
- [Developer Guide](docs/developer-guide.md)

## Requirements

- Rust 1.82+
- ~2GB disk space for AI models

## License

Copyright 2024 Novel Byte Labs

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
