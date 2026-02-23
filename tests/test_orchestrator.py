import pytest
from unittest.mock import patch

from app.orchestrator.agent import orchestrate

MOCK_SCRAPER = {
    "product_name": "Oura Ring Gen 3",
    "market": "Canada",
    "prices_by_retailer": {"Amazon.ca": 449.99},
    "average_price": 449.99,
    "competitors": [
        {"name": "Samsung Galaxy Ring", "price_cad": 549.99, "retailer": "BestBuy.ca", "category": "fitness ring"}
    ],
    "specifications": {"battery_life": "4-7 days"},
    "review_samples": ["Great product", "Worth the price"],
}

MOCK_SENTIMENT = {
    "overall_sentiment": "positive",
    "sentiment_score": 0.78,
    "strengths": ["sleep tracking"],
    "weaknesses": ["subscription cost"],
    "value_positioning": "premium",
}

MOCK_REPORT = {
    "executive_summary": "The Oura Ring Gen 3 holds a strong premium position in the Canadian market.",
    "pricing_analysis": {
        "prices_by_retailer": {"Amazon.ca": 449.99},
        "average_price": 449.99,
        "price_range": {"min": 449.99, "max": 449.99},
        "price_positioning": "Premium pricing consistent with brand positioning.",
    },
    "competitive_landscape": {
        "main_competitors": [
            {"name": "Samsung Galaxy Ring", "price_cad": 549.99, "retailer": "BestBuy.ca", "category": "fitness ring"}
        ],
        "market_position": "Market leader in the premium fitness ring segment.",
        "competitive_advantages": ["Superior sleep tracking", "Titanium build", "Long battery life"],
    },
    "sentiment_analysis": MOCK_SENTIMENT,
    "strategic_recommendations": ["Introduce a loyalty program for Canadian customers"],
}


def _patch_all():
    return (
        patch("app.orchestrator.agent.run_scraper", return_value=MOCK_SCRAPER),
        patch("app.orchestrator.agent.run_sentiment_analysis", return_value=MOCK_SENTIMENT),
        patch("app.orchestrator.agent.run_report_generator", return_value=MOCK_REPORT),
    )


def test_orchestrate_calls_all_three_tools():
    with (
        patch("app.orchestrator.agent.run_scraper", return_value=MOCK_SCRAPER) as mock_scraper,
        patch("app.orchestrator.agent.run_sentiment_analysis", return_value=MOCK_SENTIMENT) as mock_sentiment,
        patch("app.orchestrator.agent.run_report_generator", return_value=MOCK_REPORT) as mock_report,
    ):
        orchestrate("Oura Ring Gen 3", "Canada")

        mock_scraper.assert_called_once_with("Oura Ring Gen 3", "Canada")
        mock_sentiment.assert_called_once()
        mock_report.assert_called_once()


def test_orchestrate_passes_reviews_to_sentiment():
    with (
        patch("app.orchestrator.agent.run_scraper", return_value=MOCK_SCRAPER),
        patch("app.orchestrator.agent.run_sentiment_analysis", return_value=MOCK_SENTIMENT) as mock_sentiment,
        patch("app.orchestrator.agent.run_report_generator", return_value=MOCK_REPORT),
    ):
        orchestrate("Oura Ring Gen 3", "Canada")

        args, _ = mock_sentiment.call_args
        assert args[2] == MOCK_SCRAPER["review_samples"]


def test_orchestrate_passes_sentiment_to_report():
    with (
        patch("app.orchestrator.agent.run_scraper", return_value=MOCK_SCRAPER),
        patch("app.orchestrator.agent.run_sentiment_analysis", return_value=MOCK_SENTIMENT),
        patch("app.orchestrator.agent.run_report_generator", return_value=MOCK_REPORT) as mock_report,
    ):
        orchestrate("Oura Ring Gen 3", "Canada")

        args, _ = mock_report.call_args
        assert args[3] == MOCK_SENTIMENT  # 4th positional arg: sentiment_data



def test_orchestrate_raises_on_scraper_failure():
    with patch("app.orchestrator.agent.run_scraper", side_effect=RuntimeError("Scraper failed")):
        with pytest.raises(RuntimeError, match="Scraper failed"):
            orchestrate("Oura Ring Gen 3", "Canada")


def test_orchestrate_raises_on_sentiment_failure():
    with (
        patch("app.orchestrator.agent.run_scraper", return_value=MOCK_SCRAPER),
        patch("app.orchestrator.agent.run_sentiment_analysis", side_effect=ValueError("LLM parse error")),
    ):
        with pytest.raises(ValueError, match="LLM parse error"):
            orchestrate("Oura Ring Gen 3", "Canada")


def test_orchestrate_raises_on_report_failure():
    with (
        patch("app.orchestrator.agent.run_scraper", return_value=MOCK_SCRAPER),
        patch("app.orchestrator.agent.run_sentiment_analysis", return_value=MOCK_SENTIMENT),
        patch("app.orchestrator.agent.run_report_generator", side_effect=RuntimeError("LLM parse error")),
    ):
        with pytest.raises(RuntimeError, match="LLM parse error"):
            orchestrate("Oura Ring Gen 3", "Canada")
