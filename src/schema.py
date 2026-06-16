"""The contract for a valid classification answer.

Every model's reply is parsed and validated against the models defined here.
Anything outside the allowed vocabularies is *rejected* rather than silently
accepted -- that lets the harness measure how often each model produces
malformed output, which is itself a quality signal.

Normalisation policy (applied identically to every model so the comparison
stays fair): surrounding whitespace and letter case are normalised before
validation. We are testing classification ability, not whether a model happens
to capitalise "Billing" or wrap its answer in a code fence.
"""

from __future__ import annotations

import json
import re
from enum import Enum

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator


class Category(str, Enum):
    billing = "billing"
    technical = "technical"
    account = "account"
    feature_request = "feature_request"
    complaint = "complaint"
    other = "other"


class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Sentiment(str, Enum):
    negative = "negative"
    neutral = "neutral"
    positive = "positive"


class Classification(BaseModel):
    """The structured answer we expect back for a single ticket."""

    # Extra keys (e.g. a model adding "reasoning") are ignored, not fatal --
    # we only require the three fields to be present and valid.
    model_config = ConfigDict(extra="ignore")

    category: Category
    urgency: Urgency
    sentiment: Sentiment

    @field_validator("category", "urgency", "sentiment", mode="before")
    @classmethod
    def _normalise(cls, value: object) -> object:
        # Lenient on formatting, strict on vocabulary: trim + lowercase, then the
        # enum rejects anything not in the allowed set.
        if isinstance(value, str):
            return value.strip().lower()
        return value


class ParseError(ValueError):
    """Raised when a model's raw text cannot be turned into a valid Classification."""


# Grab the first '{' through the last '}' so we tolerate code fences and prose
# around the JSON object the model was asked to return.
_JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def parse_classification(raw_text: str) -> Classification:
    """Extract and validate a Classification from a model's raw text reply.

    Tolerates markdown fences / surrounding prose, then validates strictly.
    Raises ParseError on anything that is not a single valid classification.
    """
    if not raw_text or not raw_text.strip():
        raise ParseError("empty output")

    match = _JSON_OBJECT.search(raw_text)
    if match is None:
        raise ParseError("no JSON object found in output")

    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ParseError(f"invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ParseError("parsed JSON is not an object")

    try:
        return Classification.model_validate(data)
    except ValidationError as exc:
        raise ParseError(f"schema validation failed: {exc}") from exc
