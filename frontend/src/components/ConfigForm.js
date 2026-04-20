import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { useToast } from '../context/ToastContext';

const optimizationMethods = [
  { 
    value: 'quantization', 
    label: 'Quantization',
    description: '4-bit or 8-bit quantization for memory reduction',
    icon: '🔧',
    color: '#6366f1'
  },
  { 
    value: 'lora', 
    label: 'LoRA Fine-tuning',
    description: 'Parameter-efficient model adaptation with low-rank matrices',
    icon: '🎯',
    color: '#8b5cf6'
  },
  { 
    value: 'awq', 
    label: 'AWQ',
    description: 'Activation-aware Weight Quantization',
    icon: '⚡',
    color: '#10b981'
  },
  { 
    value: 'gptq', 
    label: 'GPTQ',
    description: 'Post-training quantization for inference optimization',
    icon: '🚀',
    color: '#f59e0b'
  },
];

const ConfigForm = ({ onSubmit, onClose }) => {
  const { addToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    optimization_method: 'quantization',
    model_name: '',
    parameters: {},
  });
  const [advancedParams, setAdvancedParams] = useState({
    bits: '4',
    batch_size: '1',
    max_memory: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAdvancedChange = (e) => {
    const { name, value } = e.target;
    setAdvancedParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const params = {};
      if (advancedParams.bits) params.bits = parseInt(advancedParams.bits);
      if (advancedParams.batch_size) params.batch_size = parseInt(advancedParams.batch_size);
      if (advancedParams.max_memory) params.max_memory = advancedParams.max_memory;
      
      const payload = {
        ...formData,
        parameters: params
      };
      
      const response = await apiClient.post('/tasks/', payload);
      addToast('Task created successfully!', 'success');
      onSubmit(response.data);
      
      // Reset form
      setFormData({
        name: '',
        optimization_method: 'quantization',
        model_name: '',
        parameters: {},
      });
      setAdvancedParams({
        bits: '4',
        batch_size: '1',
        max_memory: '',
      });
      
      if (onClose) onClose();
    } catch (error) {
      console.error('Failed to create task:', error);
      addToast(
        error.response?.data?.detail || 'Failed to create task. Please try again.',
        'error'
      );
    } finally {
      setLoading(false);
    }
  };

  const selectedMethod = optimizationMethods.find(m => m.value === formData.optimization_method);

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="form-card">
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>
          Create Optimization Task
        </h2>
        
        {/* Method Selection */}
        <div className="form-group">
          <label>Optimization Method</label>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
            gap: '1rem',
            marginTop: '0.5rem'
          }}>
            {optimizationMethods.map(method => (
              <div
                key={method.value}
                onClick={() => setFormData(prev => ({ ...prev, optimization_method: method.value }))}
                style={{
                  padding: '1rem',
                  borderRadius: '12px',
                  border: `2px solid ${formData.optimization_method === method.value ? method.color : 'var(--border-color)'}`,
                  background: formData.optimization_method === method.value ? `${method.color}10` : 'var(--bg-color)',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
              >
                <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{method.icon}</div>
                <div style={{ fontWeight: 600, marginBottom: '0.25rem' }}>{method.label}</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  {method.description}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="name">Task Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g., Llama-2-7b Quantization"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="model_name">Model Name *</label>
            <input
              type="text"
              id="model_name"
              name="model_name"
              value={formData.model_name}
              onChange={handleChange}
              placeholder="e.g., meta-llama/Llama-2-7b-hf"
              required
            />
          </div>
        </div>

        {/* Advanced Parameters */}
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>
            Advanced Parameters (Optional)
          </h3>
          
          <div className="form-row">
            {selectedMethod?.value === 'quantization' && (
              <div className="form-group">
                <label htmlFor="bits">Bits</label>
                <select
                  id="bits"
                  name="bits"
                  value={advancedParams.bits}
                  onChange={handleAdvancedChange}
                >
                  <option value="4">4-bit (highest compression)</option>
                  <option value="8">8-bit (better quality)</option>
                </select>
              </div>
            )}
            
            <div className="form-group">
              <label htmlFor="batch_size">Batch Size</label>
              <input
                type="number"
                id="batch_size"
                name="batch_size"
                value={advancedParams.batch_size}
                onChange={handleAdvancedChange}
                min="1"
                max="32"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="max_memory">Max Memory (GB)</label>
              <input
                type="number"
                id="max_memory"
                name="max_memory"
                value={advancedParams.max_memory}
                onChange={handleAdvancedChange}
                placeholder="e.g., 16"
                min="1"
              />
            </div>
          </div>
        </div>

        <div style={{ 
          display: 'flex', 
          gap: '1rem', 
          justifyContent: 'flex-end',
          marginTop: '2rem',
          paddingTop: '1.5rem',
          borderTop: '1px solid var(--border-color)'
        }}>
          {onClose && (
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
          )}
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading && <span className="btn-spinner" />}
            {loading ? 'Creating Task...' : 'Create Task'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ConfigForm;
