import { useEffect, useRef, useState, useCallback } from 'react';

export const createWebSocket = (url, onMessage) => {
  const ws = new WebSocket(url);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };
  
  return ws;
};

export const useWebSocket = (url, onMessage) => {
  const [ws, setWs] = useState(null);
  const onMessageRef = useRef(onMessage);
  const isConnectedRef = useRef(false);
  
  // Keep the callback ref up to date without triggering re-renders
  useEffect(() => {
    onMessageRef.current = onMessage;
  });
  
  useEffect(() => {
    // Prevent creating multiple WebSockets for the same URL
    if (isConnectedRef.current) return;
    isConnectedRef.current = true;
    
    const websocket = createWebSocket(url, (data) => {
      onMessageRef.current(data);
    });
    setWs(websocket);
    
    return () => {
      if (websocket && typeof websocket.close === 'function') {
        websocket.close();
      }
      isConnectedRef.current = false;
    };
  }, [url]);
  
  return ws;
};
