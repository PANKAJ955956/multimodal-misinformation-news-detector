import hashlib
from typing import Optional

def hash_text(text: str) -> str:
    """Generates SHA256 hash for text input."""
    if not text:
        return ""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

def hash_image_bytes(image_bytes: bytes) -> str:
    """Generates SHA256 hash for image bytes."""
    if not image_bytes:
        return ""
    return hashlib.sha256(image_bytes).hexdigest()

def generate_cache_key(text: Optional[str], image_hash: Optional[str], model_version: str) -> str:
    """Generates deterministic Redis cache key from inputs and model version."""
    t_hash = hash_text(text) if text else "no_text"
    i_hash = image_hash if image_hash else "no_image"
    raw_key = f"prediction:{model_version}:{t_hash}:{i_hash}"
    return hashlib.md5(raw_key.encode("utf-8")).hexdigest()
