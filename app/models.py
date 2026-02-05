from pydantic import BaseModel, Field, validator
from typing import Optional, Literal


class VoiceAnalysisResponse(BaseModel):
    status: Literal["success", "error"]
    language: Optional[str] = None
    classification: Optional[Literal["AI_GENERATED", "HUMAN"]] = None
    confidenceScore: Optional[float] = None
    explanation: Optional[str] = None
    message: Optional[str] = None # For error cases
