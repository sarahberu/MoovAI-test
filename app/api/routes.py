import logging

from fastapi import APIRouter, HTTPException

from app.models.request import AnalyzeRequest
from app.models.response import AnalyzeResponse
from app.orchestrator.agent import orchestrate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Trigger a full market analysis for a product in a given market.

    Orchestrates three tools in sequence:
    1. Web Scraper (mocked) — pricing, competitors, reviews
    2. Sentiment Analyzer (LLM) — structured review insights
    3. Report Generator (LLM) — strategic intelligence report
    """
    try:
        result = orchestrate(request.product_name, request.market)
        return AnalyzeResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.error("Analysis pipeline failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Analysis pipeline failed. Check server logs for details.",
        ) from exc
