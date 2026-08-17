import numpy as np
import hashlib
from typing import Dict, Any
from PIL import Image
from app.config import settings
from app.utils.logging import logger

class VisionEncoder:
    def __init__(self, model_name: str = settings.VISION_MODEL, device: str = settings.MODEL_DEVICE):
        self.model_name = model_name
        self.device = device
        self.processor = None
        self.model = None
        self._is_real_loaded = False

        if not settings.DEMO_MODE:
            self._try_load_real_model()

    def _try_load_real_model(self):
        try:
            import torch
            from transformers import AutoProcessor, AutoModel
            logger.info(f"Loading HuggingFace Vision Model: {self.model_name}...")
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
            self.model.eval()
            self._is_real_loaded = True
            logger.info(f"Successfully loaded vision model {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not load HuggingFace vision model '{self.model_name}' ({e}). Falling back to Demo Mode.")
            self._is_real_loaded = False

    def encode_image(self, pil_image: Image.Image) -> Dict[str, Any]:
        """Encodes PIL image into a 512-dimensional embedding vector."""
        width, height = pil_image.size if pil_image else (0, 0)

        if not pil_image:
            return {
                "embedding": [0.0] * 512,
                "model_name": self.model_name,
                "model_version": settings.MODEL_VERSION,
                "image_width": 0,
                "image_height": 0,
                "demo_mode": not self._is_real_loaded
            }

        if self._is_real_loaded:
            try:
                import torch
                inputs = self.processor(images=pil_image, return_tensors="pt").to(self.device)
                with torch.no_grad():
                    if "clip" in self.model_name.lower():
                        image_features = self.model.get_image_features(**inputs)
                    else:
                        outputs = self.model(**inputs)
                        image_features = outputs.last_hidden_state.mean(dim=1)
                    embedding = image_features.squeeze().cpu().numpy().tolist()
                return {
                    "embedding": embedding,
                    "model_name": self.model_name,
                    "model_version": settings.MODEL_VERSION,
                    "image_width": width,
                    "image_height": height,
                    "demo_mode": False
                }
            except Exception as e:
                logger.error(f"Error during real vision model encoding: {e}. Reverting to demo vector.")

        # Deterministic Demo Mode Embedding via pixel byte hash
        img_bytes = pil_image.tobytes() if pil_image else b""
        seed_int = int(hashlib.sha256(img_bytes).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed_int)
        demo_vector = rng.normal(loc=0.0, scale=1.0, size=512)
        norm_vector = (demo_vector / np.linalg.norm(demo_vector)).tolist()

        return {
            "embedding": norm_vector,
            "model_name": f"{self.model_name}-demo",
            "model_version": settings.MODEL_VERSION,
            "image_width": width,
            "image_height": height,
            "demo_mode": True
        }
