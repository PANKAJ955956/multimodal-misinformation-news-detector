from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class TextAnalysisResponse(BaseModel):
    score: float = Field(..., description="Text prediction score")
    tokens_processed: int = 0
    model_name: str = ""

class ImageAnalysisResponse(BaseModel):
    score: float = Field(..., description="Image prediction score")
    width: int = 0
    height: int = 0
    model_name: str = ""

class MultimodalAnalysisResponse(BaseModel):
    fusion_score: float = Field(..., description="Multimodal fusion score")
    alignment_score: float = Field(..., description="Text-image semantic alignment score (0-1)")
    alignment_level: str = Field(..., description="LOW, MODERATE, or HIGH alignment")
    fusion_strategy: str = "late_fusion"

class ImportantPhrase(BaseModel):
    text: str
    importance: float

class ExplainabilityResponse(BaseModel):
    important_phrases: List[ImportantPhrase] = []
    heatmap_available: bool = False
    saliency_heatmap: Optional[str] = Field(None, description="Base64 encoded PNG saliency overlay")
    evidence_summary: str = ""

class PredictionRequestText(BaseModel):
    text: str = Field(..., min_length=3, description="Article or claim text to analyze")

class PredictionRequestURL(BaseModel):
    url: str = Field(..., description="Public HTTP/HTTPS article URL to analyze")

class PredictionResponse(BaseModel):
    id: str
    input_type: str = Field(..., description="text, image, multimodal, or url")
    prediction: str = Field(..., description="REAL, FAKE, MISLEADING, SATIRE, or MANIPULATED")
    confidence: float = Field(..., description="Overall model confidence score (0-1)")
    risk_level: str = Field(..., description="LOW, MODERATE, HIGH, or UNCERTAIN")
    probabilities: Dict[str, float] = Field(..., description="Probabilities for each of the 5 classes")
    text_analysis: Optional[TextAnalysisResponse] = None
    image_analysis: Optional[ImageAnalysisResponse] = None
    multimodal_analysis: Optional[MultimodalAnalysisResponse] = None
    explainability: ExplainabilityResponse
    human_review_required: bool = False
    model_version: str
    cached: bool = False
    warning: str = ""
    demo_mode: bool = True
