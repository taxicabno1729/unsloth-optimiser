def test_base_worker_is_abstract():
    from src.api.workers.base_worker import BaseOptimizationWorker
    import inspect
    
    assert inspect.isabstract(BaseOptimizationWorker)
    assert hasattr(BaseOptimizationWorker, 'optimize')
    assert hasattr(BaseOptimizationWorker, 'validate_config')

def test_quantization_worker_interface():
    from src.api.workers.quantization_worker import QuantizationWorker
    
    worker = QuantizationWorker()
    assert hasattr(worker, 'optimize')
    assert hasattr(worker, 'validate_config')
    assert callable(worker.optimize)
    assert callable(worker.validate_config)

def test_quantization_worker_validation():
    from src.api.workers.quantization_worker import QuantizationWorker
    
    worker = QuantizationWorker()
    # Valid config
    assert worker.validate_config({'bits': 4, 'quant_type': 'nf4'}) == True
    assert worker.validate_config({'bits': 8, 'quant_type': 'q8_0'}) == True
    # Invalid config
    assert worker.validate_config({'bits': 16, 'quant_type': 'nf4'}) == False
    assert worker.validate_config({'bits': 4, 'quant_type': 'invalid'}) == False

def test_lora_worker_interface():
    from src.api.workers.lora_worker import LoRAWorker
    
    worker = LoRAWorker()
    assert hasattr(worker, 'supported_ranks')
    assert worker.supported_ranks == [8, 16, 32, 64]

def test_lora_worker_validation():
    from src.api.workers.lora_worker import LoRAWorker
    
    worker = LoRAWorker()
    # Valid config
    assert worker.validate_config({'r': 8, 'lora_alpha': 32}) == True
    assert worker.validate_config({'r': 16}) == True
    # Invalid config
    assert worker.validate_config({'r': 100}) == False

def test_awq_worker_interface():
    from src.api.workers.awq_worker import AWQWorker
    
    worker = AWQWorker()
    assert callable(worker.optimize)
    assert callable(worker.validate_config)

def test_gptq_worker_interface():
    from src.api.workers.gptq_worker import GPTQWorker
    
    worker = GPTQWorker()
    assert callable(worker.optimize)
    assert callable(worker.validate_config)
