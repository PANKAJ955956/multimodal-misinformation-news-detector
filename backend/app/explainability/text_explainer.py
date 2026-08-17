import re
from typing import List, Dict, Any

SENSATIONAL_KEYWORDS = {
    "miracle": 0.85, "cure": 0.82, "secret": 0.78, "shocking": 0.88,
    "conspiracy": 0.80, "breaking": 0.65, "doctored": 0.90, "fake": 0.85,
    "unbelievable": 0.75, "guaranteed": 0.70, "banned": 0.72, "hidden": 0.76,
    "exposed": 0.84, "deepfake": 0.92, "proof": 0.60
}

class TextExplainer:
    def explain(self, text: str, demo_mode: bool = True) -> List[Dict[str, Any]]:
        """Extracts influential phrases and calculates importance scores."""
        if not text:
            return []

        phrases = []
        words = re.findall(r'\w+', text.lower())
        
        # Keyword-based token importance evaluation
        for word in words:
            if word in SENSATIONAL_KEYWORDS:
                phrases.append({
                    "text": word,
                    "importance": SENSATIONAL_KEYWORDS[word]
                })

        # Fallback if no sensational keywords found
        if not phrases and len(words) > 0:
            # Pick longest / most significant words
            unique_words = sorted(list(set(w for w in words if len(w) > 4)), key=len, reverse=True)[:3]
            for idx, w in enumerate(unique_words):
                phrases.append({
                    "text": w,
                    "importance": round(0.55 - idx * 0.1, 2)
                })

        # Return top 5 phrases sorted by importance
        phrases = sorted(phrases, key=lambda x: x["importance"], reverse=True)[:5]
        return phrases
