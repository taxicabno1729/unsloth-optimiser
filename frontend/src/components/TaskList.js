import React from 'react';
import { Link } from 'react-router-dom';

const TaskList = ({ tasks, onTaskClick }) => {
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
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getRelativeTime = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.round(diffMs / 60000);
    const diffHours = Math.round(diffMs / 3600000);
    const diffDays = Math.round(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    return `${diffDays} days ago`;
  };

  if (tasks.length === 0) {
    return (
      <div className="card empty-state">
        <div className="empty-state-icon">📭</div>
        <h3>No tasks found</h3>
        <p style={{ color: 'var(--text-secondary)' }}>
          Create a new task to see it here.
        </p>
      </div>
    );
  }

  return (
    <div className="tasks-grid">
      {tasks.map(task => (
        <div 
          key={task.task_id} 
          className="task-card"
          onClick={() => onTaskClick && onTaskClick(task)}
          style={{ cursor: onTaskClick ? 'pointer' : 'default' }}
        >
          <div className="task-info">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '1.25rem' }}>{getMethodIcon(task.optimization_method)}</span>
              <h4>{task.name}</h4>
            </div>
            
            <div className="task-meta">
              <span className="task-method">
                {task.optimization_method}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                📦 {task.model_name}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                🕐 {getRelativeTime(task.created_at)}
              </span>
            </div>
            
            {task.result && (
              <div style={{ 
                marginTop: '0.75rem', 
                padding: '0.5rem',
                background: 'var(--bg-color)',
                borderRadius: '8px',
                fontSize: '0.875rem',
                fontFamily: 'monospace'
              }}>
                {typeof task.result === 'string' ? task.result : JSON.stringify(task.result, null, 2)}
              </div>
            )}
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.75rem' }}>
            <span className={`status-badge ${getStatusClass(task.status)}`}>
              {task.status || 'pending'}
            </span>
            
            <Link 
              to={`/tasks/${task.task_id}`}
              className="btn btn-secondary"
              style={{ 
                fontSize: '0.875rem', 
                padding: '0.5rem 1rem',
                textDecoration: 'none'
              }}
              onClick={(e) => e.stopPropagation()}
            >
              View Details →
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
