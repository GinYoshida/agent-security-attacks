# Responsible-disclosure draft — Session-wide propagation of skill/context content

> **Status: HOLD until an upstream reporting channel exists.**
> Per the agreed sequencing, do **not** send this upstream until `SECURITY.md`
> (with private vulnerability reporting) is merged into obra/superpowers. Then submit
> via the private channel, not a public issue.
>
> This document is a **demonstration of impact for defensive disclosure**, not an attack
> tool. It deliberately uses a harmless marker and does not include a weaponized skill.

## Class of issue

Superpowers' `SessionStart` hook reads skill Markdown and injects it, wrapped in an
`EXTREMELY_IMPORTANT` envelope, into the context of **every** session — main agent and
sub-agents alike. Consequences:

1. **Blast radius.** A single modified skill file affects all sessions of all users who
   install that version, and reaches sub-agents that the user never directly configured.
2. **High-trust framing.** The injected text is presented as `EXTREMELY_IMPORTANT`, i.e.
   with elevated authority relative to ordinary file content the agent reads later.
3. **Amplification of a supply-chain compromise.** This is not a remote-exploitable bug on
   its own — it presupposes that an attacker can alter skill content (compromised upstream,
   a malicious fork, a poisoned dependency, or a tampered local checkout). The finding is
   about **how far such a compromise travels and how much authority it inherits**, which is
   what makes supply-chain integrity (pinning, review, `SECURITY.md`) load-bearing here.

This complements the already-fixed [#1014](https://github.com/obra/superpowers/issues/1014)
(remote cross-origin injection into the brainstorm server): #1014 is the *entry*, this is
the *propagation and privilege* once content is in the skill path.

## Benign demonstration (marker only — no payload)

Purpose: show that skill content reaches sub-agent context with elevated framing, using a
string that does nothing harmful.

1. In a **local, throwaway checkout** of the plugin, append one line to an already-loaded
   skill's Markdown — a unique, inert marker such as:
   `CANARY-7f3a: (harmless disclosure marker — no instruction).`
2. Start a fresh session, then dispatch a trivial sub-agent task.
3. Observe the marker string present in the injected context of **both** the main session
   and the sub-agent, carried under the `EXTREMELY_IMPORTANT` wrapper.

The marker is deliberately a non-instruction. The point demonstrated is **reach and
framing**, not any behavior change. No exfiltration, command execution, or destructive
action is performed or described.

## Impact (stated, not enacted)

If the modified content were an *instruction* rather than an inert marker, it would inherit
the `EXTREMELY_IMPORTANT` authority and apply to every session and sub-agent. That is the
severity argument. This document intentionally stops at the marker to keep it a defensive
artifact.

## Proposed mitigations (for maintainer discussion)

| Layer | Mitigation |
| ----- | ---------- |
| Integrity | Ship a manifest of expected skill-file hashes; have the hook verify skill files against it before injecting, and warn on mismatch. |
| Framing | Reconsider the `EXTREMELY_IMPORTANT` envelope for auto-injected content; lower framing reduces the authority a poisoned skill inherits (relates to #1480). |
| Provenance | Pin the plugin/marketplace to a commit SHA and document review-before-bump so silent updates cannot reach users (relates to a `SECURITY.md` policy). |
| Least privilege | Document how to constrain hook-originated Bash/network via the host agent's permission model; note current limits explicitly. |

## Reporting metadata (fill in at submission time)

- Affected component: `hooks/session-start` + `skills/**` injection path.
- Version/commit: `<pin the exact SHA reproduced against>`.
- Preconditions: attacker can modify skill content (supply-chain), not remote-unprivileged.
- Reporter: `<your handle>` — prior contributor to this project.
