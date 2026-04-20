import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <nav style={{ marginTop: '10px', marginBottom: '20px' }}>
      <Link to="/" style={{ marginRight: '15px' }}>Home</Link>
      <Link to="/create" style={{ marginRight: '15px' }}>Create Task</Link>
    </nav>
  );
};

export default Navigation;
