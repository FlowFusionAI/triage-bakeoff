# triage-bakeoff

**Which cheap LLM should power a support-ticket triage classifier — and what does each quality tier cost?**

A reproducible benchmark ("bake-off") that runs **one fixed support-ticket classification task** across several budget LLMs and measures the **accuracy × cost × latency** trade-off. The headline output is a Pareto frontier chart and a short, honest findings writeup.

> 🚧 **Status: under active construction.** The methodology and repo structure are in place; the harness is being built out in documented phases (see [Roadmap](#roadmap)). This README will turn into the final methodology + results doc as the project lands. Nothing here claims to be a finished result yet.

---

## The task

Given a raw support ticket (free text), a model must return a structured JSON object with three fields:

| Field | Values | Metric |
|---|---|---|
| `category` | `billing`, `technical`, `account`, `feature_request`, `complaint`, `other` | macro-F1 |
| `urgency` | `low`, `medium`, `high`, `critical` | accuracy |
| `sentiment` | `negative`, `neutral`, `positive` | accuracy |

**The same prompt is used for every model** — no per-model tuning (any exception is documented explicitly, because a hidden prompt difference would invalidate the comparison). All calls run at **temperature 0**.

## Method (at a glance)

1. **Golden set** — ~60–80 human-verified tickets ([`data/golden_set.jsonl`](data/golden_set.jsonl)), stratified across every category and urgency level, with ~15% deliberately hard cases (multi-issue, sarcasm, ambiguous urgency, garbage input). Labelling rules live in [`data/rubric.md`](data/rubric.md). *A benchmark is only as trustworthy as its ground truth — every label is human-verified.*
2. **Runner** — for each **model × ticket × repeat (N=3)**, call the API and record raw output, parsed output, input/output tokens, wall-clock latency, and retry/error counts. Rate limits are handled with a concurrency cap + exponential backoff.
3. **Scoring** — compare parsed output to gold per field; compute cost from measured tokens × price, and latency p50/p95 from the wall-clock samples.
4. **Two-layer results** — every individual call is logged raw to [`results/raw_calls.csv`](results/raw_calls.csv) and never edited; [`results/summary.csv`](results/summary.csv) is computed *from* it. Re-scoring never re-spends money.

## Models benchmarked

Five-model cheap-tier spread. **Pricing and exact model IDs are verified live on the run date** and recorded with a price-snapshot date (prices move monthly).

| Provider | Model | Why it's here |
|---|---|---|
| OpenAI | GPT-5 mini | Recognisable budget tier |
| Anthropic | Claude Haiku 4.5 | Strong instruction-following budget |
| Google | Gemini Flash | Cheapest proprietary tier, free tier |
| DeepSeek | DeepSeek V3 | Price-leader outlier (OpenAI-compatible endpoint) |
| Groq | Llama 4 / Qwen | Open-weight, fast (OpenAI-compatible endpoint) |

> **Access note:** every model is called **directly** on its own provider API (DeepSeek and Groq via the `openai` SDK with a `base_url` override). No third-party relay sits in the path, so **latency is directly comparable across all five models**.
>
> **Price snapshot date:** _TBD — recorded here when the benchmark is run._

## Metrics

Per model: accuracy per field (+ overall), cost per 1,000 calls, latency p50 & p95.
Derived: the Pareto frontier (accuracy vs cost/1k), and the cheapest model that clears 95% overall accuracy.
Rigor add-ons: consistency across the 3 temp-0 repeats, and a bootstrap confidence interval on overall accuracy (≈70 items is a small sample — we state uncertainty honestly rather than over-claiming).

## Reproduce it

> ⚠️ Not yet runnable end-to-end — these are the target commands.

```bash
cp .env.example .env      # then fill in your API keys
uv sync                   # install dependencies
make run                  # call every model × ticket × repeat -> results/raw_calls.csv
make score                # aggregate -> results/summary.csv
make chart                # render results/pareto.png
make test                 # run the scorer/parser unit tests
```

## Repo structure

```
triage-bakeoff/
├── config/models.yaml     # model list + per-model pricing (one-line to add a model)
├── prompts/classify.txt   # the single shared classification prompt
├── data/
│   ├── golden_set.jsonl   # the labelled evaluation set
│   └── rubric.md          # labelling rubric (one paragraph per field)
├── src/
│   ├── schema.py          # pydantic models for the expected output
│   ├── providers.py       # one normalised call() interface per provider
│   ├── runner.py          # explicit loops: model × ticket × repeat
│   ├── scorer.py          # per-field accuracy / macro-F1, cost, latency
│   ├── aggregate.py       # raw calls -> summary table
│   └── chart.py           # Pareto frontier image
├── results/               # raw_calls.csv, summary.csv, pareto.png
└── writeup/findings.md    # the findings report
```

## Roadmap

- [x] Repo + methodology scaffold
- [x] Schema, prompt, rubric, config
- [ ] Synthetic golden set (human verification pending)
- [ ] Provider adapters + runner with rate-limit handling
- [ ] Scorer + aggregation + tests
- [ ] Live benchmark run + Pareto chart
- [ ] Findings writeup

> **Build journal:** the per-phase decisions, diagrams, and metrics live in [`docs/`](docs/) —
> the source material for the final writeup.

## Development & attribution

Built with AI-assisted development (Claude Code). The **methodology is mine** — the task design, the labelling rubric, the human verification of every golden-set label, the choice of metrics, and the analysis and production recommendation in the writeup. The assistant accelerated implementation; the judgement calls that a benchmark lives or dies on are my own. Being explicit about tooling is intentional: it's the same standard of honesty this project applies to its results.

## License

[MIT](LICENSE) © 2026 FlowFusionAI
