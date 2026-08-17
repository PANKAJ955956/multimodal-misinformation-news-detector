from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any, List
from app.database import crud
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.utils.logging import logger

class FeedbackService:
    def submit_feedback(self, db: Session, feedback_in: FeedbackCreate) -> FeedbackResponse:
        # Check prediction exists
        prediction = crud.get_prediction_by_id(db, feedback_in.prediction_id)
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prediction with ID '{feedback_in.prediction_id}' not found."
            )

        valid_labels = {"REAL", "FAKE", "MISLEADING", "SATIRE", "MANIPULATED", "UNCERTAIN"}
        if feedback_in.human_label not in valid_labels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid label '{feedback_in.human_label}'. Allowed: {valid_labels}"
            )

        db_feedback = crud.create_feedback(db, {
            "prediction_id": feedback_in.prediction_id,
            "human_label": feedback_in.human_label,
            "reviewer_comment": feedback_in.reviewer_comment
        })

        crud.create_audit_log(
            db,
            action="SUBMIT_FEEDBACK",
            prediction_id=feedback_in.prediction_id,
            metadata={"human_label": feedback_in.human_label, "ai_prediction": prediction.prediction}
        )

        logger.info(f"Feedback submitted for prediction {feedback_in.prediction_id}: {feedback_in.human_label}")
        return db_feedback

    def list_feedback(self, db: Session, skip: int = 0, limit: int = 50) -> List[FeedbackResponse]:
        return crud.get_all_feedback(db, skip=skip, limit=limit)

feedback_service = FeedbackService()
