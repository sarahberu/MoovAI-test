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


def run_report_generator(
    product_name: str,
    market: str,
    scraper_data: dict[str, Any],
    sentiment_data: dict[str, Any],
) -> dict[str, Any]:
    """
    LLM-based report generator tool.

    Acts as a Market Intelligence Analyst: synthesizes pricing data,
    competitive landscape, and sentiment insights into a structured
    strategic business report in JSON format.
    """
    system_prompt = (
        f"You are a Market Intelligence Analyst specializing in the {market} market. "
        "Base your analysis strictly on the data provided. "
        "Do not invent prices, competitors, or market information not present in the input."
    )

    user_prompt = f"""Generate a comprehensive market intelligence report based on the following data.

Product: {product_name}
Market: {market}

Pricing Data:
{json.dumps({"prices_by_retailer": scraper_data["prices_by_retailer"], "average_price": scraper_data["average_price"]}, indent=2)}

Competitor Landscape:
{json.dumps(scraper_data["competitors"], indent=2)}

Product Specifications:
{json.dumps(scraper_data["specifications"], indent=2)}

Sentiment Analysis Results:
{json.dumps(sentiment_data, indent=2)}

Respond with ONLY valid JSON in this exact format, no markdown, no explanation:
{{
    "executive_summary": "<2-3 sentence strategic summary of the product position in the {market} market>",
    "pricing_analysis": {{
        "retailers": {json.dumps(scraper_data["retailers"])},
        "prices_by_retailer": {json.dumps(scraper_data["prices_by_retailer"])},
        "average_price": {scraper_data["average_price"]},
        "price_range": {{"min": <float>, "max": <float>}},
        "price_positioning": "<narrative about how the product is priced relative to competitors in {market}>"
    }},
    "competitive_landscape": {{
        "main_competitors": {json.dumps(scraper_data["competitors"])},
        "market_position": "<description of where the product sits in the {market} competitive landscape>",
        "competitive_advantages": ["advantage1", "advantage2", "advantage3"]
    }},
    "sentiment_analysis": {{
        "overall_sentiment": "{sentiment_data['overall_sentiment']}",
        "sentiment_score": {sentiment_data['sentiment_score']},
        "strengths": {json.dumps(sentiment_data['strengths'])},
        "weaknesses": {json.dumps(sentiment_data['weaknesses'])},
        "value_positioning": "{sentiment_data['value_positioning']}"
    }},
    "strategic_recommendations": ["recommendation1", "recommendation2", "recommendation3", "recommendation4"]
}}"""

    client = _get_client()
    try:
        message = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=2048,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as e:
        raise RuntimeError(f"Anthropic API error during report generation: {e}") from e

    raw = message.content[0].text
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {raw!r}")
    return json.loads(match.group())
