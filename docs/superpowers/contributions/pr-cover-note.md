# Cover note for the SECURITY.md PR (ready to post)

> Paste this (lightly adapted) as the PR description when proposing `SECURITY.md` upstream.
> The tone is deliberately deferential to a near-solo maintainer's time.

---

Hi — long-time Superpowers user here (and past contributor). Thank you for the project.

This PR adds a `SECURITY.md`. I know the repo is maintained by a very small team, so I've
written this specifically to **not add ongoing burden**:

- **No SLA.** It says triage is best-effort, with no fixed response deadline — nothing here
  commits you to a timeline you'd have to defend.
- **No bounty.** Stated explicitly, so it doesn't become a magnet for beg-bounty / AI-slop
  reports (the curl/Linux problem).
- **Reproduction required.** Reports without a concrete repro can be deprioritized/closed —
  a front-door filter that reduces vague-report triage load rather than increasing it.
- **Routes to a channel, not to you personally.** It points to GitHub private vulnerability
  reporting first, with `security@primeradiant.com` as the alternative — please swap in
  whatever contact you actually want. Nothing points at your personal mentions.
- **Scoped.** Host-agent bugs, documented opt-out telemetry, and unanalyzed scanner output
  are explicitly out of scope, so those don't land on you as security work.

The motivation: at the repo's current visibility, researchers and scanners are already
looking. Without a front door, findings tend to arrive as **public issues** or scattered
mentions, which is more work for you, not less. A short policy channels them privately.

Everything is placeholder-friendly — change the contact, wording, or scope freely, or close
this if it's not wanted. Happy to also enable GitHub's private vulnerability reporting toggle
guidance in a follow-up if useful.
