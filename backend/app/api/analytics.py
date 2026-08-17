from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.schemas.analytics import AnalyticsResponse

router = APIRouter()

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    summary = crud.get_analytics_summary(db)
    return summary
