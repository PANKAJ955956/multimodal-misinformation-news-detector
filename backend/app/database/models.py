from sqlalchemy import Column, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class PredictionDB(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    input_type = Column(String(20), nullable=False)
    text_content = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=True)
    url = Column(String(1000), nullable=True)
    prediction = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    text_score = Column(Float, default=0.0)
    image_score = Column(Float, default=0.0)
    multimodal_score = Column(Float, default=0.0)
    alignment_score = Column(Float, default=0.0)
    model_version = Column(String(50), nullable=False)
    cached = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    feedback_entries = relationship("FeedbackDB", back_populates="prediction_rel", cascade="all, delete-orphan")

class FeedbackDB(Base):
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    prediction_id = Column(String(36), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    human_label = Column(String(20), nullable=False)
    reviewer_comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    prediction_rel = relationship("PredictionDB", back_populates="feedback_entries")

class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    action = Column(String(100), nullable=False)
    prediction_id = Column(String(36), nullable=True)
    metadata_json = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ModelVersionDB(Base):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    model_name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
