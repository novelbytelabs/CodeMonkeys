# Code Monkeys Ship: Integration Plan

> How Ship interfaces with external tools.

---

## Phase 1: Core Interfaces (v0.1)

### 1.1 GitHub Actions Interface

**Goal:** Ship can trigger workflows, poll status, and read logs.

**Tasks:**

- [ ] Create `github::ActionsClient` with Octocrab
- [ ] Implement `trigger_workflow(repo, workflow_id, inputs)`
- [ ] Implement `poll_run_status(repo, run_id)` with timeout
- [ ] Implement `fetch_run_logs(repo, run_id)` for failure parsing
- [ ] Rate limiting with token bucket

**Files:**

- `crates/ship/src/github/actions.rs`
- `crates/ship/src/github/rate_limit.rs`

---

### 1.2 Ansible Interface

**Goal:** Ship can run playbooks with variables.

**Tasks:**

- [ ] Create `ansible::Runner` struct
- [ ] Implement `run_playbook(playbook_path, extra_vars)`
- [ ] Capture stdout/stderr, parse for errors
- [ ] Timeout handling for hung playbooks

**Files:**

- `crates/ship/src/ansible/runner.rs`

**Playbook Library:**

- `playbooks/deploy-rust-binary.yml`
- `playbooks/publish-crates-io.yml`
- `playbooks/publish-docker.yml`
- `playbooks/publish-pypi.yml`

---

### 1.3 Secrets Interface (SOPS + age)

**Goal:** Ship can decrypt secrets at deploy time.

**Tasks:**

- [ ] Create `secrets::SopsDecryptor`
- [ ] Implement `decrypt_file(path)` → returns plaintext
- [ ] Age key loaded from `~/.config/sops/age/keys.txt`
- [ ] Never log decrypted values

**Files:**

- `crates/ship/src/secrets/sops.rs`

---

### 1.4 Security Scanning Interface

**Goal:** Ship can run Trivy and cargo-audit, parse results.

**Tasks:**

- [ ] Create `security::TrivyScanner`
- [ ] Implement `scan_image(image_ref)` → `Vec<Vulnerability>`
- [ ] Create `security::CargoAuditScanner`
- [ ] Implement `audit_lockfile(path)` → `Vec<Advisory>`
- [ ] Unified `SecurityReport` type

**Files:**

- `crates/ship/src/security/trivy.rs`
- `crates/ship/src/security/cargo_audit.rs`
- `crates/ship/src/security/report.rs`

---

## Phase 2: Pillars Integration (v0.2)

### 2.1 Heal Pillar

**Integrates:** GitHub Actions + Ollama

**Flow:**

1. Watch receives CI failure event
2. Fetch logs via GitHub Actions API
3. Parse error, send to Ollama for fix
4. Commit fix, push branch
5. Trigger CI again via Actions API
6. Loop until pass or max retries

---

### 2.2 Docs Pillar

**Integrates:** MkDocs + GitHub Pages

**Flow:**

1. Detect docs drift (code changed, docs stale)
2. Regenerate docs via `mkdocs build`
3. Push to `gh-pages` branch
4. GitHub Pages auto-deploys

---

### 2.3 Release Pillar

**Integrates:** Ansible + Registries

**Flow:**

1. Detect release conditions (tags, CI green)
2. Decrypt secrets via SOPS
3. Run security scans (Trivy, cargo-audit)
4. Run publish playbook (crates.io, Docker Hub, etc.)
5. Send success webhook

---

### 2.4 Monitor Pillar

**Integrates:** Webhooks

**Flow:**

1. All events logged to Swarm DB
2. Errors trigger webhook → phone notification
3. Periodic health check of all products

---

## Phase 3: Fleet Integration (v0.3)

### 3.1 Cross-Product Operations

**Goal:** Run operations across all 50 products.

**Tasks:**

- [ ] `ship status --all` aggregates all product states
- [ ] `ship fleet update-deps` runs cargo-audit + update across fleet
- [ ] Canary ladder for fleet-wide changes

---

## Testing Strategy

### Unit Tests
- Mock external tool responses
- Test parsing of Trivy JSON, Actions logs, etc.

### Integration Tests (CI)
- Use GitHub Actions to test... GitHub Actions integration
- Test against real crates.io (with `--dry-run`)
- Test Ansible against local Docker container

### E2E Tests
- Full flow: break test → heal → publish
- On a dedicated test repo

---

## Configuration

```yaml
# .codemonkeys/config.yaml
ship:
  github:
    token_env: GITHUB_TOKEN
    
  ansible:
    playbook_dir: ./playbooks
    inventory: ./inventory.yml
    
  secrets:
    sops_age_key: ~/.config/sops/age/keys.txt
    
  security:
    trivy_enabled: true
    cargo_audit_enabled: true
    fail_on_high: true
    
  alerts:
    webhook_url_env: ALERT_WEBHOOK_URL
    
  registries:
    crates_io: true
    docker_hub: true
    pypi: false
```

---

## Success Criteria

- [ ] Ship can trigger and monitor GitHub Actions workflows
- [ ] Ship can run Ansible playbooks with decrypted secrets
- [ ] Ship can scan images and report vulnerabilities
- [ ] Ship can publish to at least one registry
- [ ] Ship can send alert webhooks on failure
- [ ] All operations logged with audit trail
