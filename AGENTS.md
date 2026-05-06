# AGENTS.md — Vigia

## Project context

Describe the project in detail here, or point to a reference file:

```
See: VIGIA_DOCS.md   # replace with your project's doc file
```

______________________________________________________________________

## Session workflow

### Beans modeling rules (MANDATORY)

- Every Bean MUST be self-contained

- Each Bean must include:

  - What needs to be done
  - Why it needs to be done
  - Where to implement (files/modules)
  - How to approach it (architecture/constraints)
  - Beans must be written in English

- Use a hierarchical structure:

  - Epic → represents a feature or high-level goal
  - Tasks → implementation steps under an epic
  - Each Epic MUST have child tasks
  - Bug → issues/defects found during development or review

> Each Epic MUST have child tasks (and/or bugs when applicable)

- Dependencies must be explicitly defined:

  - Tasks can depend on other tasks
  - Execution order is driven by dependencies, not type

Write Beans assuming:

> Another agent with zero context will execute it

### 1. Start of session

```bash
# Check whether `beans` is already initialized before running `beans init`
beans init  # initialize beans in the project (run once)
```

```bash
beans --json ready  # list available tasks
```

> `beans` — task management CLI: https://github.com/henriquebastos/beans/

> Use `beans --help` for more information about available commands

### 2. Before starting any task

```bash
beans claim <id> --actor opencode
```

### 3. Red-green-refactor (TDD — always write the test first)

```
RED    → write a failing test
GREEN  → make it pass with the minimal implementation
COMMIT → feat: <description>

REFACTOR → improve the code without changing behavior
COMMIT   → refactor: <description>
```

### 4. After completing a task

```bash
beans close <id> --reason "commit <hash>"
```

### 5. At 80% context — run handoff

Summarize what was done, what is pending, and the current state of the codebase so the next session can resume without losing context.

______________________________________________________________________

## Imports

**Imports always at the top of the file — never inside a function or class.**

______________________________________________________________________

## Commits

Each commit does **one thing**. Use conventional commit messages:

| Prefix | When to use |
|---|---|
| `feat:` | new functionality |
| `fix:` | bug fix |
| `refactor:` | code improvement, no behavior change |
| `chore:` | tooling, config, dependencies |
| `docs:` | documentation only |
| `ci:` | CI/CD changes |

When a commit resolves a bean, append `#closes <bean-id>` to the message:

```bash
git commit -m "feat: add --body flag to create command #closes bean-69b4e720"
```

______________________________________________________________________

## Before every commit

**Step 1 — tests and lint**

```bash
uv run pytest
uv run ruff check tests/
```

**Step 2 — review uncommitted changes**

Run `git diff HEAD` and review the output in 5 focused passes:

It runs a 5-pass review of uncommitted changes covering: security, correctness, design, testing, and conventions.

1. **Security** — secrets exposure, unsafe inputs, injection risks, auth issues
1. **Correctness** — logic errors, wrong assumptions, edge cases, off-by-one
1. **Design** — coupling, cohesion, SRP violations, unnecessary abstractions
1. **Testing** — missing coverage, brittle assertions, untested edge cases
1. **Conventions** — naming, import order, code style, project-specific patterns

For each pass, list issues found. Fix any issues → re-run tests → then commit.
