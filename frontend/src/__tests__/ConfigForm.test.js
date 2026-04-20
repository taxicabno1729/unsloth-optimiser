import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ConfigForm from '../components/ConfigForm';

test('renders optimization method selector', () => {
  render(<ConfigForm onSubmit={() => {}} />);
  const selector = screen.getByLabelText(/optimization method/i);
  expect(selector).toBeInTheDocument();
  
  const options = screen.getAllByRole('option');
  expect(options.length).toBeGreaterThan(0);
});

test('renders all form fields', () => {
  render(<ConfigForm onSubmit={() => {}} />);
  
  expect(screen.getByLabelText(/task name/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/optimization method/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/model name/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /create/i })).toBeInTheDocument();
});

test('renders all 4 optimization methods in dropdown', () => {
  render(<ConfigForm onSubmit={() => {}} />);
  const options = screen.getAllByRole('option');
  expect(options.length).toBe(4);
  
  expect(screen.getByText('Quantization (4-bit/8-bit)')).toBeInTheDocument();
  expect(screen.getByText('LoRA Fine-tuning')).toBeInTheDocument();
  expect(screen.getByText('AWQ (Activation-aware)')).toBeInTheDocument();
  expect(screen.getByText('GPTQ Optimization')).toBeInTheDocument();
});

test('form inputs use controlled components', () => {
  render(<ConfigForm onSubmit={() => {}} />);
  
  const nameInput = screen.getByLabelText(/task name/i);
  const modelInput = screen.getByLabelText(/model name/i);
  const methodSelector = screen.getByLabelText(/optimization method/i);
  
  fireEvent.change(nameInput, { target: { value: 'Test Task' } });
  fireEvent.change(modelInput, { target: { value: 'test-model' } });
  
  expect(nameInput.value).toBe('Test Task');
  expect(modelInput.value).toBe('test-model');
  expect(methodSelector.value).toBe('quantization');
});

test('required fields have required attribute', () => {
  render(<ConfigForm onSubmit={() => {}} />);
  
  const nameInput = screen.getByLabelText(/task name/i);
  const modelInput = screen.getByLabelText(/model name/i);
  
  expect(nameInput).toHaveAttribute('required');
  expect(modelInput).toHaveAttribute('required');
});
