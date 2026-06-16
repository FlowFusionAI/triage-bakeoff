"""Validate and summarise data/golden_set.jsonl.

Run after generating OR editing the golden set:

    uv run --no-project --with pydantic python scripts/check_golden_set.py

Checks every row parses, has the required fields, valid enum values, and a unique
id; then prints the stratification (category x urgency matrix, plus sentiment,
hard-case, and needs-review counts) so coverage is visible at a glance.
Exits non-zero if any row is invalid -- safe to wire into CI later.
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.schema import Category, Sentiment, Urgency  # noqa: E402

PATH = ROOT / "data" / "golden_set.jsonl"
CATS = [c.value for c in Category]
URGS = [u.value for u in Urgency]
SENTS = [s.value for s in Sentiment]
REQUIRED = ("id", "text", "category", "urgency", "sentiment")


def main() -> int:
    rows: list[dict] = []
    errors: list[str] = []
    seen_ids: set[str] = set()

    for n, raw in enumerate(PATH.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {n}: invalid JSON ({exc})")
            continue
        rid = row.get("id")
        for field in REQUIRED:
            if field not in row:
                errors.append(f"line {n} ({rid}): missing field '{field}'")
        if rid in seen_ids:
            errors.append(f"line {n}: duplicate id {rid}")
        seen_ids.add(rid)
        if row.get("category") not in CATS:
            errors.append(f"line {n} ({rid}): bad category {row.get('category')!r}")
        if row.get("urgency") not in URGS:
            errors.append(f"line {n} ({rid}): bad urgency {row.get('urgency')!r}")
        if row.get("sentiment") not in SENTS:
            errors.append(f"line {n} ({rid}): bad sentiment {row.get('sentiment')!r}")
        if not str(row.get("text", "")).strip():
            errors.append(f"line {n} ({rid}): empty text")
        rows.append(row)

    print(f"Loaded {len(rows)} tickets from {PATH.relative_to(ROOT)}\n")

    matrix: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        matrix[r.get("category")][r.get("urgency")] += 1

    cw = 9
    header = "category".ljust(18) + "".join(u.ljust(cw) for u in URGS) + "total"
    print(header)
    print("-" * len(header))
    totals: Counter = Counter()
    for c in CATS:
        counts = matrix[c]
        totals.update(counts)
        line = c.ljust(18) + "".join(str(counts.get(u, 0)).ljust(cw) for u in URGS)
        print(line + str(sum(counts.values())))
    print("-" * len(header))
    print("TOTAL".ljust(18) + "".join(str(totals.get(u, 0)).ljust(cw) for u in URGS) + str(sum(totals.values())))

    sent = Counter(r.get("sentiment") for r in rows)
    hard = sum(1 for r in rows if r.get("hard"))
    needs = sum(1 for r in rows if r.get("needs_review"))
    pct = (hard / len(rows) * 100) if rows else 0
    print("\nsentiment: " + ", ".join(f"{s}={sent.get(s, 0)}" for s in SENTS))
    print(f"hard cases: {hard} ({pct:.0f}%)    needs_review: {needs}/{len(rows)}")

    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors:
            print("  - " + e)
        return 1
    print("\nAll rows valid - OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
