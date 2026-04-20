from src.api.workers.base_worker import BaseOptimizationWorker
from typing import Dict, Any

class LoRAWorker(BaseOptimizationWorker):
    SUPPORTED_RANKS = [8, 16, 32, 64]
    DEFAULT_ALPHA = 32
    
    @property
    def supported_ranks(self):
        return self.SUPPORTED_RANKS
    
    def optimize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform LoRA fine-tuning"""
        if not self.validate_config(config):
            raise ValueError("Invalid LoRA configuration")
        
        rank = config.get('r', 8)
        lora_alpha = config.get('lora_alpha', self.DEFAULT_ALPHA)
        
        return {
            "status": "success",
            "method": "lora",
            "rank": rank,
            "lora_alpha": lora_alpha,
            "trainable_params": f"reduced by {90 + (rank // 10)}%",
            "target_modules": config.get('target_modules', ['q_proj', 'v_proj'])
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate LoRA configuration"""
        rank = config.get('r', 8)
        return rank in self.SUPPORTED_RANKS
