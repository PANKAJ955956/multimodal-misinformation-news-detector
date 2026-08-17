import numpy as np
import hashlib
from typing import Dict, Any, List, Optional
from app.config import settings

CLASSES = ["REAL", "FAKE", "MISLEADING", "SATIRE", "MANIPULATED"]

class MultimodalClassifier:
    def __init__(self, high_conf_threshold: float = settings.HIGH_CONFIDENCE_THRESHOLD, review_threshold: float = settings.REVIEW_THRESHOLD):
        self.classes = CLASSES
        self.high_conf_threshold = high_conf_threshold
        self.review_threshold = review_threshold

    def classify(
        self,
        fused_vector: List[float],
        text_content: Optional[str] = None,
        has_image: bool = False,
        demo_mode: bool = True
    ) -> Dict[str, Any]:
        """Performs 5-class classification and generates probabilistic AI assessment."""
        if not fused_vector or sum(fused_vector) == 0:
            # Fallback uniform probabilities
            probs = {cls: 0.20 for cls in self.classes}
            top_class = "UNCERTAIN"
            confidence = 0.20
        elif demo_mode:
            # Deterministic demo mode probabilities based on input text & image state
            combined_key = f"{text_content or ''}_{has_image}"
            seed_int = int(hashlib.sha256(combined_key.encode("utf-8")).hexdigest()[:8], 16)
            rng = np.random.RandomState(seed_int)
            
            # Simple keyword heuristic check for demo data realism
            lower_text = (text_content or "").lower()
            if "breaking" in lower_text or "secret cure" in lower_text or "miracle" in lower_text or "conspiracy" in lower_text:
                logits = [0.05, 0.10, 0.75, 0.05, 0.05]
            elif "satire" in lower_text or "onion" in lower_text or "joke" in lower_text:
                logits = [0.05, 0.05, 0.05, 0.80, 0.05]
            elif "doctored" in lower_text or "deepfake" in lower_text or "photoshop" in lower_text:
                logits = [0.05, 0.05, 0.10, 0.05, 0.75]
            elif "official" in lower_text or "report" in lower_text or "study" in lower_text or "nasa" in lower_text:
                logits = [0.82, 0.05, 0.05, 0.05, 0.03]
            else:
                raw_logits = rng.uniform(0.1, 1.0, size=5)
                # Boost one class to make confidence realistic
                max_idx = rng.randint(0, 5)
                raw_logits[max_idx] += 2.0
                exp_logits = np.exp(raw_logits - np.max(raw_logits))
                logits = (exp_logits / np.sum(exp_logits)).tolist()

            probs = {cls: round(float(logits[i]), 4) for i, cls in enumerate(self.classes)}
            top_class = max(probs, key=probs.get)
            confidence = probs[top_class]
        else:
            # Real softmax classification head over fused vector
            vec_array = np.array(fused_vector[:5]) if len(fused_vector) >= 5 else np.array([0.2]*5)
            exp_vec = np.exp(vec_array - np.max(vec_array))
            probs_list = (exp_vec / np.sum(exp_vec)).tolist()
            probs = {cls: round(float(probs_list[i]), 4) for i, cls in enumerate(self.classes)}
            top_class = max(probs, key=probs.get)
            confidence = probs[top_class]

        # Determine individual scores
        text_score = round(confidence * (0.9 if text_content else 0.5), 4)
        image_score = round(confidence * (0.85 if has_image else 0.4), 4)
        multimodal_score = round(confidence, 4)

        # Risk level determination
        if confidence < self.review_threshold:
            risk_level = "UNCERTAIN"
        elif top_class in ["FAKE", "MISLEADING", "MANIPULATED"]:
            risk_level = "HIGH" if confidence >= self.high_conf_threshold else "MODERATE"
        elif top_class == "SATIRE":
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        human_review_required = (confidence < self.review_threshold) or (top_class in ["MISLEADING", "MANIPULATED", "FAKE"])

        return {
            "prediction": top_class,
            "confidence": confidence,
            "probabilities": probs,
            "risk_level": risk_level,
            "text_score": text_score,
            "image_score": image_score,
            "multimodal_score": multimodal_score,
            "human_review_required": human_review_required
        }
