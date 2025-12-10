from typing import List, Optional
from pydantic import BaseModel


class AskResponse(BaseModel):
    answer: str
    confidence: float
    risk: str
    reasons: List[str]
    sources: List[str]
