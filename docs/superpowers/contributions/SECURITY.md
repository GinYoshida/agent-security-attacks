# Security Policy

> **Draft for upstream contribution to [obra/superpowers](https://github.com/obra/superpowers).**
> This file is intended to be placed at the repository root as `SECURITY.md`.
> Maintainers should confirm the placeholders marked `<...>` before merging.
> It is deliberately written as a **low-burden policy for a small team** — see
> `README.md` in this folder for the rationale.

## Why this matters for Superpowers specifically

Superpowers is not ordinary application code. Its skill files are **injected into the
context of every agent session** — including sub-agents — via the `SessionStart` hook. A
change to a skill's Markdown, or to a script a skill invokes, propagates to every downstream
session that installs the affected version. That makes the skill catalog a **supply-chain
surface**: the impact of a malicious or accidental change is amplified across all users.

Security-relevant components:

- Files under `skills/**` (instructions injected as agent context).
- Executable helpers invoked by skills (e.g. `skills/**/scripts/*.sh`, `*.cjs`).
- Hook scripts under `hooks/**` that run automatically at session start.
- The brainstorming visual companion server (`skills/brainstorming/scripts/server.cjs`),
  the only long-running network-listening component.

## Supported Versions

Security fixes are provided for the **latest published release only**. Users are encouraged
to pin to a specific released version (or commit SHA) rather than tracking `main`, and to
review the diff before upgrading.

## Reporting a Vulnerability

**Please do not open a public issue for security vulnerabilities.** Public disclosure
before a fix puts every user at risk.

**How to reach us**

1. Preferred: GitHub's [private vulnerability reporting](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
   for this repository (**Security** tab → **Report a vulnerability**).
2. Alternative: email `<security@primeradiant.com>`.

**Please include a reproduction.** Reports without a concrete reproduction — the injected
text or input, the tool/step sequence, and the observed impact — cannot be triaged and may
be deprioritized or closed. Also state the precondition: does the issue require an
already-compromised supply chain (e.g. write access to skill files), or is it exploitable
by an unprivileged remote party (as in [#1014](https://github.com/obra/superpowers/issues/1014))?

**What to expect.** Superpowers is maintained by a small team. We triage security reports on
a **best-effort basis and do not commit to a fixed response SLA.** We will do our best to
acknowledge valid, reproducible reports and to coordinate a fix and disclosure. There is **no
bug bounty**; please report because you want the ecosystem to be safer, not for a reward.

## Scope

**In scope**

- Prompt-injection or context-poisoning reachable through Superpowers' own components.
- Unauthorized network egress, file writes, or command execution introduced by a skill,
  hook, or bundled script beyond what its documentation describes.
- Weaknesses in the brainstorming server (origin/CSRF validation, bind address, etc.).
- Supply-chain integrity gaps (unpinned dependencies, missing change review) that would let
  a malicious update reach users silently.

**Out of scope**

- Vulnerabilities in the host agent (Claude Code, Codex, Cursor, etc.) themselves — report
  those to the respective vendor.
- Behavior that only occurs when a user has explicitly granted the agent permissions and the
  skill acts within its documented purpose.
- Documented, opt-out-able telemetry (the version beacon in the visual companion; disable
  with `SUPERPOWERS_DISABLE_TELEMETRY`).
- Reports with no reproduction, and automated-scanner output pasted without analysis.

## Hardening guidance for users

- Pin the marketplace/plugin to a specific commit SHA and review diffs before bumping.
- Set `SUPERPOWERS_DISABLE_TELEMETRY=1` (or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`) to
  eliminate the version beacon.
- Run in an ephemeral, network-policy-constrained environment where practical.
