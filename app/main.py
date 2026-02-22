import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="MoovAI Market Analysis Agent",
    description=(
        "AI agent that orchestrates web scraping, sentiment analysis, and report "
        "generation to produce structured market intelligence for the Canadian market."
    ),
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
