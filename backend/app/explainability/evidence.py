from typing import List, Dict, Any, Optional
from app.explainability.text_explainer import TextExplainer
from app.explainability.image_explainer import ImageExplainer
from PIL import Image

class EvidenceBuilder:
    def __init__(self):
        self.text_explainer = TextExplainer()
        self.image_explainer = ImageExplainer()

    def build_evidence(
        self,
        text: Optional[str],
        pil_image: Optional[Image.Image],
        prediction: str,
        confidence: float,
        alignment_score: float,
        alignment_level: str,
        demo_mode: bool = True
    ) -> Dict[str, Any]:
        important_phrases = self.text_explainer.explain(text, demo_mode=demo_mode) if text else []
        image_evidence = self.image_explainer.generate_saliency_heatmap(pil_image) if pil_image else {"heatmap_available": False, "saliency_heatmap": None}

        # Build natural language evidence summary
        summary_parts = []
        summary_parts.append(f"AI Assessment indicates class '{prediction}' with {int(confidence * 100)}% model confidence.")
        
        if important_phrases:
            top_words = ", ".join([f"'{p['text']}'" for p in important_phrases[:3]])
            summary_parts.append(f"Key influential text phrases identified: {top_words}.")

        if pil_image:
            summary_parts.append(f"Multimodal semantic text-image alignment is evaluated at {int(alignment_score * 100)}% ({alignment_level}).")

        if confidence < 0.60:
            summary_parts.append("Due to moderate/low model confidence, human fact-checker review is recommended.")

        evidence_summary = " ".join(summary_parts)

        return {
            "important_phrases": important_phrases,
            "heatmap_available": image_evidence.get("heatmap_available", False),
            "saliency_heatmap": image_evidence.get("saliency_heatmap"),
            "evidence_summary": evidence_summary
        }
