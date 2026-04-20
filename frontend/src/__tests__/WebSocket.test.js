import { renderHook, waitFor } from '@testing-library/react';
import { useWebSocket, createWebSocket } from '../hooks/useWebSocket';

// Mock WebSocket using a class to properly set properties
class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = 0; // CONNECTING
    this.onopen = null;
    this.onmessage = null;
    this.onclose = null;
    this.onerror = null;
    this.close = jest.fn();
    this.send = jest.fn();
    
    // Simulate connection opening immediately
    setTimeout(() => {
      if (this.onopen) this.onopen();
    }, 0);
  }
}

MockWebSocket.CONNECTING = 0;
MockWebSocket.OPEN = 1;
MockWebSocket.CLOSING = 2;
MockWebSocket.CLOSED = 3;

global.WebSocket = MockWebSocket;

test('createWebSocket creates WebSocket connection', () => {
  const mockOnMessage = jest.fn();
  const ws = createWebSocket('ws://localhost:8000/ws/tasks/123', mockOnMessage);
  
  expect(ws.url).toBe('ws://localhost:8000/ws/tasks/123');
  expect(typeof ws.onmessage).toBe('function');
});

test('useWebSocket hook returns WebSocket instance', async () => {
  const { result } = renderHook(() => 
    useWebSocket('ws://localhost:8000/ws/tasks/123', jest.fn())
  );
  
  // Wait for the effect to run and set the WebSocket
  await waitFor(() => {
    expect(result.current).not.toBeNull();
  });
});

test('useWebSocket calls close on unmount', async () => {
  const { result, unmount } = renderHook(() => 
    useWebSocket('ws://localhost:8000/ws/tasks/123', jest.fn())
  );
  
  // Wait for the WebSocket to be created
  await waitFor(() => {
    expect(result.current).not.toBeNull();
  });
  
  const ws = result.current;
  
  // Unmount should trigger cleanup
  unmount();
  
  // Verify close was called
  expect(ws.close).toHaveBeenCalled();
});
