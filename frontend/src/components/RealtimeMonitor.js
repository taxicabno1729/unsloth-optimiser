import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

const RealtimeMonitor = ({ taskId }) => {
  const [updates, setUpdates] = useState([]);
  const [status, setStatus] = useState('Connecting...');
  
  useWebSocket(`ws://localhost:8000/ws/tasks/${taskId}`, (data) => {
    setUpdates(prev => [...prev, data]);
    if (data.status) {
      setStatus(data.status);
    }
  });

  return (
    <div>
      <h3>Real-time Updates</h3>
      <p>Connection Status: {status}</p>
      <ul>
        {updates.map((update, index) => (
          <li key={index}>{JSON.stringify(update)}</li>
        ))}
      </ul>
    </div>
  );
};

export default RealtimeMonitor;
