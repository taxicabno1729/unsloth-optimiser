import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ConfigForm from './ConfigForm';
import TaskList from './TaskList';
import apiClient from '../api/client';
import { useToast } from '../context/ToastContext';

const Dashboard = () => {
  const { addToast } = useToast();
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    running: 0,
    completed: 0,
    failed: 0
  });
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchTasks = async () => {
    try {
      // In a real implementation, you'd have an endpoint to list all tasks
      // For now, we'll just use the local state
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    }
  };

  useEffect(() => {
    // Calculate stats from tasks
    const newStats = {
      total: tasks.length,
      pending: tasks.filter(t => t.status === 'pending').length,
      running: tasks.filter(t => t.status === 'running').length,
      completed: tasks.filter(t => t.status === 'completed').length,
      failed: tasks.filter(t => t.status === 'failed').length
    };
    setStats(newStats);
  }, [tasks]);

  const handleTaskCreated = (newTask) => {
    setTasks(prev => [newTask, ...prev]);
    addToast(`Task "${newTask.name}" created successfully!`, 'success');
  };

  const StatCard = ({ icon, title, value, color, trend }) => (
    <div className="card stat-card">
      <div className={`stat-icon ${color}`}>
        {icon}
      </div>
      <div className="stat-content">
        <h3>{value}</h3>
        <p>{title}</p>
        {trend && (
          <span style={{ 
            fontSize: '0.75rem', 
            color: trend > 0 ? 'var(--success-color)' : 'var(--text-secondary)',
            marginTop: '0.25rem',
            display: 'inline-block'
          }}>
            {trend > 0 ? '↑' : '→'} {Math.abs(trend)}% vs last hour
          </span>
        )}
      </div>
    </div>
  );

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Manage your model optimization tasks and monitor progress in real-time.</p>
      </div>

      {/* Stats Grid */}
      <div className="dashboard-grid">
        <StatCard 
          icon="📊" 
          title="Total Tasks" 
          value={stats.total} 
          color="purple" 
        />
        <StatCard 
          icon="⏳" 
          title="Pending" 
          value={stats.pending} 
          color="orange" 
        />
        <StatCard 
          icon="🔄" 
          title="Running" 
          value={stats.running} 
          color="blue" 
        />
        <StatCard 
          icon="✅" 
          title="Completed" 
          value={stats.completed} 
          color="green" 
        />
      </div>

      {/* Quick Actions */}
      <div style={{ 
        display: 'flex', 
        gap: '1rem', 
        marginBottom: '2rem',
        flexWrap: 'wrap'
      }}>
        <button 
          className="btn btn-primary"
          onClick={() => setShowCreateForm(true)}
          style={{ fontSize: '1.125rem', padding: '1rem 2rem' }}
        >
          <span>+</span> New Optimization Task
        </button>
        <Link to="/tasks" className="btn btn-secondary" style={{ textDecoration: 'none' }}>
          View All Tasks →
        </Link>
      </div>

      {/* Create Task Modal */}
      {showCreateForm && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '2rem',
          overflow: 'auto'
        }}>
          <div style={{ width: '100%', maxWidth: '900px' }}>
            <ConfigForm 
              onSubmit={handleTaskCreated}
              onClose={() => setShowCreateForm(false)}
            />
          </div>
        </div>
      )}

      {/* Recent Tasks */}
      <div>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '1rem'
        }}>
          <h2 style={{ fontSize: '1.5rem' }}>Recent Tasks</h2>
          {tasks.length > 0 && (
            <button 
              onClick={() => setTasks([])}
              className="btn btn-secondary"
              style={{ fontSize: '0.875rem' }}
            >
              Clear All
            </button>
          )}
        </div>
        
        {tasks.length === 0 ? (
          <div className="card empty-state">
            <div className="empty-state-icon">🚀</div>
            <h3>No tasks yet</h3>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              Create your first optimization task to get started!
            </p>
            <button 
              className="btn btn-primary"
              onClick={() => setShowCreateForm(true)}
              style={{ marginTop: '1rem' }}
            >
              Create Task
            </button>
          </div>
        ) : (
          <TaskList 
            tasks={tasks.slice(0, 5)} 
            onTaskClick={(task) => window.location.href = `/tasks/${task.task_id}`}
          />
        )}
      </div>

      {/* Quick Guide */}
      <div className="card" style={{ marginTop: '2rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>Quick Guide</h3>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1.5rem'
        }}>
          <div>
            <h4 style={{ color: 'var(--primary-color)', marginBottom: '0.5rem' }}>1. Choose Method</h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Select from Quantization, LoRA, AWQ, or GPTQ based on your needs.
            </p>
          </div>
          <div>
            <h4 style={{ color: 'var(--primary-color)', marginBottom: '0.5rem' }}>2. Configure</h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Enter model name and adjust advanced parameters if needed.
            </p>
          </div>
          <div>
            <h4 style={{ color: 'var(--primary-color)', marginBottom: '0.5rem' }}>3. Monitor</h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Track progress in real-time with live status updates.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
