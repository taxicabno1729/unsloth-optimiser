import React from 'react';
import ConfigForm from '../components/ConfigForm';
import { useNavigate } from 'react-router-dom';
import { useToast } from '../context/ToastContext';

const CreateTask = () => {
  const navigate = useNavigate();
  const { addToast } = useToast();

  const handleSubmit = (taskData) => {
    console.log('Task created:', taskData);
    addToast(`Task "${taskData.name}" created successfully!`, 'success');
    
    // Navigate to the task detail page
    setTimeout(() => {
      navigate(`/tasks/${taskData.task_id}`);
    }, 500);
  };

  return (
    <div>
      <div className="page-header">
        <h1>Create New Optimization Task</h1>
        <p>Configure your model optimization settings below.</p>
      </div>
      
      <ConfigForm onSubmit={handleSubmit} />
    </div>
  );
};

export default CreateTask;
