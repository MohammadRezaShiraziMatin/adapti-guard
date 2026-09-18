# Security Policy

## Supported versions

Only the current `main` branch and actively maintained feature branches receive security updates.

## Reporting a vulnerability

Do **not** disclose security vulnerabilities through public GitHub issues.

Report security issues to:

```
security@[redacted]
```

Include:

- a description of the vulnerability
- the affected component (source file, configuration, workflow)
- steps to reproduce
- the potential impact
- a suggested fix if available

You will receive a response within 72 hours.

## Private disclosure timeline

1. Reporter privately discloses the vulnerability.
2. Maintainers acknowledge receipt and triage severity.
3. A fix is prepared and validated.
4. A coordinated public disclosure is scheduled after a fix is available.
5. The reporter is credited in the release notes if desired.

## Dual-use disclaimer

AdaptiGuard studies **prompt injection attacks** for defensive purposes only. The research includes:

- adversarial prompts designed to test detector and policy robustness
- mock tool-execution environments
- sandboxed evaluation harnesses

The payloads, attack templates, and evaluation methodologies are disclosed for scientific reproducibility and defensive research.

**Misuse is the responsibility of the actor.** The authors do not endorse using these techniques against production systems.

## Responsible-use expectations

- Do not deploy AdaptiGuard against production LLM agents without security review.
- Do not use adversarial prompts against systems you do not own or have authorization to test.
- Disclose vulnerabilities responsibly to affected parties before public disclosure.
- Respect the dual-use nature of security research.

## Adversarial prompt research disclosure

This repository contains adversarial prompt injection payloads and attack templates. These are provided for:

- scientific reproducibility of the evaluation
- defensive research and red-teaming
- development of robust detector and policy mechanisms

All adversarial content is clearly labeled and confined to frozen benchmark packs.

## Contact

For security questions: `security@[redacted]`
