# Code Monkeys Ship: External Tooling Stack

> The minimal, powerful stack for solo-scale automation on a single workstation.

---

## Philosophy

Ship orchestrates external tools — it doesn't replace them. Each tool is called via CLI or API, with Ship reading output to decide next steps. This keeps Ship focused on decision-making while leveraging battle-tested tools for execution.

---

## The Stack

### CI/CD
| Tool | Purpose | Interface |
|------|---------|-----------|
| **GitHub Actions** | Build, test, CI pipelines | GitHub API (trigger workflows, poll status, read logs) |

### Deployment
| Tool | Purpose | Interface |
|------|---------|-----------|
| **Ansible** | Deploy, configure, publish | CLI (`ansible-playbook` with vars) |

### Secrets
| Tool | Purpose | Interface |
|------|---------|-----------|
| **SOPS + age** | Encrypted secrets in Git | CLI (`sops -d` to decrypt at deploy time) |

### Security Scanning
| Tool | Purpose | Interface |
|------|---------|-----------|
| **Trivy** | Container/image/IaC scanning | CLI (JSON output for parsing) |
| **cargo-audit** | Rust dependency vulnerabilities | CLI (JSON output for parsing) |

### Testing
| Tool | Purpose | Interface |
|------|---------|-----------|
| **cargo test** | Rust unit/integration tests | CLI (exit code + JSON output) |
| **pytest** | Python tests | CLI (exit code + JSON output) |
| **Playwright** | E2E browser tests | CLI (exit code + reports) |

### Alerts
| Tool | Purpose | Interface |
|------|---------|-----------|
| **Webhooks** | Notify on events | HTTP POST to phone/Discord/Slack |

### Registries
| Tool | Purpose | Interface |
|------|---------|-----------|
| **Docker Hub / ghcr.io** | Container images | `docker push` via Ansible |
| **crates.io** | Rust packages | `cargo publish` via Ansible |
| **PyPI** | Python packages | `twine upload` via Ansible |
| **npm** | JavaScript packages | `npm publish` via Ansible |

### Documentation Hosting
| Tool | Purpose | Interface |
|------|---------|-----------|
| **GitHub Pages** | Docs/website hosting | Git push to `gh-pages` branch |
| **MkDocs** | Documentation generation | CLI (`mkdocs build`) |

---

## What Ship Does NOT Use

| Tool | Why Skipped |
|------|-------------|
| Kubernetes | No cluster, single workstation |
| Argo CD | GitOps for K8s we don't run |
| Jenkins | GitHub Actions is simpler for our scale |
| Vault | SOPS+age is sufficient, no server to maintain |
| Harbor/Nexus | Public registries are fine |
| Alertmanager | Overkill; simple webhooks work |
| iTop | ITSM for teams; we're solo |
| OpenTofu | Only if/when cloud infra is needed |

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CODE MONKEYS SHIP                        │
│                                                             │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│   │  Heal   │  │  Docs   │  │ Release │  │ Monitor │       │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│        │            │            │            │             │
└────────┼────────────┼────────────┼────────────┼─────────────┘
         │            │            │            │
         ▼            ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ GitHub  │  │ MkDocs  │  │ Ansible │  │Webhooks │
    │ Actions │  │   +     │  │    +    │  │         │
    │         │  │ GitHub  │  │Registries│ │         │
    │         │  │ Pages   │  │         │  │         │
    └─────────┘  └─────────┘  └─────────┘  └─────────┘
```

---

## Interface Patterns

### Pattern 1: CLI Subprocess
Ship spawns a process, captures stdout/stderr, checks exit code.

```rust
// Example: Run Ansible playbook
let output = Command::new("ansible-playbook")
    .args(["deploy.yml", "--extra-vars", &vars])
    .output()?;

if output.status.success() {
    // Parse output, log success
} else {
    // Handle failure, maybe retry
}
```

### Pattern 2: HTTP API
Ship makes HTTP requests, parses JSON responses.

```rust
// Example: Trigger GitHub Actions workflow
let response = client
    .post(&format!("{}/actions/workflows/{}/dispatches", repo_url, workflow_id))
    .header("Authorization", &format!("Bearer {}", token))
    .json(&trigger_payload)
    .send()?;
```

### Pattern 3: Git Operations
Ship uses libgit2 (via git2 crate) for branch/commit/push.

```rust
// Example: Push to gh-pages
let repo = Repository::open(".")?;
// ... stage files, commit, push
```

---

## Security Model

1. **Secrets never in code** — SOPS-encrypted in Git, decrypted at runtime
2. **Minimal permissions** — GitHub tokens scoped to specific repos/actions
3. **Audit trail** — Every tool invocation logged with timestamp, command, output
4. **Fail-safe** — On error, stop and alert rather than retry blindly

---

## Next Steps (Integration Plan)

See: `SHIP_INTEGRATION_PLAN.md`
