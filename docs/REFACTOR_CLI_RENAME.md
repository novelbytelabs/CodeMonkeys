# Refactoring Plan: CLI Rename (codemonkeys → codemonkeys)

## Overview

The CLI binary must be renamed from `codemonkeys` to `codemonkeys` to reserve the `codemonkeys` namespace for a meta-system that orchestrates multiple Code Monkeys products.

**Current**: `codemonkeys init`, `codemonkeys scan`, `codemonkeys heal`, etc.
**Target**: `codemonkeys init`, `codemonkeys scan`, `codemonkeys heal`, etc.

---

## Affected Files

### 1. Cargo.toml

**File**: `Cargo.toml`

**Change**: Update binary name

```diff
 [[bin]]
-name = "codemonkeys"
+name = "codemonkeys"
 path = "src/main.rs"
```

---

### 2. Source Code

**File**: `src/main.rs`

**Change**: Update Clap app name and any self-references

```diff
 #[derive(Parser)]
-#[command(name = "codemonkeys")]
+#[command(name = "codemonkeys")]
 #[command(about = "DevSecOps CLI")]
 struct Cli { ... }
```

Search for any hardcoded "codemonkeys" strings:
```bash
grep -r '"codemonkeys"' src/
grep -r "'arqon'" src/
grep -r "codemonkeys " src/
```

---

### 3. Configuration

**File**: `src/config.rs`

**Change**: Update config directory name if applicable

```diff
 fn default_config_dir() -> PathBuf {
-    PathBuf::from(".arqon")
+    PathBuf::from(".codemonkeys")
 }
```

**Decision needed**: Keep `.codemonkeys/` for backward compatibility or rename to `.codemonkeys/`?

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
sed -i 's/codemonkeys init/codemonkeys init/g' docs/*.md README.md
sed -i 's/codemonkeys scan/codemonkeys scan/g' docs/*.md README.md
sed -i 's/codemonkeys chat/codemonkeys chat/g' docs/*.md README.md
sed -i 's/codemonkeys heal/codemonkeys heal/g' docs/*.md README.md
sed -i 's/codemonkeys ship/codemonkeys ship/g' docs/*.md README.md
sed -i 's/codemonkeys watch/codemonkeys watch/g' docs/*.md README.md
sed -i "s/'arqon'/'codemonkeys'/g" docs/*.md README.md
sed -i 's/`codemonkeys`/`codemonkeys`/g' docs/*.md README.md
```

---

### 5. CI Workflows

**File**: `.github/workflows/ci.yml`

**Change**: Update any references to the binary

```bash
grep -r "codemonkeys" .github/
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

**Change**: Update all `codemonkeys` command references to `codemonkeys`

---

## Verification Steps

After refactoring, run these checks:

```bash
# 1. Build succeeds
cargo build --release

# 2. Binary has correct name
ls target/release/codemonkeys

# 3. Help works
./target/release/codemonkeys --help

# 4. All commands work
./target/release/codemonkeys init
./target/release/codemonkeys scan
./target/release/codemonkeys chat -q "test"
./target/release/codemonkeys heal --help
./target/release/codemonkeys ship --dry-run

# 5. Tests pass
cargo test

# 6. No stray references
grep -rn '"codemonkeys"' src/ docs/ README.md
grep -rn "'arqon'" src/ docs/ README.md
# Should return 0 matches (or only valid ones like "Code Monkeys")

# 7. Docs build
mkdocs build
```

---

## Implementation Checklist

- [ ] Update `Cargo.toml` binary name
- [ ] Update `src/main.rs` Clap command name
- [ ] Decide: rename `.codemonkeys/` to `.codemonkeys/` or keep?
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
- [ ] Commit with message: `refactor: rename CLI binary from codemonkeys to codemonkeys`

---

## Notes for Implementer

1. **Case sensitivity**: `codemonkeys` vs `Arqon` vs `Code Monkeys` — only lowercase command-line usage should change
2. **Package name**: `codemonkeys` in Cargo.toml stays the same
3. **Config directory**: Recommend changing to `.codemonkeys/` for consistency
4. **Backward compatibility**: Not needed (pre-v1.0)
