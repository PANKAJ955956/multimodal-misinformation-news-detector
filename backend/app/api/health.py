from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db, engine
from app.services.cache_service import cache_service
from app.config import settings

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "healthy"
    try:
        with engine.connect() as conn:
            pass
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    redis_status = "connected" if cache_service.redis_client is not None else "disconnected (fallback mode)"

    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "database": db_status,
        "redis": redis_status,
        "demo_mode": settings.DEMO_MODE
    }
