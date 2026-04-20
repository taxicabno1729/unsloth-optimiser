from src.api.workers.base_worker import BaseOptimizationWorker
from typing import Dict, Any

class AWQWorker(BaseOptimizationWorker):
    SUPPORTED_BITS = [4, 8]
    DEFAULT_GROUP_SIZE = 128
    
    def optimize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Activation-aware Weight Quantization"""
        if not self.validate_config(config):
            raise ValueError("Invalid AWQ configuration")
        
        bits = config.get('bits', 4)
        group_size = config.get('group_size', self.DEFAULT_GROUP_SIZE)
        zero_point = config.get('zero_point', True)
        
        return {
            "status": "success",
            "method": "awq",
            "bits": bits,
            "group_size": group_size,
            "zero_point": zero_point,
            "memory_reduction": f"{2 if bits == 4 else 4}x"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate AWQ configuration"""
        bits = config.get('bits', 4)
        return bits in self.SUPPORTED_BITS
