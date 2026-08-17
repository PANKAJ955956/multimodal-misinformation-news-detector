from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.database import get_db
from app.database import crud

router = APIRouter()

@router.get("/predictions")
def get_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items = crud.get_predictions_list(db, skip=skip, limit=limit)
    total = crud.count_predictions(db)
    
    formatted_items = []
    for item in items:
        formatted_items.append({
            "id": item.id,
            "input_type": item.input_type,
            "text_content": item.text_content,
            "image_path": item.image_path,
            "url": item.url,
            "prediction": item.prediction,
            "confidence": item.confidence,
            "text_score": item.text_score,
            "image_score": item.image_score,
            "multimodal_score": item.multimodal_score,
            "alignment_score": item.alignment_score,
            "model_version": item.model_version,
            "cached": item.cached,
            "created_at": item.created_at
        })
        
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": formatted_items
    }

@router.get("/predictions/{prediction_id}")
def get_prediction_detail(prediction_id: str, db: Session = Depends(get_db)):
    item = crud.get_prediction_by_id(db, prediction_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction with ID '{prediction_id}' not found."
        )

    feedback_list = crud.get_feedback_for_prediction(db, prediction_id)
    
    return {
        "id": item.id,
        "input_type": item.input_type,
        "text_content": item.text_content,
        "image_path": item.image_path,
        "url": item.url,
        "prediction": item.prediction,
        "confidence": item.confidence,
        "text_score": item.text_score,
        "image_score": item.image_score,
        "multimodal_score": item.multimodal_score,
        "alignment_score": item.alignment_score,
        "model_version": item.model_version,
        "cached": item.cached,
        "created_at": item.created_at,
        "human_feedback": [
            {
                "id": f.id,
                "human_label": f.human_label,
                "reviewer_comment": f.reviewer_comment,
                "created_at": f.created_at
            }
            for f in feedback_list
        ]
    }
