# Security Policy

> **Draft for upstream contribution to [obra/superpowers](https://github.com/obra/superpowers).**
> This file is intended to be placed at the repository root as `SECURITY.md`.
> Maintainers should fill in the placeholders marked `<...>` before merging.

## Why this matters for Superpowers specifically

Superpowers is not ordinary application code. It is a **plugin whose skill files are
injected into the context of every agent session** — including sub-agents — via the
`SessionStart` hook. A change to a skill's Markdown, or to a script a skill invokes,
propagates to every downstream session that installs the affected version. That makes
the skill catalog a **supply-chain surface**: the impact of a malicious or accidental
change is amplified across all users and all of their sessions.

For that reason, this project treats the following as security-relevant:

- The contents of files under `skills/**` (instructions injected as agent context).
- Executable helpers invoked by skills (e.g. `skills/**/scripts/*.sh`, `*.cjs`).
- Hook scripts under `hooks/**` that run automatically at session start.
- The brainstorming visual companion server (`skills/brainstorming/scripts/server.cjs`),
  the only long-running network-listening component.

## Supported Versions

Security fixes are provided for the latest published release. Users are strongly
encouraged to pin to a specific released version (or commit SHA) rather than tracking
`main`, and to review the diff before upgrading.

| Version | Supported |
| ------- | --------- |
| Latest release | ✅ |
| Older releases | ⚠️ Best effort |

## Reporting a Vulnerability

**Please do not open a public issue for security vulnerabilities.**

Preferred channel: GitHub's [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
for this repository (Security tab → "Report a vulnerability"). If that is not enabled,
email `<security-contact@example.com>`.

Please include:

- Affected component (skill / hook / script / server) and version or commit SHA.
- A minimal reproduction: the injected text, the tool sequence, and the observed impact.
- Whether the issue requires an already-compromised supply chain (e.g. write access to
  skill files) or is exploitable by an unprivileged remote party (e.g. a web page a user
  visits, as in [#1014](https://github.com/obra/superpowers/issues/1014)).

We aim to acknowledge reports within `<N>` business days and to provide a remediation
timeline after triage.

## Scope

**In scope**

- Prompt-injection or context-poisoning reachable through Superpowers' own components.
- Unauthorized network egress, file writes, or command execution introduced by a skill,
  hook, or bundled script beyond what its documentation describes.
- Weaknesses in the brainstorming server (origin/CSRF validation, bind address, etc.).
- Supply-chain integrity gaps (unpinned dependencies, missing change review) that would
  let a malicious update reach users silently.

**Out of scope**

- Vulnerabilities in the host agent (Claude Code, Codex, Cursor, etc.) themselves — report
  those to the respective vendor.
- Behavior that only occurs when a user has explicitly granted the agent permissions and
  the skill acts within its documented purpose.
- Telemetry that is documented and opt-out-able (the version beacon in the visual
  companion; disable with `SUPERPOWERS_DISABLE_TELEMETRY`).

## Hardening guidance for users

- Pin the marketplace/plugin to a specific commit SHA and review diffs before bumping.
- Set `SUPERPOWERS_DISABLE_TELEMETRY=1` (or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`)
  to eliminate the version beacon.
- Run in an ephemeral, network-policy-constrained environment where practical.
