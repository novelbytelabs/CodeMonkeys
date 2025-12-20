# The Constitution of CodeMonkeys
> *The Supreme Law of the Autonomous Troop*

## Preamble

This document defines the **non-negotiable principles** that govern how CodeMonkeys operates.
If a decision conflicts with this constitution, **the decision is wrong**.

---

## Rule: No Hardcoded Secrets
Severity: error

```codemonkeys-rule
id: "gov.no_secrets"
version: "1"
since: "2025-12-20"
severity: "error"
owners: ["security@company.com"]
scope:
  paths:
    include: ["**/*"]
    exclude: ["**/*.lock", "**/*.schema.json"]
check:
  kind: "secret_scan"
  tool: "builtin_regex"
  patterns:
    - "AKIA[0-9A-Z]{16}"
    - "-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"
    - "ghp_[a-zA-Z0-9]{36}"
    - "sk-[a-zA-Z0-9]{48}"
message: "Secret detected. Remove and rotate credentials immediately."
rationale: "Secrets in git history are recoverable; treat as incident."
```

---

## Rule: No Unsafe Without Justification
Severity: error

```codemonkeys-rule
id: "rust.unsafe_requires_safety"
version: "1"
since: "2025-12-20"
severity: "error"
scope:
  paths:
    include: ["src/**/*.rs"]
    exclude: ["tests/**"]
check:
  kind: "tree_sitter"
  language: "rust"
  query: "(unsafe_block) @b"
  requires:
    comment_regex_nearby: "SAFETY:"
message: "unsafe blocks must include a `// SAFETY:` justification comment."
rationale: "Unsafe code requires explicit reasoning for review."
```

---

## Rule: No unwrap() in Production Code
Severity: warning

```codemonkeys-rule
id: "rust.no_unwrap_in_prod"
version: "1"
since: "2025-12-20"
severity: "warning"
scope:
  paths:
    include: ["src/**/*.rs"]
    exclude: ["tests/**", "examples/**"]
check:
  kind: "semgrep"
  pattern: "$X.unwrap()"
message: "Prefer Result propagation (?) over unwrap() in production code."
rationale: "Panics in production cause service disruptions."
```

---

## Rule: Function Length Limit
Severity: warning

```codemonkeys-rule
id: "quality.function_length"
version: "1"
since: "2025-12-20"
severity: "warning"
scope:
  paths:
    include: ["src/**/*.rs"]
check:
  kind: "metrics"
  metric: "function_lines"
  max: 80
message: "Function exceeds 80 lines; consider refactoring."
rationale: "Long functions are harder to test and maintain."
```

---

**Version**: 1.0.0 (CodeMonkeys)
**Ratified**: 2025-12-20
