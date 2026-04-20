import React, { useState } from 'react';
import ConfigForm from './ConfigForm';
import TaskList from './TaskList';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);

  const handleTaskCreated = (newTask) => {
    setTasks(prev => [...prev, newTask]);
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <ConfigForm onSubmit={handleTaskCreated} />
      <TaskList tasks={tasks} />
    </div>
  );
};

export default Dashboard;
