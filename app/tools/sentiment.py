import json
import os
import re
from typing import Any

import anthropic

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def run_sentiment_analysis(product_name: str, market: str, review_samples: list[str]) -> dict[str, Any]:
    """
    LLM-based sentiment analyzer tool.

    Takes customer review samples and extracts structured insights:
    overall sentiment, strengths, weaknesses, and value positioning.
    Uses a low temperature for stable, deterministic output.
    """
    reviews_text = "\n".join(f"- {review}" for review in review_samples)

    system_prompt = (
        "You are a sentiment analysis expert. "
        "Base your analysis strictly on the reviews provided. "
        "Do not invent data or make assumptions beyond what is explicitly stated in the reviews."
    )

    user_prompt = f"""Analyze the following customer reviews for {product_name} in the {market} market.

Reviews:
{reviews_text}

Respond with ONLY valid JSON in this exact format, no markdown, no explanation:
{{
    "overall_sentiment": "positive|negative|neutral|mixed",
    "sentiment_score": <float between 0.0 and 1.0 where 1.0 is most positive>,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "value_positioning": "budget|mid-range|premium"
}}"""

    client = _get_client()
    try:
        message = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=1024,
            temperature=0.1,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as e:
        raise RuntimeError(f"Anthropic API error during sentiment analysis: {e}") from e

    raw = message.content[0].text
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {raw!r}")
    return json.loads(match.group())
