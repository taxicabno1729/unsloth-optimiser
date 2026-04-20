import React, { useState } from 'react';
import apiClient from '../api/client';

const optimizationMethods = [
  { value: 'quantization', label: 'Quantization (4-bit/8-bit)' },
  { value: 'lora', label: 'LoRA Fine-tuning' },
  { value: 'awq', label: 'AWQ (Activation-aware)' },
  { value: 'gptq', label: 'GPTQ Optimization' },
];

const ConfigForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    optimization_method: 'quantization',
    model_name: '',
    parameters: {},
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/tasks/', formData);
      onSubmit(response.data);
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Task Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      
      <div>
        <label htmlFor="optimization_method">Optimization Method:</label>
        <select
          id="optimization_method"
          name="optimization_method"
          value={formData.optimization_method}
          onChange={handleChange}
        >
          {optimizationMethods.map(method => (
            <option key={method.value} value={method.value}>
              {method.label}
            </option>
          ))}
        </select>
      </div>
      
      <div>
        <label htmlFor="model_name">Model Name:</label>
        <input
          type="text"
          id="model_name"
          name="model_name"
          value={formData.model_name}
          onChange={handleChange}
          required
        />
      </div>
      
      <button type="submit">Create Optimization Task</button>
    </form>
  );
};

export default ConfigForm;
