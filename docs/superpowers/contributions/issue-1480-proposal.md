# Proposal for #1480 — Reword the SessionStart injection text to avoid self-triggering injection detection

> Draft comment for [obra/superpowers#1480](https://github.com/obra/superpowers/issues/1480).
> The issue is currently labeled `needs-repro-case`; this proposal supplies a
> reproduction procedure plus a concrete, low-risk fix.

## Summary

The `SessionStart` hook wraps the injected skill context as:

```
<EXTREMELY_IMPORTANT>
You have superpowers.
...
```

The phrase **"You have superpowers."**, especially inside an `EXTREMELY_IMPORTANT`
envelope, pattern-matches the shape of a prompt-injection attempt ("you now have new
capabilities / ignore prior limits"). With extended thinking enabled, the model spends
reasoning tokens deciding whether this is an injection before proceeding. The end result
is usually correct, but the false positive is (a) visible in thinking blocks, (b) a waste
of reasoning tokens on every session, and (c) mildly corrosive to the user's trust in the
plugin.

## Reproduction procedure (addresses the `needs-repro-case` label)

1. Install Superpowers and enable it so the `SessionStart` hook runs.
2. Start a fresh Claude Code session **with extended thinking enabled** (the effect is
   most visible here; it is a thinking-phase artifact).
3. In the first thinking block, observe reasoning that questions whether the
   "You have superpowers." line is a legitimate instruction or an injection attempt —
   e.g. weighing whether to trust a message claiming to grant new capabilities.
4. Confirm the model still proceeds correctly afterward (functional impact is low; the
   cost is wasted reasoning + eroded trust, not a wrong answer).

Notes to aid triage:
- The trigger is the **framing** ("You have superpowers." under `EXTREMELY_IMPORTANT`),
  not the skill content that follows.
- The effect is intermittent across model versions because it depends on the model's
  injection heuristics; capturing one thinking transcript is sufficient evidence.

## Proposed fix (minimal, behavior-preserving)

Replace the capability-claim phrasing with a neutral, factual framing that describes what
is available rather than asserting a granted power:

| Current | Proposed |
| ------- | -------- |
| `You have superpowers.` | `The following skills are available to you via the Skill tool.` |
| (alt.) | `You have access to the following skills.` |

Both alternatives preserve the hook's purpose (advertise the skills) while removing the
"granted new capabilities" pattern that the detector keys on. This is a one-line change in
`hooks/session-start` (and any harness manifest that duplicates the wrapper text).

## Why this is worth doing despite low functional impact

- It runs on **every session**, so the wasted reasoning and the trust cost recur constantly.
- It undermines the plugin's credibility precisely for the security-conscious users who
  read thinking output.
- The fix is one line, reversible, and carries no behavioral risk.

If maintainers prefer, I'm happy to open a PR implementing the reword plus a small snapshot
test asserting the injected context no longer contains the capability-claim phrasing.
