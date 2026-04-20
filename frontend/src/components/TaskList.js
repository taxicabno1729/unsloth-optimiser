import React from 'react';

const TaskList = ({ tasks }) => {
  return (
    <div>
      <h2>Tasks</h2>
      {tasks.length === 0 ? (
        <p>No tasks yet</p>
      ) : (
        <ul>
          {tasks.map(task => (
            <li key={task.task_id}>
              {task.name} - {task.optimization_method} ({task.status})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;
