# Contributing to Code Monkeys

Thank you for your interest in contributing to Code Monkeys!

## Development Setup

```bash
# Clone
git clone https://github.com/novelbytelabs/Code Monkeys.git
cd Code Monkeys

# Build
cargo build

# Test
cargo test

# Lint
cargo clippy -- -D warnings
cargo fmt --check
```

## Code Style

- Run `cargo fmt` before committing
- All code must pass `cargo clippy -- -D warnings`
- Follow Rust naming conventions

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit with conventional commits (`feat:`, `fix:`, `docs:`, etc.)
4. Push and open a PR
5. Wait for CI to pass
6. Request review

## Reporting Issues

- Check existing issues first
- Use issue templates
- Include reproduction steps

## License

By contributing, you agree that your contributions will be licensed under Apache 2.0.
