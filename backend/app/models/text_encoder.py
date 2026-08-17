import numpy as np
import hashlib
from typing import Dict, Any, List
from app.config import settings
from app.utils.logging import logger

class TextEncoder:
    def __init__(self, model_name: str = settings.TEXT_MODEL, device: str = settings.MODEL_DEVICE):
        self.model_name = model_name
        self.device = device
        self.tokenizer = None
        self.model = None
        self._is_real_loaded = False
        
        if not settings.DEMO_MODE:
            self._try_load_real_model()

    def _try_load_real_model(self):
        try:
            import torch
            from transformers import AutoTokenizer, AutoModel
            logger.info(f"Loading HuggingFace Text Model: {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
            self.model.eval()
            self._is_real_loaded = True
            logger.info(f"Successfully loaded text model {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not load HuggingFace text model '{self.model_name}' ({e}). Falling back to Demo Mode.")
            self._is_real_loaded = False

    def encode_text(self, text: str) -> Dict[str, Any]:
        """Encodes text into a 768-dimensional embedding vector."""
        if not text:
            return {
                "embedding": [0.0] * 768,
                "model_name": self.model_name,
                "model_version": settings.MODEL_VERSION,
                "demo_mode": not self._is_real_loaded
            }

        if self._is_real_loaded:
            try:
                import torch
                inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True).to(self.device)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    # Mean pooling
                    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
                return {
                    "embedding": embedding,
                    "model_name": self.model_name,
                    "model_version": settings.MODEL_VERSION,
                    "demo_mode": False
                }
            except Exception as e:
                logger.error(f"Error during real text model encoding: {e}. Reverting to demo vector.")

        # Deterministic Demo Mode Embedding Generation via SHA256 seed
        seed_int = int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed_int)
        demo_vector = rng.normal(loc=0.0, scale=1.0, size=768)
        norm_vector = (demo_vector / np.linalg.norm(demo_vector)).tolist()

        return {
            "embedding": norm_vector,
            "model_name": f"{self.model_name}-demo",
            "model_version": settings.MODEL_VERSION,
            "demo_mode": True
        }
