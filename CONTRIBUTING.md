# Contributing to AdaptiGuard

AdaptiGuard is a hash-locked evaluation testbed for prompt-injection and related LLM-agent attacks, comparing fixed and adaptive discrete intervention policies under shared security, utility, and cost metrics.

## How to report a bug

Open a GitHub issue with:

- a clear description of the problem
- the exact command that triggered it
- your Python version and OS
- relevant logs or error messages

## Security issues

Do **not** disclose security vulnerabilities through public GitHub issues. Report security issues to `security@[redacted]`.

## Pull request procedure

1. Fork the repository and create a branch named `cursor/<descriptive-name>-f6f3`.
2. Make your changes. Keep commits focused and descriptive.
3. Ensure no experimental data, frozen evidence, or metrics are modified.
4. Update or add tests where applicable.
5. Update `CHANGELOG.md` if your change is user-facing.
6. Open a pull request against the appropriate base branch.

## Branch naming

Use lowercase, kebab-case, the `cursor/` prefix, and the `-f6f3` suffix:

```
cursor/<descriptive-name>-f6f3
```

## Commit style

Write clear, descriptive commit messages:

```
docs(q2): publication hardening — attribution protocol, not a new defense
ci: add ruff lint job to GitHub Actions
```

## Python code style

- Target Python 3.12+.
- Type hints are encouraged for new code.
- Follow existing formatting conventions. Ruff is configured in `pyproject.toml`.

## Linting

Ruff is the configured linter:

```
ruff check src/ tests/
```

Configuration lives in `pyproject.toml` under `[tool.ruff]`. Do not suppress lint errors globally; fix them or use targeted inline `# noqa` with justification.

## Type checking

No type checker is currently configured. If you add mypy or pyright, do not introduce errors in existing code.

## Research integrity

This is a **research codebase**. Contributions must not alter:

- experimental results
- frozen dataset contents (P1/P2/Q2)
- evidence hashes (SHA-256)
- benchmark membership
 attack/benign counts
- detector thresholds or seeds
- historical metrics (`metrics.json`, `*.jsonl` traces)
- published figures (`*.png`)
- scientific claims in the manuscript

If your contribution affects experimental evidence, document the change in `CHANGELOG.md` and ensure the frozen evidence hashes remain unchanged.
