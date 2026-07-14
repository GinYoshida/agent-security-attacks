# Superpowers contribution drafts

Drafts prepared for contributing back to [obra/superpowers](https://github.com/obra/superpowers).
These live here for review and version control; the actual upstream submission (PR / private
security report) is done manually from an environment with access to that repository.

## Contents

| File | Track | Upstream target | Status |
| ---- | ----- | --------------- | ------ |
| `SECURITY.md` | Short-term | New file at repo root (public PR) | Ready for review |
| `pr-cover-note.md` | Short-term | PR description for the `SECURITY.md` PR | Ready for review |
| `issue-1480-proposal.md` | Short-term | Comment/PR on [#1480](https://github.com/obra/superpowers/issues/1480) | Ready for review |
| `skill-injection-propagation-disclosure.md` | Mid-term | **Private** security report | **HOLD** until `SECURITY.md` merged |
| `skills/data-verification-before-modeling/SKILL.md` | Mid-term | New skill PR | Draft |

### SECURITY.md design intent (low burden for a near-solo maintainer)

The policy is written to *reduce* maintainer load, not add it:
no SLA (best-effort only), no bounty (deters beg-bounty / AI-slop), reproduction required
(front-door filter), contact routed to GitHub private reporting + an org address rather than
personal mentions, and a scope that excludes host-agent bugs, opt-out telemetry, and raw
scanner output. `pr-cover-note.md` explains this framing to the maintainer when submitting.

## Suggested sequencing

1. **`SECURITY.md`** first — it creates the reporting channel the disclosure needs, and it is
   a low-controversy, high-value gap (no `SECURITY.md`, 0 advisories today).
2. **`issue-1480-proposal.md`** — small, self-contained, and it now includes the reproduction
   the issue was blocked on (`needs-repro-case`).
3. **`skill-injection-propagation-disclosure.md`** — only after step 1, via the private
   channel. It is a demonstration of impact (benign marker), not a weaponized exploit.
4. **`data-verification-before-modeling`** — independent of the security items; can go anytime.

## Constraint note

The session that authored these drafts had GitHub access scoped to the author's own
repositories only, so it could not open issues or PRs on obra/superpowers directly. Review
each draft, then submit from your own environment.
