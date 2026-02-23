import json
from unittest.mock import MagicMock, patch

from app.tools.sentiment import run_sentiment_analysis

MOCK_SENTIMENT = {
    "overall_sentiment": "positive",
    "sentiment_score": 0.78,
    "strengths": ["sleep tracking", "battery life", "build quality"],
    "weaknesses": ["subscription cost", "no display"],
    "value_positioning": "premium",
}

SAMPLE_MARKET = "Canada"
SAMPLE_REVIEWS = [
    "The sleep tracking on this ring is incredibly accurate.",
    "Great device but the subscription feels like a cash grab.",
]


def _mock_message(payload: dict) -> MagicMock:
    msg = MagicMock()
    msg.content = [MagicMock(text=json.dumps(payload))]
    return msg


def test_sentiment_returns_required_schema():
    with patch("app.tools.sentiment._get_client") as mock_get_client:
        mock_get_client.return_value.messages.create.return_value = _mock_message(MOCK_SENTIMENT)

        result = run_sentiment_analysis("Oura Ring Gen 3", SAMPLE_MARKET, SAMPLE_REVIEWS)

        for key in ("overall_sentiment", "sentiment_score", "strengths", "weaknesses", "value_positioning"):
            assert key in result


def test_sentiment_score_is_float_in_range():
    with patch("app.tools.sentiment._get_client") as mock_get_client:
        mock_get_client.return_value.messages.create.return_value = _mock_message(MOCK_SENTIMENT)

        result = run_sentiment_analysis("Oura Ring Gen 3", SAMPLE_MARKET, SAMPLE_REVIEWS)

        assert isinstance(result["sentiment_score"], float)
        assert 0.0 <= result["sentiment_score"] <= 1.0


def test_sentiment_strengths_and_weaknesses_are_lists():
    with patch("app.tools.sentiment._get_client") as mock_get_client:
        mock_get_client.return_value.messages.create.return_value = _mock_message(MOCK_SENTIMENT)

        result = run_sentiment_analysis("Oura Ring Gen 3", SAMPLE_MARKET, SAMPLE_REVIEWS)

        assert isinstance(result["strengths"], list)
        assert isinstance(result["weaknesses"], list)
        assert len(result["strengths"]) > 0


def test_sentiment_calls_llm_with_reviews():
    with patch("app.tools.sentiment._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = _mock_message(MOCK_SENTIMENT)
        mock_get_client.return_value = mock_client

        run_sentiment_analysis("Oura Ring Gen 3", SAMPLE_MARKET, SAMPLE_REVIEWS)

        mock_client.messages.create.assert_called_once()
        call_kwargs = mock_client.messages.create.call_args
        prompt = call_kwargs.kwargs["messages"][0]["content"]
        assert "Oura Ring Gen 3" in prompt
        assert SAMPLE_REVIEWS[0] in prompt
