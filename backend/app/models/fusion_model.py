import numpy as np
from typing import Dict, Any, List

class FusionModel:
    def compute_alignment(self, text_embedding: List[float], image_embedding: List[float]) -> Dict[str, Any]:
        """Calculates cosine similarity alignment between text and visual representations."""
        if not text_embedding or not image_embedding or sum(text_embedding) == 0 or sum(image_embedding) == 0:
            return {"alignment_score": 0.5, "alignment_level": "MODERATE ALIGNMENT"}
            
        t_vec = np.array(text_embedding)
        i_vec = np.array(image_embedding)
        
        # Match dimensions if necessary using slicing / padding
        min_dim = min(len(t_vec), len(i_vec))
        t_sub = t_vec[:min_dim]
        i_sub = i_vec[:min_dim]
        
        norm_t = np.linalg.norm(t_sub)
        norm_i = np.linalg.norm(i_sub)
        
        if norm_t == 0 or norm_i == 0:
            cos_sim = 0.0
        else:
            cos_sim = float(np.dot(t_sub, i_sub) / (norm_t * norm_i))
            
        # Scale cosine similarity from [-1, 1] to [0, 1]
        scaled_score = round(max(0.0, min(1.0, (cos_sim + 1.0) / 2.0)), 4)
        
        if scaled_score < 0.40:
            level = "LOW ALIGNMENT"
        elif scaled_score < 0.70:
            level = "MODERATE ALIGNMENT"
        else:
            level = "HIGH ALIGNMENT"
            
        return {
            "alignment_score": scaled_score,
            "alignment_level": level
        }

    def fuse(
        self,
        text_embedding: List[float],
        image_embedding: List[float],
        fusion_strategy: str = "late_fusion"
    ) -> Dict[str, Any]:
        """Performs multimodal fusion across text and visual feature vectors."""
        alignment_data = self.compute_alignment(text_embedding, image_embedding)
        
        if fusion_strategy == "early_fusion":
            # Early fusion: Concatenate text & visual vectors
            fused_vector = text_embedding + image_embedding
            strategy_name = "early_fusion_concatenation"
        elif fusion_strategy == "cross_attention":
            # Cross-modal attention representation
            t_array = np.array(text_embedding[:256]) if len(text_embedding) >= 256 else np.zeros(256)
            i_array = np.array(image_embedding[:256]) if len(image_embedding) >= 256 else np.zeros(256)
            attn_weights = np.outer(t_array, i_array)
            fused_vector = np.mean(attn_weights, axis=0).tolist() + text_embedding[:256]
            strategy_name = "cross_modal_attention"
        else:
            # Late fusion: Weighted element-wise combination
            min_dim = min(len(text_embedding), len(image_embedding))
            t_array = np.array(text_embedding[:min_dim])
            i_array = np.array(image_embedding[:min_dim])
            fused_vector = (0.5 * t_array + 0.5 * i_array).tolist()
            strategy_name = "late_fusion_weighted_average"
            
        return {
            "fused_vector": fused_vector,
            "fusion_strategy": strategy_name,
            "alignment_score": alignment_data["alignment_score"],
            "alignment_level": alignment_data["alignment_level"]
        }
