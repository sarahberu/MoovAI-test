import logging
from typing import Any

from app.tools.report import run_report_generator
from app.tools.scraper import run_scraper
from app.tools.sentiment import run_sentiment_analysis

logger = logging.getLogger(__name__)


def orchestrate(product_name: str, market: str) -> dict[str, Any]:
    """
    Core orchestrator that coordinates tool execution in sequence.

    Execution flow:
    1. Web Scraper      → raw market data (prices, competitors, reviews)
    2. Sentiment Tool   → structured review insights
    3. Report Generator → final strategic report

    Each step is logged. Exceptions propagate to the API layer for
    centralized HTTP error handling.
    """
    logger.info("Starting analysis for '%s' in %s", product_name, market)

    # Step 1: Collect market data
    logger.info("Step 1/3: Running web scraper")
    scraper_data = run_scraper(product_name, market)
    logger.info(
        "Scraper complete. Retailers: %d | Competitors: %d | Reviews: %d",
        len(scraper_data["prices_by_retailer"]),
        len(scraper_data["competitors"]),
        len(scraper_data["review_samples"]),
    )

    # Step 2: Analyze sentiment from collected reviews
    logger.info("Step 2/3: Running sentiment analysis")
    sentiment_data = run_sentiment_analysis(product_name, market, scraper_data["review_samples"])
    logger.info(
        "Sentiment complete. Overall: %s (score: %.2f)",
        sentiment_data["overall_sentiment"],
        sentiment_data["sentiment_score"],
    )

    # Step 3: Generate strategic report from aggregated data
    logger.info("Step 3/3: Generating strategic report")
    report = run_report_generator(product_name, market, scraper_data, sentiment_data)
    logger.info("Report generation complete")

    return report
