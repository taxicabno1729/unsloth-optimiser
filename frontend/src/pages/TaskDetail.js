import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';
import { useToast } from '../context/ToastContext';

const TaskDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updates, setUpdates] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    fetchTask();
    const interval = setInterval(fetchTask, 3000);
    return () => clearInterval(interval);
  }, [id]);

  const fetchTask = async () => {
    try {
      const response = await apiClient.get(`/tasks/${id}`);
      setTask(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch task:', error);
      setLoading(false);
      addToast('Failed to load task details', 'error');
    }
  };

  // WebSocket for real-time updates
  const handleWebSocketMessage = (data) => {
    setUpdates(prev => [data, ...prev].slice(0, 50)); // Keep last 50 updates
    setWsConnected(true);
    
    // Update task status if included in message
    if (data.status && data.status !== 'connected' && data.status !== 'update') {
      setTask(prev => prev ? { ...prev, status: data.status } : null);
    }
  };

  useWebSocket(`ws://localhost:8000/ws/tasks/${id}`, handleWebSocketMessage);

  const getStatusClass = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return 'status-pending';
      case 'running':
        return 'status-running';
      case 'completed':
        return 'status-completed';
      case 'failed':
        return 'status-failed';
      default:
        return 'status-pending';
    }
  };

  const getMethodIcon = (method) => {
    switch (method?.toLowerCase()) {
      case 'quantization':
        return '🔧';
      case 'lora':
        return '🎯';
      case 'awq':
        return '⚡';
      case 'gptq':
        return '🚀';
      default:
        return '📦';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="task-detail">
        <div className="card" style={{ padding: '4rem', textAlign: 'center' }}>
          <div className="loading-skeleton" style={{ height: '40px', width: '60%', margin: '0 auto 1rem' }} />
          <div className="loading-skeleton" style={{ height: '20px', width: '40%', margin: '0 auto' }} />
        </div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="task-detail">
        <div className="card empty-state">
          <div className="empty-state-icon">❌</div>
          <h3>Task not found</h3>
          <p style={{ color: 'var(--text-secondary)' }}>
            The task you're looking for doesn't exist.
          </p>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/')}
            style={{ marginTop: '1rem' }}
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="task-detail">
      {/* Back Button */}
      <button 
        onClick={() => navigate('/')}
        className="btn btn-secondary"
        style={{ marginBottom: '1.5rem' }}
      >
        ← Back to Dashboard
      </button>

      {/* Task Header */}
      <div className="task-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span style={{ fontSize: '2rem' }}>{getMethodIcon(task.optimization_method)}</span>
            <div>
              <h2>{task.name}</h2>
              <div style={{ color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                ID: <code style={{ background: 'var(--bg-color)', padding: '0.25rem 0.5rem', borderRadius: '4px' }}>{task.task_id}</code>
              </div>
            </div>
          </div>
          <span className={`status-badge ${getStatusClass(task.status)}`} style={{ fontSize: '1rem' }}>
            {task.status?.toUpperCase() || 'PENDING'}
          </span>
        </div>

        <div className="task-details-grid">
          <div className="detail-item">
            <span className="detail-label">Optimization Method</span>
            <span className="detail-value">{task.optimization_method}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Model</span>
            <span className="detail-value">{task.model_name}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Created</span>
            <span className="detail-value">{formatDate(task.created_at)}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Celery Task ID</span>
            <span className="detail-value">
              <code style={{ fontSize: '0.875rem' }}>{task.celery_task_id?.substring(0, 16)}...</code>
            </span>
          </div>
        </div>

        {task.result && (
          <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)' }}>
            <h3 style={{ marginBottom: '1rem' }}>Results</h3>
            <pre style={{ 
              background: 'var(--bg-color)', 
              padding: '1rem', 
              borderRadius: '8px',
              overflow: 'auto',
              fontSize: '0.875rem'
            }}>
              {JSON.stringify(task.result, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* Live Updates Section */}
      <div style={{ display: 'grid', gap: '1.5rem' }}>
        <div className="live-updates">
          <h3>
            <span className="live-indicator" /> Live Updates
            <span style={{ 
              fontSize: '0.75rem', 
              color: wsConnected ? 'var(--success-color)' : 'var(--warning-color)',
              marginLeft: '0.5rem',
              fontWeight: 500
            }}>
              {wsConnected ? '● Connected' : '○ Disconnected'}
            </span>
          </h3>
          
          {updates.length === 0 ? (
            <div style={{ 
              textAlign: 'center', 
              padding: '2rem',
              color: 'var(--text-secondary)'
            }}>
              Waiting for updates...
            </div>
          ) : (
            updates.map((update, index) => (
              <div key={index} className="update-item">
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  marginBottom: '0.5rem'
                }}>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.75rem' }}>
                    {new Date().toLocaleTimeString()}
                  </span>
                  {update.status && (
                    <span style={{ 
                      fontSize: '0.75rem',
                      padding: '0.125rem 0.5rem',
                      background: 'var(--bg-tertiary)',
                      borderRadius: '4px'
                    }}>
                      {update.status}
                    </span>
                  )}
                </div>
                <div>{JSON.stringify(update)}</div>
              </div>
            ))
          )}
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button 
            className="btn btn-primary"
            onClick={fetchTask}
          >
            🔄 Refresh
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => {
              navigator.clipboard.writeText(task.task_id);
              addToast('Task ID copied to clipboard!', 'success');
            }}
          >
            📋 Copy ID
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskDetail;
