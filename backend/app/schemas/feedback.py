from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    prediction_id: str = Field(..., description="Target prediction ID")
    human_label: str = Field(..., description="REAL, FAKE, MISLEADING, SATIRE, MANIPULATED, or UNCERTAIN")
    reviewer_comment: Optional[str] = Field(None, description="Optional fact-checker comment")

class FeedbackResponse(BaseModel):
    id: str
    prediction_id: str
    human_label: str
    reviewer_comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
