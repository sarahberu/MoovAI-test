from typing import Any

from pydantic import BaseModel


class RetailerDetail(BaseModel):
    price_cad: float
    in_stock: bool
    platform_rating: float
    review_count: int
    shipping: str


class PricingAnalysis(BaseModel):
    retailers: dict[str, RetailerDetail]
    prices_by_retailer: dict[str, float]
    average_price: float
    price_range: dict[str, float]
    price_positioning: str


class CompetitiveLandscape(BaseModel):
    main_competitors: list[dict[str, Any]]
    market_position: str
    competitive_advantages: list[str]


class SentimentAnalysis(BaseModel):
    overall_sentiment: str
    sentiment_score: float
    strengths: list[str]
    weaknesses: list[str]
    value_positioning: str


class AnalyzeResponse(BaseModel):
    executive_summary: str
    pricing_analysis: PricingAnalysis
    competitive_landscape: CompetitiveLandscape
    sentiment_analysis: SentimentAnalysis
    strategic_recommendations: list[str]
