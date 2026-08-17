import re
from typing import Dict, Any

class TextProcessor:
    def __init__(self, max_length: int = 512):
        self.max_length = max_length

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        # Remove unusual whitespace characters
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def process(self, text: str) -> Dict[str, Any]:
        cleaned = self.clean_text(text)
        words = cleaned.split()
        truncated_words = words[:self.max_length]
        final_text = " ".join(truncated_words)
        
        return {
            "cleaned_text": final_text,
            "word_count": len(words),
            "char_count": len(cleaned),
            "is_truncated": len(words) > self.max_length
        }
