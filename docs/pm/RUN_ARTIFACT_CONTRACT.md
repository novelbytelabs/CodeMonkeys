# Run Artifact Contract

**Version**: 0.1
**Status**: Active
**Owner**: Code Monkeys Core

## Purpose
This document defines the contract between **artifact producers** (pipeline, report generator, CI) and **artifact consumers** (Dash, Nexus, operators).

## 1. Directory Layout

```
dash/
├── products.json                     # Fleet registry (read by Dash)
├── schemas/
│   ├── products.schema.json          # JSON Schema for products
│   └── last_run.schema.json          # JSON Schema for run reports
└── runs/
    └── <product_id>/
        ├── last_run.json             # Most recent run report
        └── <run_id>/
            ├── pytest_output.log     # Test output
            ├── test-report.json      # Structured test results (optional)
            ├── screenshot.png        # UI proof (optional)
            └── evidence/             # Additional artifacts
```

## 2. File Contracts

### products.json
- **Location**: `dash/products.json`
- **Schema**: `dash/schemas/products.schema.json`
- **Updated by**: Manual or `codemonkeys fleet register`
- **Read by**: Dash (to list products)

### last_run.json
- **Location**: `dash/runs/<product_id>/last_run.json`
- **Schema**: `dash/schemas/last_run.schema.json`
- **Updated by**: `scripts/generate_run_report.py` or CI pipeline
- **Read by**: Dash (to show run status)

## 3. Schema Versioning

| Version | Status | Notes |
|---------|--------|-------|
| 0.1 | Active | Bootstrap version, basic fields |
| 0.2 | Planned | Add duration, detailed metrics |

### Versioning Rules
1. `schema_version` field is **required** in all artifacts.
2. Consumers MUST check `schema_version` before parsing.
3. Backward-incompatible changes require a new major version.
4. Dash should render gracefully if version is unrecognized.

## 4. What Dash Renders

| Field | Source | Required |
|-------|--------|----------|
| Product Name | `products.json` | YES |
| Product Status | `products.json` | YES |
| Run ID | `last_run.json` | YES |
| Run Status | `last_run.json` | YES |
| Summary | `last_run.json` | YES |
| Evidence Paths | `last_run.json` | YES |
| Banana Economy | `last_run.json` | YES |
| Kill Switch | `last_run.json` | YES |
| PR Wave | `last_run.json` | YES |

## 5. Error Handling

### Missing Artifact
- Dash shows: "Missing artifact: [path]"
- Status: Error badge

### Invalid Schema
- Dash shows: "Invalid artifact: [validation error]"
- Status: Error badge

### Unknown Version
- Dash shows: "Unsupported schema version: [version]"
- Proceed with best-effort rendering

## 6. Evidence Requirements

### Bootstrap Mode
- Minimum: Screenshot of rendered UI
- Structured: `pytest_output.log` or equivalent

### Production Mode
- Required: `pytest_output.log`, `last_run.json`
- Recommended: `test-report.json` (structured), screenshots
