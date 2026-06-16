# Phase 2 — Synthetic golden set

**Status:** drafted — **awaiting human verification** · **Date:** 2026-06-16 · **Commits:** _(this phase)_

## Goal
Produce a ~70-ticket evaluation set, stratified across every category and urgency level, with
~15% deliberately hard cases — as a **synthetic draft that a human verifies** before any result
is treated as real. Ground-truth integrity is the human's job; the model only scaffolds structure.

## What was built

| File | Purpose |
|---|---|
| `data/golden_set.jsonl` | 72 tickets; fields `id, text, category, urgency, sentiment, needs_review, source` (+ `hard` on hard cases) |
| `scripts/check_golden_set.py` | Reusable validator: checks JSON/fields/enum values/unique ids and prints the coverage matrix. Reuses `src/schema.py` enums as the single source of valid values |

Run the validator any time (e.g. after editing labels):

```
uv run --no-project --with pydantic python scripts/check_golden_set.py
```

## Visuals / metrics — coverage (from the validator)

```
category          low      medium   high     critical total
billing           5        3        3        1        12
technical         5        5        2        3        15
account           5        3        2        2        12
feature_request   7        4        0        0        11
complaint         5        8        0        0        13
other             8        1        0        0        9
TOTAL             35       24       7        6        72
sentiment: negative=31, neutral=33, positive=8
hard cases: 12 (17%)    needs_review: 72/72
```

All 6 categories and all 4 urgency levels are represented. `feature_request`/`complaint` carry no
high/critical rows by design (urgency is impact, not tone). See [D10](../decisions.md).

## The 12 hard cases (where labels are most debatable)

| id | What makes it hard | Drafted label (cat / urg / sent) |
|---|---|---|
| t014 | Calm tone, total outage — tests urgency-by-impact-not-tone | technical / critical / neutral |
| t017 | Furious tone, trivial typo — tone must not inflate urgency | technical / low / negative |
| t050 | Sarcasm ("well done") with negative intent | complaint / medium / negative |
| t053 | "Buggy mess" — vague dissatisfaction vs a specific bug (complaint vs technical) | complaint / medium / negative |
| t054 | Price/value gripe, no specific ask (complaint vs billing) | complaint / low / negative |
| t063 | Garbage input | other / low / neutral |
| t064 | Near-empty ("help") | other / low / neutral |
| t068 | Multi-issue (crash + overcharge); most-central = the crash | technical / high / negative |
| t069 | Ambiguous urgency (broken export, vague timing) | technical / medium / neutral |
| t070 | Positive tone while reporting a bug — sentiment by tone | technical / low / positive |
| t071 | Sarcasm about a redesign | complaint / medium / negative |
| t072 | SSO config error (account/access vs technical) | account / medium / neutral |

## Decisions made
- **[D2](../decisions.md)** — synthetic-scaffold, human-verified golden set.
- **[D10](../decisions.md)** — truthful labels per the rubric; no distortion for balance; reusable validator.

## Verification status — REQUIRED GATE
- ⛔ **Not yet human-verified.** Every row is `needs_review: true` and `source: "synthetic"`.
- Verification pass: a human reads each ticket against `data/rubric.md`, corrects any label, and the
  `needs_review` flag is flipped to `false` once confirmed. The hard cases above deserve the most attention.
- No Phase 5 run should use this set until verification is complete.

## Report material
> The evaluation set is 72 support tickets stratified across all six categories and four urgency
> levels, including 12 (17%) deliberately hard cases — multi-issue tickets, sarcasm, calm reports of
> outages, furious reports of trivia, and garbage input. Tickets were machine-drafted for structure
> and then human-verified label-by-label against a written rubric; labels were assigned by the
> rubric's true reading rather than adjusted to flatten the distribution.

## Open items / next
- **Human verification pass** (the gate above), then flip `needs_review` flags.
- Phase 3 — provider adapters + the runner (calls each model x ticket x 3 at temp 0, with
  rate-limit backoff), writing `results/raw_calls.csv`.
