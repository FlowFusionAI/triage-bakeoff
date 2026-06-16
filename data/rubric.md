# Labelling rubric

These are the rules a **human** follows to assign ground-truth labels to each ticket in
`golden_set.jsonl`. The same field definitions are given to every model in
`prompts/classify.txt`, so models are judged against the boundaries described here. When a
ticket is ambiguous, prefer the rule stated below over personal judgement, so the labels
stay consistent across the whole set.

## category

The main subject of the ticket. **billing** = payments, invoices, charges, refunds,
pricing, subscriptions. **technical** = bugs, errors, outages, broken functionality.
**account** = login, access, passwords, profile, roles/permissions. **feature_request** =
asking for a new or improved capability that does not yet exist. **complaint** =
dissatisfaction with no specific actionable fix (pure frustration, threats to cancel with
no concrete ask). **other** = fits none of the above (general questions, partnership or
press enquiries, spam). If a ticket spans several topics, label the **most central** one —
the issue the customer most wants resolved — and use the same tie-break the models are given.

## urgency

How time-sensitive the ticket is, judged on **impact, not tone**. **low** = general
question or minor issue; nothing is blocked. **medium** = affects the user's work but they
can still continue. **high** = the user is blocked or materially impacted and needs a timely
fix. **critical** = active business-critical damage right now: outage, data loss, security
breach, or money actively being lost. Do not let an angry tone inflate urgency — a calm
report of a full outage is still `critical`, and a furious message about a cosmetic typo is
still `low`.

## sentiment

The emotional tone of the **text**, independent of urgency or of whether the request is
reasonable. **negative** = frustrated, angry, disappointed, sarcastic. **neutral** =
matter-of-fact, no strong emotion. **positive** = appreciative, friendly, satisfied. Judge
sarcasm by intent ("great, another outage, exactly what I needed today" is `negative`). A
polite, plain request with no emotional content is `neutral`, not `positive`.

## Hard cases (~15% of the set)

Deliberately include tickets that stress these boundaries, because this is where models
diverge: multi-issue tickets (test the "most central" rule), sarcasm (tests sentiment),
an outage reported calmly vs. a trivial issue reported furiously (tests urgency-vs-tone),
and near-empty or garbage input (label as best fits — usually `other` / `low` / `neutral`).

---

> **Synthetic-draft notice:** the initial `golden_set.jsonl` is machine-drafted to get the
> structure going. Every row is marked `NEEDS REVIEW` and its labels are **not trustworthy
> until a human has verified them against this rubric.** A benchmark is only as good as its
> ground truth.
