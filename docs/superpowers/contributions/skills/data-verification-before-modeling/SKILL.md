---
name: data-verification-before-modeling
description: Use BEFORE training or evaluating any model on a dataset. Enforces a data-integrity gate — leakage, distribution shift, target/imbalance, and split hygiene — so that no modeling effort is spent on top of a broken dataset. This is the data analogue of verification-before-completion.
---

# Data Verification Before Modeling

Superpowers' core discipline is: **do not claim done until verified.** The same rule
applies to data. A model score is meaningless if the dataset underneath it is leaking,
shifted, or split wrong. This skill is a **mandatory gate you run before modeling**, not an
optional EDA nicety.

## When to use

- Before the first `fit`/`train` on a new dataset or a new feature set.
- Before trusting any validation/leaderboard score that suddenly looks "too good."
- Before submitting to a competition (e.g. Kaggle) where train/test drift is common.

## The gate — four checks, each must pass or be explicitly waived

Run these as a checklist. Treat a failure as a **blocker**, not a footnote. If you waive a
check, write down why.

### 1. Leakage
- [ ] No feature is a proxy for the target (near-perfect single-feature separation is a red flag — investigate, do not celebrate).
- [ ] No future information leaks into past rows (time-ordered data split by time, not randomly).
- [ ] No identifier/aggregate computed over the full dataset (target encoding, group stats) leaks across the split boundary — fit such transforms on train folds only.

### 2. Distribution shift (train vs test/holdout)
- [ ] Compare feature distributions between train and test. Large divergence on an important feature means your validation will not predict test performance.
- [ ] A quick adversarial-validation check (can a classifier tell train from test?) that scores well above 0.5 AUC signals shift — record which features drive it.

### 3. Target and imbalance
- [ ] Target distribution inspected; class imbalance quantified and reflected in the metric and the split (stratification).
- [ ] The evaluation metric matches the problem (imbalanced → not raw accuracy).

### 4. Split hygiene
- [ ] Groups that must not be split across folds (same user/session/entity) are kept together (grouped CV).
- [ ] Validation strategy mirrors how the model will be judged (time-based holdout for time series, etc.).
- [ ] Preprocessing is fit on train folds only and applied to validation — no fitting on the full set before splitting.

## Discipline: interrogate surprising results, don't paper over them

A verification result that contradicts your hypothesis is a signal to **dig, not to patch**.
- A suspiciously high CV score → suspect leakage first, before believing the model.
- A validation score that won't reproduce on holdout → suspect shift or split leakage, not
  "just variance."
Do not respond to a failed check with a quick fallback that hides it. Fix the dataset or
document the limitation, then proceed.

## Output of this skill

Before modeling begins, produce a short **data verification note**:
- Which checks passed, which failed, which were waived (and why).
- The concrete evidence (a distribution comparison, the adversarial-validation AUC, the
  leakage candidate found).
- The validation strategy chosen, and why it mirrors the real evaluation.

Only after this note exists is modeling considered "unblocked."

## Relationship to other skills

- Pairs with `verification-before-completion`: this is its data-layer counterpart.
- Pairs with `systematic-debugging`: when a score regresses, bisect the data pipeline the
  same way you bisect code.
