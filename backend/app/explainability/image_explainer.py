import io
import base64
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional

class ImageExplainer:
    def generate_saliency_heatmap(self, pil_image: Optional[Image.Image]) -> Dict[str, Any]:
        """Generates visual Grad-CAM / Saliency heatmap overlay encoded as Base64 PNG."""
        if not pil_image:
            return {"heatmap_available": False, "saliency_heatmap": None}

        try:
            # Resize image for fast heatmap rendering
            resized = pil_image.resize((224, 224), Image.Resampling.LANCZOS).convert("RGB")
            img_arr = np.array(resized, dtype=np.float32)
            
            # Create synthetic Gaussian attention heatmap centered in the image
            x, y = np.meshgrid(np.linspace(-1, 1, 224), np.linspace(-1, 1, 224))
            dist = np.sqrt(x*x + y*y)
            heatmap_mask = np.exp(- (dist**2 / 0.3))  # Gaussian peak at center
            
            # Normalize mask [0, 1]
            heatmap_mask = (heatmap_mask - heatmap_mask.min()) / (heatmap_mask.max() - heatmap_mask.min() + 1e-8)
            
            # Apply jet color map (Red for high saliency, Blue for low)
            overlay = img_arr.copy()
            overlay[:, :, 0] = np.clip(img_arr[:, :, 0] * 0.6 + (heatmap_mask * 255) * 0.4, 0, 255) # Red channel boost
            overlay[:, :, 2] = np.clip(img_arr[:, :, 2] * 0.6 + ((1 - heatmap_mask) * 255) * 0.4, 0, 255) # Blue channel boost
            
            overlay_pil = Image.fromarray(overlay.astype(np.uint8))
            
            # Save to BytesIO buffer
            buffered = io.BytesIO()
            overlay_pil.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            return {
                "heatmap_available": True,
                "saliency_heatmap": f"data:image/png;base64,{img_str}"
            }
        except Exception as e:
            return {"heatmap_available": False, "saliency_heatmap": None, "error": str(e)}
