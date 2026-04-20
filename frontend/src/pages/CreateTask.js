import React from 'react';
import ConfigForm from '../components/ConfigForm';

const CreateTask = () => {
  const handleSubmit = (taskData) => {
    console.log('Task created:', taskData);
    // Could navigate to task detail here
    alert(`Task created: ${taskData.name} (${taskData.task_id})`);
  };

  return (
    <div>
      <h2>Create New Optimization Task</h2>
      <ConfigForm onSubmit={handleSubmit} />
    </div>
  );
};

export default CreateTask;
