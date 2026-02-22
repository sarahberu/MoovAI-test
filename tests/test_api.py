from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MOCK_REPORT = {
    "executive_summary": "The Oura Ring Gen 3 holds a strong premium position in the Canadian market.",
    "pricing_analysis": {
        "prices_by_retailer": {"Amazon.ca": 449.99, "BestBuy.ca": 459.99},
        "average_price": 454.99,
        "price_range": {"min": 449.99, "max": 459.99},
        "price_positioning": "Premium pricing consistent with brand positioning.",
    },
    "competitive_landscape": {
        "main_competitors": [
            {"name": "Samsung Galaxy Ring", "price_cad": 549.99, "retailer": "BestBuy.ca", "category": "fitness ring"}
        ],
        "market_position": "Market leader in the premium fitness ring segment.",
        "competitive_advantages": ["Superior sleep tracking", "Titanium build"],
    },
    "sentiment_analysis": {
        "overall_sentiment": "positive",
        "sentiment_score": 0.78,
        "strengths": ["sleep tracking", "battery life"],
        "weaknesses": ["subscription cost"],
        "value_positioning": "premium",
    },
    "strategic_recommendations": ["Introduce a loyalty program for Canadian customers"],
}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_200():
    with patch("app.api.routes.orchestrate", return_value=MOCK_REPORT):
        response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3", "market": "Canada"})
    assert response.status_code == 200


def test_analyze_response_contains_all_fields():
    with patch("app.api.routes.orchestrate", return_value=MOCK_REPORT):
        response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3", "market": "Canada"})
    data = response.json()
    for field in ("executive_summary", "pricing_analysis", "competitive_landscape", "sentiment_analysis", "strategic_recommendations"):
        assert field in data, f"Missing field: {field}"


def test_analyze_rejects_non_canada_market():
    response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3", "market": "USA"})
    assert response.status_code == 422


def test_analyze_requires_product_name():
    response = client.post("/analyze", json={"market": "Canada"})
    assert response.status_code == 422


def test_analyze_requires_market():
    response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3"})
    assert response.status_code == 422


def test_analyze_returns_500_on_pipeline_failure():
    with patch("app.api.routes.orchestrate", side_effect=Exception("Unexpected error")):
        response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3", "market": "Canada"})
    assert response.status_code == 500


def test_analyze_pricing_analysis_structure():
    with patch("app.api.routes.orchestrate", return_value=MOCK_REPORT):
        response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3", "market": "Canada"})
    pricing = response.json()["pricing_analysis"]
    assert "prices_by_retailer" in pricing
    assert "average_price" in pricing
    assert "price_range" in pricing
    assert "price_positioning" in pricing


def test_analyze_strategic_recommendations_is_list():
    with patch("app.api.routes.orchestrate", return_value=MOCK_REPORT):
        response = client.post("/analyze", json={"product_name": "Oura Ring Gen 3", "market": "Canada"})
    recs = response.json()["strategic_recommendations"]
    assert isinstance(recs, list)
    assert len(recs) > 0
