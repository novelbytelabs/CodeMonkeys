# CodeMonkeys: The Autonomous Software Troope
> *CodeMonkeys write the code. You run the zoo.*

## The Pivot
**Identity:** We are dropping the corporate "Arqon" prefix. We are **CodeMonkeys**.
**Mission:** "100 Monkeys typing on 100 keyboards *will* eventually write Shakespeare... if you have a Silverback reviewing their PRs."

---

## 1. The Metaphor: The Primate Hierarchy (Roles)

The "Software Factory" layers flow naturally into the Primate Hierarchy:

### 🦍 The Silverback (Governance / Layer 2)
*   **Role:** The Constitution Enforcer.
*   **Behavior:** Stern, silent, unyielding.
*   **Action:** Rejects code that violates the Law. Does not write code; only blocks it.
*   **Identity:** Previously "Justice Agent".

### 🐒 The Code Monkey (Worker / Layer 4)
*   **Role:** The Tactician. Writes code, runs tests.
*   **Behavior:** High energy, high speed, potentially chaotic.
*   **Action:** "See Ticket -> Write Code -> Run Test -> Fail -> Fix -> Pass."
*   **Identity:** Previously "Healer/Builder".

### 🦧 The Architect (Planning / Layer 3)
*   **Role:** The Orchestrator. Breaks DDD intent into tickets.
*   **Behavior:** Thoughtful, slow, sees the big picture.
*   **Action:** Reads `context.md`, outputs a Plan.
*   **Identity:** Previously "Planner/Conductor".

### 🙈 The Observer (Context / Layer 5)
*   **Role:** The Memory.
*   **Behavior:** Watches the logs, remembers the past errors.
*   **Action:** "We tried that fix last week, and it broke production."
*   **Identity:** Previously "Oracle".

---

## 2. New Feature Ideas (Brainstorming)

### "Infinite Monkey Theorem" (Fuzzing)
*   **Idea:** Spin up 50 "Chaos Monkeys" that randomly click/curl your API.
*   **Goal:** Find crashes the TDD suite missed.
*   **Governance:** The Silverback watches them and reverts the DB if they break it.

### "Banana Tokens" (Gamified Economics)
*   **Idea:** Agents spend tokens to run expensive tests or call LLMs.
*   **Goal:** Prevent "Infinite Loops" of spending.
*   **Mechanism:** Each PR gets a budget of 100 Bananas. If the Monkey spends them all without passing tests, the PR is closed.

### "The ZooKeeper" (Human Interface)
*   **Idea:** A dashboard where you "feed" the monkeys (give them tickets) and "clean the cage" (approve PRs).
*   **Goal:** Gamified, visual management of the autonomous fleet.

### "Monkey See, Monkey Do" (Few-Shot Learning)
*   **Idea:** You fix a bug manually once. The Observer records it.
*   **Effect:** Next time, the Code Monkey mimics your exact git diff pattern.

---

## 4. Decisions (Locked In)

| Question | Decision |
|----------|----------|
| **Tone** | Professional by default. Optional `--fun` mode for playful output. |
| **Scope** | Solo Dev CLI first (`cargo install codemonkeys`). Design internals for Enterprise later. |
| **Chaos Monkey** | ✅ **Must Have.** Core feature, not deferred. |

---

## 5. Revised Feature Set (MVP)

### Core Agents (The Troop)
1. **The Silverback** — Governance enforcement (Constitution check)
2. **Code Monkey** — Builder agent (writes code, runs tests)
3. **Chaos Monkey** — Fuzzing agent (random inputs, crash detection)
4. **The Observer** — Memory/Context (past fixes, logs)

### CLI Commands (v0.1)
```bash
codemonkeys init           # Setup .codemonkeys/ in repo
codemonkeys check          # Run Silverback governance check
codemonkeys chaos [target] # Run Chaos Monkey fuzzing
codemonkeys heal [error]   # Run Code Monkey to fix an error
codemonkeys status         # Show Troop status
```

---

## 6. Tech Stack
*   **Language:** Rust (Safety first)
*   **CLI Framework:** `clap`
*   **Config:** `.codemonkeys/config.toml`
*   **Chaos Engine:** `cargo-fuzz` integration or custom HTTP fuzzer
