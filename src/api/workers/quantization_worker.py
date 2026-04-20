from src.api.workers.base_worker import BaseOptimizationWorker
from typing import Dict, Any

class QuantizationWorker(BaseOptimizationWorker):
    SUPPORTED_BITS = [4, 8]
    SUPPORTED_TYPES = ['nf4', 'q8_0']
    
    def optimize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform 4-bit or 8-bit quantization"""
        if not self.validate_config(config):
            raise ValueError("Invalid quantization configuration")
        
        bits = config.get('bits', 4)
        quant_type = config.get('quant_type', 'nf4')
        
        # Simulate optimization
        return {
            "status": "success",
            "method": "quantization",
            "bits": bits,
            "quant_type": quant_type,
            "memory_reduction": f"{2 if bits == 4 else 4}x",
            "estimated_size_reduction": f"{50 if bits == 4 else 75}%"
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate quantization configuration"""
        bits = config.get('bits', 4)
        quant_type = config.get('quant_type', 'nf4')
        
        return (
            bits in self.SUPPORTED_BITS and
            quant_type in self.SUPPORTED_TYPES
        )
