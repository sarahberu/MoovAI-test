import json
from unittest.mock import MagicMock, patch

from app.tools.report import run_report_generator

MOCK_SCRAPER = {
    "retailers": {
        "Amazon.ca": {"price_cad": 449.99, "in_stock": True, "platform_rating": 4.3, "review_count": 1842, "shipping": "Free with Prime"},
    },
    "prices_by_retailer": {"Amazon.ca": 449.99},
    "average_price": 449.99,
    "competitors": [{"name": "Samsung Galaxy Ring", "price_cad": 549.99, "retailer": "BestBuy.ca", "category": "fitness ring"}],
    "specifications": {"battery_life": "4-7 days", "sensors": ["heart rate", "SpO2"]},
}

MOCK_SENTIMENT = {
    "overall_sentiment": "positive",
    "sentiment_score": 0.78,
    "strengths": ["sleep tracking"],
    "weaknesses": ["subscription cost"],
    "value_positioning": "premium",
}

MOCK_REPORT = {
    "executive_summary": "Strong premium position in the Canadian market.",
    "pricing_analysis": {
        "retailers": MOCK_SCRAPER["retailers"],
        "prices_by_retailer": {"Amazon.ca": 449.99},
        "average_price": 449.99,
        "price_range": {"min": 449.99, "max": 449.99},
        "price_positioning": "Premium pricing consistent with brand positioning.",
    },
    "competitive_landscape": {
        "main_competitors": MOCK_SCRAPER["competitors"],
        "market_position": "Market leader in the premium fitness ring segment.",
        "competitive_advantages": ["Superior sleep tracking", "Titanium build"],
    },
    "sentiment_analysis": MOCK_SENTIMENT,
    "strategic_recommendations": ["Launch loyalty program", "Expand retail presence"],
}


def _mock_message(payload: dict) -> MagicMock:
    msg = MagicMock()
    msg.content = [MagicMock(text=json.dumps(payload))]
    return msg


def test_report_returns_required_schema():
    with patch("app.tools.report._get_client") as mock_get_client:
        mock_get_client.return_value.messages.create.return_value = _mock_message(MOCK_REPORT)

        result = run_report_generator("Oura Ring Gen 3", "Canada", MOCK_SCRAPER, MOCK_SENTIMENT)

        for key in ("executive_summary", "pricing_analysis", "competitive_landscape", "sentiment_analysis", "strategic_recommendations"):
            assert key in result


def test_report_calls_llm_with_product_and_market():
    with patch("app.tools.report._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _mock_message(MOCK_REPORT)
        mock_get_client.return_value = mock_client

        run_report_generator("Oura Ring Gen 3", "Canada", MOCK_SCRAPER, MOCK_SENTIMENT)

        mock_client.messages.create.assert_called_once()
        prompt = mock_client.messages.create.call_args.kwargs["messages"][0]["content"]
        assert "Oura Ring Gen 3" in prompt
        assert "Canada" in prompt


