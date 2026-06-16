# CLAUDE.md — working notes for `triage-bakeoff`

> **For any Claude/dev instance picking this up:** this file is the single source of
> truth for *how the build is going*. The public-facing methodology lives in
> [README.md](README.md); this file tracks **phase status, decisions, and gotchas**.
>
> 🔁 **Maintenance rule (the user explicitly asked for this):** whenever you complete
> or change work in a phase, update (a) that phase's checkbox/status below and (b) the
> **Progress Log** at the bottom with a dated one-line entry. Keep this file truthful —
> it is how the next instance knows what is already done.

---

## What this is

A reproducible benchmark comparing five cheap LLMs on one fixed support-ticket
classification task (`category` / `urgency` / `sentiment`), measuring
**accuracy × cost × latency** to produce a Pareto frontier chart + findings writeup.
Built from `PROJECT_BRIEF.md`. Portfolio/credibility project — clarity and honest
methodology matter as much as the result.

## Key decisions (dated)

- **2026-06-16** — Repo is **public**, owned by the **FlowFusionAI** org:
  https://github.com/FlowFusionAI/triage-bakeoff
- **2026-06-16** — Golden set is **synthetic-scaffolded, human-verified**: Claude drafts
  ~70 tickets marked `NEEDS REVIEW`; no result is treated as real until the user verifies labels.
- **2026-06-16** — **Provider access (all DIRECT):** OpenAI, Anthropic, Google/Gemini, plus
  **DeepSeek** and **Groq** (the latter two via the `openai` SDK with a `base_url` override —
  both OpenAI-compatible). User obtained direct Groq + DeepSeek keys, so there is **no relay**
  in the path and latency is directly comparable across all five. OpenRouter was considered as
  an unblock-now option and dropped; it remains only an optional fallback.
- **2026-06-16** — **Transparency:** README discloses AI-assisted development (Claude Code);
  the methodology, golden-set verification, metric choices, and analysis are the user's own.
- **2026-06-16** — Fixed harness rules: **temperature 0**, **N=3 repeats**, **one shared prompt**
  for all models (any per-model deviation must be documented).
- **2026-06-16** — Stack: Python 3.13, `uv`, `pydantic`, `tenacity`, `pandas`, `matplotlib`, `pytest`.

## Open items

- Live **model IDs + pricing** for all five — web-verify on run day, record snapshot date
  (placeholders in `config/models.yaml` are marked `VERIFY`).
- Provider **rate limits** on the ~1,050-call run — handled by the concurrency cap + backoff (Phase 3).

---

## Phase plan & status

Legend: `[ ]` not started · `[~]` in progress · `[x]` done

- `[x]` **Phase 0 — Repo & scaffold.** Public repo created; README (methodology, WIP),
  LICENSE (MIT), `.gitignore` (blocks `.env`), `.env.example`, this file, `.gitattributes`.

- `[ ]` **Phase 1 — Contracts & config** *(offline, no keys)*
  - `src/schema.py` — pydantic models + enums; rejects/flags malformed model output.
  - `prompts/classify.txt` — the single shared prompt **(user sign-off required before use)**.
  - `config/models.yaml` — model list + per-model `price_in`/`price_out` + optional `base_url`.
  - `data/rubric.md` — labelling rules, one paragraph per field.
  - `pyproject.toml` (uv) + `Makefile` (`run`/`score`/`chart`/`test`).

- `[ ]` **Phase 2 — Synthetic golden set** *(offline)*
  - `data/golden_set.jsonl` — ~70 tickets, stratified across all categories/urgencies,
    ~15% hard cases, every row marked `NEEDS REVIEW`. Human verification pass with the user.

- `[ ]` **Phase 3 — Providers & runner** *(keys needed to fire live; testable offline via a fake provider)*
  - `src/providers.py` — normalised `call(prompt, ticket) -> {raw_text, input_tokens, output_tokens}` per provider.
  - `src/runner.py` — explicit `model × ticket × repeat` loops, temp 0, concurrency cap +
    `tenacity` backoff on 429s → `results/raw_calls.csv`.

- `[ ]` **Phase 4 — Scorer, aggregation & tests** *(offline)*
  - `src/scorer.py` — macro-F1 (category), accuracy (urgency, sentiment), cost, latency p50/p95.
  - `src/aggregate.py` — `raw_calls.csv` → `results/summary.csv`.
  - `tests/` — scorer macro-F1 on a known fixture; parser rejects malformed output.

- `[ ]` **Phase 5 — Live run & chart** *(needs keys + ~$1–2 budget)*
  - `make run` (~1,050 calls) → `make score` → `src/chart.py` → `results/pareto.png`.

- `[ ]` **Phase 6 — Writeup.** `writeup/findings.md` (problem → method → results → chart →
  findings → production recommendation). Record price-snapshot date.

---

## Conventions / gotchas

- **Never commit `.env`** — keys are read from it; only `.env.example` is tracked.
- **`results/raw_calls.csv` is sacred** (one row per call, never hand-edited). `summary.csv`
  is *derived* from it, so re-scoring is free and never re-spends on APIs.
- **Prompt is held fixed** across all models — the comparison depends on it.
- **Synthetic ≠ verified.** Golden-set labels are not trustworthy until a human checks them.
- Line endings normalised to LF via `.gitattributes`.

## Progress log

- **2026-06-16** — Phase 0 done: public repo scaffolded (README, LICENSE, `.gitignore`,
  `.env.example`). Added CLAUDE.md phase tracker + `.gitattributes`.
- **2026-06-16** — Provider access finalised to **all-direct** (user obtained Groq + DeepSeek
  keys); dropped OpenRouter to optional fallback, removed the proxy-latency caveat. Added
  AI-assistance disclosure to README. Cleared for Phase 1.
