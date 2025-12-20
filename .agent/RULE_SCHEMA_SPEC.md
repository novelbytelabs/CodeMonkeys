# Living Linter Rule Schema Specification

> **Version:** 1.0  
> **Synthesized from:** GPT-5.2, Grok, Gemini, Copilot (2025-12-20)

---

## Design Principles

1. **Engine-Agnostic**: Same rule can have detectors for Semgrep, tree-sitter, or CodeQL
2. **Scoping First-Class**: Languages, paths, repos, and semantic context are explicit
3. **Triage-Ready**: Severity, confidence, fingerprints, suppression, ownership
4. **Fix-Ready**: Remediation recipes with optional autofix
5. **Testable**: Rules ship with positive/negative examples for CI

---

## Schema Definition

```yaml
schema_version: 1

pack:
  id: string                    # Unique pack identifier
  name: string                  # Human-friendly name
  owners: [string]              # Team/email contacts
  default_severity: enum        # info | warning | error | critical

rules:
  - id: string                  # Unique rule ID (e.g., "rust.no_unwrap_in_handlers")
    title: string               # Human-friendly title
    intent: string              # One-line purpose ("Prevent panics in handlers")
    rationale: string           # Detailed explanation
    
    # Severity & Confidence
    severity: enum              # info | warning | error | critical
    confidence: float           # 0.0 to 1.0 (your system's estimate)
    enabled: boolean            # Can be disabled without deleting
    
    # Metadata & References
    references:
      incident: string          # INC-2024-042
      tickets: [string]         # ENG-1337, JIRA-123
      cwe: [string]             # CWE-248 (optional)
      docs: [string]            # Internal wiki links
    
    tags: [string]              # For filtering (rust, reliability, panic)
    owners: [string]            # Rule maintainers
    
    # Scope: Where this rule applies
    scope:
      languages: [string]       # rust, python, javascript
      paths:
        include: [glob]         # src/handlers/**
        exclude: [glob]         # **/tests/**, **/generated/**
      repos:
        include: [glob]         # my-org/*, production-*
        exclude: [glob]         # experimental-*
      code_context:             # Semantic scoping (beyond file paths)
        any_of:
          - kind: enum          # function, impl, module, attribute
            name_regex: string  # .*handler.*
          - kind: enum
            contains: string    # #[axum::handler]
    
    # Detection: Multi-engine support
    detection:
      mode: enum                # union | best | first
      detectors:
        - engine: enum          # tree_sitter | semgrep | codeql
          language: string
          query: string         # Engine-specific query
          constraints:          # Additional runtime constraints
            require_scope_context: boolean
        
        - engine: semgrep
          language: string
          ruleset:
            - pattern: string   # Semgrep pattern
          metavariables:        # Optional pattern constraints
            X:
              allow_regex: string
    
    # Reporting: How findings are presented
    reporting:
      message: string           # Human-readable finding message
      primary_location: enum    # callsite | function | file
      fingerprint:
        strategy: enum          # stable_v1, path_based, content_hash
      suppressions:
        inline:
          formats: [string]     # living-linter:ignore rust.no_unwrap
        expiry_days_default: int
    
    # Remediation: Fix guidance
    remediation:
      recipe_id: string         # Machine-readable fix ID
      guidance: string          # Human-readable steps
      autofix:
        kind: enum              # none | suggestion | patch
        patch_template: string  # Find/replace template
      examples:
        - before: string
          after: string
    
    # Testing: Rule validation
    tests:
      positive:                 # Should match
        - path: string
          code: string
      negative:                 # Should NOT match
        - path: string
          code: string
    
    # Versioning
    metadata:
      version: string           # 1.0, 1.1, etc.
      created: date
      updated: date
      changelog: string
```

---

## Severity Ladder

| Level | Name | CI Impact | Use Case |
|-------|------|-----------|----------|
| 0 | `info` | None | Educational, no enforcement |
| 1 | `warning` | Visible, non-blocking | Proven pattern, building confidence |
| 2 | `error` | Blocks merge | High-signal, low false-positive |
| 3 | `critical` | Blocks all, even legacy | Security-critical |

---

## Detection Modes

| Mode | Behavior |
|------|----------|
| `union` | All detectors run, findings merged |
| `best` | Highest-confidence detector wins |
| `first` | First detector to match wins |

---

## Fingerprint Strategies

| Strategy | Description |
|----------|-------------|
| `stable_v1` | Hash of (repo, path, line range, rule_id) |
| `path_based` | Hash of (repo, path, rule_id) |
| `content_hash` | Hash of matched code content |

---

## File Organization

```
.arqonship/
├── constitution.toml          # Governance rules
├── rules/
│   ├── pack.yaml              # Pack metadata
│   ├── rust/
│   │   ├── no_unwrap_in_handlers.yaml
│   │   ├── no_panic_in_production.yaml
│   │   └── require_timeout_on_http.yaml
│   ├── security/
│   │   ├── no_hardcoded_secrets.yaml
│   │   └── no_sql_injection.yaml
│   └── quality/
│       └── max_function_length.yaml
└── recipes/
    └── rust/
        └── replace_unwrap_with_question_mark.yaml
```
