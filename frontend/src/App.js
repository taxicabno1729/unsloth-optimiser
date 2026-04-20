import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Navigation from './components/Navigation';
import CreateTask from './pages/CreateTask';
import TaskDetail from './pages/TaskDetail';
import Dashboard from './components/Dashboard';

// AppRoutes - used for testing with MemoryRouter
export const AppRoutes = () => {
  return (
    <div className="App">
      <header>
        <h1>Unsloth Optimiser</h1>
        <Navigation />
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/create" element={<CreateTask />} />
          <Route path="/tasks/:id" element={<TaskDetail />} />
        </Routes>
      </main>
    </div>
  );
};

// App - production component with BrowserRouter
function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

export default App;
