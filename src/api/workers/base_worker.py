from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseOptimizationWorker(ABC):
    """Base class for all optimization workers"""
    
    @abstractmethod
    def optimize(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize model according to configuration"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate optimization configuration"""
        pass
