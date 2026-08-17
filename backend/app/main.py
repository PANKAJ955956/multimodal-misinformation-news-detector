import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.database import init_db
from app.api import health, predict, feedback, analytics, models, history
from app.utils.logging import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Joint Text-Image AI Analysis & Explainable Evidence for Fake News Detection",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Uploads Static Directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Register Routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(predict.router, prefix="/api", tags=["Prediction & Analysis"])
app.include_router(feedback.router, prefix="/api", tags=["Human Review & Feedback"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics & Metrics"])
app.include_router(models.router, prefix="/api", tags=["Models & Info"])
app.include_router(history.router, prefix="/api", tags=["Prediction History"])

@app.on_event("startup")
def on_startup():
    logger.info("Initializing Multimodal Fake News Detector FastAPI Backend...")
    init_db()
    logger.info("FastAPI Backend startup complete. Swagger docs available at /docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
