import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { AppRoutes } from '../App';

test('navigation renders correctly', () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <AppRoutes />
    </MemoryRouter>
  );
  
  expect(screen.getByText(/Unsloth Optimiser/i)).toBeInTheDocument();
  expect(screen.getByText(/Home/i)).toBeInTheDocument();
  expect(screen.getByText(/Create Task/i)).toBeInTheDocument();
});

test('create task route renders CreateTask page', () => {
  render(
    <MemoryRouter initialEntries={['/create']}>
      <AppRoutes />
    </MemoryRouter>
  );
  
  expect(screen.getByText(/Create New Optimization Task/i)).toBeInTheDocument();
});

test('task detail route renders TaskDetail page', () => {
  render(
    <MemoryRouter initialEntries={['/tasks/123']}>
      <AppRoutes />
    </MemoryRouter>
  );
  
  expect(screen.getByText(/Task Details/i)).toBeInTheDocument();
});
