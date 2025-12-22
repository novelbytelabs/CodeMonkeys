# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.4.0] - 2025-12-22
### Added
- **Release Gate Enforcement**: `codemonkeys ship` command enforces preflight checks before tagging.
- **Preflight Check**: `scripts/preflight_check.py` validates git cleanliness and Silverback compliance.
- **Ship Command**: `src/codemonkeys/commands/ship.py` with `--dry-run` and `--force` options.
- **Release Gate Tests**: `tests/gates/test_release_gate.py` verifies gate behavior.
- **DEC-0005 Naming Decision**: Arqon/ArqonShip forbidden; Code Monkeys is official identity.

### Changed
- **Naming Refactor**: Converted 409 Arqon/ArqonShip references to Code Monkeys/codemonkeys.
- **Product ID**: Renamed `arqonship-cli` to `codemonkeys-cli` in Dash registry.

### Removed
- `.arqonship/` legacy configuration directory.

## [v0.3.0] - 2024-12-19

### Added
- Initial release
- Codebase Oracle: Tree-sitter parsing, Graph extraction, Vector embeddings
- Self-Healing CI: Log parsing, Context building, LLM integration (stub)
- Governed Releases: Constitution checks, SemVer, Changelog generation
- CLI commands: `init`, `scan`, `chat`, `heal`, `ship`
