from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.config import settings
from app.database import crud

class ModelService:
    def get_model_info(self, db: Session) -> Dict[str, Any]:
        db_versions = crud.get_model_versions(db)
        active_version = db_versions[0] if db_versions else None

        return {
            "text_model": settings.TEXT_MODEL,
            "vision_model": settings.VISION_MODEL,
            "fusion_strategy": "Late Fusion (Weighted Text/Vision Average) + Cross-Modal Attention",
            "model_version": settings.MODEL_VERSION,
            "device": settings.MODEL_DEVICE,
            "demo_mode": settings.DEMO_MODE,
            "high_confidence_threshold": settings.HIGH_CONFIDENCE_THRESHOLD,
            "review_threshold": settings.REVIEW_THRESHOLD,
            "active_db_version": {
                "version": active_version.version if active_version else settings.MODEL_VERSION,
                "model_name": active_version.model_name if active_version else "Multimodal Transformer Baseline",
                "metrics": active_version.metrics if active_version else {"status": "uninitialized"}
            }
        }

model_service = ModelService()
