from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from app.database.models import PredictionDB, FeedbackDB, AuditLogDB, ModelVersionDB

def create_prediction(db: Session, prediction_data: dict) -> PredictionDB:
    db_obj = PredictionDB(**prediction_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_prediction_by_id(db: Session, prediction_id: str) -> Optional[PredictionDB]:
    return db.query(PredictionDB).filter(PredictionDB.id == prediction_id).first()

def get_predictions_list(db: Session, skip: int = 0, limit: int = 50) -> List[PredictionDB]:
    return db.query(PredictionDB).order_by(PredictionDB.created_at.desc()).offset(skip).limit(limit).all()

def count_predictions(db: Session) -> int:
    return db.query(func.count(PredictionDB.id)).scalar() or 0

def create_feedback(db: Session, feedback_data: dict) -> FeedbackDB:
    db_obj = FeedbackDB(**feedback_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_feedback_for_prediction(db: Session, prediction_id: str) -> List[FeedbackDB]:
    return db.query(FeedbackDB).filter(FeedbackDB.prediction_id == prediction_id).all()

def get_all_feedback(db: Session, skip: int = 0, limit: int = 50) -> List[FeedbackDB]:
    return db.query(FeedbackDB).order_by(FeedbackDB.created_at.desc()).offset(skip).limit(limit).all()

def create_audit_log(db: Session, action: str, prediction_id: Optional[str] = None, metadata: Optional[dict] = None) -> AuditLogDB:
    db_obj = AuditLogDB(action=action, prediction_id=prediction_id, metadata_json=metadata)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_analytics_summary(db: Session) -> Dict[str, Any]:
    total_analyses = db.query(func.count(PredictionDB.id)).scalar() or 0
    
    # Class breakdown
    class_counts_query = db.query(PredictionDB.prediction, func.count(PredictionDB.id)).group_by(PredictionDB.prediction).all()
    predictions_by_class = {cls: count for cls, count in class_counts_query}
    for cls in ["REAL", "FAKE", "MISLEADING", "SATIRE", "MANIPULATED"]:
        if cls not in predictions_by_class:
            predictions_by_class[cls] = 0

    # Average confidence
    avg_conf = db.query(func.avg(PredictionDB.confidence)).scalar() or 0.0

    # Feedback counts
    human_review_count = db.query(func.count(FeedbackDB.id)).scalar() or 0
    
    # Correction count: feedback human_label != prediction.prediction
    corrections_count = db.query(func.count(FeedbackDB.id)).join(
        PredictionDB, FeedbackDB.prediction_id == PredictionDB.id
    ).filter(FeedbackDB.human_label != PredictionDB.prediction).scalar() or 0

    return {
        "total_analyses": total_analyses,
        "predictions_by_class": predictions_by_class,
        "average_confidence": round(float(avg_conf), 4),
        "human_review_count": human_review_count,
        "corrections_count": corrections_count,
    }

def get_model_versions(db: Session) -> List[ModelVersionDB]:
    return db.query(ModelVersionDB).order_by(ModelVersionDB.created_at.desc()).all()
