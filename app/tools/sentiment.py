import json
import os
from typing import Any

import anthropic

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def run_sentiment_analysis(product_name: str, review_samples: list[str]) -> dict[str, Any]:
    """
    LLM-based sentiment analyzer tool.

    Takes customer review samples and extracts structured insights:
    overall sentiment, strengths, weaknesses, and value positioning.
    Uses a low temperature for stable, deterministic output.
    """
    reviews_text = "\n".join(f"- {review}" for review in review_samples)

    prompt = f"""You are a sentiment analysis expert. Analyze the following customer reviews for {product_name} in the Canadian market.

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
    message = client.messages.create(
        model=os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=1024,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code blocks if the LLM wraps its response in ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
