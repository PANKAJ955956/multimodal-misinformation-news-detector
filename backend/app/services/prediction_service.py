import os
import uuid
import io
from typing import Optional, Dict, Any
from PIL import Image
from sqlalchemy.orm import Session

from app.config import settings
from app.preprocessing.text_processor import TextProcessor
from app.preprocessing.image_processor import ImageProcessor
from app.models.text_encoder import TextEncoder
from app.models.vision_encoder import VisionEncoder
from app.models.fusion_model import FusionModel
from app.models.classifier import MultimodalClassifier
from app.explainability.evidence import EvidenceBuilder
from app.services.cache_service import cache_service
from app.database import crud
from app.utils.hashing import hash_text, hash_image_bytes, generate_cache_key
from app.utils.logging import logger

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class PredictionService:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.image_processor = ImageProcessor()
        self.text_encoder = TextEncoder()
        self.vision_encoder = VisionEncoder()
        self.fusion_model = FusionModel()
        self.classifier = MultimodalClassifier()
        self.evidence_builder = EvidenceBuilder()

    def predict(
        self,
        db: Session,
        input_type: str,
        text_content: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        url: Optional[str] = None,
        image_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs the complete multimodal AI inference & explainability pipeline."""
        # 1. Image processing & saving
        pil_image = None
        saved_image_path = None
        image_hash = None
        image_meta = {"score": 0.0, "width": 0, "height": 0, "model_name": settings.VISION_MODEL}

        if image_bytes:
            image_hash = hash_image_bytes(image_bytes)
            img_proc_res = self.image_processor.process_bytes(image_bytes)
            pil_image = img_proc_res["pil_image"]
            image_meta["width"] = img_proc_res["original_width"]
            image_meta["height"] = img_proc_res["original_height"]
            
            # Save uploaded image to disk safely
            safe_filename = f"{uuid.uuid4().hex}_{image_filename or 'image.png'}"
            saved_image_path = os.path.join(UPLOAD_DIR, safe_filename)
            try:
                pil_image.save(saved_image_path)
            except Exception as e:
                logger.warning(f"Could not save image to upload directory: {e}")

        # 2. Check Redis cache hit
        cache_key = generate_cache_key(text_content, image_hash, settings.MODEL_VERSION)
        cached_result = cache_service.get_prediction(cache_key)
        if cached_result:
            return cached_result

        # 3. Text Preprocessing & Encoding
        text_meta = {"score": 0.0, "tokens_processed": 0, "model_name": settings.TEXT_MODEL}
        text_encoded = self.text_encoder.encode_text(text_content or "")
        if text_content:
            proc_text = self.text_processor.process(text_content)
            text_meta["tokens_processed"] = proc_text["word_count"]

        # 4. Vision Encoding
        vision_encoded = self.vision_encoder.encode_image(pil_image)

        # 5. Multimodal Fusion
        fusion_res = self.fusion_model.fuse(
            text_embedding=text_encoded["embedding"],
            image_embedding=vision_encoded["embedding"],
            fusion_strategy="late_fusion"
        )

        # 6. Classification
        is_demo = text_encoded["demo_mode"] or vision_encoded["demo_mode"] or settings.DEMO_MODE
        class_res = self.classifier.classify(
            fused_vector=fusion_res["fused_vector"],
            text_content=text_content,
            has_image=(pil_image is not None),
            demo_mode=is_demo
        )

        text_meta["score"] = class_res["text_score"]
        image_meta["score"] = class_res["image_score"]

        # 7. Explainability Evidence Generation
        evidence = self.evidence_builder.build_evidence(
            text=text_content,
            pil_image=pil_image,
            prediction=class_res["prediction"],
            confidence=class_res["confidence"],
            alignment_score=fusion_res["alignment_score"],
            alignment_level=fusion_res["alignment_level"],
            demo_mode=is_demo
        )

        prediction_id = str(uuid.uuid4())
        warning_msg = "DEMO MODE: Development fallback model predictions. Not a validated fact-checking result." if is_demo else ""

        response_payload = {
            "id": prediction_id,
            "input_type": input_type,
            "prediction": class_res["prediction"],
            "confidence": class_res["confidence"],
            "risk_level": class_res["risk_level"],
            "probabilities": class_res["probabilities"],
            "text_analysis": text_meta if text_content else None,
            "image_analysis": image_meta if pil_image else None,
            "multimodal_analysis": {
                "fusion_score": class_res["multimodal_score"],
                "alignment_score": fusion_res["alignment_score"],
                "alignment_level": fusion_res["alignment_level"],
                "fusion_strategy": fusion_res["fusion_strategy"]
            },
            "explainability": evidence,
            "human_review_required": class_res["human_review_required"],
            "model_version": settings.MODEL_VERSION,
            "cached": False,
            "warning": warning_msg,
            "demo_mode": is_demo
        }

        # 8. Persist Prediction to Database
        try:
            crud.create_prediction(db, {
                "id": prediction_id,
                "input_type": input_type,
                "text_content": text_content,
                "image_path": saved_image_path,
                "url": url,
                "prediction": class_res["prediction"],
                "confidence": class_res["confidence"],
                "text_score": class_res["text_score"],
                "image_score": class_res["image_score"],
                "multimodal_score": class_res["multimodal_score"],
                "alignment_score": fusion_res["alignment_score"],
                "model_version": settings.MODEL_VERSION,
                "cached": False
            })
            crud.create_audit_log(db, action="ANALYZE_CONTENT", prediction_id=prediction_id, metadata={"input_type": input_type, "prediction": class_res["prediction"]})
        except Exception as e:
            logger.error(f"Error persisting prediction to database: {e}")

        # 9. Store in Redis Cache
        cache_service.set_prediction(cache_key, response_payload)

        return response_payload

prediction_service = PredictionService()
