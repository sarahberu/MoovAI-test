from typing import Literal

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    product_name: str
    market: Literal["Canada"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_name": "Oura Ring Gen 3",
                "market": "Canada",
            }
        }
    }
