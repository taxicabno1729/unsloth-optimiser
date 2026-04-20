import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';

test('renders application header', () => {
  render(<App />);
  const header = screen.getByText(/Unsloth Optimiser/i);
  expect(header).toBeInTheDocument();
});
