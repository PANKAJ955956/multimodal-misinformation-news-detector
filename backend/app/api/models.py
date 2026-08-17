from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.database import crud
from app.schemas.analytics import ModelVersionResponse
from app.services.model_service import model_service

router = APIRouter()

@router.get("/models", response_model=List[ModelVersionResponse])
def list_models(db: Session = Depends(get_db)):
    return crud.get_model_versions(db)

@router.get("/model-info")
def get_model_info(db: Session = Depends(get_db)):
    return model_service.get_model_info(db)
