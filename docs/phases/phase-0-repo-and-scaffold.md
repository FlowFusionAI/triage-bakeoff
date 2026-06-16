# Phase 0 — Repo & scaffold

**Status:** done · **Date:** 2026-06-16 · **Commits:** `982386b`, `ffb4c5e`, `8f4fc0b`

## Goal
Stand up a clean, public repository with the foundation files and a documented methodology,
so the project reads as a real, reproducible piece of work from commit one.

## What was built

| File | Purpose |
|---|---|
| `README.md` | Public methodology + status (clearly marked WIP) |
| `LICENSE` | MIT |
| `.gitignore` | Blocks `.env` (secrets) and Python/tooling noise; keeps `results/` tracked |
| `.env.example` | Lists the five required API keys, no values |
| `CLAUDE.md` | Living build tracker (phase checkboxes, decisions, progress log) |
| `.gitattributes` | Normalises line endings to LF (silences Windows CRLF warnings) |

## Decisions made
- **[D1](../decisions.md)** — public repo under the FlowFusionAI org.
- **[D3](../decisions.md)** — provider access settled to all-direct (interim OpenRouter plan dropped).
- **[D4](../decisions.md)** — AI-assisted development disclosed in the README.

## Visuals
Repo layout is documented in the root [README structure section](../../README.md#repo-structure).

## Metrics / evidence
- Environment verified: git 2.47, gh 2.86 (authenticated), Python 3.13.1, uv 0.11.16.
- Repo created and pushed public: https://github.com/FlowFusionAI/triage-bakeoff

## Report material
> The benchmark is developed in the open as a public repository, with a methodology README and
> an explicit AI-assistance disclosure — the same transparency standard the project applies to
> its results.

## Open items / next
Phase 1 — define the answer schema, the shared prompt, the model config, and the labelling rubric.
