import React from 'react';
import { useParams } from 'react-router-dom';

const TaskDetail = () => {
  const { id } = useParams();
  
  return (
    <div>
      <h2>Task Details</h2>
      <p>Task ID: {id}</p>
      <p>Task information and real-time monitoring will be displayed here.</p>
      {/* TODO: Add RealtimeMonitor component */}
    </div>
  );
};

export default TaskDetail;
