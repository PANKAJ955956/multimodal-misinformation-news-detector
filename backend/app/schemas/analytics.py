from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class AnalyticsResponse(BaseModel):
    total_analyses: int
    predictions_by_class: Dict[str, int]
    average_confidence: float
    human_review_count: int
    corrections_count: int

class ModelVersionResponse(BaseModel):
    id: str
    model_name: str
    version: str
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
