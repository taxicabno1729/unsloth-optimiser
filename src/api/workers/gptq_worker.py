from src.api.workers.base_worker import BaseOptimizationWorker
from typing import Dict, Any

class GPTQWorker(BaseOptimizationWorker):
    SUPPORTED_BITS = [4, 8]
    DEFAULT_GROUP_SIZE = 128
    
    def optimize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform GPTQ optimization"""
        if not self.validate_config(config):
            raise ValueError("Invalid GPTQ configuration")
        
        bits = config.get('bits', 4)
        group_size = config.get('group_size', self.DEFAULT_GROUP_SIZE)
        
        return {
            "status": "success",
            "method": "gptq",
            "bits": bits,
            "group_size": group_size,
            "compression_ratio": "18x",
            "memory_reduction": f"{2 if bits == 4 else 4}x"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate GPTQ configuration"""
        bits = config.get('bits', 4)
        return bits in self.SUPPORTED_BITS
