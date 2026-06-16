# Decision log

Lightweight ADRs (Architecture Decision Records). Each entry: the context, the call we
made, why, the alternatives, and the consequences. Newest decisions are appended at the
bottom. This is the "why" bank for the final writeup's methodology section.

---

## D1 — Public repo under the FlowFusionAI org
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** This is a portfolio/credibility piece intended to be public.
- **Decision:** Host at `github.com/FlowFusionAI/triage-bakeoff`, public from commit one.
- **Why / alternatives:** Personal account was the obvious alternative; the user chose the
  FlowFusionAI org. Building in the open keeps the methodology honest and reviewable.
- **Consequences:** Nothing half-finished should be misrepresented; WIP is clearly marked.

## D2 — Synthetic-scaffolded, human-verified golden set
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** A benchmark is only as trustworthy as its ground truth, but hand-writing ~70
  stratified tickets from scratch is slow.
- **Decision:** Machine-draft ~70 stratified tickets (incl. ~15% hard cases), mark every row
  `NEEDS REVIEW`, and treat no result as real until a human verifies the labels against the rubric.
- **Why / alternatives:** Pure-real tickets (highest authenticity, blocks progress) or
  treat-synthetic-as-final (fast, but dishonest). The scaffold-then-verify path gets a runnable
  harness immediately without compromising ground-truth integrity.
- **Consequences:** A human verification pass is a required gate before the Phase 5 run.

## D3 — All-direct provider access (no relay)
- **Date:** 2026-06-16 · **Status:** accepted (superseded an interim OpenRouter plan)
- **Context:** The user had OpenAI/Anthropic/Gemini keys but was unsure about DeepSeek/Groq, and
  had a free OpenRouter key that could reach both.
- **Decision:** Call all five models **directly** on their own APIs (DeepSeek & Groq via the
  `openai` SDK + `base_url` override). The user obtained direct DeepSeek + Groq keys.
- **Why / alternatives:** OpenRouter would have unblocked us instantly, but a relay adds a proxy
  hop (inflating/altering latency for those two models) and can route to quantized variants
  (risking accuracy). Going direct keeps **latency comparable across all five** and removes the
  quantization risk. OpenRouter remains an optional fallback.
- **Consequences:** No latency caveat needed; two extra signups were required (done).

## D4 — Disclose AI-assisted development
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** Built with Claude Code; the project's whole theme is honest measurement.
- **Decision:** README states the tooling openly and that the methodology, golden-set
  verification, metric choices, and analysis are the author's own.
- **Why / alternatives:** Concealing AI use reads worse than owning it; confident transparency
  matches the project's values and what reviewers actually assess (can you defend the work?).
- **Consequences:** The author must be able to defend every methodology choice — these docs help.

## D5 — Fixed harness rules: temp 0, N=3, one shared prompt
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** A fair comparison requires holding everything constant except the model.
- **Decision:** Temperature 0 for all calls; 3 repeats per ticket; one identical prompt for every
  model (any per-model deviation must be documented).
- **Why / alternatives:** Temp 0 asks for determinism; running 3× anyway *measures* whether each
  provider actually is deterministic (a stretch metric). A single prompt prevents hidden tuning
  from invalidating the comparison.
- **Consequences:** ~1,050 calls total (5 × ~70 × 3); consistency is reportable.

## D6 — Two-layer results + measured (not fatal) malformed output
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** Scoring logic will evolve; live API calls cost money; models sometimes return junk.
- **Decision:** `raw_calls.csv` (one row per call) is the immutable raw layer; `summary.csv` is
  derived. Malformed model output is recorded and counts against the model, never crashes the run.
- **Why / alternatives:** Re-scoring from raw is free; re-calling APIs is not. "Junk-output rate"
  becomes a quality signal rather than a hidden failure.
- **Consequences:** The scorer must handle parse failures explicitly; raw data is never hand-edited.

## D7 — Schema is lenient on format, strict on vocabulary
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** Models vary in casing and may wrap JSON in prose/fences or add extra keys.
- **Decision:** Normalise case + whitespace (identically for all models) and extract JSON from
  surrounding text before validating; reject any value outside the allowed enums; ignore extra keys.
- **Why / alternatives:** Forbidding extra keys or punishing capitalisation would grade formatting,
  not classification. Rejecting unknown values keeps the vocabulary honest.
- **Consequences:** Fair grading; the parser is the unit under one of the required tests.

## D8 — Prompt gives value definitions and explicit boundary rules
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** Bare enum labels leave too much to interpretation; the hard cases sit on boundaries.
- **Decision:** The shared prompt defines each value briefly, sets a multi-issue tie-break ("most
  central issue"), and states "urgency by impact, not tone" / "sentiment by tone, not
  fulfillability" — the same boundaries as the human rubric.
- **Why / alternatives:** Bare labels would test whether a model *guesses* our intuitions; defining
  the spec tests whether it can *follow* one. The latter is the more defensible, reproducible test.
- **Consequences:** Prompt and rubric must stay in sync; user signed off the wording on 2026-06-16.

## D9 — Prices and model IDs are run-day placeholders
- **Date:** 2026-06-16 · **Status:** accepted
- **Context:** Pricing and exact model IDs drift monthly.
- **Decision:** `config/models.yaml` carries clearly-marked `VERIFY` placeholders; the authoritative
  values + a `price_snapshot_date` are set on the actual run day (Phase 5) and mirrored in the README.
- **Why / alternatives:** Baking in stale numbers now would mislead; the brief explicitly wants a
  recorded snapshot date.
- **Consequences:** Phase 5 includes a live verification step before any cost figures are trusted.

## D10 — Golden set: scenario-based draft, truthful labels (not balanced by force)
- **Date:** 2026-06-16 · **Status:** accepted (labels awaiting human verification)
- **Context:** Need ~70 stratified tickets with ~15% hard cases, but labels must be defensible.
- **Decision:** Author 72 realistic, varied tickets covering all six categories and all four urgency
  levels, with 12 (17%) boundary-stressing hard cases. Label each by the rubric's true reading —
  **do not relabel rows to hit a target distribution.** A reusable validator
  (`scripts/check_golden_set.py`) checks structure and prints the coverage matrix.
- **Why / alternatives:** Forcing a uniform urgency histogram would corrupt ground truth (a receipts
  request is genuinely `low`). A benchmark's answer key must mirror the rubric, not a quota.
- **Consequences:** Distribution is low-heavy and `feature_request`/`complaint` carry no high/critical
  rows (realistic). Every label is `needs_review: true` until a human verifies it against the rubric —
  a required gate before the Phase 5 run.
