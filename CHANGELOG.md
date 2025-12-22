# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.3.0] - 2025-12-22
### Added
- **Constitution Enforcement**: Silverback now validates the `Constitution > Dossier > Spec` authority chain.
- **Governed Docs Registry**: `docs/pm/GOVERNED_DOCS.md` lists mandatory "law" documents.
- **Silverback Validator**: Updated rules to check Dossier governance refs and Spec constitution headers.
- **Nexus Escalation**: Validation failures now trigger `clarification_required` Nexus requests.
- **Bootstrap Constitution**: Created initial `constitution.md`.
- **Dossier Intake**: Restored and integrated Design Dossier CLI commands (`new`, `validate`, `to-spec`).

## [0.1.0] - 2024-12-19

### Added
- Initial release
- Codebase Oracle: Tree-sitter parsing, Graph extraction, Vector embeddings
- Self-Healing CI: Log parsing, Context building, LLM integration (stub)
- Governed Releases: Constitution checks, SemVer, Changelog generation
- CLI commands: `init`, `scan`, `chat`, `heal`, `ship`
