# Refactoring Plan: CLI Rename (arqon → arqonship)

## Overview

The CLI binary must be renamed from `arqon` to `arqonship` to reserve the `arqon` namespace for a meta-system that orchestrates multiple Arqon products.

**Current**: `arqon init`, `arqon scan`, `arqon heal`, etc.
**Target**: `arqonship init`, `arqonship scan`, `arqonship heal`, etc.

---

## Affected Files

### 1. Cargo.toml

**File**: `Cargo.toml`

**Change**: Update binary name

```diff
 [[bin]]
-name = "arqon"
+name = "arqonship"
 path = "src/main.rs"
```

---

### 2. Source Code

**File**: `src/main.rs`

**Change**: Update Clap app name and any self-references

```diff
 #[derive(Parser)]
-#[command(name = "arqon")]
+#[command(name = "arqonship")]
 #[command(about = "DevSecOps CLI")]
 struct Cli { ... }
```

Search for any hardcoded "arqon" strings:
```bash
grep -r '"arqon"' src/
grep -r "'arqon'" src/
grep -r "arqon " src/
```

---

### 3. Configuration

**File**: `src/config.rs`

**Change**: Update config directory name if applicable

```diff
 fn default_config_dir() -> PathBuf {
-    PathBuf::from(".arqon")
+    PathBuf::from(".arqonship")
 }
```

**Decision needed**: Keep `.arqon/` for backward compatibility or rename to `.arqonship/`?

---

### 4. Documentation

**Files to update**:
- `README.md`
- `docs/index.md`
- `docs/cli-reference.md`
- `docs/configuration.md`
- `docs/developer-guide.md`
- `docs/architecture.md`

**Pattern to replace**:
```bash
# All documentation
sed -i 's/arqon init/arqonship init/g' docs/*.md README.md
sed -i 's/arqon scan/arqonship scan/g' docs/*.md README.md
sed -i 's/arqon chat/arqonship chat/g' docs/*.md README.md
sed -i 's/arqon heal/arqonship heal/g' docs/*.md README.md
sed -i 's/arqon ship/arqonship ship/g' docs/*.md README.md
sed -i 's/arqon watch/arqonship watch/g' docs/*.md README.md
sed -i "s/'arqon'/'arqonship'/g" docs/*.md README.md
sed -i 's/`arqon`/`arqonship`/g' docs/*.md README.md
```

---

### 5. CI Workflows

**File**: `.github/workflows/ci.yml`

**Change**: Update any references to the binary

```bash
grep -r "arqon" .github/
```

---

### 6. Pre-commit Config

**File**: `.pre-commit-config.yaml`

**Change**: None expected (uses cargo, not binary name)

---

### 7. Agent/Workflow Files

**Directory**: `.agent/`

**Files**:
- `.agent/VISION.md`
- `.agent/FLEET_ARCHITECTURE.md`

**Change**: Update all `arqon` command references to `arqonship`

---

## Verification Steps

After refactoring, run these checks:

```bash
# 1. Build succeeds
cargo build --release

# 2. Binary has correct name
ls target/release/arqonship

# 3. Help works
./target/release/arqonship --help

# 4. All commands work
./target/release/arqonship init
./target/release/arqonship scan
./target/release/arqonship chat -q "test"
./target/release/arqonship heal --help
./target/release/arqonship ship --dry-run

# 5. Tests pass
cargo test

# 6. No stray references
grep -rn '"arqon"' src/ docs/ README.md
grep -rn "'arqon'" src/ docs/ README.md
# Should return 0 matches (or only valid ones like "ArqonShip")

# 7. Docs build
mkdocs build
```

---

## Implementation Checklist

- [ ] Update `Cargo.toml` binary name
- [ ] Update `src/main.rs` Clap command name
- [ ] Decide: rename `.arqon/` to `.arqonship/` or keep?
- [ ] Update `src/config.rs` if config dir changes
- [ ] Update `README.md` (all command examples)
- [ ] Update `docs/index.md` (all command examples)
- [ ] Update `docs/cli-reference.md`
- [ ] Update `docs/configuration.md`
- [ ] Update `docs/developer-guide.md`
- [ ] Update `docs/architecture.md`
- [ ] Update `.agent/VISION.md`
- [ ] Update `.agent/FLEET_ARCHITECTURE.md`
- [ ] Check `.github/workflows/` for references
- [ ] Run verification steps
- [ ] Commit with message: `refactor: rename CLI binary from arqon to arqonship`

---

## Notes for Implementer

1. **Case sensitivity**: `arqon` vs `Arqon` vs `ArqonShip` — only lowercase command-line usage should change
2. **Package name**: `arqonship` in Cargo.toml stays the same
3. **Config directory**: Recommend changing to `.arqonship/` for consistency
4. **Backward compatibility**: Not needed (pre-v1.0)
