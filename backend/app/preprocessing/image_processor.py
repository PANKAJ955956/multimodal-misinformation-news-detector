from PIL import Image
import io
import numpy as np
from typing import Dict, Any, Tuple

class ImageProcessor:
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size

    def process_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        image = Image.open(io.BytesIO(image_bytes))
        orig_width, orig_height = image.size
        
        # Convert to RGB mode
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # Resize to target size
        resized_image = image.resize(self.target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(resized_image, dtype=np.float32) / 255.0
        
        return {
            "pil_image": resized_image,
            "original_width": orig_width,
            "original_height": orig_height,
            "target_width": self.target_size[0],
            "target_height": self.target_size[1],
            "image_array": img_array
        }
