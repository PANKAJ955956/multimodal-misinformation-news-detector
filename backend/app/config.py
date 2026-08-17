import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multimodal Fake News & Misinformation Detector"
    PROJECT_VERSION: str = "0.1.0"
    
    # Environment & Server
    ENV: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    
    # Databases & Caching
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/fakenews"
    SQLITE_FALLBACK_URL: str = "sqlite:///./fakenews.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI & Machine Learning
    DEMO_MODE: bool = True
    MODEL_DEVICE: str = "cpu"
    TEXT_MODEL: str = "roberta-base"
    VISION_MODEL: str = "openai/clip-vit-base-patch32"
    MODEL_VERSION: str = "0.1.0"
    
    # Thresholds
    HIGH_CONFIDENCE_THRESHOLD: float = 0.80
    REVIEW_THRESHOLD: float = 0.60
    MAX_UPLOAD_MB: int = 8
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
